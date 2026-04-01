import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "pawpal_system.py"
SPEC = importlib.util.spec_from_file_location("pawpal_system", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load pawpal_system module for tests")

pawpal_system = importlib.util.module_from_spec(SPEC)
sys.modules["pawpal_system"] = pawpal_system
SPEC.loader.exec_module(pawpal_system)

Pet = pawpal_system.Pet
Task = pawpal_system.Task
Owner = pawpal_system.Owner
Scheduler = pawpal_system.Scheduler


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


def test_change_task_creates_one_daily_recurrence_only_once() -> None:
    owner = Owner(gender="female", age=28)
    pet = Pet("pet-1", "Buddy", "Beagle", 12.0, "healthy")
    owner.addPet(pet)

    task = Task("task-1", "Morning walk", 20, "daily", pet_id="pet-1")
    owner.addTask(task)

    assert owner.changeTask("task-1", is_completed=True) is True
    assert len(owner.tasks_ordered) == 2
    assert owner.getTaskById("task-1-r1") is not None

    # Re-marking a completed task should not generate another recurrence.
    assert owner.changeTask("task-1", is_completed=True) is True
    assert len(owner.tasks_ordered) == 2


@pytest.mark.parametrize(
    "frequency,should_recur",
    [
        ("daily", True),
        ("weekly", True),
        ("monthly", False),
        ("once", False),
        ("as_needed", False),
    ],
)
def test_recurrence_supported_frequencies_only(
    frequency: str, should_recur: bool
) -> None:
    owner = Owner(gender="male", age=35)
    task = Task("task-freq", "Check water", 5, frequency)
    owner.addTask(task)

    owner.changeTask("task-freq", is_completed=True)

    recurrence = owner.getTaskById("task-freq-r1")
    assert (recurrence is not None) is should_recur


def test_recurrence_due_date_uses_existing_due_date_as_baseline() -> None:
    owner = Owner(gender="female", age=30)
    start_due = date.today() + timedelta(days=10)
    task = Task(
        "task-due",
        "Medication",
        10,
        "weekly",
        due_date=start_due,
    )
    owner.addTask(task)

    owner.changeTask("task-due", is_completed=True)

    next_task = owner.getTaskById("task-due-r1")
    assert next_task is not None
    assert next_task.due_date == start_due + timedelta(days=7)


def test_recurrence_task_id_skips_existing_suffixes() -> None:
    owner = Owner(gender="male", age=44)
    base = Task("task-base", "Feed cat", 8, "daily")
    owner.addTask(base)
    owner.addTask(Task("task-base-r1", "Feed cat", 8, "daily"))
    owner.addTask(Task("task-base-r2", "Feed cat", 8, "daily"))

    owner.changeTask("task-base", is_completed=True)

    assert owner.getTaskById("task-base-r3") is not None


def test_organize_tasks_respects_frequency_rank() -> None:
    scheduler = Scheduler()
    tasks = [
        Task("t-once", "A", 10, "once"),
        Task("t-daily", "B", 10, "daily"),
        Task("t-needed", "C", 10, "as_needed"),
        Task("t-weekly", "D", 10, "weekly"),
        Task("t-monthly", "E", 10, "monthly"),
    ]

    ordered = scheduler.organizeTasks(tasks)
    ordered_ids = [task.task_id for task in ordered]

    assert ordered_ids == ["t-daily", "t-weekly", "t-monthly", "t-once", "t-needed"]


def test_organize_tasks_tie_breakers_duration_then_description() -> None:
    scheduler = Scheduler()
    tasks = [
        Task("t3", "Zoo time", 20, "daily"),
        Task("t1", "alpha play", 10, "daily"),
        Task("t2", "Bravo game", 10, "daily"),
    ]

    ordered = scheduler.organizeTasks(tasks)
    ordered_ids = [task.task_id for task in ordered]

    assert ordered_ids == ["t1", "t2", "t3"]


def test_make_schedule_excludes_completed_tasks() -> None:
    scheduler = Scheduler()
    tasks = [
        Task("t1", "Done item", 5, "daily", is_completed=True),
        Task("t2", "Open item", 5, "daily", is_completed=False),
    ]

    plan = scheduler.makeSchedule(tasks, time_available=20)

    assert [task.task_id for task in plan] == ["t2"]


def test_make_schedule_time_available_boundaries() -> None:
    scheduler = Scheduler()
    tasks = [
        Task("t1", "Task one", 10, "daily"),
        Task("t2", "Task two", 5, "daily"),
    ]

    assert scheduler.makeSchedule(tasks, time_available=0) == []
    assert [task.task_id for task in scheduler.makeSchedule(tasks, time_available=15)] == [
        "t2",
        "t1",
    ]

    with pytest.raises(ValueError):
        scheduler.makeSchedule(tasks, time_available=-1)


def test_make_schedule_preferences_prioritize_matching_tasks() -> None:
    scheduler = Scheduler()
    tasks = [
        Task("t1", "Brush teeth", 10, "daily"),
        Task("t2", "Evening walk", 10, "weekly"),
        Task("t3", "Nail trim", 10, "monthly"),
    ]

    plan = scheduler.makeSchedule(tasks, time_available=30, preferences="walk")

    assert [task.task_id for task in plan][0] == "t2"


def test_detect_time_conflicts_only_for_same_scheduled_time() -> None:
    scheduler = Scheduler()
    tasks = [
        Task("t1", "Feed", 10, "daily", scheduled_time="09:00"),
        Task("t2", "Walk", 20, "daily", scheduled_time="09:00"),
        Task("t3", "Play", 15, "daily", scheduled_time="10:00"),
        Task("t4", "Optional", 5, "as_needed", scheduled_time=None),
    ]

    warnings = scheduler.detectTimeConflicts(tasks)

    assert len(warnings) == 1
    assert "09:00" in warnings[0]
    assert "t1" in warnings[0]
    assert "t2" in warnings[0]
