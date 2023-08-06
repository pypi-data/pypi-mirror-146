class A:
    def __init__(self, zk):
        self._zk = zk

    def __getattr__(self, item):
        return getattr(self._zk, item)


a = A([1, 2, 3])

a.append(4)

print(a._zk)
