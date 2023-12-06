def MySqrt(x: int) -> int:
    assert x >= 0, "Cannot take square root of negative numbers"
    if x == 0:
        return 0
    z = x
    z_o = 0
    while abs(z_o - z) >  0.1:
        z_o = z
        z = (z_o + x / z_o) / 2
    z = int(z)
    while True:
        if z * z <= x:
            return z
        z -= 1

if __name__ == '__main__':
    x = int(input('Input an integer x: '))
    print(f"The square root of {x} is {MySqrt(x)}")
