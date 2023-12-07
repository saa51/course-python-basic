import numpy as np
from math import comb

def unique_path(m: int, n: int):
    dp = np.zeros((m, n), dtype=int)
    dp[0] = 1
    dp[:, 0] = 1
    for i in range(1, m):
        for j in range(1, n):    
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    assert dp[-1][-1] == comb(m + n - 2, m - 1)
    return dp[-1][-1]

if __name__ == '__main__':
    m = int(input('input m: '))
    n = int(input('input n: '))
    print(f'The number of unique path: {unique_path(m, n)}')
