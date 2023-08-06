from typing import Type, Tuple, Union, Any, Iterable
import ctypes
from enum import IntEnum
from .impl.imnodes import *
class ImGuiContext(ctypes.Structure):
    pass
from enum import IntEnum

class ImNodesCol_(IntEnum):
    NodeBackground = 0x0
    NodeBackgroundHovered = 0x1
    NodeBackgroundSelected = 0x2
    NodeOutline = 0x3
    TitleBar = 0x4
    TitleBarHovered = 0x5
    TitleBarSelected = 0x6
    Link = 0x7
    LinkHovered = 0x8
    LinkSelected = 0x9
    Pin = 0xa
    PinHovered = 0xb
    BoxSelector = 0xc
    BoxSelectorOutline = 0xd
    GridBackground = 0xe
    GridLine = 0xf
    MiniMapBackground = 0x10
    MiniMapBackgroundHovered = 0x11
    MiniMapOutline = 0x12
    MiniMapOutlineHovered = 0x13
    MiniMapNodeBackground = 0x14
    MiniMapNodeBackgroundHovered = 0x15
    MiniMapNodeBackgroundSelected = 0x16
    MiniMapNodeOutline = 0x17
    MiniMapLink = 0x18
    MiniMapLinkSelected = 0x19
    MiniMapCanvas = 0x1a
    MiniMapCanvasOutline = 0x1b
    COUNT = 0x1c

class ImNodesStyleVar_(IntEnum):
    GridSpacing = 0x0
    NodeCornerRounding = 0x1
    NodePadding = 0x2
    NodeBorderThickness = 0x3
    LinkThickness = 0x4
    LinkLineSegmentsPerLength = 0x5
    LinkHoverDistance = 0x6
    PinCircleRadius = 0x7
    PinQuadSideLength = 0x8
    PinTriangleSideLength = 0x9
    PinLineThickness = 0xa
    PinHoverRadius = 0xb
    PinOffset = 0xc
    MiniMapPadding = 0xd
    MiniMapOffset = 0xe
    COUNT = 0xf

class ImNodesStyleFlags_(IntEnum):
    NONE = 0x0
    NodeOutline = 0x1
    GridLines = 0x4

class ImNodesPinShape_(IntEnum):
    Circle = 0x0
    CircleFilled = 0x1
    Triangle = 0x2
    TriangleFilled = 0x3
    Quad = 0x4
    QuadFilled = 0x5

class ImNodesAttributeFlags_(IntEnum):
    NONE = 0x0
    EnableLinkDetachWithDragClick = 0x1
    EnableLinkCreationOnSnap = 0x2

class ImNodesMiniMapLocation_(IntEnum):
    BottomLeft = 0x0
    BottomRight = 0x1
    TopLeft = 0x2
    TopRight = 0x3

