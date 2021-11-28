class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        # put the paremthese in middle of previous parethese

        # put the paremthese at the left of previous parethese


        # put the paremthese at the right of previous parethese



        def generate(p, left, right, results=[]):
            if left:         generate(p + '(', left-1, right)
            if right > left: generate(p + ')', left, right-1)
            if not right:    results += p,
            return results

        return generate('', n, n)
