from django.test import TestCase
from locations.models import State


class StateTestCase(TestCase):
    def setUp(self):
        pass

    def test_state_attributes(self):
        ro = State.objects.get(id=11)
        self.assertEqual(ro.id, 11)
        self.assertEqual(ro.code, "RO")
        self.assertEqual(ro.name, "Rondônia")
