from ._w2w_base import W2WBaseClass, load_fields

FIELDS = load_fields("position")


class Position(W2WBaseClass):
    """
    Representation of a position for which a shift can be made.

    Attributes:
        company_id (str): Unique ID for the company.
        position_id (str): Unique ID for the position within the company.
        position_name (str): Name of the position.
        position_custom1 (str): Custom field 1 for the position.
        position_custom2 (str): Custom field 2 for the position.
        position_custom3 (str): Custom field 3 for the position.
        last_changed_ts (datetime): Timestamp of the last change to the position.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(FIELDS, **kwargs)

    def __str__(self) -> str:
        return f"{self.position_name} ({self.position_id})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        return self.position_id == other.position_id

    def __hash__(self) -> int:
        return hash(self.position_id)
