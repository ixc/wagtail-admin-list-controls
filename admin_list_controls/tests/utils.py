from django.test import TestCase


class BaseTestCase(TestCase):
    def assertObjectSerializesTo(self, obj, subset):
        serialized = obj.serialize()
        self.assertDictContainsSubset(subset, serialized)