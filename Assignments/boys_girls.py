queries = int(input("Enter number of queries: "))
for i in range(queries):
    size = int(input("Enter no of students: "))
    boys = []
    girls = []
    for i in range(size):
        input_num = int(input())
        boys.append(input_num)
    for i in range(size):
        input_num = int(input())
        girls.append(input_num)
    boys.sort()
    girls.sort()
    arranged_list =[]
    for i in range(size):
        if boys[0] > girls [0]:
            arranged_list.append(girls[i])
            arranged_list.append(boys[i])
        else:
            arranged_list.append(boys[i])
            arranged_list.append(girls[i])
    sorted_list = boys + girls
    sorted_list.sort()
    if sorted_list == arranged_list:
        print("YES")
    else:
        print("NO")