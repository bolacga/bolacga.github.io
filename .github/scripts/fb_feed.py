# Lay bai moi nhat cua Facebook page -> data/fb.json (landing page doc file nay).
# Can 2 secret trong repo: FB_PAGE_ID, FB_PAGE_TOKEN (Page access token khong het han).
# Loi (token chet, mang) -> GIU file cu, khong ghi de bang rong.
import json, os, sys, urllib.parse, urllib.request

API = "https://graph.facebook.com/v19.0"
pid, tok = os.environ.get("FB_PAGE_ID", "").strip(), os.environ.get("FB_PAGE_TOKEN", "").strip()
if not pid or not tok:
    print("Chua co FB_PAGE_ID / FB_PAGE_TOKEN -> bo qua"); sys.exit(0)

def get(path, **q):
    q["access_token"] = tok
    with urllib.request.urlopen(f"{API}/{path}?{urllib.parse.urlencode(q)}", timeout=30) as r:
        return json.load(r)

try:
    page = get(pid, fields="name,link,followers_count,picture.width(120).height(120){url}")
    posts = get(f"{pid}/posts", fields="message,created_time,full_picture,permalink_url", limit=6)
except Exception as e:
    print("Loi goi Facebook:", e); sys.exit(1)

items = []
for p in posts.get("data", []):
    if not p.get("permalink_url"): continue
    msg = (p.get("message") or "").strip()
    items.append({"text": msg[:280], "time": p.get("created_time", ""), "image": p.get("full_picture", ""), "url": p["permalink_url"]})
    if len(items) >= 3: break

out = {"name": page.get("name", ""), "url": page.get("link") or "https://www.facebook.com/bolacga1",
       "followers": page.get("followers_count"), "avatar": ((page.get("picture") or {}).get("data") or {}).get("url", ""),
       "posts": items}
os.makedirs("data", exist_ok=True)
with open("data/fb.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(f"OK: {out['name']} - {len(items)} bai")