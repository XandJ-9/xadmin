from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.db.models import Q
from PIL import Image, ImageDraw, ImageFont
from .models import Post,Dept,User, Role, Menu, SystemConfig, Captcha, UserRole, SystemDictType,SystemDictData
from .serializers import *
from .permissions import IsAdminUser, IsOwnerOrAdmin,HasRolePermission

from utils.viewset import CustomModelViewSet
from utils.serializer import build_tree
import logging, uuid

logger = logging.getLogger('django')

class SystemViewMixin:

    @action(detail=False, methods=['put'])
    def changeStatus(self, request, pk=None):
        model = self.queryset.model
        pk = request.data.get(f'{model.__name__.lower()}Id')
        # 使用queryset.update方法无法使的时间字段自动更新
        # model.objects.filter(id=pk).update(status=request.data.get('status'))
        # 使用model.save方法可以使时间字段自动更新
        obj = model.objects.get(id=pk)
        obj.status = request.data.get('status')
        obj.save()
        ser = self.get_serializer(obj)
        return Response(ser.data, status=status.HTTP_200_OK)

class PostViewSet(SystemViewMixin,CustomModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class DeptViewSet(CustomModelViewSet):
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    # permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'])
    def exclude(self, request, dept_id):
        # queryset = self.queryset.exclude(id=dept_id)
        # 排除 id为dept_id的部门以及其子部门
        excluded_dept_ids = [dept_id]
        def get_children(dept_id):
            children = Dept.objects.filter(parent_id=dept_id)
            for child in children:
                excluded_dept_ids.append(child.id)
                get_children(child.id)
        get_children(dept_id)
        queryset = Dept.objects.exclude(id__in=excluded_dept_ids)
        serizlizer = self.get_serializer(queryset, many = True)
        return Response(serizlizer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        获取部门树形结构
        :param request:
        :return:
        """
        depts = Dept.objects.all()
        serializer = DeptSerializer(depts, many=True)
        dept_tree = build_tree(serializer.data)
        return Response(dept_tree, status=status.HTTP_200_OK)

class RoleViewSet(SystemViewMixin,CustomModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    export_serializer_class = RoleSerializer
    permission_classes = [IsOwnerOrAdmin]
    export_field_label = {
        'roleName': '角色名称',
        'roleKey': '角色权限字符串',
        'roleSort': '显示顺序',
        'status': '角色状态',
        'remark': '备注'
    }
    
    @action(detail=True, methods=['get'])
    def menus(self, request, pk=None):
        """获取角色的菜单权限"""
        role = self.get_object()
        # 获取角色关联的所有菜单ID
        role_menus = role.role_menus.all()
        menu_ids = [rm.menu_id for rm in role_menus]
        return Response({'menu_ids': menu_ids}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['put'])
    def updateRoleMenu(self, request, pk=None):
        """
        设置角色的菜单
        """
        role = self.get_object()
        menu_ids = request.data.get('menuIds', [])
        
        # 验证菜单ID是否有效
        if not all(isinstance(mid, int) for mid in menu_ids):
            return Response({'error': '菜单ID必须为整数'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证菜单是否存在
        valid_menu_ids = set(Menu.objects.filter(id__in=menu_ids).values_list('id', flat=True))
        invalid_ids = set(menu_ids) - valid_menu_ids
        if invalid_ids:
            return Response({'error': f'菜单ID不存在: {list(invalid_ids)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 筛选应该删除的菜单id,并删除之
        existed_menu_ids = role.role_menus.all().values_list('menu_id', flat=True)
        delete_menu_ids = set(existed_menu_ids) - set(menu_ids)
        RoleMenu.objects.filter(role_id=role.id, menu_id__in=delete_menu_ids).delete()

        
        # 创建新的角色菜单关联
        new_role_menu_ids = set(menu_ids) - set(existed_menu_ids)
        ser = RoleMenuSerializer(data=[{'role': role.id, 'menu': menu_id} for menu_id in new_role_menu_ids], many=True, request=request)
        if ser.is_valid(raise_exception=True):
            ser.save()
        new_role_menu_ids = role.role_menus.all().values_list('menu_id', flat=True)
        return Response({'menu_ids': new_role_menu_ids}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def deptTree(self, request, roleId = None):
        if not roleId:
            return Response({'message': '参数错误'},status=status.HTTP_400_BAD_REQUEST)
        role = Role.objects.filter(id=roleId).first()
        depts = Dept.objects.filter(id__in=role.role_depts.all().values_list('dept_id', flat=True))
        dept_tree = build_tree(DeptSerializer(depts, many=True).data)
        return Response(dept_tree, status=status.HTTP_200_OK)

class UserViewSet(SystemViewMixin,CustomModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ['status','username','phonenumber']
    export_field_label = {'username':'姓名','nickname':'昵称','phonenumber':'手机号码','deptName':'部门名称'}
    export_serializer_class = UserExportSerializer
    import_serializer_class = UserImportSerializer
    import_field_dict = {
        "nickname": "昵称",
        "username": "用户名称",
        "email": "用户邮箱",
        "phonenumber": "手机号码",
        "create_time":  "创建时间",
        "sex": {
            "title": "用户性别",
            "choices": {
                # "data": {"未知": 2, "男": 1, "女": 0},
                "queryset": SystemDictData.objects.filter(dict_type='sys_user_sex'),
            }
        },
        "is_active": {
            "title": "帐号状态",
            "choices": {
                "data": {"启用": True, "禁用": False},
            }
        },
        "dept_name": {"title": "部门", "choices": {"queryset": Dept.objects.filter(status='1'), "values_name": "dept_name"}},
        "role": {"title": "角色", "choices": {"queryset": Role.objects.filter(status='1'), "values_name": "role_name"}},
    }

    def filter_queryset(self, queryset):
        '''
        外键搜索单独处理
        '''
        dept_id = self.request.query_params.get('deptId', None)
        if dept_id:
            # 部门存在，查找子级部门
            try:
                dept = Dept.objects.get(id=dept_id)
                # 如果部门存在，获取该部门及其子部门
                ancestors=','.join([dept.ancestors,str(dept.id)])+','
                dept_ids = Dept.objects.filter(Q(ancestors__startswith=ancestors) 
                                               | Q(id = dept_id)
                                               ).values_list('id', flat=True)
                queryset = queryset.filter(dept_id__in=dept_ids)
            except Dept.DoesNotExist:
                # 如果部门不存在，返回空查询集
                queryset = queryset.none()
        userIds = self.request.data.get('userIds', None) if self.request.data else None
        if userIds:
            # 如果userIds存在，过滤出指定的用户
            queryset = queryset.filter(id__in=userIds)
        return super().filter_queryset(queryset)

    def get_permissions(self):
        if self.action in ['login', 'register', 'captchaImage']:
            return [AllowAny()]
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsOwnerOrAdmin()]

    def retrieve(self, request, *args, **kwargs):
        '''
        自定义返回单个对象的数据格式
        '''
        instance = self.get_object()
        user_data = self.get_serializer(instance)
        role_ids = instance.user_roles.all().values_list('role_id', flat=True)
        post_ids = instance.user_posts.all().values_list('post_id', flat=True)
        return Response(data={
            'user': user_data.data,
            'roleIds': list(role_ids),
            'postIds': list(post_ids)
        })
    
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
        return Response({'img': base64_code,'uuid':uuid_str, 'code':code}, status=status.HTTP_200_OK)

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
            # token = refresh_token.access_token
            token = refresh_token
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
        token = request.auth
        if token:
            uuid_str = token.get('uuid')
            if Captcha.objects.filter(uuid=uuid_str).exists():
                # 删除验证码
                # Captcha.objects.filter(uuid=uuid_str).delete()
                # 要想限制用户有效退出登录，将token加入黑名单
                token.blacklist()
            else:
                return Response({'message': '用户已退出'},status=status.HTTP_401_UNAUTHORIZED)

        return Response({'message': '登出成功'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def getInfo(self, request):
        user = request.user
        if user.is_authenticated:
            # 获取用户角色
            user_roles = user.user_roles.all()
            role_ids = [user_role.role.id for user_role in user_roles]
            permissions = ['*:*:*']
            return Response({"user": UserSerializer(user).data,"roles": role_ids, "permissions": permissions})
        else:
            return Response({'error': '用户未登录'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['put'])
    def resetPwd(self, request, pk=None):
        password = request.data.get("password", None)
        if password is None or password.strip() == '':
            return Response({'error': '密码不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()
        ser = UserSerializer(instance=user, data={'password': password, 'username': user.username}, request=request)
        if ser.is_valid(raise_exception=True):
            ser.save()
        
        if user.email:
            # 发送邮件通知用户密码已重置
            mail_msg = f'您的登录信息已被重置:用户名 {user.username} ,密码 {password}'
            user.email_user(subject='密码重置成功',
                        message= mail_msg)
        return Response({'message': '密码重置成功','data': ser.data}, status=status.HTTP_200_OK)
    @action(detail=True, methods=['get'], url_path='authRole')
    def authRole(self, request, pk=None):
        user = self.get_object()
        user_roles = user.user_roles.all().values_list('role_id', flat=True)
        roles = Role.objects.all()
        ret = {
            'user': UserSerializer(user).data,
            'userRoles':user_roles,
            'roles': RoleSerializer(roles, many=True).data
        }
        return Response(ret)

    @action(detail=True, methods=['put'])
    def updateAuthRole(self, request, pk=None):
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
        
        role_ids = request.data.get('roleIds',[])

        # # 验证用户ID是否有效
        if not all(isinstance(rid, int) for rid in role_ids):
            return Response({'error': f'角色ID必须为整数 {role_ids}'}, status=status.HTTP_400_BAD_REQUEST)

        # 判断角色id是否都存在
        valid_role_ids = set(Role.objects.filter(id__in=role_ids).values_list('id', flat=True))
        invalid_ids = set(role_ids) - valid_role_ids
        if invalid_ids:
            return Response({'error': f'角色ID不存在: {list(invalid_ids)}'}, status=status.HTTP_400_BAD_REQUEST)

        existed_role_ids = UserRole.objects.filter(user_id=user.id).values_list('role_id', flat=True)
        
        # 删除原有的用户角色关联
        delete_role_ids = set(existed_role_ids) - set(role_ids)
        # for roleId in delete_role_ids:
            # UserRole.objects.filter(user_id=user.id, role_id=roleId).delete()
        UserRole.objects.filter(user_id=user.id, role_id__in=delete_role_ids).delete()

        # 添加新的用户角色关联
        new_role_ids = set(role_ids) - set(existed_role_ids)
        ser = UserRoleSerializer(data=[{'user': user.id, 'role': role_id} for role_id in new_role_ids], many=True, request=request)
        if ser.is_valid(raise_exception=True):
            ser.save()
        new_role_ids = user.user_roles.all().values_list('role_id', flat=True)
        return Response({'message': '授权成功','role_ids':new_role_ids}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        user = request.user
        return Response({"user":UserSerializer(user).data,
                         "roleGroup":[user_role.role.role_name for user_role in user.user_roles.all()],
                         "postGroup":[user_post.post.post_name for user_post in user.user_posts.all()]
                         })
    @action(detail=False, methods=['put'], url_path='profile/update')
    def updateProfile(self, request):
        user = request.user
        ser = UserSerializer(instance=user, data=request.data, request=request)
        if ser.is_valid():
            ser.save()
        return Response({'message': '更新成功', "data":ser.data})
    
    @action(detail=False, methods=['put'], url_path='profile/updatePwd')
    def updatePwd(self, request):
        """
        修改密码
        :param request:
        :return:
        """
        user = request.user
        old_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')
        
        if not user.check_password(old_password):
            return Response({'error': '旧密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': '密码修改成功'}, status=status.HTTP_200_OK)

class MenuViewSet(CustomModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    # permission_classes = [IsAdminUser]
    filter_fields=['status','menu_name','menu_type','visible']


    def get_permissions(self):
        '''
        自定义获取菜单数据的权限逻辑
        '''
        if self.action in ['create', 'update', 'partial_update', 'destroy','all']:
            return [IsAdminUser()]
        elif self.action in ['user_menus','getRouters']:
            if self.request.user.is_authenticated:
                # roles = self.request.user.user_roles.all()
                roles = Role.objects.filter(id__in=self.request.user.user_roles.values_list('role_id', flat=True))
                return [HasRolePermission(allowed_roles = [role.role_key for role in roles])]
        return [IsAdminUser()]

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
                menu_ids = [menu.id for menu in Menu.objects.filter(status='0').exclude(menu_type ='F').order_by('order_num')]
            else:
                role_menus = user_role.role.role_menus.all()
                menu_ids.extend([rm.menu_id for rm in role_menus])
        
        # 去重
        menu_ids = list(set(menu_ids))
        
        # 获取所有菜单并按排序字段排序
        all_menus = Menu.objects.filter(id__in=menu_ids, status='0').exclude(menu_type='F').order_by('order_num')
        
        # 获取顶级菜单
        top_menus = [menu for menu in all_menus if menu.parent is None]

        # 构建树形结构
        def build_menu_tree(menu):
            menu_dict = {
                'name': menu.route_name,
                'path': menu.path,
                'hidden': int(menu.visible),
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

    @action(detail=False, methods=['get'])
    def roleMenuTreeselect(self, request, roleId):
        role = Role.objects.filter(id=roleId).first()
        menu_ids = role.role_menus.all().values_list('menu_id', flat=True)
        menus = Menu.objects.filter(id__in=menu_ids).order_by('order_num')
        serializer = MenuSerializer(menus, many=True)
        tree_data = build_tree(serializer.data, parent_id=None, parent_field_name='parentId', pk_field_name='menuId')
        return Response(tree_data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=False)
    def treeselect(self, request):
        ser = MenuSerializer(Menu.objects.all(), many=True)
        tree_data = build_tree(ser.data, parent_id=None, parent_field_name='parentId', pk_field_name='menuId')
        return Response(tree_data, status=status.HTTP_200_OK)

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
    filter_fields = ['status', 'dict_name','dict_type']

    @action(detail=False, methods=['get'], url_path='optionselect')
    def optionselect(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def refreshCache(self, request):
        return Response({"message":"refresh"})

class SystemDictDataViewSet(CustomModelViewSet):
    queryset = SystemDictData.objects.all()
    serializer_class = SystemDictDataSerializer

    @action(detail=False, methods=['get'])
    def get_data_by_type(self, request,dict_type=None):
        dict_type_items = SystemDictData.objects.filter(dict_type=dict_type)
        serializer = self.get_serializer(dict_type_items, many=True)
        return Response({"data": serializer.data})
