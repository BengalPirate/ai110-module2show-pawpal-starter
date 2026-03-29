"""
Initial test suite for PawPal+ system.
Tests core functionality including task completion, task addition, sorting, filtering,
recurring tasks, and conflict detection.
"""

import pytest
from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTask:
    """Test suite for Task class."""

    def test_task_completion(self):
        """Verify that calling mark_complete() changes the task's status."""
        task = Task(
            description="Morning walk",
            time="08:00",
            duration_minutes=30,
            priority="high"
        )
        assert task.is_completed is False

        task.mark_complete()
        assert task.is_completed is True

    def test_recurring_task_daily(self):
        """Verify that daily recurring tasks create next day instance."""
        task = Task(
            description="Morning walk",
            time="08:00",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            due_date=date.today()
        )

        next_task = task.create_next_occurrence()
        assert next_task is not None
        assert next_task.description == task.description
        assert next_task.time == task.time
        assert next_task.is_completed is False
        assert next_task.due_date == date.today() + timedelta(days=1)

    def test_recurring_task_weekly(self):
        """Verify that weekly recurring tasks create next week instance."""
        task = Task(
            description="Vet checkup",
            time="10:00",
            duration_minutes=60,
            priority="high",
            frequency="weekly",
            due_date=date.today()
        )

        next_task = task.create_next_occurrence()
        assert next_task is not None
        assert next_task.due_date == date.today() + timedelta(weeks=1)

    def test_non_recurring_task(self):
        """Verify that one-time tasks don't create next occurrence."""
        task = Task(
            description="Grooming appointment",
            time="14:00",
            duration_minutes=90,
            priority="medium",
            frequency="once"
        )

        next_task = task.create_next_occurrence()
        assert next_task is None


class TestPet:
    """Test suite for Pet class."""

    def test_add_task_to_pet(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        pet = Pet(name="Mochi", species="dog", age=3)
        assert pet.get_task_count() == 0

        task = Task(
            description="Morning walk",
            time="08:00",
            duration_minutes=30,
            priority="high"
        )
        pet.add_task(task)

        assert pet.get_task_count() == 1
        assert task.pet_name == "Mochi"

    def test_get_pending_tasks(self):
        """Verify that get_pending_tasks only returns incomplete tasks."""
        pet = Pet(name="Whiskers", species="cat", age=5)

        task1 = Task(description="Breakfast", time="08:00", duration_minutes=5, priority="high")
        task2 = Task(description="Play session", time="10:00", duration_minutes=15, priority="medium")
        task3 = Task(description="Dinner", time="18:00", duration_minutes=5, priority="high")

        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        # Mark one task complete
        task1.mark_complete()

        pending = pet.get_pending_tasks()
        assert len(pending) == 2
        assert task1 not in pending
        assert task2 in pending
        assert task3 in pending


class TestOwner:
    """Test suite for Owner class."""

    def test_add_pet(self):
        """Verify that pets can be added to an owner."""
        owner = Owner("Jordan")
        assert len(owner.pets) == 0

        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)

        assert len(owner.pets) == 1
        assert owner.pets[0].name == "Mochi"

    def test_get_all_tasks(self):
        """Verify that get_all_tasks aggregates tasks from all pets."""
        owner = Owner("Jordan")

        pet1 = Pet(name="Mochi", species="dog", age=3)
        pet2 = Pet(name="Whiskers", species="cat", age=5)

        pet1.add_task(Task(description="Walk", time="08:00", duration_minutes=30, priority="high"))
        pet1.add_task(Task(description="Breakfast", time="08:30", duration_minutes=10, priority="high"))
        pet2.add_task(Task(description="Breakfast", time="09:00", duration_minutes=5, priority="high"))

        owner.add_pet(pet1)
        owner.add_pet(pet2)

        all_tasks = owner.get_all_tasks()
        assert len(all_tasks) == 3

    def test_get_pet_by_name(self):
        """Verify that pets can be retrieved by name."""
        owner = Owner("Jordan")
        pet1 = Pet(name="Mochi", species="dog", age=3)
        pet2 = Pet(name="Whiskers", species="cat", age=5)

        owner.add_pet(pet1)
        owner.add_pet(pet2)

        found_pet = owner.get_pet_by_name("Whiskers")
        assert found_pet is not None
        assert found_pet.name == "Whiskers"

        not_found = owner.get_pet_by_name("Fluffy")
        assert not_found is None


class TestScheduler:
    """Test suite for Scheduler class."""

    def test_sorting_by_time(self):
        """Verify tasks are returned in chronological order."""
        owner = Owner("Jordan")
        pet = Pet(name="Mochi", species="dog", age=3)

        # Add tasks out of order
        pet.add_task(Task(description="Evening walk", time="18:00", duration_minutes=30, priority="high"))
        pet.add_task(Task(description="Morning walk", time="07:00", duration_minutes=30, priority="high"))
        pet.add_task(Task(description="Lunch", time="12:00", duration_minutes=10, priority="medium"))

        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        sorted_tasks = scheduler.sort_by_time(pet.get_tasks())

        assert len(sorted_tasks) == 3
        assert sorted_tasks[0].time == "07:00"
        assert sorted_tasks[1].time == "12:00"
        assert sorted_tasks[2].time == "18:00"

    def test_filter_by_status(self):
        """Verify that tasks can be filtered by completion status."""
        owner = Owner("Jordan")
        pet = Pet(name="Mochi", species="dog", age=3)

        task1 = Task(description="Walk", time="08:00", duration_minutes=30, priority="high")
        task2 = Task(description="Breakfast", time="09:00", duration_minutes=10, priority="high")
        task3 = Task(description="Play", time="10:00", duration_minutes=15, priority="medium")

        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        task1.mark_complete()

        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        completed = scheduler.filter_by_status(pet.get_tasks(), completed=True)
        pending = scheduler.filter_by_status(pet.get_tasks(), completed=False)

        assert len(completed) == 1
        assert len(pending) == 2
        assert task1 in completed
        assert task2 in pending
        assert task3 in pending

    def test_filter_by_pet(self):
        """Verify that tasks can be filtered by pet name."""
        owner = Owner("Jordan")

        mochi = Pet(name="Mochi", species="dog", age=3)
        whiskers = Pet(name="Whiskers", species="cat", age=5)

        mochi.add_task(Task(description="Walk", time="08:00", duration_minutes=30, priority="high"))
        whiskers.add_task(Task(description="Breakfast", time="08:00", duration_minutes=5, priority="high"))

        owner.add_pet(mochi)
        owner.add_pet(whiskers)

        scheduler = Scheduler(owner)
        all_tasks = owner.get_all_tasks()

        mochi_tasks = scheduler.filter_by_pet(all_tasks, "Mochi")
        whiskers_tasks = scheduler.filter_by_pet(all_tasks, "Whiskers")

        assert len(mochi_tasks) == 1
        assert len(whiskers_tasks) == 1
        assert mochi_tasks[0].description == "Walk"
        assert whiskers_tasks[0].description == "Breakfast"

    def test_conflict_detection(self):
        """Verify that the Scheduler correctly identifies duplicate times for the same pet."""
        owner = Owner("Jordan")
        pet = Pet(name="Mochi", species="dog", age=3)

        # Create two tasks at the same time for the same pet
        pet.add_task(Task(description="Walk", time="08:00", duration_minutes=30, priority="high"))
        pet.add_task(Task(description="Vet appointment", time="08:00", duration_minutes=60, priority="high"))

        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        conflicts = scheduler.detect_conflicts(pet.get_tasks())

        assert len(conflicts) == 1
        assert "Mochi" in conflicts[0]
        assert "08:00" in conflicts[0]

    def test_no_conflict_different_pets(self):
        """Verify that same time for different pets is not a conflict."""
        owner = Owner("Jordan")

        mochi = Pet(name="Mochi", species="dog", age=3)
        whiskers = Pet(name="Whiskers", species="cat", age=5)

        mochi.add_task(Task(description="Breakfast", time="08:00", duration_minutes=10, priority="high"))
        whiskers.add_task(Task(description="Breakfast", time="08:00", duration_minutes=5, priority="high"))

        owner.add_pet(mochi)
        owner.add_pet(whiskers)

        scheduler = Scheduler(owner)
        all_tasks = owner.get_all_tasks()

        conflicts = scheduler.detect_conflicts(all_tasks)

        assert len(conflicts) == 0

    def test_mark_task_complete_with_recurrence(self):
        """Verify that marking a recurring task complete creates next occurrence."""
        owner = Owner("Jordan")
        pet = Pet(name="Mochi", species="dog", age=3)

        task = Task(
            description="Morning walk",
            time="08:00",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            due_date=date.today()
        )
        pet.add_task(task)
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        initial_count = pet.get_task_count()

        scheduler.mark_task_complete(task)

        assert task.is_completed is True
        assert pet.get_task_count() == initial_count + 1  # New task created

        # Verify new task exists for tomorrow
        all_tasks = pet.get_tasks()
        tomorrow_tasks = [t for t in all_tasks if t.due_date == date.today() + timedelta(days=1)]
        assert len(tomorrow_tasks) == 1
        assert tomorrow_tasks[0].description == "Morning walk"
