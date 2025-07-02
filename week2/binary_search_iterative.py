def binary_search(sorted_list, left, right, target):
    while left <= right:
        mid = (left + right)//2
        if sorted_list[mid] > target:
            right = mid - 1
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            return mid

list1 = [1,2,4,5,6,8,34,56,786,8798]
right = len(list1)-1
print(binary_search(list1,0,right,56))