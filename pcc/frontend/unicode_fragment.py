from unicodeitplus import replace

class UnicodeFragment:

    def __init__(self, source: str):
        self._ascii: str = source

    @property
    def ascii(self) -> str:
        return self._ascii

    @property
    def transformed(self) -> str:
        return replace(self._ascii)

    def __str__(self):
        return f"UnicodeFragment(\"{self._ascii}\")"

    def __eq__(self, other):
        if isinstance(other, UnicodeFragment):
            return self._ascii == other._ascii
        if isinstance(other, str):
            return self._ascii == other
        raise ValueError(f"Incompatible comparison of types UnicodeFragment and {type(other)}")

def split_unicode_fragments(s: str) -> list[str | UnicodeFragment]:
    split: list[str | UnicodeFragment] = []
    curr: str = ""
    is_ascii = True
    for character in s:
        if character == "$":
            # add curr to split
            # if currently in unicode mode, append as unicode fragment
            if is_ascii:
                split.append(curr)
            else:
                split.append(UnicodeFragment(curr))
            curr = ""
            is_ascii = not is_ascii
        else:
            curr += character
    if curr != "":
        split.append(curr)
    return split
