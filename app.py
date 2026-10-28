import os
from flask import Flask, send_from_directory, request

app = Flask(__name__)
VIDEO_FOLDER = os.path.join(os.path.dirname(__file__), "static", "videos")

def clean_title(filename):
    name = filename.replace(".mp4","").replace(".MP4","")
    name = name.replace("VID-", "").replace("WA", " WhatsApp ").replace("-", " ").replace("_", " ")
    # Nettoyer les dates collées
    name = " ".join(name.split())
    return name.strip().title() if len(name) > 3 else filename

def get_videos(q=""):
    if not os.path.exists(VIDEO_FOLDER):
        return []
    files = [f for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith(".mp4")]
    if q:
        q = q.lower()
        files = [f for f in files if q in f.lower() or q in clean_title(f).lower()]
    return sorted(files)

@app.route('/')
def home():
    return """
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <div style='padding:20px; font-family:sans-serif; text-align:center'>
    <h1 style='color:red'>▶️ MAKOLA</h1>
    <a href='/freddy-y' style='display:block; background:red; color:white; padding:20px; border-radius:12px; text-decoration:none; font-size:22px; margin-top:30px'>Entrer sur Freddy-Y</a>
    <p style='color:gray; margin-top:20px'>YouTube Local - Sans Mega</p>
    </div>
    """

@app.route('/freddy-y')
def freddy_y():
    q = request.args.get("q","")
    videos = get_videos(q)
    html = f"""
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{{margin:0; font-family:Roboto, Arial, sans-serif; background:#f9f9f9}}</style>
    <div style='background:white; padding:10px; position:sticky; top:0; z-index:10; border-bottom:1px solid #ddd; display:flex; align-items:center; gap:10px'>
      <span style='color:red; font-weight:bold; font-size:20px'>▶️ Freddy-Y</span>
      <form action='/freddy-y' style='flex:1; display:flex'>
        <input name='q' value='{q}' placeholder='Rechercher' style='flex:1; padding:10px 15px; border:1px solid #ccc; border-radius:20px 0 0 20px; outline:none'>
        <button style='padding:10px 15px; border:1px solid #ccc; border-left:0; border-radius:0 20px 20px 0; background:#f8f8f8'>🔍</button>
      </form>
    </div>
    <div style='padding:10px; color:gray; font-size:14px'>{len(videos)} vidéos {f'pour "{q}"' if q else ''} | <a href='/freddy-y'>Tout voir</a></div>
    """
    if not videos:
        html += f"<p style='text-align:center; margin-top:50px'>Aucune vidéo trouvée pour <b>{q}</b></p>"
    
    for v in videos:
        titre = clean_title(v)
        html += f"""
        <div style='background:white; margin-bottom:10px; display:flex; padding:8px; gap:10px'>
          <a href='/watch/{v}' style='text-decoration:none; display:flex; gap:10px; width:100%'>
            <div style='min-width:160px; width:160px; height:90px; background:#000; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-size:30px; position:relative'>▶<span style='position:absolute; bottom:4px; right:4px; background:rgba(0,0,0,0.8); font-size:10px; padding:2px 4px; border-radius:4px'>00:45</span></div>
            <div style='flex:1'>
              <div style='font-weight:500; font-size:14px; color:black; line-height:18px; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden'>{titre}</div>
              <div style='font-size:12px; color:gray; margin-top:4px'>{v}<br>Freddy • Local • Sans Méga</div>
            </div>
          </a>
        </div>
        """
    return html

@app.route('/watch/<path:filename>')
def watch(filename):
    titre = clean_title(filename)
    return f"""
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{{margin:0; font-family:Roboto, sans-serif; background:black; color:white}}</style>
    <div style='background:#212121; padding:10px'><a href='/freddy-y' style='color:white; text-decoration:none'>⬅️ Retour</a></div>
    <video controls autoplay style='width:100%; max-height:55vh; background:black' src='/videos/{filename}'></video>
    <div style='background:white; color:black; padding:12px; border-radius:12px 12px 0 0; margin-top:-10px'>
      <h3 style='margin:0; font-size:16px'>{titre}</h3>
      <p style='font-size:12px; color:gray; margin:5px 0'>{filename}</p>
      <p style='font-size:13px; color:#606060'>Freddy-Y • 15 vues • Local sans internet</p>
      <div style='display:flex; gap:15px; margin-top:12px; overflow-x:auto'>
        <button style='border:1px solid #ddd; padding:8px 15px; border-radius:20px; background:#f2f2f2'>👍 Like</button>
        <button style='border:1px solid #ddd; padding:8px 15px; border-radius:20px; background:#f2f2f2'>🔗 Partager</button>
        <button style='border:1px solid #ddd; padding:8px 15px; border-radius:20px; background:#f2f2f2'>⬇️ Télécharger</button>
      </div>
    </div>
    """

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
