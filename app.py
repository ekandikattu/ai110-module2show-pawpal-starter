import streamlit as st
from pawpal_system import Task, Scheduler, Pet, Owner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
preferences = st.text_input(
    "Scheduling preferences (comma-separated)",
    value="walk, medicine",
    help="Examples: walk, medicine, grooming",
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(gender="unspecified", age=0, preferences="")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
if "task_counter" not in st.session_state:
    st.session_state.task_counter = 1
if "pet_counter" not in st.session_state:
    st.session_state.pet_counter = 1

st.session_state.owner.setPreferences(preferences)

if st.button("Add pet"):
    try:
        pet_id = f"pet-{st.session_state.pet_counter:03d}"
        st.session_state.pet_counter += 1
        new_pet = Pet(
            pet_id=pet_id,
            name=pet_name,
            breed=species,
            weight=10.0,
            health_status="healthy",
        )
        st.session_state.owner.addPet(new_pet)
        st.success(f"Added pet: {pet_name} ({pet_id})")
    except ValueError as err:
        st.error(str(err))

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

pet_options = {
    pet.pet_id: f"{pet.name} ({pet.pet_id})" for pet in st.session_state.owner.pets_ordered
}
selected_pet_id = None
if pet_options:
    selected_pet_id = st.selectbox(
        "Assign task to pet",
        options=list(pet_options.keys()),
        format_func=lambda pet_id: pet_options[pet_id],
    )
else:
    st.info("Add a pet to assign pet-specific tasks.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    priority_to_frequency = {"high": "daily", "medium": "weekly", "low": "as_needed"}
    try:
        task_id = f"task-{st.session_state.task_counter:03d}"
        st.session_state.task_counter += 1
        task = Task(
            task_id=task_id,
            description=task_title,
            time_minutes=int(duration),
            frequency=priority_to_frequency[priority],
            pet_id=selected_pet_id,
        )
        st.session_state.owner.addTask(task)
        st.success(f"Added task: {task_title} ({task_id})")
    except ValueError as err:
        st.error(str(err))

if st.session_state.owner.tasks_ordered:
    st.write("Current tasks (sorted)")

    display_col1, display_col2 = st.columns(2)
    with display_col1:
        show_completed = st.checkbox("Show completed tasks", value=True)
    with display_col2:
        filter_pet_name = st.selectbox(
            "Filter by pet",
            options=["All"] + [pet.name for pet in st.session_state.owner.pets_ordered],
            index=0,
        )

    is_completed_filter = None if show_completed else False
    pet_name_filter = None if filter_pet_name == "All" else filter_pet_name
    filtered_tasks = st.session_state.owner.filterTasks(
        is_completed=is_completed_filter,
        pet_name=pet_name_filter,
    )
    sorted_tasks = st.session_state.scheduler.organizeTasks(filtered_tasks)

    st.table(
        [
            {
                "task_id": task.task_id,
                "description": task.description,
                "time_minutes": task.time_minutes,
                "frequency": task.frequency,
                "is_completed": task.is_completed,
                "pet_id": task.pet_id,
                "due_date": str(task.due_date) if task.due_date else "",
                "scheduled_time": task.scheduled_time or "",
            }
            for task in sorted_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

time_available = st.number_input("Time available today (minutes)", min_value=0, max_value=480, value=60)

if st.button("Generate schedule"):
    try:
        owner_tasks = st.session_state.scheduler.retrieveTasks(st.session_state.owner)
        schedule = st.session_state.scheduler.makeSchedule(
            owner_tasks=owner_tasks,
            time_available=int(time_available),
            preferences=st.session_state.owner.getPreferences(),
        )
        total_minutes = sum(task.time_minutes for task in schedule)
        st.success(
            f"Today's schedule for {owner_name}: {len(schedule)} tasks, {total_minutes} total minutes"
        )

        if schedule:
            st.table(
                [
                    {
                        "task_id": task.task_id,
                        "description": task.description,
                        "time_minutes": task.time_minutes,
                        "frequency": task.frequency,
                        "pet_id": task.pet_id,
                        "due_date": str(task.due_date) if task.due_date else "",
                        "scheduled_time": task.scheduled_time or "",
                    }
                    for task in schedule
                ]
            )

            warnings = st.session_state.scheduler.showWarnings()
            for warning_message in warnings:
                st.warning(warning_message)
        else:
            st.info("No tasks fit into the available time.")
    except ValueError as err:
        st.error(str(err))
