def merge_recursive(arr, key):
    if len(arr) > 1:
        # Divide
        q = len(arr) // 2

        p = arr[:q]

        r = arr[q:]

        merge_recursive(p, key)

        merge_recursive(r, key)

        i, j, k = 0, 0, 0

        # Combine
        while i < len(p) and j < len(r):
            if p[i]['appid'] < r[j]['appid']:
                arr[k] = p[i]
                i += 1
            else:
                arr[k] = r[j]
                j += 1
            k += 1

        while i < len(p):
            arr[k] = p[i]
            i += 1
            k += 1
        while j < len(r):
            arr[k] = r[j]
            j += 1
            k += 1
    return arr

# FIX THIS!
def binary_recursive(arr, appid):
    q = len(arr) // 2
    selected = arr[q]['appid']
    print(arr[q]['appid'])
    if len(arr) == 1:
        return True if int(selected) == int(appid) else False
    elif int(selected) == int(appid):
        return True
    else:
        if int(selected) < int(appid):
            return binary_recursive((arr[q:]), appid)
        else:
            return binary_recursive((arr[:q]), appid)
