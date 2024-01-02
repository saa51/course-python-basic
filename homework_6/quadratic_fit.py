import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def quadratic_func(x, w):
    return np.vstack((np.ones(x.shape), x, x * x)).T @ w

def quadratic_grad(x, y, w):
    basis = np.vstack((np.ones(x.shape), x, x * x)).T
    return np.average((basis @ w - y).T * basis.T, axis=1) * 2

if __name__ == '__main__':
    sample_size = 100
    lr = 0.01
    iter_num = 1000
    w = np.zeros(3)
    w_true = np.array([2, 1, 1])
    x = np.random.normal(0, 1, sample_size)
    y = quadratic_func(x, w_true) + np.random.normal(0, 0.1, sample_size)
    for iter in tqdm(range(iter_num)):
        grad = quadratic_grad(x, y, w)
        w = w - lr * grad

    grid = np.linspace(np.min(x), np.max(x), 100)
    plt.scatter(x, y, label='sample point')
    plt.plot(grid, quadratic_func(grid, w_true), label='true function')
    plt.plot(grid, quadratic_func(grid, w), label='estimation')
    plt.legend()
    plt.savefig('./figures/quadratic_fit.png')
    plt.show()
