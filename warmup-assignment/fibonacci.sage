#### fibonacci.sage : Prints the first eleven Fibonacci numbers
#### Author: <Your Name Here>
#### Date: <Today's Date>

## Fibonacci : Computes the nth Fibonacci number
 # @param n: Natural number n >= 0
 # @return:  The nth Fibonacci number
## 
def Fibonacci(n):
     if n <= 0:
          return 0
     elif n == 1:
          return 1
     fibNumbers = [0, 1]
     for n in range(2, n + 1):
          fibNum = fibNumbers[n - 1] + fibNumbers[n - 2]
          fibNumbers += [fibNum]
     ##
     return fibNumbers[n]
##
 
## Print the first 11 Fibonacci numbers in the specified format: 
print "The First Fibonacci Numbers:"
for n in range(0, 12):
     print "   >> Fib(%2d) = %d" % (n, Fibonacci(n))
##

