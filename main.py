# Змінні
from csp import CSP
# Обмеження
constraints = [
    # Викладач не може проводити більше однієї лекції одночасно
    {
        "vars": ("lecturer", "time"),
        "predicate": lambda events, l, t: sum(
            e.get("lecturer") == l and e.get("time") == t for e in events
        ) <= 1,
    },
    # Група не може бути присутньою на кількох лекціях одночасно
    {
        "vars": ("group", "time"),
        "predicate": lambda events, g, t: sum(
            e.get("group") == g and e.get("time") == t for e in events
        ) <= 1,
    },
    # Одна аудиторія не може використовуватись для кількох лекцій одночасно
    {
        "vars": ("classroom", "time"),
        "predicate": lambda events, r, t: sum(
            e.get("classroom") == r and e.get("time") == t for e in events
        ) <= 1,
    },
    # Викладач має бути закріплений за певною групою
    {
        "vars": ("lecturer", "group"),
        "predicate": lambda events, l, g: (l, g) in [
            ("Ivanov", "Group A"),
            ("Petrov", "Group B"),
            ("Sidorov", "Group C"),
        ],
    },
    # Часові обмеження для викладачів
    {
        "vars": ("lecturer", "time"),
        "predicate": lambda events, l, t: (l, t) in [
            ("Ivanov", "Monday 9:00"),
            ("Ivanov", "Monday 11:00"),
            ("Ivanov", "Tuesday 9:00"),
            ("Ivanov", "Tuesday 11:00"),
            ("Petrov", "Monday 9:00"),
            ("Petrov", "Tuesday 9:00"),
            ("Petrov", "Tuesday 11:00"),
            ("Sidorov", "Monday 9:00"),
            ("Sidorov", "Monday 11:00"),
            ("Sidorov", "Tuesday 9:00"),
        ],
    },
    # Викладач має щонайменше одну лекцію на день
    {
        "vars": ("lecturer",),
        "predicate": lambda events, l: any(
            any(e.get("lecturer") == l and e.get("time").startswith(day) for e in events)
            for day in ["Monday", "Tuesday"]
        ),
    },
]




# Змінні
variables = ["lecturer", "classroom", "group", "time"]

# Області визначення
domains = {
    "lecturer": ["Ivanov", "Petrov", "Sidorov"],
    "time": ["Monday 9:00", "Monday 11:00", "Tuesday 9:00", "Tuesday 11:00"],
    "classroom": ["Room 101", "Room 102", "Room 103"],
    "group": ["Group A", "Group B", "Group C"],
}

# Ініціалізація CSP
csp = CSP(variables, domains, constraints)

# Генерація розкладу
solution = csp.backtracking_search()

if solution:
    print("Розклад знайдено:")
    for assignment in solution:
        print(assignment)

    # Оцінка якості розкладу
    fitness_score = csp.fitness()
    print(f"Оцінка якості розкладу: {fitness_score}")
else:
    print("Розклад не знайдено.")

