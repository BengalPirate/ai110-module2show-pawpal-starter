"""
PawPal+ Demo Script
CLI demonstration of the pet care scheduling system.
"""

from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler


def print_divider():
    """Print a visual divider."""
    print("\n" + "=" * 70 + "\n")


def print_schedule(schedule, title="Today's Schedule"):
    """Print a formatted schedule."""
    print(f"\n{title}")
    print("-" * 70)

    if not schedule:
        print("No tasks scheduled.")
        return

    for task in schedule:
        status = "[X]" if task.is_completed else "[ ]"
        priority_marker = {"high": "!!!", "medium": "!!", "low": "!"}.get(task.priority, "")
        print(f"{status} {task.time} | {task.pet_name:12} | {task.description:25} | "
              f"{task.duration_minutes}min | {task.priority:6} {priority_marker} | {task.frequency}")


def main():
    """Run the PawPal+ system demo."""

    print_divider()
    print("Welcome to PawPal+ - Smart Pet Care Management System")
    print_divider()

    # Create an Owner
    print("Creating owner: Jordan")
    owner = Owner("Jordan")

    # Create Pets
    print("\nAdding pets...")
    mochi = Pet(name="Mochi", species="dog", age=3)
    whiskers = Pet(name="Whiskers", species="cat", age=5)

    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    print(f"  - Added {mochi.name} (dog, age {mochi.age})")
    print(f"  - Added {whiskers.name} (cat, age {whiskers.age})")

    # Add Tasks with different times (intentionally out of order to demo sorting)
    print("\nAdding tasks...")

    # Mochi's tasks
    mochi.add_task(Task(
        description="Morning walk",
        time="07:00",
        duration_minutes=30,
        priority="high",
        frequency="daily"
    ))

    mochi.add_task(Task(
        description="Breakfast",
        time="07:30",
        duration_minutes=10,
        priority="high",
        frequency="daily"
    ))

    mochi.add_task(Task(
        description="Evening walk",
        time="18:00",
        duration_minutes=30,
        priority="high",
        frequency="daily"
    ))

    # Whiskers' tasks
    whiskers.add_task(Task(
        description="Breakfast",
        time="08:00",
        duration_minutes=5,
        priority="high",
        frequency="daily"
    ))

    whiskers.add_task(Task(
        description="Play session",
        time="10:00",
        duration_minutes=15,
        priority="medium",
        frequency="daily"
    ))

    whiskers.add_task(Task(
        description="Medication",
        time="12:00",
        duration_minutes=5,
        priority="high",
        frequency="daily"
    ))

    whiskers.add_task(Task(
        description="Dinner",
        time="18:00",
        duration_minutes=5,
        priority="high",
        frequency="daily"
    ))

    print(f"  - Added {mochi.get_task_count()} tasks for {mochi.name}")
    print(f"  - Added {whiskers.get_task_count()} tasks for {whiskers.name}")

    # Create Scheduler
    scheduler = Scheduler(owner)

    # Display Today's Schedule (sorted by time)
    print_divider()
    schedule = scheduler.get_todays_schedule()
    print_schedule(schedule, "Today's Full Schedule (Sorted by Time)")

    # Demonstrate conflict detection
    print_divider()
    print("Checking for scheduling conflicts...")
    conflicts = scheduler.detect_conflicts(schedule)

    if conflicts:
        print("\nWARNING: Conflicts detected:")
        for conflict in conflicts:
            print(f"  - {conflict}")
    else:
        print("No conflicts found. Schedule looks good!")

    # Demonstrate filtering by pet
    print_divider()
    mochi_tasks = scheduler.filter_by_pet(schedule, "Mochi")
    print_schedule(mochi_tasks, f"Tasks for {mochi.name}")

    whiskers_tasks = scheduler.filter_by_pet(schedule, "Whiskers")
    print_schedule(whiskers_tasks, f"Tasks for {whiskers.name}")

    # Demonstrate task completion and recurrence
    print_divider()
    print("Completing a recurring task...")
    morning_walk = schedule[0]  # First task (07:00 Morning walk)
    print(f"\nMarking '{morning_walk.description}' as complete...")
    scheduler.mark_task_complete(morning_walk)

    print(f"Task completed! Next occurrence created for: {morning_walk.due_date + __import__('datetime').timedelta(days=1)}")

    # Show updated schedule with completion status
    print_divider()
    updated_schedule = scheduler.get_todays_schedule()
    print_schedule(updated_schedule, "Updated Schedule (After Completing Morning Walk)")

    # Demonstrate filtering by completion status
    print_divider()
    pending = scheduler.filter_by_status(updated_schedule, completed=False)
    completed = scheduler.filter_by_status(updated_schedule, completed=True)

    print(f"\nPending tasks: {len(pending)}")
    print(f"Completed tasks: {len(completed)}")

    print_schedule(pending, "Pending Tasks")
    print_schedule(completed, "Completed Tasks")

    # Summary
    print_divider()
    print("Demo Summary:")
    print(f"  - Owner: {owner.name}")
    print(f"  - Pets: {len(owner.pets)}")
    print(f"  - Total tasks: {len(owner.get_all_tasks())}")
    print(f"  - Today's tasks: {len(schedule)}")
    print(f"  - Conflicts detected: {len(conflicts)}")
    print_divider()

    print("\nPawPal+ system demo complete!")


if __name__ == "__main__":
    main()
