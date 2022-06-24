class Employee:
    """Сотрудник."""

    def __init__(self, salary):
        super().__init__()
        self.salary = salary


class Organization:
    """Организация."""

    @property
    def can_analyze_count(self):
        """Количество сотрудников, которые могут анализировать задачи."""
        return self._count_employees_by_type(Analyst)

    @property
    def can_develop_count(self):
        """Количество сотрудников, которые могут разрабатывать задачи."""
        return self._count_employees_by_type(Developer)

    @property
    def can_test_count(self):
        """Количество сотрудников, которые могут тестировать задачи."""
        return self._count_employees_by_type(Tester)

    def __init__(self):
        self._employee = []

    def accept_employee(self, employee):
        """Принимает сотрудника на работу."""
        if not isinstance(employee, Employee):
            raise TypeError
        self._employee.append(employee)

        return self

    def accept_employees(self, *employees):
        """Принимает сотрудников на работу."""
        for employee in employees:
            self.accept_employee(employee)

    def _count_employees_by_type(self, employee_type) -> int:
        """Подсчет сотрудников по типу выполняемой работы."""
        count = 0
        for employee in self._employee:
            if isinstance(employee, employee_type):
                count += 1
        return count

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
    pass


class Developer(Employee):
    pass


class Tester(Employee):
    pass


class CEO(Analyst, Developer, Tester):
    pass


class TeamLead(Developer, Tester):
    pass


class ProductOwner(Analyst, Tester):
    pass


class Freelancer(Employee):

    def __new__(cls, employee):
        obj = super().__new__(employee.__class__)
        obj.salary = 0
        obj.freelancer_salary = employee.salary
        return obj


