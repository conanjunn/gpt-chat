from flask import Flask, request, jsonify, Response, send_from_directory
import requests
import json
import time
from config import API_URL, API_KEY, MODEL, INSTRUCTIONS

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/marked.min.js')
def marked_js():
    return send_from_directory('.', 'marked.min.js')

# 内存存储聊天记录
conversations = {}
last_access = {}

def cleanup_old_conversations():
    """清理超过1小时未使用的会话"""
    now = time.time()
    to_delete = [cid for cid, t in last_access.items() if now - t > 3600]
    for cid in to_delete:
        conversations.pop(cid, None)
        last_access.pop(cid, None)

@app.route('/chat', methods=['POST'])
def chat():
    cleanup_old_conversations()

    data = request.json
    user_message = data.get('message', '')
    conversation_id = data.get('conversation_id', 'default')

    # 获取或创建会话
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    # 更新访问时间
    last_access[conversation_id] = time.time()

    # 添加用户消息
    conversations[conversation_id].append({
        "type": "message",
        "role": "user",
        "content": [{"type": "input_text", "text": user_message}]
    })

    # 保持最多20条消息
    if len(conversations[conversation_id]) > 20:
        conversations[conversation_id] = conversations[conversation_id][-20:]

    # 调用 API
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    api_data = {
        "model": MODEL,
        "instructions": INSTRUCTIONS,
        "input": conversations[conversation_id],
        "stream": True,
        "store": True,
        "tools": [{"type": "web_search"}]
    }

    def generate():
        response = requests.post(API_URL, headers=headers, json=api_data, stream=True)
        assistant_message = ""

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    content = line[6:]
                    if content != '[DONE]':
                        try:
                            chunk = json.loads(content)
                            if chunk.get('type') == 'response.output_text.delta':
                                if 'delta' in chunk:
                                    delta = chunk['delta']
                                    assistant_message += delta
                                    yield delta
                        except:
                            pass

        # 保存助手回复
        conversations[conversation_id].append({
            "type": "message",
            "role": "assistant",
            "content": [{"type": "output_text", "text": assistant_message}]
        })

    return Response(generate(), mimetype='text/plain')

@app.route('/history/<conversation_id>', methods=['GET'])
def get_history(conversation_id):
    return jsonify(conversations.get(conversation_id, []))

@app.route('/clear/<conversation_id>', methods=['POST'])
def clear_history(conversation_id):
    if conversation_id in conversations:
        del conversations[conversation_id]
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
