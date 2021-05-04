from django.test import TestCase
from dashboard.forms import DesignationForm, LoginForm

# Designation Form Test
class TestDesignationForms(TestCase):

    def test_designation_form_valid_data(self):

        form = DesignationForm(data={
            'name': 'Luis Suarez',
            'position': 'Striker',
            'gender' : 'MALE',
            'date_of_birth' : '2021-01-12'
        })

        self.assertTrue(form.is_valid())


    def test_designation_form_invalid_data(self):

        form = DesignationForm(data={})

        self.assertFalse(form.is_valid())



