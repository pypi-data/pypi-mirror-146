from typing import Literal
import re


def climate_controlled_tagging(description_text: str) -> bool:
    """
        Checks if any of the key terms are in the description text and flags the result accordingly
        :param description_text: String containing description of the storage unit
       :return: Boolean indicating if the storage unit is climate controlled or not
        """

    terms = ['climate', 'air condition', 'air cool', 'humid', 'heat', 'central air', 'dehumidified']
    negation_terms = [f'{a} {b}' for a in ['no', 'not'] for b in terms]

    for neg_term in negation_terms:
        if neg_term in description_text.lower():
            return False

    for term in terms:
        if term in description_text.lower():
            return True

    return False


def calculate_square_footage_from_description(size_text: str) -> float:
    """
    Calculate square footage based on the area
    :param size_text: String containing description of the storage unit
    :return: square footage
    """

    # checks the format (feet by feet, or a x b, etc.)
    if bool(re.match("[0-9]+.?[0-9]? (foot|feet) by [0-9]+.?[0-9]? f+", size_text)) or bool(
            re.match(r"[0-9]+.?[0-9]?'\s*x\s*[0-9]+.?[0-9]?'", size_text)):
        tmp_dimensions = re.findall("[0-9]+.?[0-9]?", size_text)[:2]
        tmp_dimensions = [d.strip() for d in tmp_dimensions]
        tmp_dimensions = [d.replace("'", "") for d in tmp_dimensions]
    elif bool(re.match(r"[0-9]+.?[0-9]?\s*x\s*[0-9]+.?[0-9]?", size_text)):
        tmp_dimensions = re.split(r'x| \s*', size_text.replace(" x ", "x"))[:2]
    else:
        return None

    return float(tmp_dimensions[0]) * float(tmp_dimensions[1])


def size_category_tagging(size_text: str) -> str:
    """
    Categorizes size into small, medium or large based on the area
    :param size_text: String containing description of the storage unit
    :return: size category (small, medium or large)
    """

    # checks the format (feet by feet, or a x b, etc.)
    if bool(re.match("[0-9]+.?[0-9]? (foot|feet) by [0-9]+.?[0-9]? f+", size_text)) or bool(
            re.match(r"[0-9]+.?[0-9]?'\s*x\s*[0-9]+.?[0-9]?'", size_text)):
        tmp_dimensions = re.findall("[0-9]+.?[0-9]?", size_text)[:2]
        tmp_dimensions = [d.strip() for d in tmp_dimensions]
        tmp_dimensions = [d.replace("'", "") for d in tmp_dimensions]
    elif bool(re.match(r"[0-9]+.?[0-9]?\s*x\s*[0-9]+.?[0-9]?", size_text)):
        tmp_dimensions = re.split(r'x| \s*', size_text.replace(" x ", "x"))[:2]
    else:
        return 'Unknown'

    size_sq_ft = float(tmp_dimensions[0]) * float(tmp_dimensions[1])

    if size_sq_ft < 100:
        return "s"
    elif 100 <= size_sq_ft < 200:
        return "m"
    elif 200 <= size_sq_ft < 100000:
        return "l"
    else:
        return f'To big value: {size_sq_ft}'


def properly_format_size(size_text: str) -> str:
    """
    Categorizes size into small, medium or large based on the area
    :param size_text: String containing description of the storage unit
    :return: description formatted in a n'xn' format
    """

    # checks the format (feet by feet, or a x b, etc.)
    if bool(re.match("[0-9]+.?[0-9]? (foot|feet) by [0-9]+.?[0-9]? f+", size_text)) or bool(
            re.match(r"[0-9]+.?[0-9]?'\s*x\s*[0-9]+.?[0-9]?'", size_text)):
        tmp_dimensions = re.findall("[0-9]+.?[0-9]?", size_text)[:2]
        tmp_dimensions = [d.strip() for d in tmp_dimensions]
        tmp_dimensions = [d.replace("'", "") for d in tmp_dimensions]
    elif bool(re.match(r"[0-9]+.?[0-9]?\s*x\s*[0-9]+.?[0-9]?", size_text)):
        tmp_dimensions = re.split(r'x| \s*', size_text.replace(" x ", "x"))[:2]
    else:
        return 'Unknown'

    return f"{tmp_dimensions[0]}'x{tmp_dimensions[1]}'"


def elevator_access_tagging(description_text: str) -> bool:
    """
        Checks if any of the key terms are in the description text and flags the result accordingly
        :param description_text: String containing description of the storage unit
       :return: Boolean indicating if the storage unit is with elevator access or not
    """
    terms = ['elevator', 'lift']
    negation_terms = [f'{a} {b}' for a in ['no', 'not'] for b in terms]

    for neg_term in negation_terms:
        if neg_term in description_text.lower():
            return False

    for term in terms:
        if term in description_text.lower():
            return True

    return False


def ground_floor_tagging(description_text: str) -> bool:
    """
        Checks if any of the key terms are in the description text and flags the result accordingly
        :param description_text: String containing description of the storage unit
       :return: Boolean indicating if the storage unit is on the ground floor
    """
    terms = ['1st floor', 'ground level']
    negation_terms = [f'{a} {b}' for a in ['no', 'not'] for b in terms]

    for neg_term in negation_terms:
        if neg_term in description_text.lower():
            return False

    for term in terms:
        if term in description_text.lower():
            return True

    return False


def drive_up_tagging(description_text: str) -> bool:
    """
        Checks if any of the key terms are in the description text and flags the result accordingly
        :param description_text: String containing description of the storage unit
       :return: Boolean indicating if the storage unit is with drive up access or not
    """
    terms = ['drive-up', 'drive up', 'covered loading area/indoor access', 'loading bay access']
    negation_terms = [f'{a} {b}' for a in ['no', 'not'] for b in terms]

    for neg_term in negation_terms:
        if neg_term in description_text.lower():
            return False

    for term in terms:
        if term in description_text.lower():
            return True

    return False


def check_special_case_tagging(description_text: str) -> str:
    """
    Flags every storage unit considered a special case (e.g. storage has no dimensions, wine/vehicle storage, etc.)
    :param description_text: String containing description of the storage unit
    :return: special case type or nan for regular storage units
    """
    vehicles = ['boat', 'motorcycle', 'car', 'vehicle', 'parking']

    if isinstance(description_text, float):
        raise TypeError('Input must be text description.')
    elif "wine" in description_text.lower():
        return "Wine Storage"
    elif "parking" in description_text.lower() or "RV" in description_text or any(
            v in description_text.lower() for v in vehicles):
        return "Vehicle Storage"
    elif "locker" in description_text.lower():
        return "Locker"
    elif "mailbox" in description_text.lower():
        return "Mailbox"

    return ''
