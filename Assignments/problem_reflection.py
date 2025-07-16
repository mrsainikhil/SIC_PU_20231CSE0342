def is_same_reflection(word1, word2):
    temp_str = word2 * 2
    ans = temp_str.find(word1)
    if ans == -1 :
        return False
    else:
        return True

original_str = input("Enter the original String: ")
rotated_str = input("Enter the rotated String: ")
if(is_same_reflection(original_str,rotated_str)):
    print("Both strings are rotations of each other")
else:
    print("Both strings are not rotations of each other")