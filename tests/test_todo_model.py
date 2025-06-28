import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from todo import Todo

def test_todo_model_fields():
    todo = Todo(id=1, user_id=1, title="Test Todo", completed=True)
    assert todo.id == 1
    assert todo.user_id == 1
    assert todo.title == "Test Todo"
    assert todo.completed is True

def test_todo_str_repr():
    todo = Todo(id=2, user_id=2, title="Another Todo", completed=False)
    assert "Another Todo" in str(todo)
    assert "False" in repr(todo)
