"""Builds both apps as flat files (no folders needed on GitHub).
   index.html  = Ladybug Lab (Winnie)   from ladybug-lab.html
   summit.html = Summit (Margot)        from summit-source.html
   Run:  python3 build.py"""
import os, re, json
ROOT = os.path.dirname(os.path.abspath(__file__))
SW = """const C="app-v1";
self.addEventListener("install",e=>self.skipWaiting());
self.addEventListener("activate",e=>e.waitUntil(self.clients.claim()));
self.addEventListener("fetch",e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=="GET" || u.pathname.includes("/rest/v1/")) return;
  e.respondWith(fetch(e.request).then(r=>{ const c=r.clone(); caches.open(C).then(x=>x.put(e.request,c)); return r; })
    .catch(()=>caches.match(e.request)));
});
"""

def build_app(src_name, page, prefix, title, theme):
    src = open(os.path.join(ROOT, src_name), encoding="utf-8").read()
    src = src.replace('? "kid1" : "winnie"', '? "kid1" : "kid1"')  # keep names out of the public site
    cut = src.index("</style>") + len("</style>")
    head, body = src[:cut], src[cut:]
    head = re.sub(r"<title>.*?</title>\s*", "", head)
    man = prefix + "manifest.webmanifest" if prefix else "manifest.webmanifest"
    page_html = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="theme-color" content="{theme}">
<link rel="manifest" href="{man}">
<link rel="icon" href="{prefix}icon-192.png">
<link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="{title}">
<script src="config.js"></script>
<style>html,body{{margin:0}}body{{padding-top:max(12px,env(safe-area-inset-top,0px))!important}}</style>
{head}
</head><body>
{body}
<script>if("serviceWorker" in navigator) addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{{}}));</script>
</body></html>
"""
    open(os.path.join(ROOT, page), "w", encoding="utf-8").write(page_html)
    manifest = {"name": title, "short_name": title, "id": page, "start_url": page, "scope": "./", "display": "standalone",
                "background_color": "#fdf8ef", "theme_color": theme,
                "icons": [{"src": prefix + "icon-192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": prefix + "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}
    open(os.path.join(ROOT, man), "w").write(json.dumps(manifest, indent=2))
    print("built", page)

open(os.path.join(ROOT, "sw.js"), "w").write(SW)
build_app("ladybug-lab.html", "index.html", "", "Ladybug Lab", "#e0483d")
build_app("summit-source.html", "summit.html", "summit-", "Summit", "#D4622A")
