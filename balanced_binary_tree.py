# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:

        balanced = True

        def dfs(node, balanced):

            if not node:
                return 0, True
            l, lb = dfs(node.left, balanced)
            r, rb = dfs(node.right,balanced)
            # print(l, r)
            # print(abs(l-r))
            if abs(l-r) > 1:
                # print("here")
                balanced = False
            # print("balanced = ", balanced)
            balanced = lb and rb and balanced
            return max(l, r) + 1, balanced

        h, balanced = dfs(root, balanced)
        # dfs(root.left)
        # dfs(root.right)

        return balanced

#         if not root:
#             return True

#         return abs(self.getHeight(root.left) - self.getHeight(root.right)) < 2 and self.isBalanced(root.left) and self.isBalanced(root.right)

#     def getHeight(self, root):
#         if not root:
#             return 0

#         return 1 + max(self.getHeight(root.left), self.getHeight(root.right))

         # self.Bal = True

#         def dfs(node):
#             if not node: return 0
#             lft, rgh = dfs(node.left), dfs(node.right)
#             if abs(lft - rgh) > 1: self.Bal = False
#             return max(lft, rgh) + 1

#         dfs(root)
#         return self.Bal
