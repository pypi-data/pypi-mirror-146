"""
(Custom) Attributes utilities.
"""
from typing import Callable, Optional, cast, Dict, Any, Union, Sequence, List


def get_custom_attribute(item: dict, attribute_code: str, coerce_as: Optional[Callable] = None):
    """
    Get a custom attribute from an item given its code.

    For example:
        >>> get_custom_attribute(..., "my_custom_attribute")
        "0"

        >>> get_custom_attribute(..., "my_custom_attribute", bool)
        False

    :param item:
    :param attribute_code:
    :param coerce_as: optional callable that is called on the attribute value if it's set.
      This is useful to circumvent Magento's limitation where all attribute values are strings.
    :return: attribute value or None.
    """
    for attribute in item.get("custom_attributes", []):
        if attribute["attribute_code"] == attribute_code:
            value = attribute["value"]
            if coerce_as:
                if coerce_as == bool:
                    # "0" -> False / "1" -> True
                    return bool(int(value))
                return coerce_as(value)
            return value


def get_boolean_custom_attribute(item: dict, attribute_code: str) -> Optional[bool]:
    """
    Equivalent of ``get_custom_attribute(item, attribute_code, coerce_as=bool)`` with proper typing.
    """
    return cast(Optional[bool], get_custom_attribute(item, attribute_code, coerce_as=bool))


def get_custom_attributes_dict(item: Dict[str, Any]) -> Dict[str, Union[Sequence[str], str]]:
    """
    Get all custom attributes from an item as a dict of code->value.
    :param item:
    :return: dict
    """
    d = {}
    for attribute in item.get("custom_attributes", []):
        d[attribute["attribute_code"]] = attribute["value"]

    return d


def pretty_custom_attributes(custom_attributes: List[Dict[str, Any]]):
    """
    Return a human-friendly compact representation of a sequence of custom attributes.

    :param custom_attributes:
    :return:
    """
    pairs = []
    for custom_attribute in custom_attributes:
        k = custom_attribute["attribute_code"]
        v = custom_attribute["value"]
        pairs.append(f"{k}={repr(v)}")

    return ", ".join(pairs)


def set_custom_attribute(item: dict, attribute_code: str, attribute_value: Union[str, int, float, bool, None]):
    """
    Set a custom attribute in an item dict.

    For example:
        >>> set_custom_attribute({}, "my_custom_attribute", 42)
        >>> set_custom_attribute({}, "my_custom_attribute", False)

    :param item: item dict. It’s modified in-place.
    :param attribute_code:
    :param attribute_value:
    :return: the modified item dict.
    """
    if isinstance(attribute_value, bool):
        serialized_value = "1" if attribute_value else "0"
    elif attribute_value is None:
        serialized_value = ""
    else:
        serialized_value = str(attribute_value)

    item.setdefault("custom_attributes", [])

    for attribute in item["custom_attributes"]:
        if attribute["attribute_code"] == attribute_code:
            attribute["value"] = serialized_value
            return item

    item["custom_attributes"].append({
        "attribute_code": attribute_code,
        "value": serialized_value,
    })
    return item
