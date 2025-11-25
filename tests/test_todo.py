import pytest
import json
import os
from todo.core import (
    load_tasks,
    save_tasks,
    add_task,
    delete_task,
    complete_task,
    list_tasks,
    TASKS_FILE,
)


@pytest.fixture
def temp_tasks_file(monkeypatch, tmp_path):
    temp_file = tmp_path / "tasks.json"
    monkeypatch.setattr("todo.core.TASKS_FILE", str(temp_file))
    return temp_file


def test_load_tasks_existing_file(temp_tasks_file):
    tasks = [{"id": 1, "description": "Test task", "completed": False}]
    with open(temp_tasks_file, "w") as f:
        json.dump(tasks, f)

    loaded_tasks = load_tasks()
    assert loaded_tasks == tasks


def test_load_tasks_nonexistent_file(monkeypatch):
    temp_file = "nonexistent.json"
    monkeypatch.setattr("todo.core.TASKS_FILE", str(temp_file))

    tasks = load_tasks()
    assert tasks == []


def test_save_tasks(temp_tasks_file):
    tasks = [{"id": 1, "description": "Test task", "completed": False}]

    save_tasks(tasks)
    with open(temp_tasks_file, "r") as f:
        saved_tasks = json.load(f)
    assert saved_tasks == tasks


def test_add_task_empty_list(temp_tasks_file):
    tasks = []
    add_task(tasks, "New task")
    assert len(tasks) == 1
    assert tasks[0] == {"id": 1, "description": "New task", "completed": False}

    with open(temp_tasks_file, "r") as f:
        saved_tasks = json.load(f)
    assert saved_tasks == tasks


def test_add_task_non_empty_list(temp_tasks_file):
    tasks = [{"id": 1, "description": "Buy milk", "completed": True}]
    add_task(tasks, "New task")
    assert len(tasks) == 2
    assert tasks[1] == {"id": 2, "description": "New task", "completed": False}

    with open(temp_tasks_file, "r") as f:
        saved_tasks = json.load(f)
    assert saved_tasks == tasks


def test_delete_task_existing(temp_tasks_file):
    tasks = [{"id": 1, "description": "Buy milk", "completed": False}]

    delete_task(tasks, 1)
    assert tasks == []

    with open(temp_tasks_file, "r") as f:
        saved_tasks = json.load(f)
    assert saved_tasks == []


def test_delete_task_nonexistent():
    tasks = [{"id": 1, "description": "Buy milk", "completed": False}]

    delete_task(tasks, 999)
    assert tasks == [{"id": 1, "description": "Buy milk", "completed": False}]


def test_complete_task_existing(temp_tasks_file):
    tasks = [{"id": 1, "description": "Buy milk", "completed": False}]

    complete_task(tasks, 1)
    assert tasks[0]["completed"] is True

    with open(temp_tasks_file, "r") as f:
        saved_tasks = json.load(f)
    assert saved_tasks[0]["completed"] is True


def test_complete_task_nonexisting():
    tasks = [{"id": 1, "description": "Buy milk", "completed": False}]

    complete_task(tasks, 999)
    assert tasks[0]["completed"] is False


def test_list_tasks_empty(capsys):
    tasks = []
    list_tasks(tasks)
    captured = capsys.readouterr()
    assert "No tasks found." in captured.out


def test_list_tasks_non_empty(capsys):
    tasks = [{"id": 1, "description": "Buy milk", "completed": True}]
    list_tasks(tasks)
    captured = capsys.readouterr()
    assert "ID: 1 - Buy milk" in captured.out
