l520i00   st = []
size = int(input("Enter the size of the list: "))
print("Enter the numbers")
for i in range(size):
    input_number = int(input())
    list.append(input_number)
final_list=[]
for i in list:
    if i not in final_list:
        final_list.append(i)
print(f"List after removing duplicates: {final_list}")