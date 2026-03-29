import streamlit as st
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("**Smart Pet Care Management System**")

st.divider()

# Initialize session state for Owner and Scheduler
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Pet Owner")
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

# Sidebar for Pet Management
with st.sidebar:
    st.header("🐕 Pet Management")

    with st.form("add_pet_form"):
        st.subheader("Add New Pet")
        pet_name = st.text_input("Pet Name", value="")
        pet_species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
        pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=1)
        add_pet_button = st.form_submit_button("Add Pet")

        if add_pet_button and pet_name:
            # Check if pet already exists
            if owner.get_pet_by_name(pet_name):
                st.error(f"Pet '{pet_name}' already exists!")
            else:
                new_pet = Pet(name=pet_name, species=pet_species, age=pet_age)
                owner.add_pet(new_pet)
                st.success(f"Added {pet_name} ({pet_species})!")
                st.rerun()

    st.divider()

    # Display current pets
    if owner.pets:
        st.subheader("Your Pets")
        for pet in owner.pets:
            st.write(f"🐾 **{pet.name}** ({pet.species}, {pet.age} yrs) - {pet.get_task_count()} tasks")
    else:
        st.info("No pets yet. Add one above!")

# Main area - Task Management
st.header("📋 Task Management")

# Task addition form
if owner.pets:
    with st.form("add_task_form"):
        st.subheader("Schedule a Task")

        col1, col2 = st.columns(2)
        with col1:
            selected_pet = st.selectbox("Pet", [pet.name for pet in owner.pets])
            task_desc = st.text_input("Task Description", value="")
            task_time = st.time_input("Time", value=None)

        with col2:
            task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=15)
            task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
            task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=0)

        add_task_button = st.form_submit_button("Add Task")

        if add_task_button and task_desc and task_time:
            pet = owner.get_pet_by_name(selected_pet)
            if pet:
                new_task = Task(
                    description=task_desc,
                    time=task_time.strftime("%H:%M"),
                    duration_minutes=task_duration,
                    priority=task_priority,
                    frequency=task_frequency,
                    due_date=date.today()
                )
                pet.add_task(new_task)
                st.success(f"Added '{task_desc}' for {selected_pet}!")
                st.rerun()
else:
    st.warning("Please add a pet first (use the sidebar)!")

st.divider()

# Display Today's Schedule
st.header("📅 Today's Schedule")

if owner.pets and len(owner.get_all_tasks()) > 0:
    schedule = scheduler.get_todays_schedule()

    if schedule:
        # Check for conflicts
        conflicts = scheduler.detect_conflicts(schedule)
        if conflicts:
            st.warning("⚠️ **Schedule Conflicts Detected:**")
            for conflict in conflicts:
                st.write(f"- {conflict}")
            st.divider()

        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            filter_pet = st.selectbox(
                "Filter by pet",
                ["All pets"] + [pet.name for pet in owner.pets],
                key="filter_pet"
            )
        with col2:
            filter_status = st.selectbox(
                "Filter by status",
                ["All tasks", "Pending only", "Completed only"],
                key="filter_status"
            )

        # Apply filters
        filtered_schedule = schedule.copy()

        if filter_pet != "All pets":
            filtered_schedule = scheduler.filter_by_pet(filtered_schedule, filter_pet)

        if filter_status == "Pending only":
            filtered_schedule = scheduler.filter_by_status(filtered_schedule, completed=False)
        elif filter_status == "Completed only":
            filtered_schedule = scheduler.filter_by_status(filtered_schedule, completed=True)

        # Display schedule as a table
        if filtered_schedule:
            for i, task in enumerate(filtered_schedule):
                status_icon = "✅" if task.is_completed else "⏳"
                priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")

                with st.container():
                    col1, col2, col3, col4 = st.columns([0.5, 2, 1, 1])

                    with col1:
                        st.write(status_icon)
                    with col2:
                        st.write(f"**{task.time}** - {task.pet_name}: {task.description}")
                    with col3:
                        st.write(f"{priority_icon} {task.priority} | {task.duration_minutes}min")
                    with col4:
                        if not task.is_completed:
                            if st.button("Complete", key=f"complete_{i}"):
                                scheduler.mark_task_complete(task)
                                st.success(f"Completed '{task.description}'!")
                                if task.frequency != "once":
                                    st.info(f"Next occurrence scheduled for tomorrow!")
                                st.rerun()

                    st.divider()
        else:
            st.info("No tasks match your filters.")

        # Statistics
        st.subheader("📊 Statistics")
        pending_count = len(scheduler.filter_by_status(schedule, completed=False))
        completed_count = len(scheduler.filter_by_status(schedule, completed=True))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", len(schedule))
        with col2:
            st.metric("Pending", pending_count)
        with col3:
            st.metric("Completed", completed_count)
    else:
        st.info("No tasks scheduled for today.")
else:
    st.info("No tasks yet. Add some pets and tasks to get started!")
