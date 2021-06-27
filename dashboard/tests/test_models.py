
from model_bakery import baker
from pprint import pprint

from django.test import TestCase, Client

from dashboard.models import Designation

# Designation Model Test
class TestDesignationModel(TestCase):

    def setUp(self):
        self.designation = baker.make(Designation)
        pprint(self.designation.__dict__)
    
    def test_if_designation_is_created(self):
        designation = Designation.objects.all().first()
        self.assertEquals(self.designation.pk, designation.pk)

    
    
    
    



        