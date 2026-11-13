// Supabase project settings (Supabase → Project Settings → API).
// The "anon public" key is meant to be public; the family code keeps each family's data private.
window.LL_CONFIG = {
  supabaseUrl: "PASTE_PROJECT_URL_HERE",   // e.g. https://abcdefghijk.supabase.co
  supabaseKey: "PASTE_ANON_PUBLIC_KEY_HERE"
};
if (window.LL_CONFIG.supabaseUrl.startsWith("PASTE")) window.LL_CONFIG.supabaseUrl = "";
