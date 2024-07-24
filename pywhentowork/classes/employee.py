from ._w2w_base import W2WBaseClass, load_fields

FIELDS = load_fields("employee")


class Employee(W2WBaseClass):
    """
    Representation of an employee in W2W.

    Attributes:
        company_id (str): Unique ID for the company.
        w2w_employee_id (str): ID for an employee (Unique over employees in W2W system).
        employee_number (str): ID for employee (Unique over employees in the company).
        first_name (str): First name of employee.
        last_name (str): Last name of Employee.
        phone (str): Primary Phone number of employee.
        phone_2 (str): Secondary Phone number of employee.
        mobile_phone (str): Mobile phone number of employee.
        emails (str): Email of employee.
        last_sign_in (datetime): Datetime of last sign to W2W in for employee.
        sign_in_count (int): Number of times employee has signed in to W2W.
        address (str): Street address of employee.
        address_2 (str): Unit/Apt number of employee.
        city (str): City of employee's address.
        state (str): State of employee's address.
        zip (str): Zip Code of Employee's address.
        comments (str): Comments managers have given to employee.
        max_hrs_day (float): Maximum allowed hours assigned per day for employee.
        max_shifts_day (int): Maximum allowed shifts assigned per day for employee.
        max_hrs_week (float): Maximum allowed hours assigned per week for employee.
        max_days_week (int): Maximum allowed days assigned per week for employee.
        hire_date (datetime): Date employee was hired.
        status (str): Employment status.
        priority_group (str): Priority group of the employee.
        custom_1 (str): Custom field 1 for the employee.
        custom_2 (str): Custom field 2 for the employee.
        biweekly_target_hrs (float): Target hours to be assigned to employee every 2 weeks.
        pay_rate (float): Hourly Pay rate for employee.
        alert_date (datetime): Date for next alert.
        next_alert (datetime): Next alert date.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(FIELDS, **kwargs)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Employee):
            return False
        return self.w2w_employee_id == other.w2w_employee_id

    def __hash__(self) -> int:
        return hash(self.w2w_employee_id)
