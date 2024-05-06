def dp_solver(weights_array, values_array, max_weight):
    count_items = len(weights_array)
    A = [[0 for _ in range(max_weight + 1)] for _ in range(count_items + 1)]
    for k in range(1, count_items + 1):
        for s in range(1, max_weight + 1):
            if s >= weights_array[k - 1]:
                A[k][s] = max(A[k - 1][s], A[k - 1][s - weights_array[k - 1]] + values_array[k - 1])
            else:
                A[k][s] = A[k - 1][s]
    return A[count_items][max_weight]