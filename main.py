from flask import Flask, request, render_template_string
import os, requests, time, random, string, json, atexit
from threading import Thread, Event

app = Flask(__name__)
app.secret_key = 'ADNAN_SECRET_KEY'
app.debug = True

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': '/',
    'Accept-Language': 'en-US,en;q=0.9',
}

stop_events, threads, active_users = {}, {}, {}
TASK_FILE = 'tasks.json'

def save_tasks():
    with open(TASK_FILE, 'w', encoding='utf-8') as f:
        json.dump(active_users, f, ensure_ascii=False, indent=2)

def load_tasks():
    if not os.path.exists(TASK_FILE): return
    with open(TASK_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for tid, info in data.items():
            active_users[tid] = info
            stop_events[tid] = Event()
            if info.get('status') == 'ACTIVE':
                if not info.get('fb_name'):
                    info['fb_name'] = fetch_profile_name(info['token'])
                th = Thread(
                    target=send_messages,
                    args=(
                        info['tokens_all'],
                        info['thread_id'],
                        info['name'],
                        info.get('delay', 1),
                        info['msgs'],
                        tid
                    ),
                    daemon=True
                )
                th.start()
                threads[tid] = th

atexit.register(save_tasks)
load_tasks()

def fetch_profile_name(token: str) -> str:
    try:
        res = requests.get(
            f'https://graph.facebook.com/me?access_token={token}',
            timeout=8
        )
        return res.json().get('name', 'Unknown')
    except Exception:
        return 'Unknown'

def send_messages(tokens, thread_id, mn, delay, messages, task_id):
    ev = stop_events[task_id]
    tok_i, msg_i = 0, 0
    total_tok, total_msg = len(tokens), len(messages)
    while not ev.is_set():
        tk = tokens[tok_i]
        msg = messages[msg_i]
        try:
            requests.post(
                f'https://graph.facebook.com/v15.0/t_{thread_id}/',
                data={'access_token': tk, 'message': f"{mn} {msg}"},
                headers=headers,
                timeout=10
            )
            print(f"[✔️ SENT] {msg[:40]} via TOKEN-{tok_i+1}")
        except Exception as e:
            print("[⚠️ ERROR]", e)
        tok_i = (tok_i + 1) % total_tok
        msg_i = (msg_i + 1) % total_msg
        time.sleep(delay)

@app.route('/', methods=['GET', 'POST'])
def home():
    msg_html = stop_html = ""
    if request.method == 'POST':
        if 'txtFile' in request.files:
            tokens = (
                [request.form.get('singleToken').strip()]
                if request.form.get('tokenOption') == 'single'
                else request.files['tokenFile'].read()
                .decode(errors='ignore')
                .splitlines()
            )
            tokens = [t for t in tokens if t]
            uid = request.form.get('threadId','').strip()
            hater = request.form.get('kidx','').strip()
            delay = max(int(request.form.get('time',1) or 1),1)
            file = request.files['txtFile']
            msgs = [m for m in file.read().decode(errors='ignore').splitlines() if m]
            if not (tokens and uid and hater and msgs):
                msg_html = "<div class='alert alert-danger rounded-pill p-2'>⚠️ All fields required!</div>"
            else:
                tid = 'brokennadeem' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                stop_events[tid] = Event()
                th = Thread(
                    target=send_messages,
                    args=(tokens, uid, hater, delay, msgs, tid),
                    daemon=True
                )
                th.start()
                threads[tid] = th
                active_users[tid] = {
                    'name': hater,
                    'token': tokens[0],
                    'tokens_all': tokens,
                    'fb_name': fetch_profile_name(tokens[0]),
                    'thread_id': uid,
                    'msg_file': file.filename or 'messages.txt',
                    'msgs': msgs,
                    'delay': delay,
                    'msg_count': len(msgs),
                    'status': 'ACTIVE'
                }
                save_tasks()
                msg_html = f"<div class='stop-key rounded-pill p-3'>🔑 <b>STOP KEY↷</b><br><code>{tid}</code></div>"
        elif 'taskId' in request.form:
            tid = request.form.get('taskId','').strip()
            if tid in stop_events:
                stop_events[tid].set()
                if tid in active_users:
                    active_users[tid]['status'] = 'OFFLINE'
                save_tasks()
                stop_html = "<div class='stop-ok rounded-pill p-3'>⏹️ <b>STOPPED</b><br><code>{}</code></div>".format(tid)
            else:
                stop_html = "<div class='stop-bad rounded-pill p-3'>❌ <b>INVALID KEY</b><br><code>{}</code></div>".format(tid)
    return render_template_string(html_template, msg_html=msg_html, stop_html=stop_html)

html_template = '''
 <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>𝐀𝐃𝐍𝐀𝐍 𝐎𝐍𝐅||𝐑𝐄</title>
            <style>
                :root {
                    --bg: #000000;
                    --card: #111111;
                    --accent: #7f00ff;
                    --text: #f0f0f0;
                    --text-dim: #888888;
                    --danger: #ff3366;
                }
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', system-ui, sans-serif;
                }
                body {
                    background: var(--bg);
                    color: var(--text);
                    min-height: 100vh;
                    padding: 20px;
                    line-height: 1.6;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background: var(--card);
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0 0 20px rgba(127, 0, 255, 0.1);
                    border: 1px solid rgba(255,255,255,0.05);
                }
                h1 {
                    text-align: center;
                    margin-bottom: 25px;
                    color: var(--accent);
                    font-size: 28px;
                    letter-spacing: 1px;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    color: var(--text-dim);
                    font-size: 14px;
                }
                input[type="text"],
                input[type="number"],
                input[type="password"],
                input[type="file"] {
                    width: 100%;
                    padding: 12px 15px;
                    background: rgba(0,0,0,0.3);
                    border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 6px;
                    color: var(--text);
                    font-size: 15px;
                    transition: all 0.3s;
                }
                input:focus {
                    outline: none;
                    border-color: var(--accent);
                    box-shadow: 0 0 0 3px rgba(127, 0, 255, 0.2);
                }
                .radio-group {
                    display: flex;
                    gap: 20px;
                    margin-bottom: 20px;
                }
                .radio-group label {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    cursor: pointer;
                }
                input[type="radio"] {
                    accent-color: var(--accent);
                }
                button {
                    width: 100%;
                    padding: 14px;
                    background: var(--accent);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.3s;
                    margin-top: 10px;
                    letter-spacing: 0.5px;
                }
                button:hover {
                    background: #6a00d4;
                    transform: translateY(-2px);
                }
                .file-input {
                    display: none;
                }
                .file-label {
                    display: block;
                    padding: 12px;
                    background: rgba(0,0,0,0.3);
                    border: 1px dashed rgba(255,255,255,0.2);
                    border-radius: 6px;
                    text-align: center;
                    cursor: pointer;
                    transition: all 0.3s;
                    margin-bottom: 15px;
                }
                .file-label:hover {
                    border-color: var(--accent);
                    background: rgba(127, 0, 255, 0.1);
                }
                .nav-links {
                    display: flex;
                    justify-content: center;
                    gap: 15px;
                    margin-top: 25px;
                }
                .nav-links a {
                    color: var(--text-dim);
                    text-decoration: none;
                    font-size: 14px;
                    transition: all 0.3s;
                    padding: 8px 12px;
                    border-radius: 4px;
                }
                .nav-links a:hover {
                    color: var(--accent);
                    background: rgba(127, 0, 255, 0.1);
                }
                .glow {
                    animation: glow 2s infinite alternate;
                }
                @keyframes glow {
                    from {
                        text-shadow: 0 0 5px rgba(127, 0, 255, 0.5);
                    }
                    to {
                        text-shadow: 0 0 10px rgba(127, 0, 255, 0.8);
                    }
                }
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
                        <label class="file-label" onclick="document.getElementById('tokenFile').click()">
                            Click to Upload Token File
                        </label>
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
                        <label class="file-label" onclick="document.getElementById('messageFile').click()">
                            Click to Upload Messages File
                        </label>
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
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
