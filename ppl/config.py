disable_library_value = False


def disable_library():
    global disable_library_value
    disable_library_value = True


def get_status():
    return disable_library_value
