start_of_range = int(input("Enter start of the range : "))
end_of_range = int(input("Enter end of the range : "))
prime=[]
for i in range(end_of_range - 1, start_of_range, -1):
    check = True
    if(i % 2==0):
        continue
    for j in range(3,i//2):
        if(i % j==0):
            check =False
    if check:
        prime.append(i)
print(prime)
