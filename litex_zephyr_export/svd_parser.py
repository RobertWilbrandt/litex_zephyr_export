"""Parse a litex export in SVD format"""
import logging
import xml.etree.ElementTree

from termcolor import colored

logging.basicConfig(level=logging.INFO)


class SvdParser:
    """Parse a litex export in SVD format"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Creating SVD parser...")

    def parse(self, svd):
        """Parse an SVD export

        :param svd: Content of SVD export
        :type svd: str

        :raise RuntimeError: If there are problems parsing the SVD export
        """
        try:
            self.logger.info("Parsing SVD from xml")
            root = xml.etree.ElementTree.fromstring(svd)

            peripherals = root.find("peripherals")
            for periph in peripherals.findall("peripheral"):
                self.logger.info(
                    "Found peripheral %s",
                    colored(periph.find("name").text, attrs=["underline"]),
                )

        except xml.etree.ElementTree.ParseError as ex:
            raise RuntimeError(f"Could not parse SVD export: {ex}")

        print(root)

    def parse_file(self, path):
        """Parse an SVD export

        :param path: Path to exported file
        :type path: path-like

        :raise FileNotFoundError: If path was not found
        :raise RuntimeError: If there are problems parsing the SVD export
        """
        self.logger.debug("Parsing SVD file %s", path)

        with open(path, "r") as svd_file:
            svd = svd_file.read()
            return self.parse(svd)
