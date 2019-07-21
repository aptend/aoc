
def license_from_file():
    with open('../inputs.txt') as f:
        return [int(x) for x in f.read().strip().split()]


def read_node_meta(license, total_meta):
    n_child, n_meta, *left_license = license
    for _ in range(n_child):
        left_license = read_node_meta(left_license, total_meta)
    total_meta.extend(left_license[:n_meta])
    return left_license[n_meta:]


def meta_sum(license):
    """
    >>> meta_sum([int(x) for x in "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split()])
    138
    """
    total_meta = []
    read_node_meta(license, total_meta)
    return sum(total_meta)


def value_of_root(license):
    """
    >>> value_of_root([int(x) for x in "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split()])
    (66, [])
    """
    n_child, n_meta, *left_license = license
    child_values = []
    for _ in range(n_child):
        value, left_license = value_of_root(left_license)
        child_values.append(value)
    v = 0
    if child_values:
        for m in left_license[:n_meta]:
            if 0 < m <= len(child_values):
                v += child_values[m-1]
    else:
        v = sum(left_license[:n_meta])
    return v, left_license[n_meta:]


license = license_from_file()

print(meta_sum(license))
print(value_of_root(license))
