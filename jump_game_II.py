class Solution:
    def jump(self, nums: List[int]) -> int:

        if len(nums) <= 1:
            return 0
        left,remainder = 0, nums[0]
        jump = 1
        while remainder < len(nums) - 1:
            jump += 1
            # left = remainder
            tmp = max(i + nums[i] for i in range(left, remainder+1))
            left, remainder = remainder, tmp
        return jump
