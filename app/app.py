from flask import Flask, jsonify, request, render_template_string
import uuid
import os

app = Flask(__name__)

todos = []

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Todos</title>
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
  <style>
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
    :root{--bg:#0e0e0f;--surface:#1a1a1d;--border:#2a2a2e;--accent:#e8ff47;--text:#f0f0f0;--muted:#666}
    body{background:var(--bg);color:var(--text);font-family:'DM Mono',monospace;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:60px 20px}
    .container{width:100%;max-width:600px}
    header{margin-bottom:48px}
    header h1{font-family:'Syne',sans-serif;font-size:3.5rem;font-weight:800;letter-spacing:-2px}
    header h1 span{color:var(--accent)}
    header p{color:var(--muted);margin-top:8px;font-size:0.85rem;letter-spacing:1px;text-transform:uppercase}
    .input-row{display:flex;gap:10px;margin-bottom:40px}
    input[type="text"]{flex:1;background:var(--surface);border:1.5px solid var(--border);color:var(--text);font-family:'DM Mono',monospace;font-size:0.95rem;padding:14px 18px;border-radius:10px;outline:none;transition:border-color 0.2s}
    input[type="text"]:focus{border-color:var(--accent)}
    input[type="text"]::placeholder{color:var(--muted)}
    button.add-btn{background:var(--accent);color:#000;border:none;font-family:'Syne',sans-serif;font-weight:700;font-size:0.95rem;padding:14px 24px;border-radius:10px;cursor:pointer;transition:transform 0.15s}
    button.add-btn:hover{transform:scale(1.04)}
    .stats{display:flex;gap:20px;margin-bottom:24px;font-size:0.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:1px}
    .stats span{color:var(--accent);font-weight:700}
    .todo-list{display:flex;flex-direction:column;gap:10px}
    .todo-item{display:flex;align-items:center;gap:14px;background:var(--surface);border:1.5px solid var(--border);border-radius:12px;padding:16px 18px;transition:border-color 0.2s,transform 0.15s}
    .todo-item:hover{border-color:#3a3a3e;transform:translateX(3px)}
    .todo-item.done{opacity:0.45}
    .todo-item.done .todo-text{text-decoration:line-through;color:var(--muted)}
    .check-btn{width:24px;height:24px;border-radius:50%;border:2px solid var(--border);background:transparent;cursor:pointer;flex-shrink:0;transition:all 0.2s;display:flex;align-items:center;justify-content:center;font-size:0.7rem}
    .check-btn:hover{border-color:var(--accent)}
    .todo-item.done .check-btn{background:var(--accent);border-color:var(--accent);color:#000}
    .todo-text{flex:1;font-size:0.95rem;line-height:1.4}
    .delete-btn{background:transparent;border:none;color:var(--muted);cursor:pointer;font-size:1.1rem;padding:4px 8px;border-radius:6px;transition:color 0.2s}
    .delete-btn:hover{color:#ff6b35}
    .empty{text-align:center;color:var(--muted);font-size:0.85rem;padding:60px 0;letter-spacing:1px;text-transform:uppercase}
    .empty div{font-size:2.5rem;margin-bottom:12px}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>my<span>.</span>todos</h1>
      <p>stay focused — get it done</p>
    </header>
    <div class="input-row">
      <input type="text" id="todoInput" placeholder="what needs to be done?" />
      <button class="add-btn" onclick="addTodo()">+ Add</button>
    </div>
    <div class="stats">
      <div><span id="totalCount">0</span> total</div>
      <div><span id="doneCount">0</span> done</div>
      <div><span id="leftCount">0</span> left</div>
    </div>
    <div class="todo-list" id="todoList"></div>
  </div>
  <script>
    let todos = [];
    async function loadTodos(){const res=await fetch('/api/todos');todos=await res.json();render()}
    async function addTodo(){const input=document.getElementById('todoInput');const text=input.value.trim();if(!text)return;await fetch('/api/todos',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});input.value='';loadTodos()}
    async function toggleTodo(id){await fetch('/api/todos/'+id+'/toggle',{method:'PATCH'});loadTodos()}
    async function deleteTodo(id){await fetch('/api/todos/'+id,{method:'DELETE'});loadTodos()}
    function render(){const list=document.getElementById('todoList');const total=todos.length;const done=todos.filter(t=>t.done).length;document.getElementById('totalCount').textContent=total;document.getElementById('doneCount').textContent=done;document.getElementById('leftCount').textContent=total-done;if(todos.length===0){list.innerHTML='<div class="empty"><div>✦</div>no tasks yet</div>';return}list.innerHTML=todos.map((t,i)=>`<div class="todo-item ${t.done?'done':''}" style="animation-delay:${i*0.05}s"><button class="check-btn" onclick="toggleTodo('${t.id}')">${t.done?'✓':''}</button><span class="todo-text">${t.text}</span><button class="delete-btn" onclick="deleteTodo('${t.id}')">✕</button></div>`).join('')}
    document.getElementById('todoInput').addEventListener('keydown',e=>{if(e.key==='Enter')addTodo()});
    loadTodos();
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    todo = {"id": str(uuid.uuid4()), "text": data["text"], "done": False}
    todos.append(todo)
    return jsonify(todo), 201

@app.route("/api/todos/<id>/toggle", methods=["PATCH"])
def toggle_todo(id):
    for t in todos:
        if t["id"] == id:
            t["done"] = not t["done"]
            return jsonify(t)
    return jsonify({"error": "not found"}), 404

@app.route("/api/todos/<id>", methods=["DELETE"])
def delete_todo(id):
    global todos
    todos = [t for t in todos if t["id"] != id]
    return jsonify({"deleted": id})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)