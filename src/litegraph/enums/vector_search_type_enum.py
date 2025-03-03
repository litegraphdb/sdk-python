from enum import Enum


class VectorSearchTypeEnum(str, Enum):
    """
    Vector search type.
    """

    CosineDistance = "CosineDistance"
    CosineSimilarity = "CosineSimilarity"
    EuclidianDistance = "EuclidianDistance"
    EuclidianSimilarity = "EuclidianSimilarity"
    DotProduct = "DotProduct"
