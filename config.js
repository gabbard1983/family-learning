// Supabase project settings (Supabase → Project Settings → API).
// The "anon public" key is meant to be public; the family code keeps each family's data private.
window.LL_CONFIG = {
  supabaseUrl: https://vopjrngfbltujajacyyy.supabase.co,   // e.g. https://abcdefghijk.supabase.co
  supabaseKey: sb_publishable_7Fs-cnBtlIwblHNG1ZS9ow_bOXjxwHG
};
if (window.LL_CONFIG.supabaseUrl.startsWith("PASTE")) window.LL_CONFIG.supabaseUrl = "";
