class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        m = {}; # value : index

        for i, n in enumerate(nums):
            diff = target - n
            #print( diff)
            if diff in m:
                return [m[diff], i]
            m[n] = i
            #print(m[n])
        return
