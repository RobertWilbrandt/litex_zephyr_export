"""SoC configuration description that can be parsed from a litex export"""

import logging

from termcolor import colored

logging.basicConfig(level=logging.INFO)


class SoC:
    """A complete SoC configuration

    :param name: Name of the SoC
    :type name: str
    :param vendor: Vendor name
    :type vendor: str
    :param log_level: Logging level to use
    :type log_level: int
    """

    def __init__(self, name, vendor, log_level=logging.INFO):
        self.name = name
        self.vendor = vendor

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self.peripherals = []

        self.rom = None
        self.main_ram = None
        self.csr = None
        self.other_memory_regions = []

    def add_peripheral(self, peripheral):
        """Add a peripheral to this SoC configuration

        :param peripheral: Peripheral to be added
        :type peripheral: Peripheral
        """
        self.logger.info(
            "Addded peripheral %s at %s",
            colored(peripheral.name, "green", attrs=["underline"]),
            colored(f"0x{peripheral.base_addr:08x}", attrs=["bold"]),
        )
        self.peripherals.append(peripheral)

    def add_memory_region(self, memory_region):
        """Add a memory region to this SoC configuration

        :param memory_region: Memory region to be added
        :type memory_region: MemoryRegion
        """
        if memory_region.name == "ROM":
            self.rom = memory_region
            region_desc = "rom"
        elif memory_region.name == "MAIN_RAM":
            self.main_ram = memory_region
            region_desc = "main_ram"
        elif memory_region.name == "CSR":
            self.csr = memory_region
            region_desc = "csr"
        else:
            self.other_memory_regions.append(memory_region)
            region_desc = "other"

        self.logger.info(
            "Added %s memory region %s at %s of size %s",
            region_desc,
            colored(memory_region.name, "blue", attrs=["underline"]),
            colored(f"0x{memory_region.base_addr:08x}", attrs=["bold"]),
            colored(f"0x{memory_region.size:x}", attrs=["bold"]),
        )


class Peripheral:
    """The configuration of a single peripheral

    :param name: Peripheral name
    :type name: str
    :param base_addr: Lowest address reserved or used by the peripheral
    :type base_addr: int
    """

    def __init__(self, name, base_addr):
        self.name = name
        self.base_addr = base_addr


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
