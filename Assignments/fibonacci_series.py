input_number = int(input("Enter the number to find fibonacci series :"))
fib_1 = 1
fib_2 = 2
print("fibonacci series : ",end="")
for i in range(1, input_number+1):
    if(i==1):
        print(1,end=" ")
    elif(i==2):
        print(2,end=" ")
    else:
        fibo_next = fib_1 + fib_2
        fib_1 = fib_2
        fib_2 = fibo_next
        print(fibo_next,end=" ")