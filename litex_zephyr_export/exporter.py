"""Export SoC definition to Zephyr"""

import logging

logging.basicConfig(level=logging.INFO)


class Exporter:
    """Export SoC by exporting to a set of target files

    :param log_level: Logging level to use
    :type log_level: int
    """

    def __init__(self, log_level=logging.INFO):
        self._file_exporters = []
        self._mappings = {}

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

    def add_file_exporter(self, file_exporter):
        """Adds exporter for a specific file

        :param file_exporter: File exporter to add
        :type file_exporter: .file_exporter.FileExporter"""
        self._file_exporters.append(file_exporter)

    def add_mapping(self, periph, mapping):
        """Add a mapping from litex peripheral to zephyr output

        :param periph: Peripheral to map
        :type periph: str
        :param mapping: Mapping to apply
        :type mapping: .mapping.Mapping
        """
        self._mappings[periph] = mapping

    def export(self):
        """Export using all registered exporters"""
        self.logger.info("Starting to export to files")

        for (i, file_exporter) in enumerate(self._file_exporters):
            self.logger.info(
                "[%d/%d] Now exporting with %s",
                i + 1,
                len(self._file_exporters),
                file_exporter.name,
            )
            file_exporter.generate()
