class SpecialTypes(object):
    """
    Created when a class has special types.
    Types assigned according to built
    in dictionary
    """

    def __init__(self, special_types):
        types_list = {
            'B': "hybrid",
            'D': "distance_learning",
            'E': "enhanced",
            'H': "honors",
            'J': "joint_offer",
            'O': "online",
            'R': "research",
            'S': "service_learning",
            'W': "writing_section",
            '%': "new_course",
            '#': "restriced_financial_aid"
        }
        split_types = [char for char in special_types]
        for type_char in split_types:
            setattr(self, types_list.get(type_char), True)


def parse_special_types(special_type_full):
    """
    Parse special types into object containing
    details relating to special types.
    If there are none, "None" is added
    """
    if len(special_type_full) == 0:
        return "None"
    else:
        return SpecialTypes(special_type_full).__dict__
