def dp_solver(data):
    count_items = data["num_items"]
    max_weight = data["max_weight"]
    A = [[0 for _ in range(max_weight + 1)] for _ in range(count_items + 1)]
    for k in range(1, count_items + 1):
        for s in range(1, max_weight + 1):
            if s >= data["weights"][k - 1]:
                A[k][s] = max(A[k - 1][s], A[k - 1][s - data["weights"][k - 1]] + data["values"][k - 1])
            else:
                A[k][s] = A[k - 1][s]
    return A[count_items][max_weight]