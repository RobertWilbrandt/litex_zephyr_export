"""Export a parsed SoC configuration"""
import logging

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
        self.generate_memory_regions(devicetree_writer.add_node("memory_regions"))

        self.logger.info(devicetree_writer.write())

    def generate_memory_regions(self, node):
        """Generate memory regions node of devicetree

        :param node: Node to fill with content
        :type node: .devicetree_writer.Node
        """

        def generate_memory(node, region):
            node.address = region.base_addr
            node.add_property("device_type", '"memory"')
            node.add_property("reg", f"<0x{region.base_addr:08x} 0x{region.size:08x}>")

        node.add_property("#address-cells", "<1>")
        node.add_property("#size-cells", "<1>")

        for memory_region in self.soc.get_usable_memory_regions():
            generate_memory(node.add_node("memory"), memory_region)

        generate_memory(node.add_node("memory"), self.soc.get_main_memory_region())
