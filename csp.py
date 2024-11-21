class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables  # Список змінних
        self.domains = domains  # Області визначення для кожної змінної
        self.constraints = constraints  # Список обмежень
        self.assignments = []  # Поточний стан присвоєння (список подій)

    def is_consistent(self, new_assignment):
        """
        Перевіряє, чи не порушує нове присвоєння значення змінним обмежень.
        """
        for constraint in self.constraints:
            vars_in_constraint = constraint["vars"]
            # Збираємо всі присвоєння, що стосуються змінних у цьому обмеженні
            relevant_assignments = [
                a for a in self.assignments + [new_assignment] if all(var in a for var in vars_in_constraint)
            ]
            # Якщо є достатньо присвоєнь, перевіряємо обмеження
            for assignment in relevant_assignments:
                values = [assignment[var] for var in vars_in_constraint]
                if not constraint["predicate"](self.assignments + [new_assignment], *values):
                    return False
        return True

    def backtracking_search(self):
        """
        Генерує повний розклад.
        """
        # Генеруємо всі можливі комбінації змінних
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
                            # Якщо присвоєння не викликає конфлікту, додаємо його
                            self.assignments.append(new_assignment)

        # Повертаємо всі згенеровані події
        return self.assignments
