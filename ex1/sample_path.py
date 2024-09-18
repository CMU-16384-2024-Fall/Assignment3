import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from Robot import Robot

def sample_path(log_name=None):
    # Load log data (allow for sample data as well as arbitrary logs)
    if log_name is None:
        # Default to sample-log
        log = loadmat('sample_ground_truth.mat')
        theta = log['theta']
        show_ground_truth = True
    else:
        # For arbitrary logs, you'll need to implement a way to load them
        log = loadmat(log_name)
        theta = log['position']
        show_ground_truth = False

    # Calculate end effector path through entire log
    n = len(theta)
    x = np.zeros(n)
    y = np.zeros(n)
    robot = Robot(np.array([[0.55], [0.4]]), np.array([[1], [1]]), np.array([[1], [1]]), 0)

    # calculate end effector x/y for each timestep
    for i in range(n):
        frames = robot.fk(theta[i,:].reshape(-1,1))
        x[i] = frames[0, 2, -1]
        y[i] = frames[1, 2, -1]

    # Save calculated path
    calculated_path = np.column_stack((x, y))
    np.save('calculated_path.npy', calculated_path)

    # Plot actual data
    plt.figure()
    plt.plot(x, y, 'k-', linewidth=1)
    plt.title('Plot of end effector position over a sample run.')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.axis('equal')
    d = 1 # Limit the range to +/- 1 meter by default
    plt.xlim([-d, d])
    plt.ylim([-d, d])

    # Plot and save ground truth
    if show_ground_truth:
        gt_x = log['ground_truth_x']
        gt_y = log['ground_truth_y']
        plt.plot(gt_x, gt_y, 'g--', linewidth=1)
        plt.legend(['Your Kinematics', 'Correct Kinematics'], loc='lower center')
        
        ground_truth_path = np.column_stack((gt_x.flatten(), gt_y.flatten()))
        np.save('ground_truth_path.npy', ground_truth_path)

    plt.show()

sample_path()