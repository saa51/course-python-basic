# from collections import Counter
def my_counter(string: str) -> dict:
    ret = dict()
    for ch in string:
        ret[ch] = ret.get(ch, 0) + 1
    return ret


def IsAnagram(s: str, t: str) -> bool:
    return my_counter(s) == my_counter(t)


if __name__ == '__main__':
    s = input('String s: ')
    t = input('String t: ')
    print(IsAnagram(s, t))
