"""
Handles the API calls to the WhenToWork API
"""

import requests, datetime, pprint, regex

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

    def _sort_objects(self, obj_list: list, sort_field: str, sort_order: str) -> list:
        """
        Sort a list of objects by a field.
        """
        try:
            obj_list.sort(
                key=lambda x: getattr(x, sort_field), reverse=sort_order == "desc"
            )
        except AttributeError:
            # If the sort field is not found, raise an error
            raise ValueError(f"Invalid sort field: {sort_field}")

        return obj_list

    def get_employee_list(
        self, sort_field: str = "last_name", sort_order: str = "asc"
    ) -> list:
        """
        Get a list of all employees in the account.
        """
        response: list = self._post_to_endpoint("EmployeeList", {})["EmployeeList"]

        # Generate a list of Employee objects from the response
        employees: list[Employee] = [
            Employee.from_json(employee) for employee in response
        ]

        # Sort the list of employees
        self._sort_objects(employees, sort_field, sort_order)

        return employees

    def get_position_list(
        self,
        sort_field: str = "position_name",
        sort_order: str = "asc",
    ) -> list:
        """
        Get a list of all positions in the account.
        """
        response: list = self._post_to_endpoint("PositionList", {})["PositionList"]

        # Generate a list of Position objects from the response
        positions: list[Position] = [
            Position.from_json(position) for position in response
        ]

        # Sort the list of positions
        positions = self._sort_objects(positions, sort_field, sort_order)

        # Update self.positions with the new list of positions
        self.positions = positions

        return self.positions

    def get_category_list(
        self, sort_field: str = "category_name", sort_order: str = "asc"
    ) -> list:
        """
        Get a list of all categories in the account.
        """
        response = self._post_to_endpoint("CategoryList", {})["CategoryList"]

        # Generate a list of Category objects from the response
        categories: list[Category] = [
            Category.from_json(category) for category in response
        ]

        # Sort the list of categories
        categories = self._sort_objects(categories, sort_field, sort_order)

        return categories

    def get_assigned_shift_list(
        self,
        start_date: datetime.date | str = datetime.datetime.now().date(),
        end_date: datetime.date | str = datetime.datetime.now().date(),
        position: Position | str = "",
    ) -> list:
        """
        Get a list of all assigned shifts for a date or range of dates. Optionally filtered by position.

        :param start_date: (datetime.date or str) Start date for the query.
            - Defaults to the current date.
            - If a string is provided, it should be in the format "YYYY-MM-DD".
        :param end_date: (datetime.date or str) End date for the query.
            - Defaults to the current date.
            - If a string is provided, it should be in the format "YYYY-MM-DD".
        :param position: (Position or str) Position for which to get the shifts.
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
        )["AssignedShiftList"]

        # Generate a list of Shift objects from the response
        assigned_shifts: list[Shift] = [Shift.from_json(shift) for shift in response]

        return assigned_shifts

    def search_objects(
        self,
        obj_list: list,
        search_field: str | list[str],
        search_value: str | list[str],
    ) -> list:
        """
        Search a list of objects for a specific value in a specific field.

        :param obj_list: (list) List of objects to search.
        :param search_field: (str or list) Field(s) to search for the value(s).
        :param search_value: (str or list) Value(s) to search for in the field(s).
        """

        _search_fields = (
            search_field if isinstance(search_field, list) else [search_field]
        )
        _search_values = (
            search_value if isinstance(search_value, list) else [search_value]
        )

        # Simple regex pattern for each value
        _patterns = [
            regex.compile(
                f"{value}",
                regex.IGNORECASE,
            )
            for value in _search_values
        ]

        # For each field, try each pattern
        search_results = [
            obj
            for obj in obj_list
            if any(
                pattern.match(getattr(obj, field))
                for pattern in _patterns
                for field in _search_fields
            )
        ]

        return search_results

    def pprint_object_list(self, obj_list: list) -> None:
        """
        Pretty print a list of objects.
        """
        for obj in obj_list:
            # Get the object as a dict
            obj_dict = obj.__dict__

            # Pretty print the object
            pprint.pprint(obj_dict)
