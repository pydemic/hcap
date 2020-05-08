def trans_property(trans):
    def inner(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        wrapper.short_description = trans
        return wrapper

    return inner
