class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
            # strsdict = dict.fromkeys(strs, "")
#             count = 0
#             ml = 0
# #             compare charaters in each strings
#             ls = len(strs)
#             for index in range(ls):
#                 for i in range(strs[index]):
#                     for j in range(ls):
#                         if strs[index][i] == strs[j][i]:
#                             count = i
#             return count
#             count the same charaters length
#              find the max count
            if not strs:
                return ''

            lm = 0
            shortest = min(strs, key = len)
            for index in range(len(shortest)):
                for s in strs:
                    if shortest[index] != s[index]:
                        return shortest[:index]
#
            return shortest
