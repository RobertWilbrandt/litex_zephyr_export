"""Write formatted devicetree files"""


def indent(text, indentation):
    """Indent a text by a given amount

    :param text: Text to indent
    :type text: str
    :param indentation: Amount to indent by
    :type indentation: int
    """
    return indentation * "\t" + text


class DevicetreeWriter:
    """Write correctly formatted devicetree files"""

    def __init__(self):
        self.root = Node("/")

    def add_node(self, node):
        """Add a child to the root node

        :param node: Node to add
        :type node: Node
        """
        self.root.add_node(node)

    def write(self):
        """Write devicetree to string

        :return: Written form of devicetree
        :rtype: str
        """
        return "\n".join(self.root.write())


class Node:
    """A single devicetree node

    :param name: Node name
    :type name: str
    :param address: Optional node address
    :type address: str
    :param label: Optional label for node
    :type label: str
    """

    def __init__(self, name, address=None, label=None):
        self.name = name
        self.address = address
        self.label = label

        self.sub_nodes = []
        self.props = []

    def add_node(self, node):
        """Adds a node as subnode

        :param node: Node to add
        :type node: Node
        """
        self.sub_nodes.append(node)

    def add_property(self, name, value=None):
        """Add a property to this node

        :param name: Name of the property
        :type name: str
        :param value: Value of the property
        """
        self.props.append((name, value))

    def write(self):
        """Write node to string

        :return: Lines of written form of devicetree
        :rtype: list
        """
        out = []

        # Create node name line
        label_str = f"{self.label}: " if self.label is not None else ""
        address_str = f"@{self.address:08x}" if self.address is not None else ""
        out.append(f"{label_str}{self.name}{address_str} {'{'}")

        sub_out = []  # Collect everything inside here so it gets indented appropriately

        # Create entry for each property
        for name, value in self.props:
            if value is not None:
                sub_out.append(f"{name} = {value};")
            else:
                sub_out.append(f"{name};")

        if len(self.props) > 0 and len(self.sub_nodes) > 0:
            sub_out.append("")

        # Create subnode entries
        for i, sub_node in enumerate(self.sub_nodes):
            if i != 0:
                sub_out.append("")
            sub_out += sub_node.write()

        out += [indent(line, 1) for line in sub_out]

        # Close node
        out.append("};")

        return out
