from ._w2w_base import W2WBaseClass, load_fields

FIELDS = load_fields("shift")


class Shift(W2WBaseClass):
    """
    Represents a shift assigned to an employee.

    Attributes:
        company_id (str): Unique ID for the company.
        shift_id (str): ID for a shift, unique to the company.
        published (str): 'Y' if shift is published, 'N' if not.
        w2w_employee_id (str): ID for an employee, unique over employees in W2W system.
        first_name (str): First name of the employee.
        last_name (str): Last name of the employee.
        employee_number (str): ID for an employee, unique over employees in a company.
        start_date (str): Start date of the shift.
        start_time (str): Start time of the shift.
        end_date (str): End date of the shift.
        end_time (str): End time of the shift.
        duration (float): Duration of the shift in hours.
        description (str): Description of the shift.
        position_id (str): ID for a position, unique to the company.
        position_name (str): Name of the position.
        category_id (str): ID for a category, unique to the company.
        category_name (str): Name of the category.
        category_short (str): Abbreviated name of the category.
        color_id (str): ID for the color of the shift.
        pay_rate (float): Hourly pay rate of the shift.
        position_custom1 (str): Custom field 1 for the position.
        position_custom2 (str): Custom field 2 for the position.
        position_custom3 (str): Custom field 3 for the position.
        category_custom1 (str): Custom field 1 for the category.
        category_custom2 (str): Custom field 2 for the category.
        category_custom3 (str): Custom field 3 for the category.
        last_changed_ts (datetime): Timestamp of the last change.
        last_changed_by (str): Name of the user who last changed the shift.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(FIELDS, **kwargs)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.start_date} {self.start_time} to {self.end_date} {self.end_time}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Shift):
            return False
        return self.shift_id == other.shift_id

    def __hash__(self) -> int:
        return hash(self.shift_id)
