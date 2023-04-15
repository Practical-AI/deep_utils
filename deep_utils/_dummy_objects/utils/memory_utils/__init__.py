from deep_utils._dummy_objects.dummy_framework import DummyObject, requires_backends


class MemoryUtilsTorch(metaclass=DummyObject):
    _backend = ["torch"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, self._backend)