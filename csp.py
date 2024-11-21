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
        Пошук з поверненням для генерації повного розкладу.
        """
        # Якщо всі можливі події створені, повертаємо результат
        if len(self.assignments) == len(self.domains["time"]) * len(self.domains["group"]):
            return self.assignments

        # Генеруємо всі можливі комбінації подій
        for lecturer in self.domains["lecturer"]:
            for classroom in self.domains["classroom"]:
                for group in self.domains["group"]:
                    for time in self.domains["time"]:
                        new_assignment = {
                            "lecturer": lecturer,
                            "classroom": classroom,
                            "group": group,
                            "time": time,
                        }
                        if self.is_consistent(new_assignment):
                            # Якщо присвоєння не викликає конфлікт, додаємо його
                            self.assignments.append(new_assignment)
                            # Рекурсивно викликаємо пошук
                            result = self.backtracking_search()
                            if result:
                                return result
                            # Якщо результату немає, видаляємо присвоєння
                            self.assignments.pop()

        # Якщо жодне значення не підходить, повертаємо None
        return None
