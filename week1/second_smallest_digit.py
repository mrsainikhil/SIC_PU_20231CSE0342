input_number = int(input("Enter the number : "))
second_smallest_digit = 10
smallest_digit = 10
while(input_number != 0):
    if input_number % 10 <smallest_digit:
        second_smallest_digit = smallest_digit
        smallest_digit = input_number % 10
    elif input_number % 10 < second_smallest_digit and input_number % 10 >= smallest_digit:
        second_smallest_digit = input_number %10
    input_number = input_number //10
print(f"Second smallest digit in the given number is : {second_smallest_digit}")