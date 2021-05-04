from typing import *

# ==== ALIAS DATA TYPES implemented as named tuples with type hints ==== #
Vector2D = NamedTuple('Vector2D', [('X', float), ('Y', float)])
Vector3D = NamedTuple('Vector2D', [('X', float), ('Y', float), ('Z', float)])
Point2D = NamedTuple('Vector2D', [('X', float), ('Y', float)])
Point3D = NamedTuple('Vector2D', [('X', float), ('Y', float), ('Z', float)])
PixelSpacing = NamedTuple('PixelSpacing', [('Row', float), ('Column', float)])
Vector3DPair = NamedTuple('Vector3DPair', [('Rows', Vector2D), ('Columns', Vector3D)])
# These types support all functionality defined for classical named tuples, such as _asdict(), _make(), etc.

if __name__ == '__main__':
    v1 = Vector2D(2.87, 3.62)
    print(v1)

    v2 = Vector2D._make([2.87, 3.62])
    print(v2)

    d = v2._asdict()
    print(d)
