# --- binary search through the list ---
def binary_search(lst, target):
    """Performs a binary search on a sorted list of students or teachers."""
    left, right = 0, len(lst) - 1
    while left <= right:
        mid = (left + right) // 2
        if lst[mid]['id'] == target:
            return mid
        elif lst[mid]['id'] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None


# --- merge sort through the list ---
def merge(lst1, lst2, order):
    """
    Sub-function to sort two lists into one. 
    """
    new_lst = []

    i, j = 0, 0
    while i < len(lst1) and j < len(lst2):
        if order == "ascending":
            if lst1[i]['id'] < lst2[j]['id']:                   # ascending order
                new_lst.append(lst1[i])
                i += 1
            else:
                new_lst.append(lst2[j])
                j += 1
        else:                                                   # descending order
            if lst1[i]['id'] > lst2[j]['id']:
                new_lst.append(lst1[i])
                i += 1
            else:
                new_lst.append(lst2[j])
                j += 1

    if i < len(lst1):                                           # any remaining elements in list1 or list2.
        new_lst += lst1[i:]
    elif j < len(lst2):
        new_lst += lst2[j:]

    return new_lst 

def merge_sort(lst, order = "ascending"):
    """
    Helper function to recursively separate list for further sorting.
    :complexity
        Best-case = Worst-case = O(nlogn)
        :n is the number of elements inside the list.
    """
    if len(lst) > 1:
        mid = len(lst) // 2

        # divide the list into left and right part
        lst1 = merge_sort(lst[mid:])
        lst2 = merge_sort(lst[:mid])

        return merge(lst1, lst2, order)
    elif len(lst) == 1:
        return lst
    else:
        print("There's nothing in the list. ")
        return lst