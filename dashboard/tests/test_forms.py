# from django.test import SimpleTestCase
# from dashboard.forms import DesignationForm, LoginForm

# # Designation Form Test
# class TestDesignationForms(TestCase):

#     def test_designation_form_valid_data(self):

#         form = DesignationForm(data={
#             'name': 'Luis Suarez',
#             'position': 'Striker',
#             'gender' : 'MALE',
#             'date_of_birth' : '2021-01-12'
#         })

#         self.assertTrue(form.is_valid())


#     def test_designation_form_invalid_data(self):

#         form = DesignationForm(data={})

#         self.assertFalse(form.is_valid())

# # Login Form Test  
# class TestLoginForms(TestCase):
   
#     def test_login_with_all_data(self):

#         form = LoginForm(data={
#             'username': 'prixa',
#             'password': 'prixa123'
#         })

#         self.assertTrue(form.is_valid())
    
#     def test_login_without_any_data(self):

#         form = LoginForm(data={})
#         self.assertFalse(form.is_valid())
    
#     def test_login_without_username(self):

#         form = LoginForm(data={
#             'password': 'prixa123'
#         })
#         self.assertFalse(form.is_valid())
    
#     def test_login_without_password(self):

#         form = LoginForm(data={
#             'username': 'prixa',
#         })
#         self.assertFalse(form.is_valid())




