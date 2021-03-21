import typing


class Store:
    def __init__(self):
        self._namespaces = {}

    def initializer(self):
        pass

    def subscribe(self, ns: typing.Union[str, list]) -> None:
        """docstring for subscribe"""

    def add_reducer(self):
        pass

    def add_reducers(self):
        pass

    def remove_reducer(self):
        pass

    def remove_reducers(self):
        pass
