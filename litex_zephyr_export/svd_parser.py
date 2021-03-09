"""Parse a litex export in SVD format"""
import logging
import xml.etree.ElementTree

from termcolor import colored

from .soc import SoC

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


class SvdParser:
    """Parse a litex export in SVD format"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
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

            result = parse_device(root)

            peripherals = root.find("peripherals")
            for periph in peripherals.findall("peripheral"):
                self.logger.info(
                    "Found peripheral %s",
                    colored(periph.find("name").text, attrs=["underline"]),
                )

            vendor_extensions = root.find("vendorExtensions")

            constants = vendor_extensions.find("constants")
            for constant in constants.findall("constant"):
                self.logger.info(
                    "Found constant %s=%s",
                    colored(constant.get("name"), attrs=["underline"]),
                    constant.get("value"),
                )

            memory_regions = vendor_extensions.find("memoryRegions")
            for memory_region in memory_regions.findall("memoryRegion"):
                self.logger.info(
                    "Found memory region %s",
                    colored(memory_region.find("name").text, attrs=["underline"]),
                )

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


def parse_device(device_node):
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

    return SoC(name=name, vendor=vendor)
