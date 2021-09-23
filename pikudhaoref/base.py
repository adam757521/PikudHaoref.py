from typing import Callable


class EventManager:
    """
    An event manager that manages and calls events.
    """

    __slots__ = ("events",)

    def __init__(self):
        self.events = {}

    def call_sync_event(self, name: str, *args, **kwargs) -> None:
        """
        Calls the event name with the arguments

        :param name: The event name.
        :type name: str
        :param args: The arguments.
        :param kwargs: The key arguments.
        :return: None
        :rtype: None
        """

        if name in self.events:
            for event in self.events[name]:
                event(*args, **kwargs)

    async def call_async_event(self, name: str, *args, **kwargs) -> None:
        if name in self.events:
            for event in self.events[name]:
                await event(*args, **kwargs)

    def event(self, name=None) -> Callable:
        """
        A decorator which adds an event listener.

        :param name: The event name.
        :type name: str
        :return: The inner function.
        :rtype: Callable
        """

        def inner(func):
            self.add_event(func, name)
            return func

        return inner

    def add_event(self, func, name=None) -> None:
        """
        Adds an event to the event dictionary.

        :param func: The event callback.
        :type func: Callable
        :param name: The event name.
        :type name: str
        :return: None
        :rtype: None
        :raises: TypeError: The listener isn't async, The listener isn't sync.
        """

        name = func.__name__ if not name else name

        if name in self.events:
            self.events[name].append(func)
        else:
            self.events[name] = [func]

    def remove_event(self, func: Callable, name: str = None) -> None:
        """
        Removes an event from the event dictionary.

        :param func: The event callback.
        :type func: Callable
        :param name: The event name.
        :type name: str
        :return: None
        :rtype: None
        """

        name = func.__name__ if not name else name

        if name in self.events:
            self.events[name].remove(func)
