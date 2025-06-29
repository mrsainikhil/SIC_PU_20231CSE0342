list = [2,46,7547,24,75683,1,-13,5434]
max = list[0]
min = list[0]
for i in list:
    if i > max:
        max = i
    if i < min:
        min=i
print(f"Samllest number in the list is: {min}")
print(f"Biggest number in the list is: {max}")