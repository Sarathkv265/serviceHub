from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from service.models import Customer




class CustumerListView(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        
        cls.admin= User.objects.create_superuser(username='testadmin',password='testpassword')
        cls.url ='/api/customers/'
        cls.admin_token = Token.objects.create(user=cls.admin)
    def test_customer_create_view(self):
        # self.client.force_login(self.admin)
        print('token =',self.admin_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        
        data={
    
                    "name": "testcustomer",
                    "phone": "9961980428",
                    "email": "sarathkv8895@gmail.com",
                    "vehicle_number": "kl-59-u-6865",
                    "running_kilometer": 49000
            }
        self.response=self.client.post(self.url,data)
        print(self.response)

        self.assertEqual(self.response.status_code,201) 
        self.assertEqual(self.response.data.get('name'),'testcustomer')
        self.assertEqual(self.response.data.get('phone'),'9961980428')
        self.assertEqual(self.response.data.get('email'),'sarathkv8895@gmail.com')
        
    def test_customer_list_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        
        data={
    
                    "name": "testcustomer",
                    "phone": "9961980428",
                    "email": "sarathkv8895@gmail.com",
                    "vehicle_number": "kl-59-u-6865",
                    "running_kilometer": 49000
            }
        
        Customer.objects.create(**data,service_advisor=self.admin)
        
        data={
    
                    "name": "test_customer",
                    "phone": "90000000",
                    "email": "sarathkv8895@gmail.com",
                    "vehicle_number": "kl-55-u-6865",
                    "running_kilometer": 59000
            }
        
        Customer.objects.create(**data,service_advisor=self.admin)
        
        response = self.client.get(self.url)
        
        print(response.data)
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),2)
        
    def test_invalid_customer_list_access(self):
        
        staff=User.objects.create_user(username='amal',email='amal@gmail.com',password='testpassword')
        staff_token = Token.objects.create(user=staff)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {staff_token}')
        
        response=self.client.get(self.url)
        print(response) 
        self.assertEqual(response.status_code,403)
    def test_invalid_customer_create_access(self):
        
        staff=User.objects.create_user(username='amal',email='amal@gmail.com',password='testpassword')
        staff_token = Token.objects.create(user=staff)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {staff_token}')
        
        data={
    
                    "name": "test_customer",
                    "phone": "90000000",
                    "email": "sarathkv8895@gmail.com",
                    "vehicle_number": "kl-55-u-6865",
                    "running_kilometer": 59000
            }
        response = self.client.post(self.url,data)
        
        print(response)
        
        self.assertEqual(response.status_code,403)
        
    def test_annonymous_user_create(self):
        
        data={
    
                    "name": "test_jesin",
                    "phone": "90000000",
                    "email": "sarathkv8895@gmail.com",
                    "vehicle_number": "kl-55-u-6865",
                    "running_kilometer": 59000
            }
        response = self.client.post(self.url,data)
        
        print(response)
        self.assertEqual(response.status_code,401)
    
    def test_annoymous_user_list(self):
        
        response= self.client.get(self.url)
        
        print(response)
        
        self.assertEqual(response.status_code,401)
        
        
        
        
        
        