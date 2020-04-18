from django.test import TestCase

from hcap_geo.models import Region


class TestRegion(TestCase):
    def test_basic_creation(self):
        region = Region(code="11", kind=Region.KIND_STATE, name="Rondônia", abbr="RO")
        region.full_clean()
        region.save()
