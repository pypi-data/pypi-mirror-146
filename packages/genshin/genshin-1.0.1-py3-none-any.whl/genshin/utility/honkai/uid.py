"""Utility functions related to honkai."""
__all__ = ["recognize_honkai_server"]


def recognize_honkai_server(uid: int) -> str:
    """Recognizes which server a Honkai UID is from."""
    if 10000000 < uid < 100000000:
        return "overseas01"
    elif 100000000 < uid < 200000000:
        return "usa01"
    elif 200000000 < uid < 300000000:
        return "eur01"

    # From what I can tell, CN UIDs are all over the place,
    # seemingly even overlapping with overseas UIDs...
    # Probably gonna need some input from actual CN players here, but I know none.
    # It could be that e.g. global range is 2e8 ~ 2.5e8
    raise ValueError(f"UID {uid} isn't associated with any server")
