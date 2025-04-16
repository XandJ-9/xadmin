from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Role, Menu, SystemConfig
from. serializers import MenuSerializer, SystemConfigSerializer,UserSerializer, RoleSerializer
from .permissions import IsAdminUser, IsOwnerOrAdmin,HasRolePermission
import logging

logger = logging.getLogger('django')

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=True, methods=['get'])
    def menus(self, request, pk=None):
        """获取角色的菜单权限"""
        role = self.get_object()
        # 获取角色关联的所有菜单ID
        role_menus = role.role_menus.all()
        menu_ids = [rm.menu_id for rm in role_menus]
        return Response({'menu_ids': menu_ids}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def set_menus(self, request, pk=None):
        """设置角色的菜单权限"""
        role = self.get_object()
        menu_ids = request.data.get('menu_ids', [])
        
        # 验证菜单ID是否有效
        if not all(isinstance(mid, int) for mid in menu_ids):
            return Response({'error': '菜单ID必须为整数'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证菜单是否存在
        existing_menu_ids = set(Menu.objects.filter(id__in=menu_ids).values_list('id', flat=True))
        invalid_ids = set(menu_ids) - existing_menu_ids
        if invalid_ids:
            return Response({'error': f'菜单ID不存在: {list(invalid_ids)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 清除原有的角色菜单关联
        role.role_menus.all().delete()
        
        # 创建新的角色菜单关联
        from .models import RoleMenu
        for menu_id in menu_ids:
            RoleMenu.objects.create(
                role=role,
                menu_id=menu_id,
                creator=request.user,
                updator=request.user
            )
        
        return Response({'menu_ids': menu_ids}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['login', 'register']:
            permission_classes = [AllowAny]
            return [permission() for permission in permission_classes]
        elif self.action == 'list':
            return [IsAdminUser()]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # 根据用户名和密码判断用户是否存在
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response(
            {'error': '用户名或密码错误'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def reset_pwd(self, request, pk=None):
        user = self.get_object()
        user.set_password("123456")
        user.save()
        return Response({'message': '密码重置成功'}, status=status.HTTP_200_OK)

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    # permission_classes = [IsAdminUser]

    def get_permissions(self):
        '''
        自定义获取菜单数据的权限逻辑
        '''
        if self.action in ['create', 'update', 'partial_update', 'destroy','all']:
            return [IsAdminUser()]
        elif self.action == 'user_menus':
            return [HasRolePermission([self.request.user.role.name])]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    def list(self, request, *args, **kwargs):
        # 获取顶级菜单
        queryset = Menu.objects.filter(parent=None).order_by('sort')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def all(self, request):
        # 获取所有菜单
        queryset = Menu.objects.all().order_by('sort')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def user_menus(self, request):
        """根据当前登录用户的角色返回菜单列表（扁平结构）"""
        user = request.user
        if not user.role:
            return Response({'error': '用户没有分配角色'}, status=status.HTTP_403_FORBIDDEN)
        
        # 获取用户角色关联的所有菜单ID
        role_menus = user.role.role_menus.all()
        menu_ids = [rm.menu_id for rm in role_menus]
        
        # 获取所有菜单并按排序字段排序
        menus = Menu.objects.filter(id__in=menu_ids).order_by('sort')
        
        # 序列化菜单数据，返回扁平结构
        serializer = self.get_serializer(menus, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class SystemConfigViewSet(viewsets.ModelViewSet):
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigSerializer
    permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_key(self, request):
        key = request.query_params.get('key')
        if not key:
            return Response({'error': '请提供配置键'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            config = SystemConfig.objects.get(key=key)
            serializer = self.get_serializer(config)
            return Response(serializer.data)
        except SystemConfig.DoesNotExist:
            return Response({'error': f'未找到配置项: {key}'}, status=status.HTTP_404_NOT_FOUND)
