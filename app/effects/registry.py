"""Effect registry - imports and registers all effects."""
from app.effects.shift import ShiftRowsColumns
from app.effects.warp import Warp
from app.effects.block_shuffle import BlockShuffle
from app.effects.transform import RotateFlip, Crop, Scale
from app.effects.color import HSVAdjust, RGBCurves, ChannelShuffle, Posterize
from app.effects.grain import Grain, SharpenBlur

# Registry of all available effects
EFFECT_REGISTRY = {
    "ShiftRowsColumns": ShiftRowsColumns,
    "Warp": Warp,
    "BlockShuffle": BlockShuffle,
    "RotateFlip": RotateFlip,
    "Crop": Crop,
    "Scale": Scale,
    "HSVAdjust": HSVAdjust,
    "RGBCurves": RGBCurves,
    "ChannelShuffle": ChannelShuffle,
    "Posterize": Posterize,
    "Grain": Grain,
    "SharpenBlur": SharpenBlur,
}

# Grouped effects for UI organization
EFFECT_GROUPS = {
    "Geometry": [
        ShiftRowsColumns,
        Warp,
        BlockShuffle,
        RotateFlip,
        Crop,
        Scale,
    ],
    "Color": [
        HSVAdjust,
        RGBCurves,
        ChannelShuffle,
        Posterize,
    ],
    "Detail": [
        Grain,
        SharpenBlur,
    ],
}

# Get all effects as a list
ALL_EFFECTS = list(EFFECT_REGISTRY.values())

