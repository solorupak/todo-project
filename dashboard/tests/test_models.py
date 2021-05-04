
from django.test import TestCase, Client

from dashboard.models import Designation


# Designation Model Test
class TestDesignationModel(TestCase):

    def setUp(self):

        self.designation = Designation.objects.create(
            name = 'Luis Suarez',
            position = 'Striker',
            gender = 'MALE',
            date_of_birth = '2020-01-12'
        )
    
    def test_if_designation_is_created(self):
        designation = Designation.objects.all().first()
        self.assertEquals(self.designation.pk, designation.pk)


    
    
    
    



        