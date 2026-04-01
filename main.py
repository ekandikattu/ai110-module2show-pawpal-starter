from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
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

    task_walk = Task(
        task_id="task-001",
        description="Morning walk",
        time_minutes=30,
        frequency="daily",
        pet_id="pet-001",
    )
    task_feed = Task(
        task_id="task-002",
        description="Evening feeding",
        time_minutes=15,
        frequency="daily",
        pet_id="pet-002",
    )
    task_meds = Task(
        task_id="task-003",
        description="Medication",
        time_minutes=10,
        frequency="daily",
        pet_id="pet-001",
    )

    owner.addTask(task_walk)
    owner.addTask(task_feed)
    owner.addTask(task_meds)

    scheduler = Scheduler()
    owner_tasks = scheduler.retrieveTasks(owner)
    scheduler.makeSchedule(
        owner_tasks=owner_tasks,
        time_available=60,
        preferences=owner.getPreferences(),
    )

    print("Today's Schedule")
    print("----------------")
    for item in scheduler.showSchedule():
        print(f"- {item}")


if __name__ == "__main__":
    main()
