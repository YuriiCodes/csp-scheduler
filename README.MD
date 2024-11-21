
# 🗓️ CSP Scheduler

A Python implementation of a **Constraint Satisfaction Problem (CSP)** to generate optimal schedules for lecturers, classrooms, and student groups while adhering to various constraints. This project demonstrates the use of backtracking search, advanced heuristics, and a fitness function for effective schedule generation.

---

## 🚀 Features

- **Flexible Constraint Definitions**: Easily customizable constraints to fit various scheduling requirements.
- **Heuristics for Optimization**:
  - Degree heuristic for variable selection.
  - Least constraining value heuristic for domain values.
- **Fitness Evaluation**: Includes penalties for violations and bonuses for even distribution.
- **Dynamic CSP Handling**: Supports the addition of new variables, domains, and constraints without extensive code changes.
- **Readable Output**: Prints schedules in a clear format for easy analysis.

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.x
- Basic understanding of CSP concepts

### Installation
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/your-username/csp-scheduler.git
cd csp-scheduler
```

---

## 🧑‍💻 Usage

Run the script to generate an optimized schedule:
```bash
python scheduler.py
```

### Example Output
```plaintext
Schedule found:
{'group': 'Group A', 'time': 'Monday 9:00', 'lecturer': 'Ivanov', 'classroom': 'Room 101'}
{'group': 'Group B', 'time': 'Monday 9:00', 'lecturer': 'Petrov', 'classroom': 'Room 102'}
{'group': 'Group C', 'time': 'Monday 11:00', 'lecturer': 'Sidorov', 'classroom': 'Room 103'}
Fitness score: 15
```

---

## 🧩 CSP Explained

A **Constraint Satisfaction Problem (CSP)** consists of:
- **Variables**: Items to assign (e.g., `lecturer`, `classroom`, `group`, `time`).
- **Domains**: Possible values for variables.
- **Constraints**: Rules restricting variable assignments.

This project uses:
- **Backtracking Search**: Depth-first search to explore possible assignments.
- **Heuristics**:
  - *Degree Heuristic*: Prioritizes variables with the most constraints.
  - *Least Constraining Value*: Prefers values that minimize conflicts.
- **Fitness Function**: Quantifies the quality of a schedule.

---

## ⚙️ Configuration

### Customize Domains
Modify the `domains` dictionary in `scheduler.py`:
```python
domains = {
    "lecturer": ["Ivanov", "Petrov", "Sidorov"],
    "time": ["Monday 9:00", "Monday 11:00", "Tuesday 9:00", "Tuesday 11:00"],
    "classroom": ["Room 101", "Room 102", "Room 103"],
    "group": ["Group A", "Group B", "Group C"],
}
```

### Add Constraints
Add or modify constraints in the `constraints` list:
```python
constraints = [
    {
        "vars": ("lecturer", "time"),
        "predicate": lambda events, l, t: sum(
            e.get("lecturer") == l and e.get("time") == t for e in events
        ) <= 1,
    },
    # More constraints...
]
```

---

## 📖 Learning Goals

This project helps you:
1. Understand **CSP concepts** and their real-world applications.
2. Explore **backtracking algorithms** with heuristics.
3. Develop skills in constraint modeling and optimization.
