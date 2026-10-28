import os, json
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))
VIDEO_FOLDER = os.path.join(BASE, "static", "videos")
DATA_FILE = os.path.join(BASE, "videos.json")
os.makedirs(VIDEO_FOLDER, exist_ok=True)
ALLOWED = {".mp4",".webm",".mov",".mkv",".mp3",".avi"}

def load_data():
    if os.path.exists(DATA_FILE):
        try: return json.load(open(DATA_FILE, encoding="utf-8"))
        except: return {}
    return {}
def save_data(d):
    json.dump(d, open(DATA_FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

HOME = """
<!DOCTYPE html><html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FREDDY-V</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Roboto,Arial}
body{background:#0f0f0f;color:#fff}
header{position:sticky;top:0;z-index:20;background:#0f0f0f;padding:10px 12px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #222}
.yt{color:#FF0000;font-weight:900;font-size:18px;display:flex;align-items:center;gap:3px}
.yt i{background:#FF0000;color:#fff;border-radius:4px;padding:1px 5px;font-style:normal}
.search{flex:1}.search div{background:#121212;border:1px solid #303030;border-radius:20px;display:flex;padding:6px 14px;align-items:center}
.search input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:14px}
.bar{padding:10px 12px;display:flex;gap:8px;overflow-x:auto;white-space:nowrap}
.bar span{background:#272727;padding:7px 12px;border-radius:8px;font-size:13px}
.bar span.active{background:#fff;color:#000}
.section{padding:12px;display:flex;justify-content:space-between;align-items:center}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 8px 80px}
.card{border-radius:12px;overflow:hidden;background:#181818;position:relative}
.thumb{width:100%;aspect-ratio:9/16;background:#000;position:relative;overflow:hidden}
.thumb video{width:100%;height:100%;object-fit:cover}
.info{position:absolute;bottom:0;left:0;right:0;padding:8px;background:linear-gradient(transparent,rgba(0,0,0,0.95));}
.info h3{font-size:13px;font-weight:500;line-height:1.2;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.info p{font-size:11px;color:#aaa;margin-top:3px}
.bottom{position:fixed;bottom:0;left:0;right:0;background:#0f0f0f;border-top:1px solid #222;display:flex;justify-content:space-around;padding:8px 0}
.bottom div{text-align:center;font-size:10px;color:#aaa}.bottom div.active{color:#fff}.bottom div span{display:block;font-size:22px}
.add{position:fixed;bottom:70px;right:16px;background:#FF0000;width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;text-decoration:none;color:#fff;z-index:30}
</style></head><body>
<header><div class="yt"><i>▶</i> FREDDY-V</div><div class="search"><div><input id="q" placeholder="Rechercher par titre..." oninput="filterVids()"><span style="margin-left:8px">🔍</span></div></div></header>
<div class="bar"><span class="active">Tout</span><span>Pour toi</span><span>Masisi</span><span>Musique</span></div>
<div class="section"><h2>🔥 Shorts Masisi</h2><span>⋮</span></div>
<div class="grid" id="grid">
{% for v in videos %}
<div class="card" data-name="{{ (v.title + ' ' + v.channel + ' ' + v.filename).lower() }}">
<div class="thumb"><video src="/static/videos/{{v.filename}}" preload="metadata" muted></video>
<div class="info"><h3>{{v.title}}</h3><p>{{v.channel}} • {{v.views}} vues</p></div></div></div>
{% else %}
<div style="grid-column:1/-1;text-align:center;padding:40px;color:#666"><h3>🎬 Aucune vidéo</h3><p>Sois le premier à publier !</p>
<a href="/admin" style="display:inline-block;margin-top:12px;background:#FF0000;color:#fff;padding:10px 20px;border-radius:20px;text-decoration:none;font-weight:700">+ Publier Vidéo</a></div>
{% endfor %}
</div><a class="add" href="/admin">+</a>
<div class="bottom"><div class="active"><span>⌂</span>Accueil</div><div><span>▶</span>Shorts</div><div><span>+</span></div><div><span>◫</span>Abonn.</div><div><span>M</span>Vous</div></div>
<script>function filterVids(){let q=document.getElementById('q').value.toLowerCase();document.querySelectorAll('.card').forEach(c=>{c.style.display=c.dataset.name.includes(q)?'block':'none';});}</script>
</body></html>
"""

ADMIN = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Publier - Freddy-V</title>
<style>
body{background:#0f0f0f;color:#fff;font-family:Arial;padding:16px}
.box{max-width:480px;margin:10px auto;background:#212121;padding:20px;border-radius:12px}
label{font-size:13px;color:#aaa;margin-top:10px;display:block}
input[type=text]{width:100%;padding:12px;background:#121212;border:1px solid #333;border-radius:8px;color:#fff;margin:6px 0 12px;font-size:14px}
input[type=file]{width:100%;padding:12px;background:#121212;border:2px dashed #FF0000;border-radius:10px;color:#fff;margin:6px 0 12px}
.btn{width:100%;padding:14px;background:#FF0000;color:#fff;border:none;border-radius:24px;font-weight:800;font-size:15px;margin-top:10px}
a{color:#3ea6ff;text-decoration:none}.item{background:#121212;padding:10px;border-radius:8px;margin:6px 0;font-size:12px}
</style></head><body>
<div class="box">
<h2 style="color:#FF0000">📤 Publier Vidéo</h2>
<p style="color:#aaa;font-size:12px">Remplis le titre pour que les gens te trouvent</p>
<form method="POST" enctype="multipart/form-data">
<label>Titre de la vidéo *</label>
<input type="text" name="title" placeholder="Ex: Baptême à Masisi - 2026" required>
<label>Nom de ta chaîne *</label>
<input type="text" name="channel" placeholder="Ex: Freddy V Officiel" required>
<label>Fichier vidéo *</label>
<input type="file" name="video" accept="video/*" required>
<button class="btn">🚀 PUBLIER MAINTENANT</button>
</form>
<p style="margin-top:14px"><a href="/">← Retour Accueil</a></p>
<h3 style="margin-top:18px;font-size:13px">Vidéos publiées ({{count}})</h3>
{% for v in videos.values() %}
<div class="item"><div><b>{{v.title}}</b><br><span style="color:#aaa">{{v.channel}} - {{v.filename}}</span></div></div>
{% endfor %}
</div>
</body></html>
"""

@app.route("/")
def index():
    data=load_data()
    vids=[]
    if os.path.exists(VIDEO_FOLDER):
        for f in os.listdir(VIDEO_FOLDER):
            if os.path.splitext(f)[1].lower() in ALLOWED:
                info=data.get(f, {"title": f, "channel": "FREDDY-V", "views": "0"})
                vids.append({"filename": f, "title": info.get("title", f), "channel": info.get("channel","FREDDY-V"), "views": info.get("views","12"), "mtime": os.path.getmtime(os.path.join(VIDEO_FOLDER,f))})
    vids.sort(key=lambda x: x["mtime"], reverse=True)
    return render_template_string(HOME, videos=vids)

@app.route("/admin", methods=["GET","POST"])
def admin():
    data=load_data()
    if request.method=="POST":
        title=request.form.get("title","").strip()
        channel=request.form.get("channel","").strip()
        f=request.files.get("video")
        if f and f.filename and title and channel:
            fn=secure_filename(f.filename)
            base, ext = os.path.splitext(fn)
            counter=1
            while os.path.exists(os.path.join(VIDEO_FOLDER, fn)):
                fn=f"{base}_{counter}{ext}"
                counter+=1
            f.save(os.path.join(VIDEO_FOLDER, fn))
            data[fn]={"title": title, "channel": channel, "views": str(10+len(data)*3)}
            save_data(data)
            return redirect(url_for("admin"))
    return render_template_string(ADMIN, videos=data, count=len(data))

@app.route("/static/videos/<path:filename>")
def serve(filename):
    return send_from_directory(VIDEO_FOLDER, filename)

@app.route("/health")
def h(): return "OK"

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
