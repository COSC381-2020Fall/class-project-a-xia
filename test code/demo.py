import sys

def find_min(arr):
    if arr is None:
        print('fatal error: input array should not be none', file=sys.stderr)
        return
    
    if not arr:
        return None

    min_num = arr[0]
    
    for num in arr:
        if num < min_num:
            min_num = num
    
    return min_num

def helper():
    print('find_min(arr): function to find minimum number in array')