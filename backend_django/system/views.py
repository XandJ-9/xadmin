from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from PIL import Image, ImageDraw, ImageFont
from .models import Dept,User, Role, Menu, SystemConfig, Captcha, UserRole, SystemDictType,SystemDictData
from. serializers import *
from .permissions import IsAdminUser, IsOwnerOrAdmin,HasRolePermission
from .authentication import get_user_from_token,get_token_from_request

from utils.viewset import CustomModelViewSet
from utils.filters import SearchFilterBackend
import logging, uuid

logger = logging.getLogger('django')

class DeptViewSet(CustomModelViewSet):
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    # permission_classes = [IsAdminUser]

class RoleViewSet(CustomModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = [IsAdminUser]
    
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

class UserViewSet(CustomModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ['status','username','dept']

    # def filter_queryset(self, queryset):
    #     for field in self.filter_fields:
    #         filter_kwargs = {field+'__icontains': self.request.query_params.get(field, '')}
    #         queryset = queryset.filter(**filter_kwargs)
    #     return queryset
    
    def get_permissions(self):
        if self.action in ['login', 'register', 'captchaImage']:
            return [AllowAny()]
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        """
        在创建用户之前，添加部门
        """
        user = self.request.user
        dept_id = self.request.data.get('dept_id',user.dept.id)
        # serializer.save(dept_id=dept_id)
        serializer.validated_data['dept_id'] = dept_id
        super().perform_create(serializer)
        

    @action(detail=False, methods=['get'])
    def captchaImage(self, request):
        """
        生成验证码图片
        :param request:
        :return:
        """
        # 生成唯一uuid
        uuid_str = uuid.uuid4()
        # 生成随机字符串
        code = get_random_string(length=4, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        
        # 创建图片
        image = Image.new('RGB', (100, 40), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # 设置字体和大小
        # font = ImageFont.truetype('arial.ttf', 20)
        font = ImageFont.load_default(20)

        # 绘制验证码
        draw.text((10, 5), code, fill=(0, 0, 0), font=font)
        
        # 保存验证码到内存中
        from io import BytesIO
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        
        captcha = Captcha.objects.create()
        # 保存验证码到数据库
        captcha.code = code
        captcha.uuid = uuid_str
        captcha.save()

        # 返回验证码图片和验证码字符串
        import base64
        base64_code = base64.encodebytes(buffer.getvalue()).decode('utf-8')
        # return JsonResponse({'code': status.HTTP_200_OK, 'img': base64_code,'uuid':uuid_str})
        return Response({'img': base64_code,'uuid':uuid_str}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        code = request.data.get('code')
        uuid = request.data.get('uuid')

        # 验证验证码
        if not code or not Captcha.objects.filter(uuid=uuid, code=code.upper()).exists():
            return Response({'error': '验证码错误'}, status=status.HTTP_400_BAD_REQUEST)

        # 根据用户名和密码判断用户是否存在
        user = authenticate(username=username, password=password)

        if user:
            refresh_token = RefreshToken.for_user(user)
            refresh_token['uuid'] = uuid
            token = refresh_token.access_token
            return Response({
                'token': str(token),
                'user': UserSerializer(user).data
            },
            status=status.HTTP_200_OK)
        return Response(
            {'error': '用户名或密码错误'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """登出"""
        token = get_token_from_request(request)
        if token:
            uuid_str = token.get('uuid')
            # 删除验证码
            Captcha.objects.filter(uuid=uuid_str).delete()
            # 要想限制用户有效退出登录，将token加入黑名单
            # token.blacklist()

        return Response({'message': '登出成功'}, status=status.HTTP_200_OK)

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

    @action(detail=False, methods=['get'])
    def getInfo(self, request):
        user = get_user_from_token(request)
        if user.is_authenticated:
            # 获取用户角色
            user_roles = user.user_roles.all()
            role_ids = [user_role.role.id for user_role in user_roles]
            permissions = ['*:*:*']
            return Response({"user": UserSerializer(user).data,"roles": role_ids, "permissions": permissions})
        else:
            return Response({'error': '用户未登录'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['post'])
    def reset_pwd(self, request, pk=None):
        user = self.get_object()
        user.set_password("123456")
        user.save()
        return Response({'message': '密码重置成功'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='authRole')
    def authRole(self, request, pk=None):
        """
        授权用户角色
        :param request:
        :return:
        """
        # userId = request.query_params.get('userId')
        # user = User.objects.get(id=userId)
        user = self.get_object()
        if not user:
            return Response({'error': '用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
        
        roleIds = request.data.get('roleIds')
        # rIds = roleIds.split(",")
        # 验证用户ID是否有效
        if not all(isinstance(rid, int) for rid in roleIds):
            return Response({'error': f'角色ID必须为整数 {roleIds}'}, status=status.HTTP_400_BAD_REQUEST)

        # 判断角色id是否都存在
        existed_role_ids= set(Role.objects.filter(id__in=roleIds).values_list('id', flat=True))
        invalid_ids = set(roleIds) - existed_role_ids
        if invalid_ids:
            return Response({'error': f'角色ID不存在: {list(invalid_ids)}'}, status=status.HTTP_400_BAD_REQUEST)

        # 删除原有的用户角色关联
        user.user_roles.all().delete()

        for roleId in roleIds:
            # 关联用户和角色
             UserRole.objects.create(user=user, role_id=roleId)
        return Response({'message': '授权成功'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def deptTree(self, request):
        """
        获取部门树形结构
        :param request:
        :return:
        """
        depts = Dept.objects.all()
        serializer = DeptSerializer(depts, many=True)
        
        def build_tree(dept_list, parent_id=None):
            tree = []
            for dept in dept_list:
                if dept['parent'] == parent_id:
                    children = build_tree(dept_list, dept['id'])
                    if children:
                        dept['children'] = children
                    else:
                        dept['children'] = []
                    tree.append(dept)
            return tree
        
        dept_tree = build_tree(serializer.data)
        return Response(dept_tree, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], url_path='changeStatus')
    def changeStatus(self, request):
        """
        修改用户状态
        """
        user_id = self.request.data.get('userId')
        user_status = self.request.data.get('status')
        user = User.objects.get(id=user_id)
        user.status = user_status
        user.save()
        return Response({'message': '修改成功'}, status=status.HTTP_200_OK)

class MenuViewSet(CustomModelViewSet):
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
            if self.request.user.is_authenticated:
                # roles = self.request.user.user_roles.all()
                roles = Role.objects.filter(id__in=self.request.user.user_roles.values_list('role_id', flat=True))
                return [HasRolePermission(allowed_roles = [role.role_key for role in roles])]
        return [IsAdminUser()]
    

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, updator=self.request.user)

    @action(detail=False, methods=['get'])
    def all(self, request):
        # 获取所有菜单
        queryset = Menu.objects.all().order_by('order_num')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_menus(self, request):
        """根据当前登录用户的角色返回菜单列表（扁平结构）"""
        user = request.user
        user_roles = user.user_roles.all()
        if not user_roles.exists():
            return Response({'error': '用户没有分配角色'}, status=status.HTTP_403_FORBIDDEN)
        
        role_menus = []
        for user_role in user_roles:
            # 如果是admin角色，则拥有所有菜单权限
            if user_role.role.role_key == 'admin':
                role_menus = Menu.objects.all()
                break
            # 获取用户角色关联的所有菜单ID
            role_menus.extend(user_role.role.role_menus.all())
        
        # 获取用户角色关联的所有菜单ID
        menu_ids = [rm.id for rm in role_menus]
        # 获取所有菜单并按排序字段排序
        menus = Menu.objects.filter(id__in=set(menu_ids)).order_by('order_num')
        
        # 序列化菜单数据，返回扁平结构
        serializer = self.get_serializer(menus, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def getRouters(self, request):
        user = request.user
        # 检查用户是否有角色
        user_roles = user.user_roles.all()
        # if not user_roles.exists():
        #     return Response({'error': '用户没有分配角色'}, status=status.HTTP_403_FORBIDDEN)
        
        # 获取用户角色关联的所有菜单ID
        menu_ids = []
        for user_role in user_roles:
            # 如果是admin角色，则拥有所有菜单权限
            if user_role.role.role_key == 'admin':
                menu_ids = [menu.id for menu in Menu.objects.all()]
            else:
                role_menus = user_role.role.role_menus.all()
                menu_ids.extend([rm.menu_id for rm in role_menus])
        
        # 去重
        menu_ids = list(set(menu_ids))
        
        # 获取所有菜单并按排序字段排序
        all_menus = Menu.objects.filter(id__in=menu_ids).order_by('order_num')
        
        # 获取顶级菜单
        top_menus = [menu for menu in all_menus if menu.parent is None]

        # 构建树形结构
        def build_menu_tree(menu):
            menu_dict = {
                'name': menu.route_name,
                'path': menu.path,
                'hidden': not int(menu.visible),
                'component': menu.component,
                'meta': {
                    'title': menu.menu_name,
                    'icon':  menu.icon,
                    'noCache': not menu.is_cache
                }
            }
            
            # 添加重定向属性（如果有）
            if menu.redirect:
                menu_dict['redirect'] = menu.redirect
            
            # 查找子菜单
            children = [child for child in all_menus if child.parent_id == menu.id]
            if children:
                menu_dict['children'] = [build_menu_tree(child) for child in children]
                
            return menu_dict
        
        # 构建路由数据
        router_data = [build_menu_tree(menu) for menu in top_menus]
        
        return Response(router_data, status=status.HTTP_200_OK)

class SystemConfigViewSet(CustomModelViewSet):
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

class SystemDictTypeViewSet(CustomModelViewSet):
    queryset = SystemDictType.objects.all()
    serializer_class = SystemDictTypeSerializer

class SystemDictDataViewSet(CustomModelViewSet):
    queryset = SystemDictData.objects.all()
    serializer_class = SystemDictDataSerializer

    @action(detail=False, methods=['get'])
    def get_data_by_type(self, request,dict_type=None):
        dict_type_items = SystemDictData.objects.filter(dict_type=dict_type)
        serializer = self.get_serializer(dict_type_items, many=True)
        return Response({"data": serializer.data})
