import numpy as np
import matplotlib.pyplot as plt
from Robot import Robot

class RobotVisualizer2D:
    """
    RobotVisualizer2D draws the coordinate frames of each section in a kinematic
    chain. The axes are color-coded RGB for XY.
    """

    def __init__(self, num_frames, axis_length=0.1, ax=None):
        """
        Initialize the RobotVisualizer2D.

        :param num_frames: Number of frames to visualize
        :param axis_length: Length of the coordinate axes (default: 0.1)
        :param ax: Matplotlib axis to draw on (if None, a new figure is created)
        """
        self.num_frames = num_frames
        self.axis_length = axis_length

        if ax is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.ax = ax

        self.initialize_plot()

    def initialize_plot(self):
        """Initialize the plot with coordinate frames and labels."""
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        # Initialize coordinate frames
        self.x_lines = [self.ax.plot([], [], 'r-', linewidth=2)[0] for _ in range(self.num_frames)]
        self.y_lines = [self.ax.plot([], [], 'g-', linewidth=2)[0] for _ in range(self.num_frames)]
        self.link_lines = [self.ax.plot([], [], 'k:', linewidth=2)[0] for _ in range(self.num_frames)]

        # Add legend and labels
        self.ax.legend(['x', 'y'], loc='lower right')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')

        # Draw base coordinate frame
        self.ax.plot([0, self.axis_length], [0, 0], 'k-', linewidth=2)
        self.ax.plot([0, 0], [0, self.axis_length], 'k-', linewidth=2)

    def set_frames(self, frames):
        """
        Update the coordinate frames.

        :param frames: 3x3xN matrix of homogeneous transforms
        """
        if frames.shape[2] != self.num_frames:
            raise ValueError(f"Expected {self.num_frames} frames, got {frames.shape[2]}")

        axes_base = np.array([[0, self.axis_length, 0, self.axis_length],
                              [0, 0, 0, self.axis_length],
                              [1, 1, 1, 1]])

        for i in range(self.num_frames):
            T = frames[:,:,i]
            if i > 0:
                T_previous = frames[:,:,i-1]
            else:
                T_previous = np.eye(3)

            axes_T = T @ axes_base
            
            # Update coordinate frame lines
            self.x_lines[i].set_data([axes_T[0,0], axes_T[0,1]], [axes_T[1,0], axes_T[1,1]])
            self.y_lines[i].set_data([axes_T[0,2], axes_T[0,3]], [axes_T[1,2], axes_T[1,3]])

            # Update link lines
            start = T_previous @ np.array([0, 0, 1])
            finish = T @ np.array([0, 0, 1])
            self.link_lines[i].set_data([start[0], finish[0]], [start[1], finish[1]])

        self.ax.figure.canvas.draw()