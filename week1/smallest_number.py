print("Enter three numbers")
first_number = int(input())
second_number = int(input())
third_number = int(input())
if(first_number<second_number and first_number<third_number):
    print(first_number," is the smallest number")
elif(second_number<third_number and second_number<first_number):
    print(second_number," is the smallest number")
else:
    print(third_number," is the smallest number")