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
        Перевіряє, чи не порушує нова подія всіх обмежень.
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
        Генерує повний розклад за допомогою пошуку з евристиками.
        """
        # Якщо всі змінні заповнені, повертаємо розклад
        if len(self.assignments) == len(self.domains["time"]) * len(self.domains["group"]):
            return self.assignments

        # Вибираємо змінну за допомогою degree heuristic
        var = select_unassigned_variable(self.assignments, self.variables, self.constraints, self.domains)

        # Вибираємо значення за принципом least constraining value
        for value in order_domain_values(var, self.domains, self.assignments, self.constraints):
            new_assignment = {var: value}
            if self.is_consistent(new_assignment):
                # Додаємо подію до розкладу
                self.assignments.append(new_assignment)
                result = self.backtracking_search()
                if result:
                    return result
                # Якщо конфлікт, видаляємо подію
                self.assignments.pop()

        return None
