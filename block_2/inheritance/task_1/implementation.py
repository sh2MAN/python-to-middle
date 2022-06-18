class Employee:
    """Сотрудник."""

    def __init__(self, salary):
        super().__init__()
        self.salary = salary

    @property
    def is_analyze(self):
        return False

    @property
    def is_develop(self):
        return False

    @property
    def is_test(self):
        return False


class Organization:
    """Организация."""

    @property
    def can_analyze_count(self):
        """Количество сотрудников, которые могут анализировать задачи."""
        return len([emp for emp in self._employee if emp.is_analyze])

    @property
    def can_develop_count(self):
        """Количество сотрудников, которые могут разрабатывать задачи."""
        return len([emp for emp in self._employee if emp.is_develop])

    @property
    def can_test_count(self):
        """Количество сотрудников, которые могут тестировать задачи."""
        return len([emp for emp in self._employee if emp.is_test])

    def __init__(self):
        self._employee = []

    def accept_employee(self, employee):
        """Принимает сотрудника на работу."""
        if not isinstance(employee, Employee):
            raise TypeError

        self._employee.append(employee)
        return self

    def accept_employees(self, *employees):
        for employee in employees:
            self.accept_employee(employee)

    def calculate_salary(self):
        """Начисляет заработную плату сотрудникам.

        Returns:
            Возвращает общую сумму всех начислений
        """
        salary = 0
        for employee in self._employee:
            salary += employee.salary
        return salary


class Analyst(Employee):

    def __init__(self, salary):
        super().__init__(salary)

    @property
    def is_analyze(self):
        return True


class Developer(Employee):

    def __init__(self, salary):
        super().__init__(salary)

    @property
    def is_develop(self):
        return True


class Tester(Employee):

    def __init__(self, salary):
        super().__init__(salary)

    @property
    def is_test(self):
        return True


class CEO(Analyst, Developer, Tester):

    def __init__(self, salary):
        super().__init__(salary)


class TeamLead(Developer, Tester):

    def __init__(self, salary):
        super().__init__(salary)


class ProductOwner(Analyst, Tester):

    def __init__(self, salary):
        super().__init__(salary)


class Freelancer(Employee):

    def __new__(cls, employee):
        obj = super().__new__(employee.__class__)
        obj.salary = 0
        obj.freelancer_salary = employee.salary
        return obj


