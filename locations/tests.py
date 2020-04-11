from django.test import TestCase

from locations import fake
from locations.models import State


class TestStates(TestCase):
    def setUp(self):
        pass

    def test_state_attributes(self):
        ro = State.objects.get(id=11)
        self.assertEqual(ro.id, 11)
        self.assertEqual(ro.code, "RO")
        self.assertEqual(ro.name, "Rondônia")


class TestFakers(TestCase):
    def test_fetch_list_of_states_and_cities(self):
        states = {
            "MS",
            "RS",
            "SE",
            "PI",
            "TO",
            "MA",
            "AM",
            "MT",
            "DF",
            "RR",
            "PR",
            "SP",
            "AC",
            "AP",
            "RO",
            "PB",
            "MG",
            "GO",
            "ES",
            "CE",
            "RJ",
            "SC",
            "PE",
            "RN",
            "PA",
            "AL",
            "BA",
        }
        self.assertEqual({s.code for s in fake.states()}, states)

    def test_fetch_cities_filtered(self):
        state = fake.normalize_state("AC")
        for city in fake.cities("AC"):
            self.assertEqual(city.state, state)
