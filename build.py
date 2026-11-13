"""Builds index.html (Ladybug Lab) and summit/index.html (Summit).  Run:  python3 build.py"""
import os, re, json
ROOT = os.path.dirname(os.path.abspath(__file__))

def build_app(src_name, out_dir, title, short, theme, config_path="config.js"):
    src = open(os.path.join(ROOT, src_name), encoding="utf-8").read()
    cut = src.index("</style>") + len("</style>")
    src = src.replace("? \"kid1\" : \"winnie\"", "? \"kid1\" : \"kid1\"")  # keep names out of the public site
    cut = src.index("</style>") + len("</style>")
    head, body = src[:cut], src[cut:]
    head = re.sub(r"<title>.*?</title>\s*", "", head)
    page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="theme-color" content="{theme}">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="{short}">
<script src="{config_path}"></script>
<style>html,body{{margin:0}}body{{padding-top:max(12px,env(safe-area-inset-top,0px))!important}}</style>
{head}
</head><body>
{body}
<script>if("serviceWorker" in navigator) addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{{}}));</script>
</body></html>
"""
    os.makedirs(os.path.join(ROOT, out_dir), exist_ok=True)
    open(os.path.join(ROOT, out_dir, "index.html"), "w", encoding="utf-8").write(page)
    manifest = {"name": title, "short_name": short, "start_url": "./", "scope": "./", "display": "standalone",
                "background_color": "#fdf8ef", "theme_color": theme,
                "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}
    open(os.path.join(ROOT, out_dir, "manifest.webmanifest"), "w").write(json.dumps(manifest, indent=2))
    # network-first service worker: always fresh when online, still opens offline
    open(os.path.join(ROOT, out_dir, "sw.js"), "w").write("""const C="app-v1";
self.addEventListener("install",e=>self.skipWaiting());
self.addEventListener("activate",e=>e.waitUntil(self.clients.claim()));
self.addEventListener("fetch",e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=="GET" || u.pathname.includes("/rest/v1/")) return;
  e.respondWith(fetch(e.request).then(r=>{ const c=r.clone(); caches.open(C).then(x=>x.put(e.request,c)); return r; })
    .catch(()=>caches.match(e.request).then(r=>r||caches.match("./"))));
});
""")
    print("built", out_dir)

build_app("ladybug-lab.html", ".", "Ladybug Lab", "Ladybug Lab", "#e0483d")
build_app("summit-source.html", "summit", "Summit", "Summit", "#D4622A", "../config.js")
