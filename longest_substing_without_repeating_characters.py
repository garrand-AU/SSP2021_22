class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:

        # check elements one by one
        used = {}
        max_length = start = 0
        for i, c in enumerate(s):
            print(i, c)
            if c in used and start <= used[c]:
                start = used[c] + 1
            else:
                max_length = max(max_length, i - start + 1)

            used[c] = i


        return max_length


        # if different, add to list

        # complexity is O(N)
