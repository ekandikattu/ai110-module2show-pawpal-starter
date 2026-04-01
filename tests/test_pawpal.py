import importlib.util
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "pawpal_system.py"
SPEC = importlib.util.spec_from_file_location("pawpal_system", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load pawpal_system module for tests")

pawpal_system = importlib.util.module_from_spec(SPEC)
sys.modules["pawpal_system"] = pawpal_system
SPEC.loader.exec_module(pawpal_system)

Pet = pawpal_system.Pet
Task = pawpal_system.Task


def test_task_completion_marks_task_as_completed() -> None:
    task = Task(
        task_id="task-100",
        description="Give medicine",
        time_minutes=5,
        frequency="daily",
        is_completed=False,
    )

    task.mark_complete()

    assert task.is_completed is True


def test_add_task_to_pet_increases_task_count() -> None:
    pet = Pet(
        pet_id="pet-100",
        name="Buddy",
        breed="Beagle",
        weight=12.0,
        health_status="healthy",
    )
    task = Task(
        task_id="task-101",
        description="Evening walk",
        time_minutes=20,
        frequency="daily",
        is_completed=False,
    )

    before_count = len(pet.tasks_ordered)
    pet.addTask(task)
    after_count = len(pet.tasks_ordered)

    assert after_count == before_count + 1
