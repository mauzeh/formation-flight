if __name__ == '__main__':

    object1 = object()
    object2 = object()
    my_list = [object1, object2]

    print my_list

    del object1

    print my_list