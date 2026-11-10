from flask import Flask, send_file, Response
app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/ads.txt')
def ads_txt():
    return Response("google.com, pub-6553183721717606, DIRECT, f08c47e88d", mimetype='text/plain')

# Pour que les autres pages marchent aussi : admin.html, chaine.html, etc.
@app.route('/<path:filename>')
def serve_file(filename):
    try:
        return send_file(filename)
    except:
        return "Not Found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
