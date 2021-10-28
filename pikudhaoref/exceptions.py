__all__ = ("AccessDenied",)


class AccessDenied(Exception):
    """
    Raised when the user tries to access the pikudhaoref API from outside of Israel.
    """