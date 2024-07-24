import json


class W2WBaseClass:
    def __init__(self, fields: list, **kwargs) -> None:
        for field in fields:
            setattr(self, field, None)

        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except AttributeError as e:
                # TODO: Implement logging
                print(f"Error setting attribute {key} to {value}: {e}")

    def __repr__(self) -> str:
        # Generate a string representation of the object including the class name and all attributes
        return f"{self.__class__.__name__}({', '.join([f'{key}={value}' for key, value in self.__dict__.items()])})"

    @classmethod
    def from_json(cls, json_data) -> "W2WBaseClass":
        """
        Create a child object from the JSON data returned by the W2W API.

        Args:
            json_data (dict or str): JSON data returned by the W2W API.

        Returns:
            cls: Child object created from the JSON data.
        """

        if json_data is None:
            return None

        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        # Ensure all the keys are lowercase
        json_data = {key.lower(): value for key, value in json_data.items()}

        return cls(**json_data)


def load_fields(class_name) -> list:
    """
    Load the fields of a class from a JSON file.
    Each JSON file should contain a list of strings representing the fields of the class.
    """
    with open(f"pywhentowork/classes/{class_name}.json", "r") as f:
        fields = json.load(f)

    return fields
