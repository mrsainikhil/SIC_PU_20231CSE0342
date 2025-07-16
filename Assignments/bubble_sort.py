def bubble_sort(array):
    for i in range(0, len(array)-1):
        sorted = True
        for j in range(1, len(array)-1-i):
            if array[j] > array[j + 1]:
                temp = array[j]
                array[j] = array[j+1]
                array[j+1] = temp
                sorted = False
        if sorted:
            break
    return array

array1 = [1,34,656,234,23,5436,56,234]
print(bubble_sort(array1))