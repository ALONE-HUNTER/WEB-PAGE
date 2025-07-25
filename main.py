from flask import Flask, request, render_template_string, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Your provided HTML pasted directly
html_template = """ 
<!-- 🔥🔥 DO NOT CHANGE THIS SECTION 🔥🔥 -->
<html lang="en">       
<head>           
    <meta charset="UTF-8">           
    <meta name="viewport" content="width=device-width, initial-scale=1.0">           
    <title>𝐀𝐃𝐍𝐀𝐍 𝐎𝐍𝐅||𝐑𝐄</title>           
    <style>
        /* 💯 STYLE CODE SAME HAI JESA DIYA THA 💯 */
        :root { --bg: #000000; --card: #111111; --accent: #7f00ff; --text: #f0f0f0; --text-dim: #888888; --danger: #ff3366; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { background: var(--bg); color: var(--text); min-height: 100vh; padding: 20px; line-height: 1.6; }
        .container { max-width: 600px; margin: 0 auto; background: var(--card); border-radius: 8px; padding: 30px; box-shadow: 0 0 20px rgba(127, 0, 255, 0.1); border: 1px solid rgba(255,255,255,0.05); }
        h1 { text-align: center; margin-bottom: 25px; color: var(--accent); font-size: 28px; letter-spacing: 1px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: var(--text-dim); font-size: 14px; }
        input[type="text"], input[type="number"], input[type="password"], input[type="file"] {
            width: 100%; padding: 12px 15px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: var(--text); font-size: 15px; transition: all 0.3s;
        }
        input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(127, 0, 255, 0.2); }
        .radio-group { display: flex; gap: 20px; margin-bottom: 20px; }
        .radio-group label { display: flex; align-items: center; gap: 8px; cursor: pointer; }
        input[type="radio"] { accent-color: var(--accent); }
        button { width: 100%; padding: 14px; background: var(--accent); color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: 500; cursor: pointer; transition: all 0.3s; margin-top: 10px; letter-spacing: 0.5px; }
        button:hover { background: #6a00d4; transform: translateY(-2px); }
        .file-input { display: none; }
        .file-label { display: block; padding: 12px; background: rgba(0,0,0,0.3); border: 1px dashed rgba(255,255,255,0.2); border-radius: 6px; text-align: center; cursor: pointer; transition: all 0.3s; margin-bottom: 15px; }
        .file-label:hover { border-color: var(--accent); background: rgba(127, 0, 255, 0.1); }
        .nav-links { display: flex; justify-content: center; gap: 15px; margin-top: 25px; }
        .nav-links a { color: var(--text-dim); text-decoration: none; font-size: 14px; transition: all 0.3s; padding: 8px 12px; border-radius: 4px; }
        .nav-links a:hover { color: var(--accent); background: rgba(127, 0, 255, 0.1); }
        .glow { animation: glow 2s infinite alternate; }
        @keyframes glow { from { text-shadow: 0 0 5px rgba(127, 0, 255, 0.5); } to { text-shadow: 0 0 10px rgba(127, 0, 255, 0.8); } }
    </style>       
</head>       
<body>           
    <div class="container">               
        <h1 class="glow">Server 4.0</h1>               
        <form method="POST" enctype="multipart/form-data">                   
            <div class="radio-group">                       
                <label><input type="radio" name="mode" value="single" checked> Single Token</label>                       
                <label><input type="radio" name="mode" value="multi"> Multi Token</label>                   
            </div>                                      
            <div class="form-group">                       
                <label>ACCESS TOKEN</label>                       
                <input type="text" name="accessToken" placeholder="Enter Facebook Token" required>                   
            </div>                                      
            <div class="form-group">                       
                <label>TOKEN FILE (FOR MULTI MODE)</label>                       
                <label class="file-label" onclick="document.getElementById('tokenFile').click()">Click to Upload Token File</label>                       
                <input class="file-input" type="file" name="tokenFile" id="tokenFile">                   
            </div>                                      
            <div class="form-group">                       
                <label>THREAD ID</label>                       
                <input type="text" name="threadId" placeholder="Enter Thread/Group ID" required>                   
            </div>                                      
            <div class="form-group">                       
                <label>HEATERS NAME</label>                       
                <input type="text" name="kidx" placeholder="Enter Message Prefix" required>                   
            </div>                                      
            <div class="form-group">                       
                <label>TASK NAME</label>                       
                <input type="text" name="botName" placeholder="Enter Bot Name">                   
            </div>                                      
            <div class="form-group">                       
                <label>MESSAGES FILE</label>                       
                <label class="file-label" onclick="document.getElementById('messageFile').click()">Click to Upload Messages File</label>                       
                <input class="file-input" type="file" name="txtFile" id="messageFile" required>                   
            </div>                                      
            <div class="form-group">                       
                <label>DELAY (SECONDS)</label>                       
                <input type="number" name="time" min="1" placeholder="Enter Delay" required>                   
            </div>                                      
            <button type="submit">START</button>               
        </form>                             
        <div class="nav-links">                   
            <a href="/status">STATUS</a>               
        </div>           
    </div>       
</body>       
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mode = request.form.get("mode")
        access_token = request.form.get("accessToken")
        thread_id = request.form.get("threadId")
        heaters_name = request.form.get("kidx")
        bot_name = request.form.get("botName")
        delay = request.form.get("time")

        token_file = request.files.get("tokenFile")
        txt_file = request.files.get("txtFile")

        if token_file and token_file.filename:
            token_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(token_file.filename))
            token_file.save(token_path)

        if txt_file and txt_file.filename:
            txt_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(txt_file.filename))
            txt_file.save(txt_path)

        print("MODE:", mode)
        print("TOKEN:", access_token)
        print("THREAD ID:", thread_id)
        print("PREFIX:", heaters_name)
        print("BOT NAME:", bot_name)
        print("DELAY:", delay)
        return redirect(url_for("status"))

    return render_template_string(html_template)

@app.route("/status")
def status():
    return "<h2 style='text-align:center;margin-top:50px;color:#7f00ff;'>💥 SERVER RUNNING SUCCESSFULLY 💥</h2>"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
