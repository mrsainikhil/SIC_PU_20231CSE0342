def fib(n):
    if(n <=2):
        return n
    print(fib(n-1) + fib(n-2))
input_number=int(input("Enter the number to find the series: "))
print(f"Fibonacci series {fib(input_number)}")