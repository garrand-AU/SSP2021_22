class Solution:
    def romanToInt(self, s: str) -> int:
        sum = 0
        s = s.replace("IV", "IIII").replace("IX", "VIIII")
        s = s.replace("XL", "XXXX").replace("XC", "LXXXX")
        s = s.replace("CD", "CCCC").replace("CM", "DCCCC")

        for e in s:

            if e == "I":
                sum += 1
            if e == "V":
                sum += 5
            if e == "X":
                sum += 10
            if e == "L":
                sum += 50
            if e == "C":
                sum += 100
            if e == "D":
                sum += 500
            if e == "M":
                sum += 1000
        return sum
