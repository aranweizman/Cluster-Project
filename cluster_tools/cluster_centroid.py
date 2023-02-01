from behaviors import Behavior
import numpy as np


class ClusterCentroid:
    def __init__(self, centroid_point: Behavior, cluster_points: dict[str: Behavior]):
        # general centroid related fields
        self._centroid_point = centroid_point.get_vector()
        self._variance_changes = False

        # cluster points (calculation related) fields
        self._variance = None
        self._point_sum_total = sum(point.get_vector() for point in cluster_points.values())
        self._cluster_points = cluster_points
        self._point_count = len(cluster_points)

    def get_coordinates(self):
        return self._centroid_point

    def get_cluster_points(self):
        return self._cluster_points

    def add(self, new_point: Behavior) -> None:
        self._cluster_points[new_point.get_name()] = new_point
        self._point_sum_total += new_point.get_vector()
        self._point_count += 1

        self._variance_changes = True

    def remove(self, point: Behavior) -> None:
        del self._cluster_points[point.get_name()]
        self._point_sum_total -= point.get_vector()
        self._point_count -= 1

        self._variance_changes = True

    def update_position(self):
        if self._point_count:
            # calculate new position as point average
            new_position = self._point_sum_total / self._point_count

            # (return value) -> did the position changed
            if True in new_position != self._centroid_point:
                self._centroid_point = new_position

                self._variance_changes = True

                return True
            else:
                return False
        else:
            raise f"[e]:{self._centroid_point.vehicle_number} as centroid: " \
                                                        f"attempted to divide by 0(point count)"

    """
    This method simply calculates the vector distance between the centroid and a given (Behavior) point
    """
    def distance_to_point(self, point: Behavior) -> float:
        return np.linalg.norm(point.get_vector() -
                              self._centroid_point)

    """
    This method calculates the variance of the cluster-points-distance-to-centroid    
    """
    def get_variance(self) -> float:
        if self._variance_changes:
            self._variance = sum(self.distance_to_point(point)
                                 for point in self._cluster_points) / self._point_count
        return self._variance
