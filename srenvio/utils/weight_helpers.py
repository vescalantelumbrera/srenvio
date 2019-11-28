

import math

from .convertors import cmToVoulumetricKG


def getTotalWeight(weight, length, width, height):
    volumetric_weight = cmToVoulumetricKG(width, length, height)
    return math.ceil(volumetric_weight) if volumetric_weight > weight else math.ceil(weight)


def getOverWeight(total_weight, real_weight):
    over_weight = real_weight-total_weight
    over_weight=over_weight*(-1)

    return 0 if over_weight < 0 else math.ceil(over_weight)
