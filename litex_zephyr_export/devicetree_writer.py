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

    def add_node(self, name, address=None):
        """Add a node to devicetree node and return it

        :param name: Node name
        :type name: str
        :param address: Optional node address
        :type address: int
        """
        return self.root.add_node(name, address)

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
    """

    def __init__(self, name, address=None):
        self.name = name
        self.address = address

        self.sub_nodes = []
        self.props = []

    def add_node(self, name, address=None):
        """Adds a node as child to this one and return it

        :param name: New node name
        :type name: str
        :param address: Option address of new node
        :type address: int
        """
        new_node = Node(name, address)
        self.sub_nodes.append(new_node)
        return new_node

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

        if self.address is None:
            out.append(f"{self.name} {'{'}")
        else:
            out.append(f"{self.name}@{self.address:08x} {'{'}")

        sub_out = []

        for name, value in self.props:
            if value is not None:
                sub_out.append(f"{name} = {value};")
            else:
                sub_out.append(f"{name};")

        for sub_node in self.sub_nodes:
            sub_out += sub_node.write()

        out += [indent(line, 1) for line in sub_out]

        out.append("};")

        return out
