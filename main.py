import json

from behaviors import Behavior
from cluster_tools.cluster_tool import ClusterTool
from cluster_tools.representation_with_plot import Plotter


def main():
    json_file_path = 'data.json'
    points = {}
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        for vehicle_number in data.keys():
            for i in range(len(data[vehicle_number])):
                points[(vehicle_number, i)] = Behavior(data[vehicle_number][i], vehicle_number)

    # # # 3 lines of code that plot the points(without clusters)
    # vecs = [point.get_vector() for point in points.values()]
    # p = Plotter()
    # p.plot_points(vecs)

    tools = ClusterTool(points)
    tools.set_cluster_centroids()


if __name__ == '__main__':
    main()
