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
