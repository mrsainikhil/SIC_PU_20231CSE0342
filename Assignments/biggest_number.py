input_number = int(input("Enter the number: "))
max = 0
while(input_number > 0):
    if(input_number % 10 > max):
        max = input_number % 10
    input_number /= 10
print(f"Biggest digit in given number is {max}")