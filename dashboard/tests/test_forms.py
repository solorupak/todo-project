from django.test import TestCase
from django.contrib.auth.models import User

from dashboard.forms import DesignationForm, LoginForm


# Login Form Test  
class TestLoginForms(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('prixa','ramesh@gmail.com', 'prixa123')

   
    def test_login_with_all_data(self):

        form = LoginForm(data={
            'username': 'prixa',
            'password': 'prixa123',
        })
        self.assertTrue(form.is_valid())
    
    def test_login_without_any_data(self):

        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
    
    def test_login_without_username(self):

        form = LoginForm(data={
            'password': 'pranish123'
        })
        self.assertFalse(form.is_valid())
    
    def test_login_without_password(self):

        form = LoginForm(data={
            'username': 'pranish',
        })
        self.assertFalse(form.is_valid())

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



