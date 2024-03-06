from app import app

import pytest
import tempfile
import os

@pytest.fixture
def client():
    # Create a test client using Flask's built-in test tools
    app.config['TESTING'] = True
    client = app.test_client()

    # Create a temporary database file for testing
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    yield client

    # Cleanup after testing
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_index(client):
    # Test if the index page returns a 200 OK status
    response = client.get('/')
    assert response.status_code == 200

def test_add_multiple_tasks(client):
    # Test adding multiple tasks
    tasks_to_add = ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5',
                    'Task 6', 'Task 7', 'Task 8', 'Task 9', 'Task 10']
    
    for task in tasks_to_add:
        response = client.post('/add', data={'task': task})
        assert response.status_code == 302  # Redirect after adding task

    # Check if all tasks are added
    response = client.get('/')
    tasks_in_response = response.data.decode('utf-8').split('<br>')

    formatted_tasks = '\n'.join(tasks_in_response)
    
    print("Tasks after adding:")
    print(formatted_tasks)

    for task in tasks_to_add:
        assert task.encode() in response.data
