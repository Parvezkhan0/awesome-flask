from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
task_id = 1

@app.route('/tasks', methods=['GET'])
def get_tasks():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', len(tasks)))
    paginated_tasks = tasks[offset:offset+limit]
    return jsonify(paginated_tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    global task_id
    new_task = {"id": task_id, "task": request.json['task']}
    tasks.append(new_task)
    task_id += 1
    return jsonify(new_task), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = next((item for item in tasks if item['id'] == id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    task['task'] = request.json['task']
    return jsonify(task)

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    tasks = [task for task in tasks if task['id'] != id]
    return jsonify({"result": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True)
