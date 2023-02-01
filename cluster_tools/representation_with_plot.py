from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        plt.figure()
        self.axes = plt.axes(projection='3d')

        # Label the axes
        self.axes.set_xlabel('start_window')
        self.axes.set_ylabel('end_window')
        self.axes.set_zlabel('milage')

    def plot_points(self, points, color=None):

        x = [v[0] for v in points]
        y = [v[1] for v in points]
        z = [v[2] for v in points]
        # Plot the points

        if color:
            self.axes.scatter(x, y, z, c=color)
        else:
            self.axes.scatter(x, y, z)

        # Show the plot
        plt.show()
