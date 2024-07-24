from ._w2w_base import W2WBaseClass, load_fields

FIELDS = load_fields("category")


class Category(W2WBaseClass):
    """
    Represents a Category within the system, holding information about
    various custom attributes and identifiers unique to a company.

    Attributes:
        company_id (int): Unique ID for a company.
        category_id (int): ID for a Category, unique to the company.
        category_name (str): Name of the Category.
        category_short (str): Abbreviated name of the Category.
        category_custom1 (str): Custom field 1 for the Category.
        category_custom2 (str): Custom field 2 for the Category.
        category_custom3 (str): Custom field 3 for the Category.
        last_changed_ts (datetime): Timestamp of the last change.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(FIELDS, **kwargs)

    def __str__(self) -> str:
        return f"{self.category_name} ({self.category_id})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Category):
            return False
        return self.category_id == other.category_id

    def __hash__(self) -> int:
        return hash(self.category_id)
