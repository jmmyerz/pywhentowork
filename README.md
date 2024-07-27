# pywhentowork

Retrieves data from WhenToWork's Pro API and make it accessible using Python classes.

Version: 0.1.5 20240727

## Usage

```python
from pywhentowork import WhenToWork

w2w = WhenToWork(<w2w api key>)
```

## Methods

### get_employee_list()

Returns a list of all employees in the account.

### get_position_list()

Returns a list of all positions in the account.

### get_category_list()

Returns a list of all categories in the account.

### get_assigned_shift_list(start_date, end_date, position)

Returns a list of assigned shifts.
Arguments:

- `start_date` (datetime.date or string [YYYY-MM-DD]): The start date of the range to retrieve shifts from. (optional)
- `end_date` (datetime.date or string [YYYY-MM-DD]): The end date of the range to retrieve shifts from. (optional)
- `position` (string): The position id to retrieve shifts for. (optional)
