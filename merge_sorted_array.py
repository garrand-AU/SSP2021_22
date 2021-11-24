class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # print(nums1[:m])

        newlist = nums1[:m]+nums2
        newlist.sort()
        # print(nums1)
        for i in range(len(newlist)):
            nums1[i] = newlist[i]
