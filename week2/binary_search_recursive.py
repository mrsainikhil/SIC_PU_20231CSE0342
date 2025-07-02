def binary_search(sorted_list,left,right,target):
    if left > right:
        return "Not Found"
    mid = (left + right) // 2
    if sorted_list[mid] == target:
        return mid
    elif sorted_list[mid] > target:
        right = mid - 1 
    else:
        left = mid + 1 
    return binary_search(sorted_list,left,right,target)

list1 = [1,2,3,5,67,143,786,6577,89899]
print(binary_search(list1,0,len(list1),786))