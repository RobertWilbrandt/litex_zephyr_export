"""Parse a litex export in SVD format"""
import logging

logging.basicConfig(level=logging.INFO)


class SvdParser:
    """Parse a litex export in SVD format"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Creating SVD parser...")

    def parse(self, svd):
        """Parse an SVD export

        :param svd: Content of SVD export
        :type svd: str"""
        print(svd)

    def parse_file(self, path):
        """Parse an SVD export

        :param path: Path to exported file
        :type path: path-like

        :raise FileNotFoundError: If path was not found
        """
        self.logger.info("Parsing SVD file %s", path)

        try:
            with open(path, "r") as svd_file:
                svd = svd_file.read()
                return self.parse(svd)

        except FileNotFoundError as ex:
            self.logger.error("Could not open svd file %s: %s", path, ex)
            raise
