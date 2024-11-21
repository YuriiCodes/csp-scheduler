class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables  # Список змінних
        self.domains = domains  # Області визначення для кожної змінної
        self.constraints = constraints  # Список обмежень
        self.assignments = []  # Поточний стан присвоєння значень (як список подій)

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

    def select_unassigned_variable(self):
        """
        Евристика для вибору наступної змінної (MRV).
        """
        unassigned_vars = [v for v in self.variables if v not in {k for a in self.assignments for k in a}]
        return min(unassigned_vars, key=lambda var: len(self.domains[var]))

    def backtracking_search(self):
        """
        Пошук з поверненням.
        """
        # Якщо всі змінні мають значення, повертаємо присвоєння
        if len(self.assignments) == len(self.variables):
            return self.assignments

        # Вибираємо змінну для присвоєння
        var = self.select_unassigned_variable()
        # Перебираємо можливі значення змінної
        for value in self.domains[var]:
            new_assignment = {var: value}
            if self.is_consistent(new_assignment):
                # Якщо присвоєння не викликає конфлікту, додаємо його
                self.assignments.append(new_assignment)
                # Рекурсивно викликаємо пошук
                result = self.backtracking_search()
                if result:
                    return result
                # Якщо результату немає, видаляємо присвоєння
                self.assignments.pop()

        # Якщо жодне значення не підходить, повертаємо None
        return None
