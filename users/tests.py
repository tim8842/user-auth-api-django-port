from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserRegistrationTest(APITestCase):
    def test_registration(self):
        url = reverse('register')
        data = {
            'email': 'testuser@example.com',
            'name': 'Test User',
            'password': 'TestPassword123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')
 
class UserLoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='TestPassword123'
        )

    def test_login(self):
        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
class JWTTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='TestPassword123'
        )
        self.refresh = RefreshToken.for_user(self.user)

    def test_access_token_valid(self):
        url = reverse('profile-detail')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_token_invalid(self):
        url = reverse('profile-detail')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class UserProfileTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='TestPassword123'
        )
        self.refresh = RefreshToken.for_user(self.user)
    
    def test_profile_detail(self):
        url = reverse('profile-detail')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bio', response.data)
        self.assertIn('phone_number', response.data)
        self.assertIn('profile_picture', response.data)
        self.assertIn('location', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
    
    def test_profile_update(self):
        url = reverse('profile-update')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        data = {
            'bio': 'Updated bio',
            'phone_number': '+1234567890'
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Updated bio')
        self.assertEqual(response.data['phone_number'], '+1234567890')
        
class ChangePasswordTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='OldPassword123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

    def test_change_password_success(self):
        url = reverse('change-password')
        data = {
            'old_password': 'OldPassword123',
            'new_password': 'NewPassword456'
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        self.client.credentials()  
        login_data = {
            'email': self.user.email,
            'password': 'NewPassword456'
        }
        login_response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_change_password_wrong_old_password(self):
        url = reverse('change-password')
        data = {
            'old_password': 'WrongOldPassword123',
            'new_password': 'NewPassword456'
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)
