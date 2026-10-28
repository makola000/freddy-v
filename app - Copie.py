
import os, json, time
from flask import Flask, send_from_directory, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "freddy-v-2026-secret"
BASE = os.path.dirname(__file__)
VIDEO_FOLDER = os.path.join(BASE, "static", "videos")
USER_FILE = os.path.join(BASE, "users.json")
STATS_FILE = os.path.join(BASE, "stats.json")
COMMENT_FILE = os.path.join(BASE, "comments.json")
os.makedirs(VIDEO_FOLDER, exist_ok=True)
for p in [USER_FILE, STATS_FILE, COMMENT_FILE]:
    if not os.path.exists(p): open(p,"w").write("{}")

def load_json(f):
    try: return json.loads(open(f).read())
    except: return {}
def save_json(f,d): open(f,"w").write(json.dumps(d))

def get_videos(q=""):
    files=[f for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith(".mp4")] if os.path.exists(VIDEO_FOLDER) else []
    if q:
        q=q.lower()
        files=[f for f in files if q in f.lower()]
    return sorted(files, key=lambda x: os.path.getmtime(os.path.join(VIDEO_FOLDER,x)), reverse=True)

@app.route("/")
def home():
    user=session.get("user")
    btn = f"<div style=padding:10px>Connecté: <b>{user}</b> | <a href=/logout>Deconnexion</a> | <a href=/upload style=background:green;color:white;padding:8px 12px;border-radius:20px;text-decoration:none>📤 Publier</a></div>" if user else "<div style=padding:15px;text-align:center><a href=/login style=background:black;color:white;padding:10px 15px;border-radius:20px;text-decoration:none;margin-right:10px>Connexion</a><a href=/register style=background:red;color:white;padding:10px 15px;border-radius:20px;text-decoration:none>Créer compte</a></div>"
    return f"<meta name=viewport content='width=device-width'><div style=font-family:sans-serif><h1 style=color:red;text-align:center>🔥 FREDDY V 🔥</h1>{btn}<a href=/freddy-y style=background:red;color:white;padding:20px;display:block;text-align:center;border-radius:12px;text-decoration:none;margin:15px;font-size:20px>▶️ Voir les videos</a></div>"

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        u=request.form.get("username","").strip(); p=request.form.get("password","").strip()
        users=load_json(USER_FILE)
        if not u or not p: return "Remplis tout"
        if u in users: return "Compte existe deja <a href=/login>Connexion</a>"
        users[u]=generate_password_hash(p); save_json(USER_FILE,users); session["user"]=u
        return redirect("/")
    return "<meta name=viewport content='width=device-width'><div style=font-family:sans-serif;padding:20px;max-width:400px;margin:auto><h2 style=color:red>Créer compte FREDDY V</h2><form method=post><input name=username placeholder='Nom utilisateur' style=width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #ccc><input name=password type=password placeholder='Mot de passe' style=width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #ccc><button style=width:100%;background:red;color:white;padding:14px;border:none;border-radius:8px>Créer mon compte</button></form><p><a href=/login>Deja un compte?</a></p></div>"

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form.get("username","").strip(); p=request.form.get("password","").strip()
        users=load_json(USER_FILE)
        if u in users and check_password_hash(users[u], p):
            session["user"]=u; return redirect("/")
        return "Mot de passe faux <a href=/login>Reessayer</a>"
    return "<meta name=viewport content='width=device-width'><div style=font-family:sans-serif;padding:20px;max-width:400px;margin:auto><h2>Connexion FREDDY V</h2><form method=post><input name=username placeholder='Nom utilisateur' style=width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #ccc><input name=password type=password placeholder='Mot de passe' style=width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #ccc><button style=width:100%;background:black;color:white;padding:14px;border:none;border-radius:8px>Se connecter</button></form><p><a href=/register>Créer compte</a></p></div>"

@app.route("/logout")
def logout():
    session.pop("user",None); return redirect("/")

@app.route("/upload", methods=["GET","POST"])
def upload():
    if "user" not in session: return redirect("/login")
    if request.method=="POST":
        f=request.files.get("video")
        if f and f.filename.lower().endswith(".mp4"):
            name=secure_filename(f"{session['user']}_{f.filename}")
            f.save(os.path.join(VIDEO_FOLDER, name))
            return redirect(f"/freddy-y?play={name}")
        return "Envoie un fichier .mp4"
    return f"<meta name=viewport content='width=device-width'><div style=font-family:sans-serif;padding:20px;max-width:400px;margin:auto><h2>📤 Publier sur FREDDY V</h2><p>Connecte comme <b>{session['user']}</b></p><form method=post enctype=multipart/form-data><input type=file name=video accept=video/mp4 style=width:100%;padding:20px;border:2px dashed red;border-radius:12px;margin:15px 0><button style=width:100%;background:green;color:white;padding:14px;border:none;border-radius:8px>Publier ma video</button></form><a href=/freddy-y>Retour</a></div>"

@app.route("/view/<path:filename>")
def add_view(filename):
    stats=load_json(STATS_FILE)
    if filename not in stats: stats[filename]={"views":0,"likes":0}
    stats[filename]["views"]=stats[filename].get("views",0)+1
    save_json(STATS_FILE,stats)
    return {"views":stats[filename]["views"]}

@app.route("/like/<path:filename>")
def add_like(filename):
    stats=load_json(STATS_FILE)
    if filename not in stats: stats[filename]={"views":0,"likes":0}
    stats[filename]["likes"]=stats[filename].get("likes",0)+1
    save_json(STATS_FILE,stats)
    return {"likes":stats[filename]["likes"]}

@app.route("/comment/<path:filename>", methods=["GET","POST"])
def comment(filename):
    comments=load_json(COMMENT_FILE)
    if filename not in comments: comments[filename]=[]
    if request.method=="POST":
        if "user" not in session: return {"error":"connecte toi"},401
        text=request.form.get("text","").strip()[:200]
        if text:
            comments[filename].append({"user":session["user"],"text":text,"time":int(time.time())})
            save_json(COMMENT_FILE,comments)
        return redirect(f"/freddy-y?play={filename}")
    return {"comments":comments.get(filename,[])}

@app.route("/freddy-y")
def freddy_y():
    q=request.args.get("q",""); play=request.args.get("play","")
    user=session.get("user","")
    videos=get_videos(q)
    stats=load_json(STATS_FILE)
    comments=load_json(COMMENT_FILE)
    top = f"<div style=background:white;padding:10px;display:flex;justify-content:space-between><span>👤 {user}</span><span><a href=/upload>📤 Publier</a> | <a href=/>Accueil</a></span></div>" if user else "<div style=background:white;padding:10px;text-align:center><a href=/register style=color:red;font-weight:bold>Créer compte pour publier</a> | <a href=/login>Connexion</a></div>"
    html=""
    for v in videos:
        owner=v.split("_")[0] if "_" in v else "Anonyme"
        s=stats.get(v,{"views":0,"likes":0})
        c=len(comments.get(v,[]))
        html+=f"""<div style=background:white;display:flex;gap:10px;padding:10px;margin-bottom:8px;align-items:center>
        <div onclick="playVideo('{v}')" style=flex:1;display:flex;gap:10px;cursor:pointer>
        <div style=width:140px;height:80px;background:#000;color:white;display:flex;align-items:center;justify-content:center;border-radius:8px>▶</div>
        <div style=flex:1><b>{v[:28]}</b><br><small style=color:gray>Par: {owner}</small><br><small>👁️ {s.get('views',0)} | ❤️ {s.get('likes',0)} | 💬 {c}</small></div>
        </div>
        <a href='/videos/{v}' download style=background:#0a0;color:white;padding:8px;border-radius:20px;text-decoration:none;font-size:12px>⬇️</a>
        </div>"""
    autoplay = f"playVideo('{play}')" if play else ""
    return f"""<meta name=viewport content='width=device-width'><style>body{{margin:0;font-family:sans-serif;background:#f2f2f2}}#player{{position:sticky;top:0;background:black;z-index:20}}</style>
<div id=player><video id=mainVideo controls playsinline style=width:100%;max-height:50vh;background:black></video>
<div id=bar style=background:white;padding:10px;display:none>
<div style=flex:1><span id=videoTitle style=font-weight:bold;font-size:13px></span><br><span id=videoStats style=font-size:11px;color:gray></span>
<div id=commentList style=margin-top:10px;max-height:120px;overflow:auto;background:#f9f9f9;padding:8px;border-radius:8px></div>
<form id=commentForm method=post style=margin-top:8px;display:flex;gap:5px><input name=text id=commentInput placeholder='Ajouter un commentaire...' style=flex:1;padding:8px;border-radius:20px;border:1px solid #ccc><button style=background:red;color:white;border:none;padding:8px 12px;border-radius:20px>Envoyer</button></form>
</div>
<div style=display:flex;flex-direction:column;gap:5px;margin-left:8px><button onclick="likeCurrent()" style=background:#ff0050;color:white;border:none;padding:8px 12px;border-radius:20px>❤️ Like</button><a id=downloadBtn href='#' download style=background:green;color:white;padding:8px 12px;border-radius:20px;text-decoration:none;text-align:center>⬇️</a></div>
</div></div>
<div style=background:red;padding:12px;color:white;text-align:center;font-weight:bold;font-size:20px>🔥 FREDDY V 🔥</div>{top}
<div style=background:white;padding:10px;display:flex;gap:5px><form style=flex:1;display:flex><input name=q value='{q}' placeholder='Rechercher' style=flex:1;padding:12px;border-radius:20px 0 0 20px;border:1px solid #ccc><button style=padding:12px 15px;border-radius:0 20px 20px 0>🔍</button></form></div>
<div style=padding:8px;color:gray>{len(videos)} videos</div>{html}
<script>
var currentFile="";
function playVideo(f){{
  currentFile=f;
  var v=document.getElementById('mainVideo');
  var t=document.getElementById('videoTitle');
  var bar=document.getElementById('bar');
  var dl=document.getElementById('downloadBtn');
  var form=document.getElementById('commentForm');
  bar.style.display='flex';
  t.innerText=f;
  dl.href='/videos/'+encodeURIComponent(f);
  form.action='/comment/'+encodeURIComponent(f);
  v.src='/videos/'+encodeURIComponent(f);
  v.load(); v.play();
  fetch('/view/'+encodeURIComponent(f)).then(r=>r.json()).then(d=>{{document.getElementById('videoStats').innerText='👁️ '+d.views+' vues';}});
  fetch('/comment/'+encodeURIComponent(f)).then(r=>r.json()).then(d=>{{
    var list=document.getElementById('commentList');
    list.innerHTML='';
    d.comments.forEach(c=>{{var div=document.createElement('div'); div.style.padding='4px 0'; div.style.borderBottom='1px solid #eee'; div.innerHTML='<b>'+c.user+':</b> '+c.text; list.appendChild(div);}});
    if(d.comments.length==0) list.innerHTML='<small style=color:gray>Aucun commentaire, sois le premier!</small>';
  }});
  window.scrollTo({{top:0,behavior:'smooth'}});
}}
function likeCurrent(){{
  if(!currentFile) return;
  fetch('/like/'+encodeURIComponent(currentFile)).then(r=>r.json()).then(d=>{{alert('❤️ Merci! Likes: '+d.likes);}});
}}
window.onload=function(){{{autoplay}}}
</script>"""

@app.route("/videos/<path:filename>")
def serve_video(filename):
    return send_from_directory(VIDEO_FOLDER, filename, mimetype='video/mp4', conditional=True)

app.run(host="0.0.0.0", port=5000)
