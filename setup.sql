-- Family Learning: progress sync
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste → Run.
--
-- How it works: each family has a long random "family code" made in the app.
-- Progress rows are only reachable through the two functions below, and only
-- with the exact family code. The table itself is closed to the public key.

create table if not exists public.family_progress (
  family_code text   not null,
  kid         text   not null,
  data        jsonb  not null default '{}'::jsonb,
  version     bigint not null default 0,
  updated_at  timestamptz not null default now(),
  primary key (family_code, kid)
);

alter table public.family_progress enable row level security;
-- No policies on purpose: the public (anon) key cannot read or write the table directly.
revoke all on table public.family_progress from anon, authenticated;

create or replace function public.get_progress(p_code text, p_kid text)
returns table (r_data jsonb, r_version bigint)
language sql
security definer
set search_path = public
as $$
  select fp.data, fp.version
  from public.family_progress fp
  where fp.family_code = p_code and fp.kid = p_kid;
$$;

-- Saves only if p_version matches what's stored (so two devices never overwrite
-- each other). On a mismatch it returns the stored copy; the app merges and retries.
create or replace function public.save_progress(p_code text, p_kid text, p_data jsonb, p_version bigint)
returns table (r_ok boolean, r_data jsonb, r_version bigint)
language plpgsql
security definer
set search_path = public
as $$
declare
  cur public.family_progress%rowtype;
begin
  if p_code is null or length(p_code) < 16 or p_code !~ '^[0-9A-Z]+$' then
    raise exception 'invalid family code';
  end if;
  if p_kid is null or p_kid !~ '^[a-z0-9-]{1,32}$' then
    raise exception 'invalid kid';
  end if;
  if pg_column_size(p_data) > 200000 then
    raise exception 'progress too large';
  end if;

  select * into cur from public.family_progress fp
  where fp.family_code = p_code and fp.kid = p_kid
  for update;

  if not found then
    if p_version <> 0 then
      return query select false, null::jsonb, 0::bigint;
      return;
    end if;
    insert into public.family_progress (family_code, kid, data, version)
    values (p_code, p_kid, p_data, 1);
    return query select true, p_data, 1::bigint;
    return;
  end if;

  if cur.version <> p_version then
    return query select false, cur.data, cur.version;
    return;
  end if;

  update public.family_progress fp
  set data = p_data, version = cur.version + 1, updated_at = now()
  where fp.family_code = p_code and fp.kid = p_kid;
  return query select true, p_data, cur.version + 1;
end;
$$;

revoke all on function public.get_progress(text, text) from public;
revoke all on function public.save_progress(text, text, jsonb, bigint) from public;
grant execute on function public.get_progress(text, text) to anon, authenticated;
grant execute on function public.save_progress(text, text, jsonb, bigint) to anon, authenticated;
