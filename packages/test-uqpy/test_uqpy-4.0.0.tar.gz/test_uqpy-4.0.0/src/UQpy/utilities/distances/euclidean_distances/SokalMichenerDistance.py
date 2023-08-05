from typing import Union

from UQpy.utilities.ValidationTypes import NumpyFloatArray
from UQpy.utilities.distances.baseclass.EuclideanDistance import EuclideanDistance
from scipy.spatial.distance import pdist


class SokalMichenerDistance(EuclideanDistance):

    def compute_distance(self, points: NumpyFloatArray) -> Union[float, NumpyFloatArray]:
        return pdist(points, "sokalmichener")
