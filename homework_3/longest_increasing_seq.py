import numpy as np


def longest_increasing_seq(a: list):
    a = np.array(a)
    dp = np.zeros(len(a), dtype=int)
    dp[0] = 1
    for idx, x in enumerate(a[1:]):
        dp[idx + 1] = np.max(dp[(a < x) & (np.arange(len(a)) < idx + 1)], initial=0) + 1
    return np.max(dp)

if __name__ == '__main__':
    test_arrs = [
        [10, 9, 2, 5, 3, 7, 101, 18],
        [0, 1, 0, 3, 2, 3], 
        [2, 2, 2],
    ]
    for test_arr in test_arrs:
        print(longest_increasing_seq(test_arr))

        