import re


class Room():
    """
        Organizes room information into following:
        building code, and room number.
        Ex. 'UW1' and '020'
    """

    def __init__(self, building_code, room_number):
        self.building_code = building_code
        self.room_number = room_number


def parse_location(location_full):
    """
    Parse a course's room into
    a building code and room number.
    If there is none, "To Be Arranged" is added.
    """

    if "*    *" in location_full or len(location_full) == 0:
        return "To Be Arranged"
    location_split = re.sub(r'[*]', '', location_full).strip().split(' ')
    if len(location_split) > 1:
        while "" in location_split:
            location_split.remove("")
        return Room(location_split[0].strip(), location_split[1].strip()).__dict__
    return location_split[0]
