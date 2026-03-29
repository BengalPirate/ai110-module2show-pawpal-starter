# PawPal+ System Architecture - UML Diagram

```mermaid
classDiagram
    class Task {
        +str description
        +str time
        +int duration_minutes
        +str priority
        +str frequency
        +bool is_completed
        +str pet_name
        +date due_date
        +mark_complete()
        +create_next_occurrence() Task
    }

    class Pet {
        +str name
        +str species
        +int age
        +list~Task~ tasks
        +add_task(task)
        +get_tasks() list~Task~
        +get_pending_tasks() list~Task~
        +get_task_count() int
    }

    class Owner {
        +str name
        +list~Pet~ pets
        +add_pet(pet)
        +remove_pet(pet_name)
        +get_all_tasks() list~Task~
        +get_pet_by_name(name) Pet
    }

    class Scheduler {
        +Owner owner
        +get_todays_schedule() list~Task~
        +sort_by_time(tasks) list~Task~
        +filter_by_status(tasks, status) list~Task~
        +filter_by_pet(tasks, pet_name) list~Task~
        +detect_conflicts(tasks) list~str~
        +mark_task_complete(task)
    }

    Owner "1" --> "*" Pet : has
    Pet "1" --> "*" Task : has
    Scheduler "1" --> "1" Owner : manages
```

## Class Responsibilities:

**Task**: Represents a single pet care activity
- Stores all details about the task (what, when, how long, priority)
- Can mark itself complete and generate recurring instances

**Pet**: Represents a pet with their care tasks
- Holds pet information and their task list
- Provides access to tasks and task counts

**Owner**: Represents the pet owner managing multiple pets
- Contains all pets and provides aggregate access to tasks
- Central data store for the system

**Scheduler**: The "brain" that organizes and manages tasks
- Sorts, filters, and detects conflicts in the schedule
- Provides the main scheduling intelligence
