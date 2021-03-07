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

    def add_memory_region(self, memory_region):
        """Add a memory region to this SoC configuration

        :param memory_region: Memory region to be added
        :type memory_region: MemoryRegion
        """
        self.memory_regions += memory_region


class Peripheral:
    """The configuration of a single peripheral"""

    def __init__(self):
        pass


class MemoryRegion:
    """One SoC memory region"""

    def __init__(self):
        pass
