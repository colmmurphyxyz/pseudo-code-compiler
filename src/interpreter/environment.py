from __future__ import annotations

class Environment:
    _enclosing: Environment
    _values: dict[str, any]

    def __init__(self, enclosing_environment: Environment | None = None):
        self._values = {}
        self._enclosing = enclosing_environment

    def _assign(self, name: str, value: any) -> bool:
        """
        Assign a new value to a variable with the narrowest scope possible
        If no variable with the given name can be found, no assignment will be done
        :param name: Variable name to assign a value to
        :param value: Value for the given variable
        :return: True, if a value was assigned to an existing variable,
            False if no variable is found with the given name
        """
        if name in self._values:
            self._values[name] = value
            return True
        if self._enclosing is not None:
            return self._enclosing._assign(name, value)
        return False

    def define(self, name: str, value: any) -> None:
        if not self._assign(name, value):
            self._values[name] = value


    def get(self, name: str) -> any:
        if name not in self._values:
            raise ValueError("Undeclared variable", name)
        if self._enclosing is not None:
            return self._enclosing.get(name)
        return self._values.get(name)
