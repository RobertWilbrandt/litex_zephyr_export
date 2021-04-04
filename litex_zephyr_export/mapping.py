"""Define mapping of litex components to generated zephyr output"""


class Mapping:
    """Mapping from litex component to generated zephyr output

    :param name: Name of the mapping, only used during debugging
    :type name: str
    """

    def __init__(self, name):
        self.name = name
