class Solution:
    def reverse(self, x: int) -> int:
        sign = [1,-1][x < 0]
        x = sign * int(str(abs(x))[::-1])

        return x if -(2**31) < x < 2**31 -1 else 0
