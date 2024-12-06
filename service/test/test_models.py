from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.db.utils import IntegrityError

from service.models import Customer

from django.utils import timezone

# Create your tests here.


class TestUserModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser',email='testuser@mailinator.com',password='testpassword')
        
    def test_create_user(self):
        
        user = User.objects.get(id=1)
        
        self.assertEqual(user.username,'testuser','username not same')
        self.assertEqual(user.email,'testuser@mailinator.com','mail not same')
        self.assertTrue(user.check_password('testpassword'))
        
    def test_string_representation(self):
        
        self.assertEqual(str(self.user),'testuser')
        
    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            user=User.objects.create_user(username='testuser12',email='invalid-email',password='testpassword')
            user.full_clean()
            
    def test_duplicate_username(self):
        
        with self.assertRaises(IntegrityError):
            user=User.objects.create_user(username='testuser',email='test12@mailinater.com',password='testpassword')
            
class TestCustomerModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        
        cls.user = User.objects.create_user(username='terstuser',password='testpassword')
        cls.customer = Customer.objects.create(name='testuser',
                                               phone='9961980428',
                                               email='testuser@mailinator.com',
                                               vehicle_number = 'abc123',
                                               running_kilometer = 2500,
                                               service_advisor = cls.user,
                                               )
        
    def test_create_customer(self):
        
        custmoer_obj = Customer.objects.get(id=1)
        self.assertEqual(Customer.objects.count(),1)
        self.assertTrue(isinstance(custmoer_obj,Customer))
        self.assertEqual(custmoer_obj.name,'testuser')
        self.assertEqual(custmoer_obj.phone,'9961980428')
        self.assertEqual(custmoer_obj.email,'testuser@mailinator.com')
        self.assertEqual(custmoer_obj.vehicle_number,'abc123')
        self.assertEqual(custmoer_obj.running_kilometer,2500)
        self.assertEqual(custmoer_obj.service_advisor,self.user)
        self.assertTrue(custmoer_obj.is_active)
        
    def test_string_representation(self):
        
        self.assertEqual(str(self.customer),'testuser')
        
    def test_created_date(self):   
        
        self.assertIsNotNone(self.customer.created_date)
        
        self.assertLessEqual(self.customer.created_date,timezone.now())
        
    def test_updated_date(self):
        
        customer = Customer.objects.create(name='testuser',
                                               phone='9961980428',
                                               email='testuser@mailinator.com',
                                               vehicle_number = 'abc123',
                                               running_kilometer = 2500,
                                               service_advisor = self.user
                                               )
        
        customer.vehicle_number='abcd1234'         #to update the customer
        print(customer.vehicle_number)
        customer.save()
        
        self.assertIsNotNone(customer.created_date)
        self.assertGreaterEqual(customer.updated_date,customer.created_date)
        
    def test_work_status(self):
        
        self.assertIsNotNone(self.customer.work_status)
        self.assertEqual(self.customer.work_status,'pending')
        self.assertIn(self.customer.work_status,dict(Customer.work_status_choices).keys())
        
    def test_invalid_work_status(self):
        
        with self.assertRaises(ValidationError):
            
            customer = Customer.objects.create(name='testuser',
                                               phone='9961980428',
                                               email='testuser@mailinator.com',
                                               vehicle_number = 'abc123',
                                               running_kilometer = 2500,
                                               service_advisor = self.user,
                                               work_status = 'invalid status'
                                               )
            customer.full_clean()
        
    def test_name_exeed_max_length(self):
        
        customer = Customer.objects.create(name='testuser'*200,
                                               phone='9961980428',
                                               email='testuser@mailinator.com',
                                               vehicle_number = 'abc123',
                                               running_kilometer = 2500,
                                               service_advisor = self.user
                                               )
        with self.assertRaises(ValidationError):
            
            customer.full_clean()
            
    def test_running_kilometer_negative_integer(self):
        
        with self.assertRaises(IntegrityError):
            customer = Customer.objects.create(name='testuser',
                                               phone='9961980428',
                                               email='testuser@mailinator.com',
                                               vehicle_number = 'abc123',
                                               running_kilometer = -2500,
                                               service_advisor = self.user
                                               )
    
    def test_invalid_phone_number(self):
        
        with self.assertRaises(ValidationError):
            customer = Customer.objects.create(name='testuser',
                                               phone='99628',
                                               email='testuser@mailinator.com',
                                               vehicle_number = 'abc123',
                                               running_kilometer = 2500,
                                               service_advisor = self.user
                                               )
            customer.full_clean()    

        
        
# class TestArithamatic(TestCase):
#     @classmethod
#     def setUpTestData(cls):
        
#         cls.num1=12
#         cls.num2=0
    
#     def testMath(self):
#         with self.assertRaises(ZeroDivisionError):
#             result = self.num1/self.num2
#             self.assertEqual(result,0)
        
        
      