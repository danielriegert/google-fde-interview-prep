# LC 7: Reverse Integer
class Solution:
    """
    Conceptually interger can be reversed similar to string.
    We pop last character / digit off the end and append it at the end 
    of the reversed integer / string

    Time Complexity: O(log10(x)), as the number of iterations equals the number of digits in x.
    Space Complexity: O(1), 
    """
    def reverse(self, x: int) -> int:
        rev = 0
        sign = -1 if x < 0 else 1
        x = abs(x)

        while x != 0:
            # Pop last digit
            mod = x % 10
            x //= 10
            
            # Push
            rev = rev * 10 + mod

            # Check for overflow
            if rev > 2**31 - 1:
                return 0
            
        return sign * rev

