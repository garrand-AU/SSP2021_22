class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        # loop all elements in candidates

        # use division to get the repeat number unlimited number of times

        # use % to get the remainder after division

        # use reduction to get the rest

        # for each elements, add other element to reach target

        result = []
        self.dfs(candidates, target,[], result)
        return result
        # for i in range(len(candidates)):
        #     q , r = divmod(target, candidates[i])
        #     if r == 0:
        #         for i in range(q):
        #             tmp.append(candidates[i])
        #         result.append(tmp)
        #     else if q > 0:
        #         rest = target - q * e
        #         for j in range(len(candidates) - i):
        #             q, r = divmode(rest, candodates[i+j])

        # def comSum(candidates, target):
        #     if target == 0:
        #         return
        #     if len(candidates) == 1:
        #         if target < candidates[0]:
        #             return
        #     for i


    def dfs(self, nums, target, path, res):
        if target < 0:
            return
        if target == 0:
            res.append(path)
            return
        for i in range(len(nums)):
            self.dfs(nums[i:], target - nums[i], path+[nums[i]], res)



                
