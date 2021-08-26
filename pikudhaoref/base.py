class EventManager:
    def __init__(self):
        self.events = {}

    def call_event(self, name, *args, **kwargs):
        if name in self.events:
            for event in self.events[name]:
                event(*args, **kwargs)

    def event(self, name=None):
        def inner(func):
            self.add_event(func, name)
            return func

        return inner

    def add_event(self, func, name=None):
        name = func.__name__ if not name else name

        if name in self.events:
            self.events[name].append(func)
        else:
            self.events[name] = [func]

    def remove_event(self, func, name=None):
        name = func.__name__ if not name else name

        if name in self.events:
            self.events[name].remove(func)