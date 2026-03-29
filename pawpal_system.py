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
        pass

    def create_next_occurrence(self) -> Optional['Task']:
        """Create the next recurring instance of this task."""
        pass


@dataclass
class Pet:
    """Represents a pet with their care tasks."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's schedule."""
        pass

    def get_tasks(self) -> List[Task]:
        """Get all tasks for this pet."""
        pass

    def get_pending_tasks(self) -> List[Task]:
        """Get all incomplete tasks for this pet."""
        pass

    def get_task_count(self) -> int:
        """Get the total number of tasks."""
        pass


class Owner:
    """Represents the pet owner managing multiple pets."""

    def __init__(self, name: str):
        """Initialize owner with a name."""
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's collection."""
        pass

    def remove_pet(self, pet_name: str):
        """Remove a pet by name."""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all pets."""
        pass

    def get_pet_by_name(self, name: str) -> Optional[Pet]:
        """Find a pet by name."""
        pass


class Scheduler:
    """The brain that organizes and manages tasks."""

    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner."""
        self.owner = owner

    def get_todays_schedule(self) -> List[Task]:
        """Get all tasks scheduled for today."""
        pass

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their scheduled time."""
        pass

    def filter_by_status(self, tasks: List[Task], completed: bool) -> List[Task]:
        """Filter tasks by completion status."""
        pass

    def filter_by_pet(self, tasks: List[Task], pet_name: str) -> List[Task]:
        """Filter tasks by pet name."""
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect scheduling conflicts (same time for same pet)."""
        pass

    def mark_task_complete(self, task: Task):
        """Mark a task as complete and handle recurrence."""
        pass
