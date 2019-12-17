def split_elem(container, index, delim=" "):
    elem1, elem2 = container[index].split(delim)
    container[index] = elem2
    container.insert(index, elem1)

