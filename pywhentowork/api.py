"""
Handles the API calls to the WhenToWork API
"""

import requests, datetime, pprint

from pywhentowork.classes import *

VALID_ENDPOINTS = [
    "EmployeeList",
    "AssignedShiftList",
    "ApprovedTimeOff",
    "DailyTotals",
    "DailyPositionTotals",
    "PositionList",
    "CategoryList",
]


class WhenToWork:
    def __init__(
        self,
        key: str,
        base_url: str = "https://www3.whentowork.com/cgi-bin/w2wCC.dll/api/",
    ) -> None:
        self._key = key
        self._base_url = base_url

        self.positions = self.get_position_list()

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, key: str) -> None:
        if not key:
            raise ValueError("API key cannot be empty.")

        self._key = key

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, base_url: str) -> None:
        if not base_url:
            raise ValueError("Base URL cannot be empty.")

        self._base_url = base_url

    def _post_to_endpoint(self, endpoint: str, params: dict) -> dict:
        if endpoint not in VALID_ENDPOINTS:
            raise ValueError(f"Invalid endpoint: {endpoint}")

        # Add the API key to the parameters
        params["key"] = self.key

        response = requests.post(f"{self.base_url}{endpoint}", data=params)

        if response.status_code != 200:
            raise ValueError(f"Error accessing endpoint {endpoint}: {response.text}")

        return response.json()

    def get_employee_list(self) -> list:
        """
        Get a list of all employees in the account.
        """
        response = self._post_to_endpoint("EmployeeList", {})

        return [Employee.from_json(employee) for employee in response["EmployeeList"]]

    def get_position_list(self) -> list:
        """
        Get a list of all positions in the account.
        """
        response = self._post_to_endpoint("PositionList", {})

        # Update self.positions with the new list of positions
        self.positions = [
            Position.from_json(position) for position in response["PositionList"]
        ]

        return self.positions

    def get_category_list(self) -> list:
        """
        Get a list of all categories in the account.
        """
        response = self._post_to_endpoint("CategoryList", {})

        return [Category.from_json(category) for category in response["CategoryList"]]

    def get_assigned_shift_list(
        self,
        start_date: datetime.date | str = datetime.datetime.now().date(),
        end_date: datetime.date | str = datetime.datetime.now().date(),
        position: Position | str = "",
    ) -> list:
        """
        Get a list of all assigned shifts for an employee.

        Args:
            start_date (datetime.date or str): Start date for the query.
                - Defaults to the current date.
                - If a string is provided, it should be in the format "YYYY-MM-DD".
            end_date (datetime.date or str): End date for the query.
                - Defaults to the current date.
                - If a string is provided, it should be in the format "YYYY-MM-DD".
            position (Position or str): Position for which to get the shifts.
                - Defaults to an empty string (all positions).
                - If a string is provided, it should be the position_id.
        """

        # Convert the dates to datetime.date objects if they are strings
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        # If the start date is after the end date, ignore the end date
        if start_date > end_date:
            end_date = start_date

        # W2W accepts a max of 31 days, so constrain end_date to 31 days after start_date if necessary
        if (end_date - start_date).days > 31:
            # TODO: Log a warning that the end date was adjusted
            end_date = start_date + datetime.timedelta(days=31)

        # Convert the dates to the format expected by the API (mm/dd/yyyy)
        _start_date_string = start_date.strftime("%m/%d/%Y")
        _end_date_string = end_date.strftime("%m/%d/%Y")

        # Extract the position_id from the Position object if provided
        position_id = position.id if isinstance(position, Position) else position

        response = self._post_to_endpoint(
            "AssignedShiftList",
            {
                "start_date": _start_date_string,
                "end_date": _end_date_string,
                "position": position_id,
            },
        )

        return [Shift.from_json(shift) for shift in response["AssignedShiftList"]]

    def pprint_object_list(self, obj_list: list) -> None:
        """
        Pretty print a list of objects.
        """
        for obj in obj_list:
            # Get the object as a dict
            obj_dict = obj.__dict__

            # Pretty print the object
            pprint.pprint(obj_dict)
