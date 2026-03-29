# PawPal+ Smart Pet Care Management System

**PawPal+** is an intelligent Streamlit application that helps pet owners manage and schedule care tasks for their pets with smart sorting, filtering, conflict detection, and automated recurrence.

## Features

### Core Functionality
- **Multi-Pet Management**: Add and manage multiple pets with their individual care schedules
- **Smart Task Scheduling**: Schedule tasks with time, duration, priority, and frequency (once, daily, weekly)
- **Automatic Sorting**: Tasks are automatically sorted chronologically for efficient planning
- **Conflict Detection**: Warns when multiple tasks are scheduled at the same time for the same pet
- **Recurring Tasks**: Daily and weekly tasks automatically create the next occurrence when completed
- **Advanced Filtering**: Filter tasks by pet name and completion status

### Smarter Scheduling

The PawPal+ scheduler implements several algorithmic features:

1. **Time-Based Sorting**: Uses lambda functions to sort tasks by "HH:MM" format for chronological display
2. **Status Filtering**: Efficiently filters tasks to show pending or completed items
3. **Conflict Detection**: Compares task times across the same pet to identify scheduling conflicts
4. **Recurrence Logic**: Automatically generates next task instances using Python's `timedelta` for daily/weekly tasks
5. **Pet-Based Filtering**: Allows users to view tasks for specific pets

## System Architecture

The system is built on a modular OOP design with four core classes:

- **Task**: Represents individual care activities (dataclass)
- **Pet**: Manages a pet and their associated tasks (dataclass)
- **Owner**: Central data store managing multiple pets
- **Scheduler**: The "brain" providing sorting, filtering, and conflict detection

See `uml_diagram.md` for the complete class diagram.

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Streamlit App

```bash
streamlit run app.py
```

### Run the CLI Demo

```bash
python main.py
```

### Testing PawPal+

Run the automated test suite:

```bash
python -m pytest
```

Or with verbose output:

```bash
python -m pytest tests/test_pawpal.py -v
```

**Test Coverage**: 15 comprehensive tests covering:
- Task completion and status changes
- Recurring task generation (daily/weekly)
- Pet task management
- Owner multi-pet coordination
- Chronological sorting
- Status and pet-based filtering
- Conflict detection
- Task completion with automatic recurrence

**Confidence Level**: ⭐⭐⭐⭐⭐ (5/5) - All core functionality is tested with both happy paths and edge cases.

## How to Use

1. **Add Pets**: Use the sidebar to add pets with name, species, and age
2. **Schedule Tasks**: Use the main form to add tasks with:
   - Pet selection
   - Task description
   - Time and duration
   - Priority (low/medium/high)
   - Frequency (once/daily/weekly)
3. **View Schedule**: See today's sorted schedule with conflict warnings
4. **Filter Tasks**: Use dropdowns to filter by pet or status
5. **Complete Tasks**: Click "Complete" buttons to mark tasks done (recurring tasks auto-schedule next occurrence)
6. **Monitor Progress**: Check the statistics dashboard for overview

## Project Structure

```
.
├── pawpal_system.py      # Core logic layer (Task, Pet, Owner, Scheduler)
├── app.py                # Streamlit UI
├── main.py               # CLI demo script
├── tests/
│   └── test_pawpal.py    # Comprehensive test suite
├── uml_diagram.md        # System architecture diagram
├── reflection.md         # Project reflection and learnings
└── README.md             # This file
```

## Development Process

This project was developed using a systematic approach:

1. **Phase 1**: UML design and system architecture
2. **Phase 2**: Core implementation with CLI verification
3. **Phase 3**: UI integration with Streamlit
4. **Phase 4**: Algorithmic enhancements (sorting, filtering, conflicts)
5. **Phase 5**: Comprehensive testing
6. **Phase 6**: Documentation and polish
