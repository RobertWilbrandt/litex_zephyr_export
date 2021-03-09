"""SoC configuration description that can be parsed from a litex export"""


class SoC:
    """A complete SoC configuration

    :param name: Name of the SoC
    :type name: str
    :param vendor: Vendor name
    :type vendor: str
    """

    def __init__(self, name, vendor):
        self.name = name
        self.vendor = vendor

        self.peripherals = []
        self.memory_regions = []

    def add_peripheral(self, peripheral):
        """Add a peripheral to this SoC configuration

        :param peripheral: Peripheral to be added
        :type peripheral: Peripheral
        """
        self.peripherals += peripheral


class Peripheral:
    """The configuration of a single peripheral"""

    def __init__(self):
        pass


class MemoryRegion:
    """One SoC memory region

    :param name: Name of memory region
    :type name: str
    :param base_addr: Base address of memory region
    :type base_addr: int
    :param size: Size of memory region
    :type size: int
    """

    def __init__(self, name, base_addr, size):
        self.name = name
        self.base_addr = base_addr
        self.size = size
