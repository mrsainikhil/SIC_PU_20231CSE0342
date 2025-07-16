list = []
size = int(input("Enter the size of list: "))
for i in range(size):
    input_number = int(input())
    list.append(input_number)
number = int(input("Enter the number to find frequency: "))
frequency=0
for i in list:
    if i == number:
        frequency+=1
print(f"Frequency of {number} is {frequency}")