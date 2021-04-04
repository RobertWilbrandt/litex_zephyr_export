"""Export SoC definition to Zephyr"""


class Exporter:
    """Export SoC by exporting to a set of target files"""

    def __init__(self):
        self._file_exporters = []
        self._mappings = {}

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
        for file_exporter in self._file_exporters:
            file_exporter.generate()
