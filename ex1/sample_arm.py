import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from RobotVisualizer2D import RobotVisualizer2D
from Robot import Robot

def sample_arm(log_name=None):
    # Load log data (allow for sample data as well as arbitrary logs)
    if log_name is None:
        # Default to sample-log
        log = loadmat('sample_ground_truth.mat')
        theta = log['theta']
        show_ground_truth = True
    else:
        # For arbitrary logs, you'll need to implement a way to load them
        # This part might need adjustment based on your specific log format
        log = loadmat(log_name)
        theta = log['position']
        show_ground_truth = False

    # Prepare plots
    if show_ground_truth:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Robot Display RR')
        actual_visualizer = RobotVisualizer2D(4, 0.1, ax1)
        ax1.set_title('Your Kinematics')
        gt_visualizer = RobotVisualizer2D(4, 0.1, ax2)
        ax2.set_title('Correct Kinematics')
    else:
        fig, ax = plt.subplots()
        actual_visualizer = RobotVisualizer2D(4, 0.1, ax)
        ax.set_title('Robot Display RR')

    robot = Robot(np.array([[0.55], [0.4]]), np.array([[1], [1]]), np.array([[1], [1]]), 0)

    # Iteratively visualize data
    for i in range(len(theta)):
        # Actual frames
        frames = np.zeros((3, 3, 4))
        frames[:,:,0] = np.eye(3)
        frames[:,:,1:] = robot.fk(theta[i,:].reshape(-1,1))
        actual_visualizer.set_frames(frames)

        # Ground truth
        if show_ground_truth:
            frames = log['ground_truth_frames'][0][i]
            gt_visualizer.set_frames(frames)

        # Update the plot
        plt.draw()
        plt.pause(0.001)  # Add a small pause to control the animation speed

    plt.show()