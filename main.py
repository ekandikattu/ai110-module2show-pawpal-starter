from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Run a terminal demo of scheduling, filtering, and conflict warnings."""
    owner = Owner(gender="female", age=29, preferences="daily,walk,medication")

    pet_one = Pet(
        pet_id="pet-001",
        name="Milo",
        breed="Labrador",
        weight=28.5,
        health_status="healthy",
    )
    pet_two = Pet(
        pet_id="pet-002",
        name="Luna",
        breed="Siamese",
        weight=4.2,
        health_status="healthy",
    )

    owner.addPet(pet_one)
    owner.addPet(pet_two)

    # Add tasks in an intentionally mixed order so sorting behavior is visible.
    task_groom = Task(
        task_id="task-001",
        description="Grooming",
        time_minutes=25,
        frequency="weekly",
        pet_id="pet-001",
    )
    task_walk = Task(
        task_id="task-002",
        description="Morning walk",
        time_minutes=30,
        frequency="daily",
        pet_id="pet-001",
        scheduled_time="08:00",
    )
    task_feed = Task(
        task_id="task-003",
        description="Evening feeding",
        time_minutes=15,
        frequency="daily",
        pet_id="pet-002",
        scheduled_time="08:00",
    )
    task_meds = Task(
        task_id="task-004",
        description="Medication",
        time_minutes=10,
        frequency="daily",
        pet_id="pet-001",
    )
    task_litter = Task(
        task_id="task-005",
        description="Litter box cleanup",
        time_minutes=8,
        frequency="as_needed",
        pet_id="pet-002",
    )

    owner.addTask(task_groom)
    owner.addTask(task_walk)
    owner.addTask(task_feed)
    owner.addTask(task_meds)
    owner.addTask(task_litter)

    # Mark one task complete so completion filtering can be validated.
    owner.changeTask(task_id="task-003", is_completed=True, pet_id="pet-002")

    scheduler = Scheduler()
    owner_tasks = scheduler.retrieveTasks(owner)

    print("Tasks Added (Original Order)")
    print("----------------------------")
    for task in owner_tasks:
        print(
            f"- {task.task_id}: {task.description} "
            f"({task.time_minutes} min, {task.frequency}, completed={task.is_completed}, "
            f"pet_id={task.pet_id}, scheduled_time={task.scheduled_time})"
        )

    print("\nTasks Organized (Frequency, Time, Description)")
    print("----------------------------------------------")
    for task in scheduler.organizeTasks(owner_tasks):
        print(
            f"- {task.task_id}: {task.description} "
            f"({task.time_minutes} min, {task.frequency}, completed={task.is_completed}, "
            f"pet_id={task.pet_id}, scheduled_time={task.scheduled_time})"
        )

    print("\nFiltered Tasks (is_completed=False)")
    print("-----------------------------------")
    for task in owner.filterTasks(is_completed=False):
        print(
            f"- {task.task_id}: {task.description} "
            f"({task.time_minutes} min, {task.frequency}, completed={task.is_completed}, "
            f"pet_id={task.pet_id}, scheduled_time={task.scheduled_time})"
        )

    print("\nFiltered Tasks (pet_name='Milo')")
    print("--------------------------------")
    for task in owner.filterTasks(pet_name="Milo"):
        print(
            f"- {task.task_id}: {task.description} "
            f"({task.time_minutes} min, {task.frequency}, completed={task.is_completed}, "
            f"pet_id={task.pet_id}, scheduled_time={task.scheduled_time})"
        )

    print("\nFiltered Tasks (pet_name='Milo', is_completed=False)")
    print("-----------------------------------------------------")
    for task in owner.filterTasks(pet_name="Milo", is_completed=False):
        print(
            f"- {task.task_id}: {task.description} "
            f"({task.time_minutes} min, {task.frequency}, completed={task.is_completed}, "
            f"pet_id={task.pet_id}, scheduled_time={task.scheduled_time})"
        )

    scheduler.makeSchedule(
        owner_tasks=owner_tasks,
        time_available=60,
        preferences=owner.getPreferences(),
    )

    print("\nToday's Schedule")
    print("----------------")
    for item in scheduler.showSchedule():
        print(f"- {item}")

    print("\nWarnings")
    print("--------")
    warnings = scheduler.showWarnings()
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- No scheduling conflicts detected.")


if __name__ == "__main__":
    main()
