from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional


ALLOWED_FREQUENCIES = {"once", "daily", "weekly", "monthly", "as_needed"}
ALLOWED_HEALTH_STATUSES = {"healthy", "needs_attention", "sick", "recovering", "unknown"}


@dataclass
class Task:
    task_id: str
    description: str
    time_minutes: int
    frequency: str
    is_completed: bool = False
    pet_id: Optional[str] = None
    due_date: Optional[date] = None
    scheduled_time: Optional[str] = None


       
    def __post_init__(self) -> None:
        """Validate task fields after dataclass initialization."""
        self.validate_task_id(self.task_id)
        self.setDescription(self.description)
        self.validate_time_minutes(self.time_minutes)
        self.validate_frequency(self.frequency)
        self.validate_completion_status(self.is_completed)
        self.validate_pet_link(self.pet_id)
        self.validate_due_date(self.due_date)
        self.validate_scheduled_time(self.scheduled_time)

    def validate_task_id(self, task_id: str) -> None:
        """Validation rule: task_id must be non-empty and unique at Owner level."""
        if not isinstance(task_id, str) or not task_id.strip():
            raise ValueError("task_id must be a non-empty string")

    def validate_time_minutes(self, time_minutes: int) -> None:
        """Validation rule: time_minutes must be a positive integer."""
        if not isinstance(time_minutes, int) or time_minutes <= 0:
            raise ValueError("time_minutes must be a positive integer")

    def validate_frequency(self, frequency: str) -> None:
        """Validation rule: frequency must be one of the allowed values."""
        if not isinstance(frequency, str) or frequency.strip() not in ALLOWED_FREQUENCIES:
            allowed = ", ".join(sorted(ALLOWED_FREQUENCIES))
            raise ValueError(f"frequency must be one of: {allowed}")

    def validate_completion_status(self, is_completed: bool) -> None:
        """Validation rule: completion status must be a boolean."""
        if not isinstance(is_completed, bool):
            raise ValueError("is_completed must be a boolean")

    def validate_pet_link(self, pet_id: Optional[str]) -> None:
        """Validation rule: pet_id may be None for owner-level tasks."""
        if pet_id is not None and (not isinstance(pet_id, str) or not pet_id.strip()):
            raise ValueError("pet_id must be None or a non-empty string")

    def validate_due_date(self, due_date: Optional[date]) -> None:
        """Validation rule: due_date may be None or a datetime.date value."""
        if due_date is not None and not isinstance(due_date, date):
            raise ValueError("due_date must be None or a datetime.date instance")

    def validate_scheduled_time(self, scheduled_time: Optional[str]) -> None:
        """Validation rule: scheduled_time may be None or HH:MM in 24-hour format."""
        if scheduled_time is None:
            return
        if not isinstance(scheduled_time, str):
            raise ValueError("scheduled_time must be None or a string in HH:MM format")
        normalized = scheduled_time.strip()
        if len(normalized) != 5 or normalized[2] != ":":
            raise ValueError("scheduled_time must use HH:MM format")

        hour, minute = normalized.split(":", 1)
        if not (hour.isdigit() and minute.isdigit()):
            raise ValueError("scheduled_time must use HH:MM format")

        hour_value = int(hour)
        minute_value = int(minute)
        if not (0 <= hour_value <= 23 and 0 <= minute_value <= 59):
            raise ValueError("scheduled_time must be a valid 24-hour time")

    def setScheduledTime(self, scheduled_time: Optional[str]) -> None:
        """Set and validate the optional task start time (HH:MM)."""
        self.validate_scheduled_time(scheduled_time)
        self.scheduled_time = scheduled_time.strip() if isinstance(scheduled_time, str) else None

    def setDescription(self, description: str) -> None:
        """Set and validate the task description."""
        if not isinstance(description, str) or not description.strip():
            raise ValueError("description must be a non-empty string")
        self.description = description.strip()

    def setTimeMinutes(self, time_minutes: int) -> None:
        """Set and validate the task duration in minutes."""
        self.validate_time_minutes(time_minutes)
        self.time_minutes = time_minutes

    def setFrequency(self, frequency: str) -> None:
        """Set and validate the task frequency value."""
        normalized = frequency.strip() if isinstance(frequency, str) else frequency
        self.validate_frequency(normalized)
        self.frequency = normalized

    def mark_complete(self, is_completed: bool = True) -> None:
        """Update the task completion status."""
        self.validate_completion_status(is_completed)
        self.is_completed = is_completed

    def setPetId(self, pet_id: Optional[str]) -> None:
        """Set and validate the optional pet link for the task."""
        self.validate_pet_link(pet_id)
        self.pet_id = pet_id.strip() if isinstance(pet_id, str) else None


@dataclass
class Pet:
    pet_id: str
    name: str
    breed: str
    weight: float
    health_status: str
    tasks_ordered: List[Task] = field(default_factory=list)
    tasks_by_id: Dict[str, Task] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate pet fields and normalize embedded task collections."""
        self.validate_pet_id(self.pet_id)
        self.validate_name(self.name)
        self.validate_breed(self.breed)
        self.validate_weight(self.weight)
        self.validate_health_status(self.health_status)

        rebuilt_tasks: List[Task] = []
        rebuilt_index: Dict[str, Task] = {}
        for task in self.tasks_ordered:
            if task.task_id in rebuilt_index:
                raise ValueError(f"Duplicate task_id in pet tasks_ordered: {task.task_id}")
            if task.pet_id is None:
                task.setPetId(self.pet_id)
            if task.pet_id != self.pet_id:
                raise ValueError(f"Task {task.task_id} is linked to a different pet_id")
            rebuilt_tasks.append(task)
            rebuilt_index[task.task_id] = task

        for task_id, task in self.tasks_by_id.items():
            if task_id != task.task_id:
                raise ValueError("tasks_by_id key must match Task.task_id")
            if task.pet_id is None:
                task.setPetId(self.pet_id)
            if task.pet_id != self.pet_id:
                raise ValueError(f"Task {task.task_id} is linked to a different pet_id")
            if task_id not in rebuilt_index:
                rebuilt_tasks.append(task)
                rebuilt_index[task_id] = task

        self.tasks_ordered = rebuilt_tasks
        self.tasks_by_id = rebuilt_index

    def validate_pet_id(self, pet_id: str) -> None:
        """Validation rule: pet_id must be non-empty and unique at Owner level."""
        if not isinstance(pet_id, str) or not pet_id.strip():
            raise ValueError("pet_id must be a non-empty string")

    def validate_name(self, name: str) -> None:
        """Validation rule: pet name must be non-empty."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")

    def validate_breed(self, breed: str) -> None:
        """Validation rule: breed must be non-empty."""
        if not isinstance(breed, str) or not breed.strip():
            raise ValueError("breed must be a non-empty string")

    def validate_weight(self, weight: float) -> None:
        """Validation rule: weight must be a positive number."""
        if not isinstance(weight, (int, float)) or float(weight) <= 0:
            raise ValueError("weight must be a positive number")

    def validate_health_status(self, status: str) -> None:
        """Validation rule: health status must be one of the allowed values."""
        if not isinstance(status, str) or status.strip() not in ALLOWED_HEALTH_STATUSES:
            allowed = ", ".join(sorted(ALLOWED_HEALTH_STATUSES))
            raise ValueError(f"health_status must be one of: {allowed}")

    def getPetId(self) -> str:
        """Return the pet identifier."""
        return self.pet_id

    def getName(self) -> str:
        """Return the pet name."""
        return self.name

    def getBreed(self) -> str:
        """Return the pet breed."""
        return self.breed

    def getWeight(self) -> float:
        """Return the pet weight."""
        return self.weight

    def getStatus(self) -> str:
        """Return the pet health status."""
        return self.health_status

    def setName(self, name: str) -> None:
        """Set and validate the pet name."""
        self.validate_name(name)
        self.name = name.strip()

    def setBreed(self, breed: str) -> None:
        """Set and validate the pet breed."""
        self.validate_breed(breed)
        self.breed = breed.strip()

    def setWeight(self, weight: float) -> None:
        """Set and validate the pet weight."""
        self.validate_weight(weight)
        self.weight = float(weight)

    def setStatus(self, status: str) -> None:
        """Set and validate the pet health status."""
        normalized = status.strip() if isinstance(status, str) else status
        self.validate_health_status(normalized)
        self.health_status = normalized

    def setPetId(self, pet_id: str) -> None:
        """Set and validate the pet identifier."""
        self.validate_pet_id(pet_id)
        self.pet_id = pet_id.strip()

    def addTask(self, task: Task) -> None:
        """Add a task to this pet and sync internal task indexes."""
        if task.task_id in self.tasks_by_id:
            raise ValueError(f"Task with task_id '{task.task_id}' already exists for this pet")
        if task.pet_id is None:
            task.setPetId(self.pet_id)
        if task.pet_id != self.pet_id:
            raise ValueError(f"Task pet_id '{task.pet_id}' does not match Pet pet_id '{self.pet_id}'")

        self.tasks_ordered.append(task)
        self.tasks_by_id[task.task_id] = task

    def removeTask(self, task_id: str) -> bool:
        """Remove a task from this pet by task identifier."""
        task = self.tasks_by_id.pop(task_id, None)
        if task is None:
            return False

        self.tasks_ordered = [item for item in self.tasks_ordered if item.task_id != task_id]
        return True

    def getTaskById(self, task_id: str) -> Optional[Task]:
        """Retrieve a task for this pet by task identifier."""
        return self.tasks_by_id.get(task_id)

    def showTasks(self) -> List[str]:
        """Return display strings for all tasks owned by this pet."""
        return [
            (
                f"Task(task_id={task.task_id}, description={task.description}, "
                f"time_minutes={task.time_minutes}, frequency={task.frequency}, "
                f"is_completed={task.is_completed}, pet_id={task.pet_id})"
            )
            for task in self.tasks_ordered
        ]

    def showPetInfo(self) -> str:
        """Return a display string summarizing this pet."""
        return (
            f"Pet(pet_id={self.pet_id}, name={self.name}, breed={self.breed}, "
            f"weight={self.weight}, health_status={self.health_status}, "
            f"task_count={len(self.tasks_ordered)})"
        )


class Owner:
    def __init__(self, gender: str, age: int, preferences: str = "") -> None:
        """Initialize owner data and pet/task storage structures."""
        # Ordered lists for display
        self.pets_ordered: List[Pet] = []
        self.tasks_ordered: List[Task] = []
        # Maps for fast lookup/update/delete by ID
        self.pets_by_id: Dict[str, Pet] = {}
        self.tasks_by_id: Dict[str, Task] = {}
        self.gender: str = gender
        self.age: int = age
        self.preferences: str = preferences

    def addPet(self, pet: Pet) -> None:
        """Add a pet and merge its existing tasks into owner indexes."""
        if pet.pet_id in self.pets_by_id:
            raise ValueError(f"Pet with pet_id '{pet.pet_id}' already exists")

        self.pets_ordered.append(pet)
        self.pets_by_id[pet.pet_id] = pet

        # Merge existing pet-linked tasks into owner-level task index.
        for task in pet.tasks_ordered:
            if task.task_id in self.tasks_by_id:
                raise ValueError(
                    f"Task with task_id '{task.task_id}' already exists at owner level"
                )
            self.tasks_ordered.append(task)
            self.tasks_by_id[task.task_id] = task

    def removePet(self, pet_id: str) -> bool:
        """Remove a pet and all of its linked tasks by pet identifier."""
        pet = self.pets_by_id.pop(pet_id, None)
        if pet is None:
            return False

        self.pets_ordered = [item for item in self.pets_ordered if item.pet_id != pet_id]

        # Remove all tasks associated with this pet from owner-level task collections.
        task_ids_to_remove = [task.task_id for task in self.tasks_ordered if task.pet_id == pet_id]
        for task_id in task_ids_to_remove:
            self.tasks_by_id.pop(task_id, None)
        self.tasks_ordered = [task for task in self.tasks_ordered if task.pet_id != pet_id]

        return True

    def getPetById(self, pet_id: str) -> Optional[Pet]:
        """Retrieve a pet by pet identifier."""
        return self.pets_by_id.get(pet_id)

    def showPets(self) -> List[str]:
        """Return display strings for all pets owned by this owner."""
        return [pet.showPetInfo() for pet in self.pets_ordered]

    def showOwnerInfo(self) -> str:
        """Return a display string summarizing this owner."""
        return (
            f"Owner(gender={self.gender}, age={self.age}, preferences={self.preferences}, "
            f"pet_count={len(self.pets_ordered)}, task_count={len(self.tasks_ordered)})"
        )

    def getPreferences(self) -> str:
        """Return the owner preference string."""
        return self.preferences

    def setPreferences(self, preferences: str) -> None:
        """Set the owner preference string."""
        if not isinstance(preferences, str):
            raise ValueError("preferences must be a string")
        self.preferences = preferences

    def addTask(self, task: Task) -> None:
        """Add a task at owner level and optionally link it to a pet."""
        if task.task_id in self.tasks_by_id:
            raise ValueError(f"Task with task_id '{task.task_id}' already exists")

        if task.pet_id is not None:
            pet = self.pets_by_id.get(task.pet_id)
            if pet is None:
                raise ValueError(f"Cannot add task: pet_id '{task.pet_id}' does not exist")
            pet.addTask(task)

        self.tasks_ordered.append(task)
        self.tasks_by_id[task.task_id] = task

    def removeTask(self, task_id: str) -> bool:
        """Remove a task from owner collections and linked pet collections."""
        task = self.tasks_by_id.pop(task_id, None)
        if task is None:
            return False

        self.tasks_ordered = [item for item in self.tasks_ordered if item.task_id != task_id]

        if task.pet_id is not None and task.pet_id in self.pets_by_id:
            self.pets_by_id[task.pet_id].removeTask(task_id)

        return True

    def getTaskById(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by task identifier."""
        return self.tasks_by_id.get(task_id)

    def _generate_recurring_task_id(self, base_task_id: str) -> str:
        """Generate a unique task id for a recurring task instance."""
        counter = 1
        while True:
            candidate = f"{base_task_id}-r{counter}"
            if candidate not in self.tasks_by_id:
                return candidate
            counter += 1

    def _create_next_occurrence_if_needed(self, completed_task: Task) -> None:
        """Create the next task occurrence for supported recurring frequencies."""
        frequency_to_days = {"daily": 1, "weekly": 7}
        days = frequency_to_days.get(completed_task.frequency)
        if days is None:
            return

        next_due_date = date.today() + timedelta(days=days)
        next_task = Task(
            task_id=self._generate_recurring_task_id(completed_task.task_id),
            description=completed_task.description,
            time_minutes=completed_task.time_minutes,
            frequency=completed_task.frequency,
            is_completed=False,
            pet_id=completed_task.pet_id,
            due_date=next_due_date,
            scheduled_time=completed_task.scheduled_time,
        )
        self.addTask(next_task)

    def filterTasks(
        self,
        is_completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filter tasks by completion status and/or pet name."""
        if is_completed is not None and not isinstance(is_completed, bool):
            raise ValueError("is_completed must be a boolean or None")

        normalized_pet_name: Optional[str] = None
        if pet_name is not None:
            if not isinstance(pet_name, str):
                raise ValueError("pet_name must be a string or None")
            normalized_pet_name = pet_name.strip().lower()
            if not normalized_pet_name:
                raise ValueError("pet_name cannot be empty")

        pet_ids_for_name: Optional[set[str]] = None
        if normalized_pet_name is not None:
            pet_ids_for_name = {
                pet.pet_id
                for pet in self.pets_ordered
                if pet.name.strip().lower() == normalized_pet_name
            }

        filtered_tasks: List[Task] = []
        for task in self.tasks_ordered:
            if is_completed is not None and task.is_completed != is_completed:
                continue
            if pet_ids_for_name is not None and task.pet_id not in pet_ids_for_name:
                continue
            filtered_tasks.append(task)

        return filtered_tasks

    def changeTask(
        self,
        task_id: str,
        description: Optional[str] = None,
        time_minutes: Optional[int] = None,
        frequency: Optional[str] = None,
        is_completed: Optional[bool] = None,
        pet_id: Optional[str] = None,
    ) -> bool:
        """Update task fields and optionally move task between pets."""
        task = self.tasks_by_id.get(task_id)
        if task is None:
            return False

        if description is not None:
            task.setDescription(description)
        if time_minutes is not None:
            task.setTimeMinutes(time_minutes)
        if frequency is not None:
            task.setFrequency(frequency)
        was_completed = task.is_completed
        if is_completed is not None:
            task.mark_complete(is_completed)
            if not was_completed and task.is_completed:
                self._create_next_occurrence_if_needed(task)

        if pet_id is not None and pet_id != task.pet_id:
            if pet_id is not None and pet_id not in self.pets_by_id:
                raise ValueError(f"Cannot move task: pet_id '{pet_id}' does not exist")

            old_pet_id = task.pet_id
            if old_pet_id is not None and old_pet_id in self.pets_by_id:
                self.pets_by_id[old_pet_id].removeTask(task.task_id)

            task.setPetId(pet_id)

            if task.pet_id is not None:
                self.pets_by_id[task.pet_id].addTask(task)

        return True

    def showTasks(self) -> List[str]:
        """Return display strings for all tasks at owner level."""
        return [
            (
                f"Task(task_id={task.task_id}, description={task.description}, "
                f"time_minutes={task.time_minutes}, frequency={task.frequency}, "
                f"is_completed={task.is_completed}, pet_id={task.pet_id}, due_date={task.due_date}, "
                f"scheduled_time={task.scheduled_time})"
            )
            for task in self.tasks_ordered
        ]


class Scheduler:
    def __init__(self) -> None:
        """Initialize scheduler state for current and historical plans."""
        self.last_plan: List[Task] = []
        self.plan_history: List[List[Task]] = []
        self.last_warnings: List[str] = []

    def detectTimeConflicts(self, tasks: List[Task]) -> List[str]:
        """Detect same-time task conflicts and return warning messages."""
        tasks_by_time: Dict[str, List[Task]] = {}
        for task in tasks:
            if task.scheduled_time is None:
                continue
            tasks_by_time.setdefault(task.scheduled_time, []).append(task)

        warnings: List[str] = []
        for scheduled_time in sorted(tasks_by_time):
            conflicting_tasks = tasks_by_time[scheduled_time]
            if len(conflicting_tasks) < 2:
                continue

            task_labels = ", ".join(
                f"{task.task_id} ({task.description}, pet_id={task.pet_id})"
                for task in conflicting_tasks
            )
            warnings.append(
                f"Warning: {len(conflicting_tasks)} tasks are scheduled at {scheduled_time}: {task_labels}"
            )

        return warnings

    def makeSchedule(
        self,
        owner_tasks: List[Task],
        time_available: int,
        preferences: str = "",
    ) -> List[Task]:
        """Build a schedule within time constraints and store plan history."""
        if not isinstance(time_available, int) or time_available < 0:
            raise ValueError("time_available must be a non-negative integer")

        candidate_tasks = [task for task in owner_tasks if not task.is_completed]
        candidate_tasks = self.organizeTasks(candidate_tasks)

        preference_tokens = {
            token.strip().lower()
            for token in preferences.replace(";", ",").split(",")
            if token.strip()
        }
        if preference_tokens:
            preferred: List[Task] = []
            non_preferred: List[Task] = []
            for task in candidate_tasks:
                searchable = f"{task.description} {task.frequency}".lower()
                if any(token in searchable for token in preference_tokens):
                    preferred.append(task)
                else:
                    non_preferred.append(task)
            candidate_tasks = preferred + non_preferred

        plan: List[Task] = []
        used_minutes = 0
        for task in candidate_tasks:
            if used_minutes + task.time_minutes <= time_available:
                plan.append(task)
                used_minutes += task.time_minutes

        self.last_plan = list(plan)
        self.plan_history.append(list(plan))
        self.last_warnings = self.detectTimeConflicts(self.last_plan)
        return list(plan)

    def showWarnings(self) -> List[str]:
        """Return warnings from the most recent scheduling run."""
        return list(self.last_warnings)

    def retrieveTasks(self, owner: Owner) -> List[Task]:
        """Retrieve a copy of all owner-managed tasks."""
        return list(owner.tasks_ordered)

    def organizeTasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by frequency priority, then duration and description."""
        frequency_rank = {"daily": 0, "weekly": 1, "monthly": 2, "once": 3, "as_needed": 4}
        return sorted(
            tasks,
            key=lambda task: (
                frequency_rank.get(task.frequency, 99),
                task.time_minutes,
                task.description.lower(),
            ),
        )

    def showSchedule(self) -> List[str]:
        """Return display strings for the latest generated schedule."""
        return [
            (
                f"{task.description} ({task.time_minutes} min, {task.frequency}, "
                f"completed={task.is_completed}, pet_id={task.pet_id}, due_date={task.due_date}, "
                f"scheduled_time={task.scheduled_time})"
            )
            for task in self.last_plan
        ]
