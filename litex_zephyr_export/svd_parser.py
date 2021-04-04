"""Parse a litex export in SVD format"""
import logging
import xml.etree.ElementTree

from termcolor import colored

from .soc import MemoryRegion, Peripheral, SoC

logging.basicConfig(level=logging.INFO)


def element_get_required_child(element, child):
    """Get a required child element or fail if it doesn't exist

    :param element: Node to get child from
    :type element: xml.etree.ElementTree.Element
    :param child: Name of child element to get
    :type child: str

    :return: Child element child of element
    :rtype: xml.etree.ElementTree.Element
    :raise RuntimeError: If child does not exist
    """
    result = element.find(child)
    if result is None:
        raise RuntimeError(
            f"Could not find required child '{child}' of element '{element.tag}'"
        )
    return result


def parse_hex(text):
    """Parse a hex number from text or fail

    :param text: Text to parse hex number from
    :type text: str

    :return: Parsed hex number
    :rtype: int
    :raise RuntimeError: If text does not contain a valid hexadecimal number
    """
    try:
        return int(text, 0)
    except ValueError as ex:
        raise RuntimeError(f"Could not parse hex number '{text}': {ex}")


class SvdParser:
    """Parse a litex export in SVD format

    :param log_level: Logging level to use
    :type log_level: int
    """

    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.log_level = log_level
        self.logger.setLevel(log_level)

        self.logger.info("Creating SVD parser...")

    def parse(self, svd):
        """Parse an SVD export

        :param svd: Content of SVD export
        :type svd: str

        :return: Parsed SoC definition
        :rtype: SoC
        :raise RuntimeError: If there are problems parsing the SVD export
        """
        try:
            self.logger.info("Parsing SVD from xml")
            root = xml.etree.ElementTree.fromstring(svd)

            result = self.parse_device(root)

            # Parse peripherals
            peripherals = root.find("peripherals")
            for periph in peripherals.findall("peripheral"):
                name = element_get_required_child(periph, "name").text
                base_addr = parse_hex(
                    element_get_required_child(periph, "baseAddress").text
                )
                result.add_peripheral(Peripheral(name, base_addr))

            vendor_extensions = root.find("vendorExtensions")

            # Parse constants
            constants = vendor_extensions.find("constants")
            for constant in constants.findall("constant"):
                self.logger.debug(
                    "Found constant %s=%s",
                    colored(constant.get("name"), attrs=["underline"]),
                    constant.get("value"),
                )

            # Parse memory regions
            memory_regions = element_get_required_child(
                vendor_extensions, "memoryRegions"
            )
            for memory_region in memory_regions.findall("memoryRegion"):
                name = element_get_required_child(memory_region, "name").text
                base_addr = parse_hex(
                    element_get_required_child(memory_region, "baseAddress").text
                )
                size = parse_hex(element_get_required_child(memory_region, "size").text)
                result.add_memory_region(MemoryRegion(name, base_addr, size))

            return result

        except xml.etree.ElementTree.ParseError as ex:
            raise RuntimeError(f"Could not parse SVD export: {ex}")

    def parse_file(self, path):
        """Parse an SVD export

        :param path: Path to exported file
        :type path: path-like

        :return: Parsed SoC definition
        :rtype: SoC
        :raise FileNotFoundError: If path was not found
        :raise RuntimeError: If there are problems parsing the SVD export
        """
        self.logger.debug("Parsing SVD file %s", path)

        with open(path, "r") as svd_file:
            svd = svd_file.read()
            return self.parse(svd)

    def parse_device(self, device_node):
        """Parse the SVD device tag and create a SoC configuration from it

        :param device_node: SVD device node
        :rtype device_node: xml.etree.ElementTree.Element

        :return: SoC containing device-specific information
        :rtype: SoC
        :raise RuntimeError: If the device_node content is not valid
        """
        vendor_node = device_node.find("vendor")
        if vendor_node is None:
            vendor_id_node = device_node.find("vendorID")
            if vendor_id_node is None:
                vendor = "custom"
            else:
                vendor = vendor_id_node.text
        else:
            vendor = vendor_node.text

        name = element_get_required_child(device_node, "name").text

        series = device_node.find("series")
        if series is not None:
            name = series.text + "_" + name

        return SoC(name=name, vendor=vendor, log_level=self.log_level)
