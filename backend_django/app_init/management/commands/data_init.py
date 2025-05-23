import logging
import os
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from system.models import User, Role, UserRole, Menu, RoleMenu
from datasource.models import DataSource

logger = logging.getLogger('django')

class Command(BaseCommand):
    help = '初始化系统数据，包括默认角色、管理员用户和示例数据源'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制重新创建数据，即使数据已存在',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options.get('force', False)
        self.stdout.write(self.style.NOTICE('开始初始化系统数据...'))
        
        # 初始化角色
        self._init_roles(force)
        
        # 初始化管理员用户
        self._init_admin_user(force)
        
        # 初始化用户角色关系
        self._init_user_roles(force)
        
        # 初始化菜单
        self._init_menus(force)
        
        # 初始化角色关联菜单
        # self._init_role_menu(force)

        # # 初始化角色部门关系
        # self._init_role_dept(force)

        # # 初始化示例数据源
        # self._init_sample_datasource(force)

        self.stdout.write(self.style.SUCCESS('系统数据初始化完成！'))
    
    def _load_json_data(self, file_name):
        """从JSON文件加载数据"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        file_path = os.path.join(data_dir, file_name)
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'数据文件不存在: {file_path}'))
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'加载数据文件失败: {str(e)}'))
            return {}
    
    def _process_date_value(self, value):
        """处理日期值，将sysdate()转换为当前时间"""
        if value == 'sysdate()':
            return timezone.now()
        return value
    
    def _init_roles(self, force):
        """初始化角色数据"""
        self.stdout.write('初始化角色数据...')
        
        # 加载角色数据
        role_data = self._load_json_data('role_data.json')
        if not role_data or 'sys_role' not in role_data:
            self.stdout.write(self.style.WARNING('未找到角色数据，跳过初始化'))
            return
        
        for role_item in role_data['sys_role']:
            role, created = Role.objects.get_or_create(
                id=role_item['role_id'],
                defaults={
                    'role_name': role_item['role_name'],
                    'role_key': role_item['role_key'],
                    'role_sort': role_item['role_sort'],
                    'data_scope': role_item['data_scope'],
                    'menu_check_strictly': role_item['menu_check_strictly'],
                    'dept_check_strictly': role_item['dept_check_strictly'],
                    'status': role_item['status'],
                    'del_flag': role_item['del_flag'],
                    'created_at': self._process_date_value(role_item['create_time']),
                    'remark': role_item.get('remark', '')
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建角色: {role.role_name}'))
            elif force:
                # 更新角色信息
                role.role_name = role_item['role_name']
                role.role_key = role_item['role_key']
                role.role_sort = role_item['role_sort']
                role.data_scope = role_item['data_scope']
                role.menu_check_strictly = role_item['menu_check_strictly']
                role.dept_check_strictly = role_item['dept_check_strictly']
                role.status = role_item['status']
                role.del_flag = role_item['del_flag']
                role.remark = role_item.get('remark', '')
                role.save()
                self.stdout.write(self.style.WARNING(f'更新角色: {role.role_name}'))
            else:
                self.stdout.write(f'角色已存在: {role.role_name}')
    
    def _init_admin_user(self, force):
        """初始化管理员用户"""
        self.stdout.write('初始化管理员用户...')
        
        # 加载用户数据
        user_data = self._load_json_data('user_data.json')
        if not user_data or 'sys_user' not in user_data:
            self.stdout.write(self.style.WARNING('未找到用户数据，跳过初始化'))
            return
        
        for user_item in user_data['sys_user']:
            # 创建或更新管理员用户
            user, created = User.objects.get_or_create(
                id=user_item['user_id'],
                defaults={
                    'username': user_item['user_name'],
                    'nickname': user_item['nick_name'],
                    'dept_id': user_item['dept_id'],
                    'user_type': user_item['user_type'],
                    'email': user_item['email'],
                    'phonenumber': user_item['phonenumber'],
                    'sex': user_item['sex'],
                    'avatar': user_item['avatar'],
                    'password': make_password(user_item['password']),  # 已经是加密的密码
                    'is_active': user_item['status'] == '0',  # 0表示正常
                    'del_flag': user_item['del_flag'],
                    'login_ip': user_item['login_ip'],
                    'login_date': self._process_date_value(user_item['login_date']),
                    'created_at': self._process_date_value(user_item['create_time']),
                    'remark': user_item.get('remark', ''),
                    'is_staff': True if user_item['user_name'] == 'admin' else False,
                    'is_superuser': True if user_item['user_name'] == 'admin' else False,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建用户: {user.username}'))
            elif force:
                # 更新用户信息（不更新密码）
                user.nickname = user_item['nick_name']
                user.password = make_password(user_item['password'])  # 确保密码是加密的
                user.dept_id = user_item['dept_id']
                user.user_type = user_item['user_type']
                user.email = user_item['email']
                user.phonenumber = user_item['phonenumber']
                user.sex = user_item['sex']
                user.avatar = user_item['avatar']
                user.is_active = user_item['status'] == '0'
                user.del_flag = user_item['del_flag']
                user.login_ip = user_item['login_ip']
                user.login_date = self._process_date_value(user_item['login_date'])
                user.remark = user_item.get('remark', '')
                user.is_staff = True if user_item['user_name'] == 'admin' else False
                user.is_superuser = True if user_item['user_name'] == 'admin' else False
                user.save()
                self.stdout.write(self.style.WARNING(f'更新用户: {user.username}'))
            else:
                self.stdout.write(f'用户已存在: {user.username}')
    
    def _init_user_roles(self, force):
        """初始化用户角色关系"""
        self.stdout.write('初始化用户角色关系...')
        
        # 加载用户角色关系数据
        user_role_data = self._load_json_data('user_role_data.json')
        if not user_role_data or 'sys_user_role' not in user_role_data:
            self.stdout.write(self.style.WARNING('未找到用户角色关系数据，跳过初始化'))
            return
        
        for ur_item in user_role_data['sys_user_role']:
            try:
                user = User.objects.get(id=ur_item['user_id'])
                role = Role.objects.get(id=ur_item['role_id'])
                
                user_role, created = UserRole.objects.get_or_create(
                    user=user,
                    role=role
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'创建用户角色关系: {user.username} - {role.role_name}'))
                else:
                    self.stdout.write(f'用户角色关系已存在: {user.username} - {role.role_name}')
            except (User.DoesNotExist, Role.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f'初始化用户角色关系失败: {str(e)}'))
    
    def _init_menus(self, force):
        """初始化菜单数据"""
        self.stdout.write('初始化菜单数据...')
        
        # 加载菜单数据
        menu_data = self._load_json_data('menu_data.json')
        if not menu_data or 'sys_menu' not in menu_data:
            self.stdout.write(self.style.WARNING('未找到菜单数据，跳过初始化'))
            return
        
        # 先创建所有菜单，不设置父菜单关系
        menu_objects = {}
        for menu_item in menu_data['sys_menu']:
            menu, created = Menu.objects.get_or_create(
                id=menu_item['menu_id'],
                defaults={
                    'menu_name': menu_item['menu_name'],
                    'parent_id': menu_item['parent_id'],  # 先存储parent_id
                    'order_num': menu_item['order_num'],
                    'path': menu_item['path'],
                    'component': menu_item['component'],
                    'query': menu_item['query'],
                    'route_name': menu_item['route_name'],
                    'is_frame': menu_item['is_frame'],
                    'is_cache': menu_item['is_cache'],
                    'menu_type': menu_item['menu_type'],
                    'visible': menu_item['visible'],
                    'status': menu_item['status'],
                    'perms': menu_item.get('perms', ''),
                    'icon': menu_item['icon'],
                    'remark': menu_item.get('remark', '')
                }
            )
            
            menu_objects[menu_item['menu_id']] = menu
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建菜单: {menu.menu_name}'))
            elif force:
                # 更新菜单信息
                menu.menu_name = menu_item['menu_name']
                menu.parent_id = menu_item['parent_id']  # 先存储parent_id
                menu.order_num = menu_item['order_num']
                menu.path = menu_item['path']
                menu.component = menu_item['component']
                menu.query = menu_item['query']
                menu.route_name = menu_item['route_name']
                menu.is_frame = menu_item['is_frame']
                menu.is_cache = menu_item['is_cache']
                menu.menu_type = menu_item['menu_type']
                menu.visible = menu_item['visible']
                menu.status = menu_item['status']
                menu.perms = menu_item.get('perms', '')
                menu.icon = menu_item['icon']
                menu.remark = menu_item.get('remark', '')
                menu.save()
                self.stdout.write(self.style.WARNING(f'更新菜单: {menu.menu_name}'))
            else:
                self.stdout.write(f'菜单已存在: {menu.menu_name}')
        
        # 第二次遍历，设置父菜单关系
        for menu_item in menu_data['sys_menu']:
            if menu_item['parent_id']:  # 有父菜单
                try:
                    menu = menu_objects[menu_item['menu_id']]
                    parent_menu = menu_objects[menu_item['parent_id']]
                    menu.parent = parent_menu
                    menu.save()
                except (KeyError, Exception) as e:
                    self.stdout.write(self.style.ERROR(f'设置菜单父子关系失败: {str(e)}'))
    
    def _init_role_menu(self, force):
        """初始化角色菜单权限"""
        self.stdout.write('初始化角色菜单权限...')
        
        # 加载角色菜单关系数据
        role_menu_data = self._load_json_data('role_menu_data.json')
        if not role_menu_data or 'sys_role_menu' not in role_menu_data:
            self.stdout.write(self.style.WARNING('未找到角色菜单关系数据，跳过初始化'))
            return
        
        for rm_item in role_menu_data['sys_role_menu']:
            try:
                role = Role.objects.get(id=rm_item['role_id'])
                menu = Menu.objects.get(id=rm_item['menu_id'])
                
                # 获取管理员用户作为创建者和更新者
                admin_user = User.objects.filter(username='admin').first()
                
                role_menu, created = RoleMenu.objects.get_or_create(
                    role=role,
                    menu=menu,
                    defaults={
                        'creator': admin_user,
                        'updator': admin_user
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'创建角色菜单关系: {role.role_name} - {menu.menu_name}'))
                else:
                    self.stdout.write(f'角色菜单关系已存在: {role.role_name} - {menu.menu_name}')
            except (Role.DoesNotExist, Menu.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f'初始化角色菜单关系失败: {str(e)}'))
    
    def _init_role_dept(self, force):
        """初始化角色部门关系"""
        self.stdout.write('初始化角色部门关系...')
        
        # 加载角色部门关系数据
        role_dept_data = self._load_json_data('role_dept_data.json')
        if not role_dept_data or 'sys_role_dept' not in role_dept_data:
            self.stdout.write(self.style.WARNING('未找到角色部门关系数据，跳过初始化'))
            return
        
        # 这里需要根据实际的模型结构来实现
        # 如果系统中有RoleDept模型，则按照类似RoleMenu的方式实现
        # 如果没有，则可以跳过或者创建该模型
        self.stdout.write(self.style.WARNING('角色部门关系初始化暂未实现'))
    
    def _init_sample_datasource(self, force):
        """初始化示例数据源"""
        self.stdout.write('初始化示例数据源...')
        
        # 获取管理员用户
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('管理员用户不存在，请先初始化管理员用户'))
            return