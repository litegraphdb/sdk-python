from enum import Enum


class Vector_Index_Type_Enum(str, Enum):
    """
    Vector index type.
    """

    HnswRam = "HnswRam"
    HnswSqlite = "HnswSqlite"
