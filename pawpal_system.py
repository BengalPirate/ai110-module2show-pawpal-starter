"""
PawPal+ System Logic Layer
Contains core classes for managing pet care tasks and scheduling.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    time: str  # Format: "HH:MM"
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    frequency: str = "once"  # "once", "daily", "weekly"
    is_completed: bool = False
    pet_name: str = ""
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task as completed."""
        self.is_completed = True

    def create_next_occurrence(self) -> Optional['Task']:
        """Create the next recurring instance of this task."""
        if self.frequency == "once":
            return None

        # Calculate next due date based on frequency
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None

        # Create new task with same properties but reset completion
        return Task(
            description=self.description,
            time=self.time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            is_completed=False,
            pet_name=self.pet_name,
            due_date=next_date
        )


@dataclass
class Pet:
    """Represents a pet with their care tasks."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's schedule."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Get all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Get all incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.is_completed]

    def get_task_count(self) -> int:
        """Get the total number of tasks."""
        return len(self.tasks)


class Owner:
    """Represents the pet owner managing multiple pets."""

    def __init__(self, name: str):
        """Initialize owner with a name."""
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        """Remove a pet by name."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_pet_by_name(self, name: str) -> Optional[Pet]:
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None


class Scheduler:
    """The brain that organizes and manages tasks."""

    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner."""
        self.owner = owner

    def get_todays_schedule(self) -> List[Task]:
        """Get all tasks scheduled for today."""
        today = date.today()
        all_tasks = self.owner.get_all_tasks()
        todays_tasks = [task for task in all_tasks if task.due_date == today]
        return self.sort_by_time(todays_tasks)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their scheduled time."""
        return sorted(tasks, key=lambda task: task.time)

    def filter_by_status(self, tasks: List[Task], completed: bool) -> List[Task]:
        """Filter tasks by completion status."""
        return [task for task in tasks if task.is_completed == completed]

    def filter_by_pet(self, tasks: List[Task], pet_name: str) -> List[Task]:
        """Filter tasks by pet name."""
        return [task for task in tasks if task.pet_name == pet_name]

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect scheduling conflicts (same time for same pet)."""
        conflicts = []
        # Check each pair of tasks
        for i, task1 in enumerate(tasks):
            for task2 in tasks[i+1:]:
                # Conflict if same pet and same time
                if task1.pet_name == task2.pet_name and task1.time == task2.time:
                    conflict_msg = f"Conflict: {task1.pet_name} has '{task1.description}' and '{task2.description}' both at {task1.time}"
                    if conflict_msg not in conflicts:
                        conflicts.append(conflict_msg)
        return conflicts

    def mark_task_complete(self, task: Task):
        """Mark a task as complete and handle recurrence."""
        task.mark_complete()

        # If recurring, create next occurrence and add to pet
        next_task = task.create_next_occurrence()
        if next_task:
            pet = self.owner.get_pet_by_name(task.pet_name)
            if pet:
                pet.add_task(next_task)
