class model_property(property):
    short_description = None

    def __init__(self, *args, short_description=None, **kwargs):
        super().__init__(*args, **kwargs)
        if short_description is not None:
            self.short_description = short_description

    def __call__(self, fn):
        def wrapped_fn(*args, **kwargs):
            return fn(*args, **kwargs)

        if self.short_description is not None:
            wrapped_fn.short_description = self.short_description

        return wrapped_fn
