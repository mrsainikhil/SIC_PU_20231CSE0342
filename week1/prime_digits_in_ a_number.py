prime_digits = [2,3,5,7]
input_number = input("Enter the number : ")
count = 0
for i in input_number:
    if int(i) in prime_digits:
        count += 1
print(f"Number of prime digits in given number are {count}")