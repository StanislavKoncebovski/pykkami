from collections import namedtuple

Vector2D = namedtuple('Vector2D', 'X Y')
Vector3D = namedtuple('Vector3D', 'X Y Z')
Point2D = namedtuple('Point2D', 'X Y')
Point3D = namedtuple('Point3D', 'X Y Z')
PixelSpacing = namedtuple('PixelSpacing', 'Row Column')
Vector3DPair = namedtuple('Vector3DPair', 'Rows Columns')

# Using dataclass
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int = 1  # Set default value

# Typed version of namedtuple
import typing

PointXY = typing.NamedTuple("PointXY", [('x', int), ('y', int)])


if __name__ == '__main__':
    v1 = Vector2D(2.87, 3.62)

    print(v1.X)
    print(v1.Y)

    v2 = Vector3D(2.87, 3.62, 3.67)

    print(v2.X)
    print(v2.Y)
    print(v2.Z)

    ps = PixelSpacing(0.625, 0.5)
    print()
    print(ps.Row)
    print(ps.Column)

    v3p = Vector3DPair(Vector3D(1, 0, 0), Vector3D(0, 1, 0))
    print(v3p)

    # making named tuples from a value list
    values = [3.14, 6.28]
    p1 = Point2D._make(values)

    print(p1)

    # converting a named tuple to a dictionary:
    d1 = v2._asdict()
    print(d1)
    d2 = v3p._asdict()
    print(d2)

    # converting a dictionary to a named tuple:
    d3 = {'X': 0.51, 'Y': 0.62, 'Z': 0.73}
    v4 = Vector3D(**d3)
    print(f"v4 = {v4}")

    # replacing a named component:
    v3 = v2._replace(Z=7.50)
    print(v3)

    # listing the fields
    print(v3._fields)
    print(v3._field_defaults)

    print("\n\n\n------------------\n\n")
    print(Point(3))

    pxy = PointXY(42, 100)
    print(pxy)

    pxy2 = PointXY(42, "abs")
    print(pxy2)
