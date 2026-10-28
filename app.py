import os, json, datetime
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
<title>FREDDY-V MASISI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Roboto,Arial}
body{background:#0f0f0f;color:#fff}
header{position:sticky;top:0;z-index:20;background:#0f0f0f;padding:10px 12px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #222}
.yt{color:#FF0000;font-weight:900;font-size:18px}.yt i{background:#FF0000;color:#fff;border-radius:4px;padding:1px 5px;font-style:normal}
.search{flex:1}.search div{background:#121212;border:1px solid #303030;border-radius:20px;display:flex;padding:6px 14px}
.search input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:14px}
.bar{padding:10px 12px;display:flex;gap:8px;overflow-x:auto;white-space:nowrap}
.bar span{background:#272727;padding:7px 12px;border-radius:8px;font-size:13px}.bar span.active{background:#fff;color:#000}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 8px 80px}
.card{border-radius:12px;overflow:hidden;background:#181818;position:relative;text-decoration:none;color:#fff;display:block}
.thumb{width:100%;aspect-ratio:9/16;background:#000;overflow:hidden;position:relative}.thumb video{width:100%;height:100%;object-fit:cover}
.info{position:absolute;bottom:0;left:0;right:0;padding:8px;background:linear-gradient(transparent,rgba(0,0,0,0.95))}
.info h3{font-size:13px;font-weight:500;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.info p{font-size:11px;color:#aaa;margin-top:3px}
.add{position:fixed;bottom:70px;right:16px;background:#FF0000;width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;text-decoration:none;color:#fff;z-index:30}
.bottom{position:fixed;bottom:0;left:0;right:0;background:#0f0f0f;border-top:1px solid #222;display:flex;justify-content:space-around;padding:8px 0}
.bottom div{text-align:center;font-size:10px;color:#aaa}.bottom div.active{color:#fff}.bottom div span{display:block;font-size:22px}
</style></head><body>
<header><div class="yt"><i>▶</i> FREDDY-V</div><div class="search"><div><input id="q" placeholder="Rechercher..." oninput="filterVids()"></div></div></header>
<div class="bar"><span class="active">Tout</span><span>Masisi</span><span>Musique</span></div>
<div class="grid" id="grid">
{% for v in videos %}
<a class="card" href="/watch/{{v.filename}}" data-name="{{ (v.title + ' ' + v.channel).lower() }}">
<div class="thumb"><video src="/static/videos/{{v.filename}}" preload="metadata" muted></video>
<div class="info"><h3>{{v.title}}</h3><p>{{v.channel}} • {{v.views}} vues • {{v.likes}} 👍</p></div></div></a>
{% else %}
<div style="grid-column:1/-1;text-align:center;padding:40px;color:#666"><h3>🎬 Aucune vidéo</h3><a href="/admin" style="display:inline-block;margin-top:12px;background:#FF0000;color:#fff;padding:10px 20px;border-radius:20px;text-decoration:none;font-weight:700">+ Publier</a></div>
{% endfor %}
</div>
<a class="add" href="/admin">+</a>
<div class="bottom"><div class="active"><span>⌂</span>Accueil</div><div><span>▶</span>Shorts</div><div><span>+</span></div><div><span>◫</span>Abonn.</div><div><span>M</span>Vous</div></div>
<script>function filterVids(){let q=document.getElementById('q').value.toLowerCase();document.querySelectorAll('.card').forEach(c=>{c.style.display=c.dataset.name.includes(q)?'block':'none';});}</script>
</body></html>
"""

WATCH = """
<!DOCTYPE html><html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{video.title}}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Roboto,Arial}
body{background:#0f0f0f;color:#fff}
header{padding:10px 12px;display:flex;gap:12px;background:#0f0f0f}
header a{color:#fff;text-decoration:none;font-size:20px}
.player{width:100%;background:#000;aspect-ratio:9/16;max-height:75vh}.player video{width:100%;height:100%;object-fit:contain}
.info{padding:12px}.info h1{font-size:16px;font-weight:600;margin-bottom:6px}.meta{color:#aaa;font-size:13px;margin-bottom:12px}
.actions{display:flex;gap:8px;overflow-x:auto;padding-bottom:12px}.actions a,.actions button{background:#272727;color:#fff;border:none;padding:8px 14px;border-radius:20px;font-size:13px;text-decoration:none;display:flex;gap:6px}
.actions .down{background:#FF0000}.channel{display:flex;gap:10px;padding:12px;border-top:1px solid #222;border-bottom:1px solid #222;margin-bottom:12px}
.avatar{width:36px;height:36px;background:#FF0000;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800}
.sub{background:#fff;color:#000;padding:7px 14px;border-radius:20px;font-weight:700;font-size:13px;border:none}
.comments{padding:12px}.cmt-form{display:flex;gap:8px;margin-bottom:16px}.cmt-form input{flex:1;background:#121212;border:1px solid #333;border-radius:20px;padding:10px 14px;color:#fff}
.cmt-form button{background:#3ea6ff;color:#000;border:none;padding:8px 14px;border-radius:20px;font-weight:700}
.cmt{margin-bottom:12px;display:flex;gap:8px}.cmt-avatar{width:28px;height:28px;background:#333;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px}
.cmt-body{flex:1}.cmt-body b{font-size:12px}.cmt-body p{font-size:13px;margin:2px 0}.cmt-body span{font-size:11px;color:#aaa}
</style></head><body>
<header><a href="/">←</a><div style="font-weight:900;color:#FF0000">FREDDY-V</div></header>
<div class="player"><video src="/static/videos/{{video.filename}}" controls autoplay playsinline></video></div>
<div class="info">
<h1>{{video.title}}</h1>
<div class="meta">{{video.views}} vues • {{video.date}} • {{video.likes}} 👍</div>
<div class="actions">
<form action="/watch/{{video.filename}}/like" method="POST" style="display:inline"><button type="submit">👍 {{video.likes}} Like</button></form>
<a href="/download/{{video.filename}}" class="down">⬇️ Télécharger sur téléphone</a>
<a href="whatsapp://send?text=https://freddy-v.onrender.com/watch/{{video.filename}}">↗️ Partager</a>
</div>
<div class="channel"><div class="avatar">{{video.channel[:1]}}</div><div style="flex:1"><b>{{video.channel}}</b><br><span style="color:#aaa;font-size:12px">12,5 k abonnés</span></div><button class="sub">S'abonner</button></div>
<div class="comments">
<h3>💬 {{video.comments|length}} commentaires</h3>
<form class="cmt-form" method="POST" action="/watch/{{video.filename}}/comment">
<input name="text" placeholder="Ajouter un commentaire..." required>
<button type="submit">Envoyer</button>
</form>
{% for c in video.comments[::-1] %}
<div class="cmt"><div class="cmt-avatar">{{c.user[:1]}}</div><div class="cmt-body"><b>@{{c.user}}</b> <span>• {{c.time}}</span><p>{{c.text}}</p></div></div>
{% else %}
<p style="color:#666;font-size:13px">Sois le premier à commenter !</p>
{% endfor %}
</div>
</div>
</body></html>
"""

ADMIN = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Publier</title><style>body{background:#0f0f0f;color:#fff;font-family:Arial;padding:16px}
.box{max-width:480px;margin:10px auto;background:#212121;padding:20px;border-radius:12px}
label{font-size:13px;color:#aaa;margin-top:10px;display:block}
input[type=text]{width:100%;padding:12px;background:#121212;border:1px solid #333;border-radius:8px;color:#fff;margin:6px 0 12px}
input[type=file]{width:100%;padding:12px;background:#121212;border:2px dashed #FF0000;border-radius:10px;color:#fff;margin:6px 0 12px}
.btn{width:100%;padding:14px;background:#FF0000;color:#fff;border:none;border-radius:24px;font-weight:800}
a{color:#3ea6ff;text-decoration:none}</style></head><body>
<div class="box"><h2 style="color:#FF0000">📤 Publier Vidéo</h2>
<form method="POST" enctype="multipart/form-data">
<label>Titre *</label><input type="text" name="title" placeholder="Ex: Mariage Masisi" required>
<label>Chaîne *</label><input type="text" name="channel" placeholder="Ex: Freddy V Officiel" required>
<label>Vidéo *</label><input type="file" name="video" accept="video/*" required>
<button class="btn">🚀 PUBLIER</button>
</form><p style="margin-top:14px"><a href="/">← Accueil</a></p></div></body></html>
"""

@app.route("/")
def index():
    data=load_data()
    vids=[]
    if os.path.exists(VIDEO_FOLDER):
        for f in os.listdir(VIDEO_FOLDER):
            if os.path.splitext(f)[1].lower() in ALLOWED:
                info=data.get(f, {"title": f, "channel": "FREDDY-V", "views": 0, "likes": 0})
                vids.append({"filename": f, "title": info.get("title", f), "channel": info.get("channel","FREDDY-V"), "views": info.get("views",0), "likes": info.get("likes",0), "mtime": os.path.getmtime(os.path.join(VIDEO_FOLDER,f))})
    vids.sort(key=lambda x: x["mtime"], reverse=True)
    return render_template_string(HOME, videos=vids)

@app.route("/watch/<filename>")
def watch(filename):
    data=load_data()
    path=os.path.join(VIDEO_FOLDER, filename)
    if not os.path.exists(path): return "Video non trouvee",404
    if filename not in data:
        data[filename]={"title": filename, "channel": "FREDDY-V", "views":0, "likes":0, "comments":[], "date": datetime.datetime.now().strftime("%d/%m/%Y")}
    data[filename]["views"]=int(data[filename].get("views",0))+1
    save_data(data)
    info=data[filename]
    video={"filename": filename, "title": info.get("title", filename), "channel": info.get("channel","FREDDY-V"), "views": info.get("views",0), "likes": info.get("likes",0), "comments": info.get("comments",[]), "date": info.get("date","aujourd'hui")}
    return render_template_string(WATCH, video=video)

@app.route("/watch/<filename>/like", methods=["POST"])
def like(filename):
    data=load_data()
    if filename in data:
        data[filename]["likes"]=int(data[filename].get("likes",0))+1
        save_data(data)
    return redirect(url_for("watch", filename=filename))

@app.route("/watch/<filename>/comment", methods=["POST"])
def comment(filename):
    data=load_data()
    text=request.form.get("text","").strip()
    if text and filename in data:
        if "comments" not in data[filename]: data[filename]["comments"]=[]
        data[filename]["comments"].append({"user": "Masisi", "text": text, "time": datetime.datetime.now().strftime("%H:%M")})
        save_data(data)
    return redirect(url_for("watch", filename=filename))

@app.route("/download/<filename>")
def download(filename):
    path=os.path.join(VIDEO_FOLDER, filename)
    if not os.path.exists(path): return "Fichier non trouve",404
    return send_from_directory(VIDEO_FOLDER, filename, as_attachment=True, download_name=filename)

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
            c=1
            while os.path.exists(os.path.join(VIDEO_FOLDER, fn)):
                fn=f"{base}_{c}{ext}"
                c+=1
            f.save(os.path.join(VIDEO_FOLDER, fn))
            data[fn]={"title": title, "channel": channel, "views":0, "likes":0, "comments":[], "date": datetime.datetime.now().strftime("%d/%m/%Y")}
            save_data(data)
            return redirect(url_for("watch", filename=fn))
    return render_template_string(ADMIN)

@app.route("/static/videos/<path:filename>")
def serve(filename):
    return send_from_directory(VIDEO_FOLDER, filename)

@app.route("/health")
def h(): return "OK"

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
