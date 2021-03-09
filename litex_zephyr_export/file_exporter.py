"""Export a parsed SoC configuration"""
import logging

from termcolor import colored

logging.basicConfig(level=logging.INFO)


class FileExporter:
    """Base class for exporting completely parsed SoC definitions

    :param soc: Parsed SoC configuration
    :type soc: soc.SoC
    """

    def __init__(self, soc):
        self.soc = soc


class SoCDevicetreeExporter(FileExporter):
    """Export a parsed configuration to a SoC device tree file

    :param soc: Parsed SoC configuration
    :type soc: soc.SoC
    """

    def __init__(self, soc):
        super().__init__(soc)

        self.logger = logging.getLogger(self.__class__.__name__)

    def generate(self):
        """Generate SoC devicetree export"""
        self.logger.info("Generating SoC devicetree")
        self.logger.info("name: %s", self.soc.name)
        self.logger.info("vendor: %s", self.soc.vendor)

        main_memory_region = self.soc.get_main_memory_region()
        self.logger.info(
            "Main memory region: 0x%x - 0x%x",
            main_memory_region.base_addr,
            main_memory_region.end(),
        )

        csr_base_addr = self.soc.get_csr_base_addr()
        self.logger.info("CSR base address: 0x%x", csr_base_addr)

        self.logger.info("Additional memory regions:")
        for memory_region in self.soc.get_usable_memory_regions():
            self.logger.info(
                "- %s: 0x%x - 0x%x",
                colored(memory_region.name, attrs=["underline"]),
                memory_region.base_addr,
                memory_region.end(),
            )
