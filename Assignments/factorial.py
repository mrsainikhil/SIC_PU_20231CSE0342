def fact(n):
    if(n==1):
        return 1
    return n*fact(n-1)
input_number = int(input("Enter the number to find factorial: "))
print(f"Factorial of {input_number} is {fact(input_number)}")