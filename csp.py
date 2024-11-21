def select_unassigned_variable(assignments, variables, constraints, domains):
    """
    Вибирає змінну за допомогою degree heuristic (змінна з найбільшою кількістю обмежень).
    """
    unassigned_vars = [v for v in variables if v not in {k for a in assignments for k in a}]
    # Підрахунок кількості обмежень для кожної змінної
    def degree(var):
        return sum(1 for constraint in constraints if var in constraint["vars"])
    # Вибираємо змінну з найбільшим ступенем
    return max(unassigned_vars, key=degree)

def order_domain_values(var, domains, assignments, constraints):
    """
    Впорядковує значення для змінної за принципом least constraining value.
    """
    def count_conflicts(value):
        # Підрахунок кількості конфліктів для цього значення
        test_assignment = {var: value}
        return sum(
            not constraint["predicate"](assignments + [test_assignment], *[
                test_assignment.get(v) for v in constraint["vars"]
            ])
            for constraint in constraints if var in constraint["vars"]
        )
    # Сортуємо значення за кількістю конфліктів
    return sorted(domains[var], key=count_conflicts)


class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables  # Список змінних
        self.domains = domains  # Області визначення для кожної змінної
        self.constraints = constraints  # Список обмежень
        self.assignments = []  # Поточний розклад (список подій)

    def is_consistent(self, new_assignment):
        """
        Перевіряє, чи нова подія відповідає всім обмеженням.
        """
        for constraint in self.constraints:
            vars_in_constraint = constraint["vars"]
            relevant_assignments = [
                a for a in self.assignments + [new_assignment] if all(var in a for var in vars_in_constraint)
            ]
            for assignment in relevant_assignments:
                values = [assignment[var] for var in vars_in_constraint]
                if not constraint["predicate"](self.assignments + [new_assignment], *values):
                    return False
        return True

    def backtracking_search(self):
        """
        Генерує повний розклад.
        """
        # Якщо всі змінні заповнені, повертаємо розклад
        if len(self.assignments) == len(self.domains["time"]) * len(self.domains["group"]):
            return self.assignments

        # Вибираємо змінну для присвоєння
        for group in self.domains["group"]:
            for time in self.domains["time"]:
                for lecturer in self.domains["lecturer"]:
                    for classroom in self.domains["classroom"]:
                        new_assignment = {
                            "group": group,
                            "time": time,
                            "lecturer": lecturer,
                            "classroom": classroom,
                        }
                        if self.is_consistent(new_assignment):
                            # Додаємо подію до розкладу
                            self.assignments.append(new_assignment)

        return self.assignments

    def fitness(self):
        """
        Оцінює якість розкладу:
        - Штраф за конфлікти.
        - Бонус за рівномірний розподіл.
        """
        penalty = 0
        bonus = 0

        # Перевірка кожного обмеження
        for constraint in self.constraints:
            vars_in_constraint = constraint["vars"]
            for assignment in self.assignments:
                if all(var in assignment for var in vars_in_constraint):
                    values = [assignment[var] for var in vars_in_constraint]
                    if not constraint["predicate"](self.assignments, *values):
                        penalty += 1  # Штраф за конфлікт

        # Бонус за рівномірний розподіл часу між групами
        group_slots = {group: [] for group in self.domains["group"]}
        for event in self.assignments:
            group_slots[event["group"]].append(event["time"])

        # Рівномірність: чим більше унікальних слотів, тим краще
        for slots in group_slots.values():
            bonus += len(set(slots))

        return bonus - penalty
