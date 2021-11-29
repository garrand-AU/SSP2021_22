class Solution:
    def trap(self, height: List[int]) -> int:

        if not height or len(height) < 3:
            return 0

        volumn = 0

        left, right = 0, len(height) - 1
        l_max, r_max = height[left], height[right]
        # print(l_max)
        # print(r_max)
        while left < right:
            l_max, r_max = max(height[left], l_max), max(height[right], r_max)
            # print(l_max)
            # print(r_max)
            if l_max <= r_max:
                volumn += l_max - height[left]
                left += 1
            else:
                volumn += r_max - height[right]
                right -=1
        return volumn
#         def cal_vol(height, left, right):
#             h = height[right] - height[left]
#             vol = 0
#             for x in range(left,right):
#                 vol += h * (height[left]-height[x])
#             return vol

#         highest = max(height)
#         index = height.index(highest)
#         # print("highest:", highest)
#         # print("index: ", index)

#         ind = 0
#         length = len(height)

#         # remove the zeros in head of height
#         while height[ind] == 0 and length > 1:
#             if height[ind] == 0:
#                 height = height[1:]
#                 length -=1
#         if length == 1:
#             return 0
#         volumn = 0
#         for i in range(len(height)):
#             for j in range(len(height)):
#                 if (height[i] - height[j]) <= 0:
#                     volumn += cal_vol(height, i, j)
#             i = j
#         return volumn




            
