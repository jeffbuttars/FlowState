from ..store import Store


class Source:
    def start(self, store: Store):
        self.store = store

    def stop(self):
        pass

    def run(self):
        pass


class AsyncSource:
    async def start(self, store: Store):
        self.store = store

    async def stop(self):
        pass

    async def run(self):
        pass
