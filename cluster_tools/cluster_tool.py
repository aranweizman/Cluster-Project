from behaviors import Behavior
import sys

from cluster_tools.cluster_centroid import ClusterCentroid


class ClusterTool:
    """
    The cluster tool preforms cluster analysis on data using the K-means algorithm
    with z-score analysis for ignoring outlier points.
    data_dictionary - a dictionary with: key - name of data point
    value - class(structure) containing fields of the point coordinates
    """
    def __init__(self, point_dictionary: dict[str: Behavior]):
        assert point_dictionary  # must be non-empty
        self._points = point_dictionary
        self._centroids = {}
        self._outliers = {}
        self._centroid_color = 'orange'

    """
    This method picks points to be the cluster centers of mass.
    it uses a min-max algorithm that promises maximum variance.
    """
    # todo: get max number of centroids(optional)
    def set_cluster_centroids(self, plotter) -> None:

        # append cluster at first point
        first_key = next(iter(self._points))
        first_centroid = ClusterCentroid(self._points[first_key], self._points)
        self._centroids[self._points[first_key]] = first_centroid

        # set all points to reference initial centroid
        for point in self._points.values():
            point.set_centroid(first_centroid)

        # let clusters converge to optimal positions
        while self.update_cluster_positions():
            pass

        # save snapshot
        centroid_snapshot = self._centroids.copy()

        while True:

            # append min-max point as a function of previous centroids
            new_centroid_point = self.append_centroid()[0]
            plotter.plot_points([new_centroid_point.get_vector()], self._centroid_color)

            # check plot saturation (pre-implementation: loop is supervised by programmer)
            if input() == 'q':
                break

    """
    This method redistributes the centroids amongst the points, further optimizing the positions.
    The method iterates over all points and matches the closest centroid for each.
    It then recalculates the centroid positions as the average of the points that chose that centroid.
    """
    def update_cluster_positions(self) -> bool:
        # iterate over all points and update reference centroid
        for point in self._points.values():

            # recalculate nearest centroid
            for centroid in self._centroids.values():
                if centroid.distance_to_point(point) < point.get_centroid().distance_to_point(point):
                    point.set_centroid(centroid)

        # update centroid locations
        centroids_moved = False
        for centroid in self._centroids.values():
            if centroid.update_position():
                centroids_moved = True

        return centroids_moved

    """
    This method discards outlier points in the data.
    Outliers are defined as points with a Z-score greater than 3 or less than -3.
    The Z-score is measured relative to a given centroid(the current centroid of the point).
    """
    def discard_outliers(self):
        MAX_NON_OUTLIER_VARIANCE_RATIO = 3

        # calculate centroid variance
        for centroid in self._centroids:
            variance = centroid.get_variance()
            for point in centroid.get_cluster_points():

                # outlier found
                if centroid.distance_to_point(point) / variance > \
                                                        MAX_NON_OUTLIER_VARIANCE_RATIO:
                    self._outliers[point.get_name()] = point
                    centroid.remove(point)

    def append_centroid(self) -> tuple[Behavior, float]:
        furthest_point = (None, 0)
        for point in self._points.values():
            min_distance_to_centroid = sys.maxsize

            # find nearest centroid
            for centroid in self._centroids.values():
                new_distance = centroid.distance_to_point(point)

                if new_distance < min_distance_to_centroid:  # update min
                    min_distance_to_centroid = new_distance

            # nearest centroid found -> check if point has the largest distance to centroid
            if min_distance_to_centroid > furthest_point[1]:  # update max
                furthest_point = point, min_distance_to_centroid

        # append centroid to list
        self._centroids[furthest_point[0]] = ClusterCentroid(furthest_point[0], {})
        return furthest_point
