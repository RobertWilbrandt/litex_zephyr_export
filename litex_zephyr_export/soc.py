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

    def get_main_memory_region(self):
        """Get the main memory region to load the application to

        This region is the MAIN_RAM memory region

        :return: Main memory region
        :rtype: MemoryRegion
        :raise RuntimeError: If the main memory configuration is invalid
        """
        main_memory_regions = [
            mr for mr in self.memory_regions if mr.name == "MAIN_RAM"
        ]

        if len(main_memory_regions) == 0:
            raise RuntimeError("Could not find required memory section MAIN_RAM")
        if len(main_memory_regions) > 1:
            raise RuntimeError("Found multiple memory sections MAIN_RAM")

        return main_memory_regions[0]

    def get_usable_memory_regions(self):
        """Gets all reasonably user-usable memory regions

        This will filter out the following sections:
        - ROM
        - MAIN_RAM
        - CSR

        :return: Reasonably user-usable memory regions
        :rtype: list
        """
        return [
            mr
            for mr in self.memory_regions
            if mr.name not in ["ROM", "MAIN_RAM", "CSR"]
        ]

    def get_csr_base_addr(self):
        """Get the CSR base address

        :return: Base address of CSRs
        :rtype: int
        :raise RuntimeError: If the CSR memory region definition is invalid
        """
        csr_memory_regions = [mr for mr in self.memory_regions if mr.name == "CSR"]

        if len(csr_memory_regions) == 0:
            raise RuntimeError("Could not find required memory section CSR")
        if len(csr_memory_regions) > 1:
            raise RuntimeError("Found multiple memory regions CSR")

        return csr_memory_regions[0].base_addr


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

    def end(self):
        """Return the first address after base_address not in this memory section

        :return: End of this memory section
        :rtype: int
        """
        return self.base_addr + self.size
