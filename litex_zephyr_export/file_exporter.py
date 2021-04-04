"""Export a parsed SoC configuration"""
import logging

from .devicetree_writer import DevicetreeWriter, Node

logging.basicConfig(level=logging.INFO)


class FileExporter:
    """Base class for exporting completely parsed SoC definitions

    :param name: Name of this file exporter
    :type name: str
    """

    def __init__(self, name):
        self.name = name


class SoCDevicetreeExporter(FileExporter):
    """Export a parsed configuration to a SoC device tree file

    :param log_level: Logging level to use
    :type log_level: int
    """

    def __init__(self, log_level=logging.INFO):
        super().__init__("soc_devicetree_exporter")

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

    def generate(self, soc, periph_mappings):
        """Generate SoC devicetree export

        :param soc: SoC to generate for
        :type soc: .soc.SoC
        :param periph_mappings: List of peripherals with mappings to use on them
        :type periph_mappings: list
        """

        def generate_soc(soc):
            def generate_memory_regions(soc):
                mem_reg_node = Node("memory_regions")
                mem_reg_node.add_property("#address-cells", "<1>")
                mem_reg_node.add_property("#size-cells", "<1>")

                def generate_memory(region):
                    mem_node = Node("memory", region.base_addr)
                    mem_node.add_property("label", f'"{region.name.lower()}"')
                    mem_node.add_property("device_type", '"memory"')
                    mem_node.add_property(
                        "reg", f"<0x{region.base_addr:08x} 0x{region.size:08x}>"
                    )
                    return mem_node

                main_ram_node = generate_memory(soc.main_ram)
                main_ram_node.label = "main_ram"
                mem_reg_node.add_node(main_ram_node)

                for memory_region in soc.other_memory_regions:
                    mem_reg_node.add_node(generate_memory(memory_region))

                return mem_reg_node

            soc_node = Node("soc")
            soc_node.add_property("#address-cells", "<1>")
            soc_node.add_property("#size-cells", "<1>")
            soc_node.add_property(
                "compatible", f'"{soc.vendor.lower()},{soc.name.lower()}"'
            )
            soc_node.add_property("ranges")

            mem_reg_node = generate_memory_regions(soc)
            soc_node.add_node(mem_reg_node)

            return soc_node

        self.logger.info("Generating SoC devicetree")

        devicetree_writer = DevicetreeWriter()

        soc_node = generate_soc(soc)
        devicetree_writer.add_node(soc_node)

        self.logger.info(devicetree_writer.write())
