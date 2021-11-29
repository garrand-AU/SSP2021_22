class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:

        carry = 1
        l = len(digits) -1
        print(l)
        # res = [None for _ in range(l+1)]
        tmp = 0
        for i in range(l + 1):
            if carry:
                tmp = digits[l-i] + carry
                carry = 0
            else:
                tmp = digits[l-i]

            if tmp == 10:
                carry = 1
                digits[l-i] = 0
            else:
                digits[l-i] = tmp
        if carry:
            digits.insert(0, carry)
        return digits
