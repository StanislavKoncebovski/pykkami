from typing import *

# ==== ALIAS DATA TYPES implemented as named tuples with type hints ==== #
Vector2D = NamedTuple('Vector2D', [('X', float), ('Y', float)])
Vector3D = NamedTuple('Vector2D', [('X', float), ('Y', float), ('Z', float)])
Point2D = NamedTuple('Vector2D', [('X', float), ('Y', float)])
Point3D = NamedTuple('Vector2D', [('X', float), ('Y', float), ('Z', float)])
PixelSpacing = NamedTuple('PixelSpacing', [('Row', float), ('Column', float)])
Vector3DPair = NamedTuple('Vector3DPair', [('Rows', Vector2D), ('Columns', Vector3D)])


# These types support all functionality defined for classical named tuples, such as _asdict(), _make(), etc.

# TODO: the names of the fields seem not to be usable in assignment and retrieval operations,
#  such as the functions below; need further exploration

def point3d_to_list(point: Point3D) -> list[float]:
    return [point[0], point[1], point[2]]


def pixel_spacing_to_list(pixel_spacing: PixelSpacing) -> list[float]:
    return [pixel_spacing[0], pixel_spacing[1]]


def vector3d_pair_to_list(vp: Vector3DPair) -> list[float]:
    return [vp[0][0], vp[0][1], vp[0][2], vp[1][0], vp[1][1], vp[1][2]]
