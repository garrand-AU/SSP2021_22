class Solution:
    def strStr(self, haystack: str, needle: str) -> int:

        # lh = len(haystack)
        ln = len(needle)

        if ln == 0:
            return 0
        return haystack.find(needle)

#         if lh < ln:
#             return -1

#         for i in range(lh - ln + 1):
#             if haystack[i] == needle[0]:
#                 # print(haystack[i])
#                 # print(haystack[i:ln])
#                 if haystack[i:(i+ln)] == needle[0:ln]:
#                     return i
#         return -1
