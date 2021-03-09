"""Export a parsed SoC configuration"""
import logging

from termcolor import colored

from .devicetree_writer import DevicetreeWriter

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

        devicetree_writer = DevicetreeWriter()

        memory_regions = devicetree_writer.add_node("memory_regions")
        memory_regions.add_property("#address-cells", "<1>")
        memory_regions.add_property("#size-cells", "<1>")

        for memory_region in [
            self.soc.get_main_memory_region()
        ] + self.soc.get_usable_memory_regions():
            memory = memory_regions.add_node("memory", memory_region.base_addr)
            memory.add_property("device_type", '"memory"')
            memory.add_property(
                "reg", f"<0x{memory_region.base_addr:08x} 0x{memory_region.size:08x}>"
            )

        self.logger.info(devicetree_writer.write())
