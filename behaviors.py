import numpy as np


class Behavior:
    """
    The Behavior class is constructed by a fields dictionary and the vehicle number:
    The 'Start' and 'End' window timestamps are float types from POSIX
    The distance 'before' and 'after' are floats too and represent kilometers
    The 'vehicle number' is the unique licence plate for identification of the constructed behavior
    Methods:
    1. get the vector of floats in np.array by get_vector method
    2. get the order of the values in a list format by get_vector_order method
        This will describe to you what each value represents
    """
    def __init__(self, fields_dict, vehicle_number):
        self.__fields = fields_dict
        self._centroid = None
        self.vehicle_number = vehicle_number

    def get_name(self):
        return self.vehicle_number

    def get_vector(self):
        # take the behavior values and return a vector
        return np.array(list(self.__fields.values()))

    def get_vector_order(self):
        # return the order of the vector - what do each values represent
        return list(self.__fields.keys())

    def set_centroid(self, centroid):
        self._centroid = centroid

    def get_centroid(self):
        return self._centroid

    def __repr__(self):
        return str(self.__fields)
