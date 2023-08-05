import os


def create(path):
    """
        If it is a path where a folder can be created, the folder is created up to the parent-path.
        If it is a path where a folder can be created, return True.
        - path : string
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except OSError:
        folders = path.split("/")
        if not folders:
            return False
        folders.pop()
        return create(folders.join("/"))


def remove(path):
    """
        If it is a path where a folder can be remove, the folder is remove down to the sub-path
        If it is a path where a folder can be remove, return True.
        - path : string
    """
    if not os.path.exists(path):
        return False
    if not os.path.isdir(path):
        os.remove(path)
        return True
    for file in os.listdir(path):
        remove(path + "/" + file)
    os.rmdir(path)
    return True


if __name__ == "__main__":
    def test(name, result):
        if result is False:
            raise Exception(name + ": Test Failed!")

    create_target = './create_new_folder/create_new_sub_folder'
    remove_target = './create_new_folder'
    test("create test1", create(create_target) is True)
    test("remove test1", remove(remove_target) is True)
    test("remove test2", remove(remove_target) is False)
    print("Test Pass!")
