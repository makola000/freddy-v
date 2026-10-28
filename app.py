import os
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))
VIDEO_FOLDER = os.path.join(BASE, "static", "videos")
os.makedirs(VIDEO_FOLDER, exist_ok=True)
ALLOWED = {".mp4",".webm",".mov",".mkv",".mp3",".avi"}

HOME = """
<!DOCTYPE html><html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>FREDDY-V</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Roboto,Arial}
body{background:#0f0f0f;color:#fff}
header{position:sticky;top:0;z-index:20;background:#0f0f0f;padding:10px 12px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #222}
.yt{color:#FF0000;font-weight:900;font-size:22px;display:flex;align-items:center;gap:2px}
.yt i{background:#FF0000;color:#fff;border-radius:4px;padding:0 4px;font-style:normal;font-size:18px}
.search{flex:1}.search div{background:#121212;border:1px solid #303030;border-radius:20px;display:flex;padding:6px 14px;align-items:center}
.search input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:14px}
.bar{padding:10px 12px;display:flex;gap:8px;overflow-x:auto;white-space:nowrap}
.bar span{background:#272727;padding:7px 12px;border-radius:8px;font-size:13px}
.bar span.active{background:#fff;color:#000}
.section{padding:12px;display:flex;justify-content:space-between;align-items:center}
.section h2{font-size:18px;font-weight:700;display:flex;align-items:center;gap:8px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 8px 80px}
.card{border-radius:12px;overflow:hidden;background:#000;position:relative}
.thumb{width:100%;aspect-ratio:9/16;background:#181818;position:relative;overflow:hidden}
.thumb video{width:100%;height:100%;object-fit:cover}
.dots{position:absolute;top:8px;right:8px;background:#00000080;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.title{position:absolute;bottom:0;left:0;right:0;padding:8px;background:linear-gradient(transparent,rgba(0,0,0,0.9));font-size:13px;font-weight:500;line-height:1.2}
.bottom{position:fixed;bottom:0;left:0;right:0;background:#0f0f0f;border-top:1px solid #222;display:flex;justify-content:space-around;padding:8px 0}
.bottom div{text-align:center;font-size:10px;color:#aaa}.bottom div.active{color:#fff}.bottom div span{display:block;font-size:22px}
.add{position:fixed;bottom:70px;right:16px;background:#FF0000;width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;text-decoration:none;color:#fff}
</style></head><body>
<header><div class="yt"><i>▶</i> FREDDY-V</div><div class="search"><div><input id="q" placeholder="Rechercher" oninput="filterVids()"><span style="margin-left:8px">🔍</span></div></div></header>
<div class="bar"><span class="active">Tout</span><span>Pour toi</span><span>Musique</span><span>Baptême</span><span>Masisi</span><span>Église</span></div>
<div class="section"><h2><b style="background:#FF0000;color:#fff;padding:2px 6px;border-radius:4px">▶</b> Shorts</h2><span>⋮</span></div>
<div class="grid" id="grid">
{% for v in videos %}<div class="card" data-name="{{v.lower()}}"><div class="thumb"><video src="/static/videos/{{v}}" preload="metadata" muted></video><div class="dots">⋮</div><div class="title">{{v[:35]}}</div></div></div>
{% else %}<div style="grid-column:1/-1;text-align:center;padding:40px;color:#666"><h3>🎬 Aucune vidéo</h3><p style="margin-top:8px;font-size:13px">Clique + pour ajouter tes vidéos</p><a href="/admin" style="display:inline-block;margin-top:12px;background:#FF0000;color:#fff;padding:10px 20px;border-radius:20px;text-decoration:none;font-weight:700">+ Ajouter Vidéo</a></div>{% endfor %}
</div><a class="add" href="/admin">+</a>
<div class="bottom"><div class="active"><span>⌂</span>Accueil</div><div><span>▶</span>Shorts</div><div><span>+</span></div><div><span>◫</span>Abonn.</div><div><span>M</span>Vous</div></div>
<script>function filterVids(){let q=document.getElementById('q').value.toLowerCase();document.querySelectorAll('.card').forEach(c=>{c.style.display=c.dataset.name.includes(q)?'block':'none';});}</script>
</body></html>
"""

ADMIN = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin Freddy-V</title><style>body{background:#0f0f0f;color:#fff;font-family:Arial;padding:16px}
.box{max-width:480px;margin:20px auto;background:#212121;padding:20px;border-radius:12px}
input{width:100%;padding:14px;background:#121212;border:2px dashed #FF0000;border-radius:10px;color:#fff;margin:12px 0}
.btn{width:100%;padding:14px;background:#FF0000;color:#fff;border:none;border-radius:24px;font-weight:800}
a{color:#3ea6ff;text-decoration:none}.item{background:#121212;padding:10px;border-radius:8px;margin:6px 0;display:flex;justify-content:space-between;font-size:13px}
</style></head><body><div class="box"><h2 style="color:#FF0000">FREDDY-V ADMIN</h2>
<form method="POST" enctype="multipart/form-data"><input type="file" name="video" accept="video/*" required><button class="btn">📤 UPLOADER</button></form>
<p style="margin-top:14px"><a href="/">← Retour Accueil</a></p><h3 style="margin-top:16px;font-size:14px">Vidéos {{count}}</h3>
{% for v in videos %}<div class="item"><span>{{v}}</span><a href="/static/videos/{{v}}" target="_blank">Voir</a></div>{% endfor %}</div></body></html>
"""

@app.route("/")
def index():
    vids=[]
    if os.path.exists(VIDEO_FOLDER):
        vids=[f for f in os.listdir(VIDEO_FOLDER) if os.path.splitext(f)[1].lower() in ALLOWED]
        vids.sort(key=lambda x: os.path.getmtime(os.path.join(VIDEO_FOLDER,x)), reverse=True)
    return render_template_string(HOME, videos=vids)

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method=="POST":
        f=request.files.get("video")
        if f and f.filename:
            fn=secure_filename(f.filename)
            f.save(os.path.join(VIDEO_FOLDER, fn))
            return redirect(url_for("admin"))
    vids=os.listdir(VIDEO_FOLDER) if os.path.exists(VIDEO_FOLDER) else []
    return render_template_string(ADMIN, videos=vids, count=len(vids))

@app.route("/static/videos/<path:filename>")
def serve(filename):
    return send_from_directory(VIDEO_FOLDER, filename)

@app.route("/health")
def h(): return "OK"

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
