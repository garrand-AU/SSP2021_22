class Solution:
    def intToRoman(self, num: int) -> str:
#         result = ""

#         q, num = divmod(num, 1000)
#         result += "M"*q


#         q,num = divmod(num, 900)
#         if q == 1:
#             result += "CM"

#         q, num = divmod(num, 500)
#         if q == 1:
#             result += "D"

#         q, num = divmod(num, 400)
#         if q == 1:
#             result += "CD"


#         q, num = divmod(num, 100)
#         result += "C"*q

#         q, num = divmod(num, 90)
#         if q == 1:
#             result += "XC"


#         q, num = divmod(num, 50)
#         if q == 1:
#             result += "L"


#         q, num = divmod(num, 40)
#         if q == 1:
#             result += "XL"


#         q, num = divmod(num, 10)
#         result += "X"*q


#         q, num = divmod(num, 9)
#         if q == 1:
#             result += "IX"

#         q, num = divmod(num, 5)
#         if q == 1:
#             result += "V"

#         q, num = divmod(num, 4)
#         if q == 1:
#             result += "IV"

#         q, num = divmod(num, 1)

#         result += "I"*q

#         return result
        d = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}

        res = ""

        for i in d:
            res += (num//i) * d[i]
            num %= i

        return res
