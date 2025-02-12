from enum import Enum


class VectorSearchDomainEnum(str, Enum):
    """
    Vector search domain.
    """

    Graph = "Graph"
    Node = "Node"
    Edge = "Edge"
