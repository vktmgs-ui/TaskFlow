def insertion_sort(items, key=lambda x: x):
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1

        while j >= 0 and key(items[j]) > key(current):
            items[j + 1] = items[j]
            j -= 1

        items[j + 1] = current

    return items


def binary_search(items, target, key=lambda x: x):
    left = 0
    right = len(items) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_value = key(items[mid])

        if mid_value == target:
            return items[mid]

        if mid_value < target:
            left = mid + 1
        else:
            right = mid - 1

    return None


def linear_search(items, target, key=lambda x: x):
    for item in items:
        if key(item) == target:
            return item

    return None