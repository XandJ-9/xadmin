from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from system.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSetTestCase(APITestCase):
    """测试UserViewSet类的注册和登录功能"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 创建一个测试用户
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            phonenumber='13800138000'
        )
        
        # 设置API URL
        self.register_url = reverse('user-register')
        self.login_url = reverse('user-login')
    
    def test_register_success(self):
        """测试用户注册成功的情况"""
        # 准备注册数据
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'phonenumber': '13900139000'
        }
        
        # 发送注册请求
        response = self.client.post(self.register_url, data, format='json')
        
        # 验证响应状态码为201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 验证响应包含token和用户信息
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        
        # 验证用户已创建
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_register_invalid_data(self):
        """测试用户注册失败的情况 - 无效数据"""
        # 准备无效的注册数据（缺少必填字段）
        data = {
            'username': 'newuser'
            # 缺少密码和其他必填字段
        }
        
        # 发送注册请求
        response = self.client.post(self.register_url, data, format='json')
        
        # 验证响应状态码为400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_duplicate_username(self):
        """测试用户注册失败的情况 - 用户名已存在"""
        # 准备与已存在用户相同用户名的注册数据
        data = {
            'username': 'testuser',  # 与setUp中创建的用户相同
            'password': 'newpassword',
            'email': 'another@example.com',
            'phonenumber': '13900139000'
        }
        
        # 发送注册请求
        response = self.client.post(self.register_url, data, format='json')
        
        # 验证响应状态码为400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_success(self):
        """测试用户登录成功的情况"""
        # 准备登录数据
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        
        # 发送登录请求
        response = self.client.post(self.login_url, data, format='json')
        
        # 验证响应状态码为200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证响应包含token和用户信息
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        
        # 验证返回的用户信息正确
        self.assertEqual(response.data['user']['username'], 'testuser')
    
    def test_login_invalid_credentials(self):
        """测试用户登录失败的情况 - 无效凭据"""
        # 准备错误的登录数据
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        # 发送登录请求
        response = self.client.post(self.login_url, data, format='json')
        
        # 验证响应状态码为401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # 验证错误消息
        self.assertIn('error', response.data)
    
    def test_login_missing_fields(self):
        """测试用户登录失败的情况 - 缺少字段"""
        # 准备缺少字段的登录数据
        data = {
            'username': 'testuser'
            # 缺少密码字段
        }
        
        # 发送登录请求
        response = self.client.post(self.login_url, data, format='json')
        
        # 验证响应状态码为401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
