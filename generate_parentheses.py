class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        # put the paremthese in middle of previous parethese

        # put the paremthese at the left of previous parethese


        # put the paremthese at the right of previous parethese

        # This is the n-th Catalan number, where the first Catalan numbers for n = 0, 1, 2, 3, ... are 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786,...
        # Time & Space: n-th Catalan Number.

        def generate(p, left, right, results=[]):
            if left:         generate(p + '(', left-1, right)
            if right > left: generate(p + ')', left, right-1)
            if not right:    results += p,
            return results

        return generate('', n, n)
