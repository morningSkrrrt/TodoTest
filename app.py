from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    print(tasks)
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    tasks.append({'id': str(uuid.uuid4()), 'task': task})
    return redirect(url_for('index'))

@app.route('/delete/<string:task_id>')
def delete_task(task_id):
    task_to_delete = next((task for task in tasks if task['id'] == task_id), None)
    if task_to_delete:
        tasks.remove(task_to_delete)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
