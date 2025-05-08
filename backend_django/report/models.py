from django.db import models
from django.db.models import F
from system.models import BizBaseModel

# 平台信息
class PlatformInfo(BizBaseModel):
    name = models.CharField(max_length=255, verbose_name='平台名称', unique=True)
    desc = models.CharField(max_length=255, verbose_name='描述', null=True, blank=True)
    class Meta:
        db_table = "report_platform_info"

    def __str__(self) -> str:
        return self.name

# 模块信息
class ModuleInfo(BizBaseModel):
    name = models.CharField(max_length=255, verbose_name='模块名称', unique=True)
    desc = models.CharField(max_length=255, verbose_name='描述',blank=True, null=True)
    platform = models.ForeignKey(PlatformInfo,verbose_name="平台", on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = "report_module_info"
        ordering = ('-updated_at',)
    def __str__(self) -> str:
        return self.name

# 报表信息
class ReportInfo(BizBaseModel):
    name = models.CharField(max_length=255, verbose_name='报表名称')
    desc = models.CharField(max_length=255, verbose_name='描述', blank=True, null=True)
    module = models.ForeignKey(ModuleInfo,verbose_name="模块", on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = "report_report_info"
    def __str__(self) -> str:
        return self.name

# 接口信息
class InterfaceInfo(BizBaseModel):
    IS_TOTAL_CHOICES = (('1', '是'), ('0', '否'))
    IS_PAGING_CHOICE = (('1', '是'), ('0', '否'))
    IS_DATA_OPTION_CHOICE = (('1', '是'), ('0', '否'))
    IS_SECODN_TABLE_CHOICE = (('1', '是'), ('0', '否'))
    IS_LOGIN_VISIT_CHOICE = (('1', '是'), ('0', '否'))
    ALARM_TYPE_CHOICES = (('0', '否'), ('1', '邮件'), ('2', '短信'), ('3', '钉钉'), ('4', '企业微信'), ('5', '电话'))
    report = models.ForeignKey(ReportInfo,verbose_name="报表", on_delete=models.CASCADE)
    interface_name= models.CharField(max_length=255, verbose_name='接口名称')
    interface_code= models.CharField(max_length=255, verbose_name='接口编码',unique=True)
    interface_desc = models.TextField(verbose_name='接口描述',null=True, blank=True)
    interface_db_type = models.CharField(max_length=255, verbose_name='数据库类型')
    interface_db_name = models.CharField(max_length=255, verbose_name='数据库名称')
    interface_sql = models.TextField(verbose_name='接口sql', null=True, blank=True)
    is_total = models.CharField(default='0', max_length=1, verbose_name='是否合计',choices=IS_TOTAL_CHOICES)
    total_sql = models.TextField(verbose_name='合计sql', null=True, blank=True)
    is_paging = models.CharField(default='0', max_length=1, verbose_name='是否分页',choices=IS_PAGING_CHOICE)
    is_date_option = models.CharField(default='0', max_length=1,verbose_name='是否日期查询',choices=IS_DATA_OPTION_CHOICE)
    is_second_table = models.CharField(default='0', max_length=1,verbose_name='二级表头',choices=IS_SECODN_TABLE_CHOICE)
    is_login_visit = models.CharField(default='0', max_length=1,verbose_name='是否登陆验证',choices=IS_LOGIN_VISIT_CHOICE)
    alarm_type = models.CharField(default='0', max_length=1,verbose_name='报警类型',choices=ALARM_TYPE_CHOICES)
    user_name = models.CharField(max_length=255, verbose_name='用户名称', null=True, blank=True)

    class Meta:
        db_table = "report_interface_info"
        ordering = ('id',)
    
    def __str__(self) -> str:
        return self.interface_code
    

# 接口字段信息
# 接口数据类型 输出参数(1字符 2整数 3小数 4百分比) 输入参数(11日期 12月份 13单选 14多选 15文本)
class InterfaceField(BizBaseModel):
    DATA_TYPE_CHOICES = (
        ('1','字符'),
        ('2','整数'),
        ('3','小数'),
        ('4','百分比'),
        ('5','无格式整数'),
        ('6','无格式小数'),
        ('7','无格式百分比'),
        ('8','1位百分比'),
        ('9','1位小数'),
        ('10','年份'),
        ('11','日期'),
        ('12','月份'),
        ('13','单选'),
        ('14','多选'),
        ('15','文本')
    )
    SHOW_FLAG_CHOICES = (('1', '是'),('0','否'))
    EXPORT_FLAG_CHOICES = (('1', '是'), ('0', '否'))
    PARA_TYPE_CHOICES =(('1','输入参数'),('2','输出参数'))
    ROWSPAN_CHOICES = ((1, '是'), (0, '否'))
    interface = models.ForeignKey(InterfaceInfo,verbose_name="接口",on_delete=models.CASCADE)
    interface_para_code = models.CharField(max_length=255, verbose_name='接口参数编码')
    interface_para_name = models.CharField(max_length=255, verbose_name='接口参数名称')
    interface_para_position = models.IntegerField(verbose_name='接口参数位置')
    interface_para_type = models.CharField(max_length=255, verbose_name='接口参数类型', choices=PARA_TYPE_CHOICES)
    interface_data_type = models.CharField(max_length=255, verbose_name='接口参数数据类型', choices=DATA_TYPE_CHOICES)
    interface_para_default = models.CharField(max_length=255, verbose_name='接口参数默认值', null=True, blank=True)

    interface_para_rowspan = models.IntegerField(verbose_name='接口参数跨行', null=True, blank=True, choices=ROWSPAN_CHOICES)
    interface_parent_name = models.CharField(max_length=255, verbose_name='接口参数父级名称',null=True, blank=True)
    interface_parent_position = models.IntegerField(verbose_name='接口参数父级位置',null=True, blank=True)
    interface_para_interface_code = models.CharField(max_length=255, verbose_name='接口参数接口编码',null=True, blank=True)
    interface_cascade_para = models.CharField(max_length=255, verbose_name='接口参数级联参数',null=True, blank=True)
    interface_show_flag = models.CharField(max_length=255, verbose_name='接口参数是否显示', choices=SHOW_FLAG_CHOICES, default='1')
    interface_export_flag= models.CharField(max_length=255, verbose_name='接口参数是否导出',choices=EXPORT_FLAG_CHOICES, default='1')
    interface_show_desc = models.CharField(max_length=255, verbose_name='接口参数显示名称',null=True, blank=True, choices=SHOW_FLAG_CHOICES)
    interface_para_desc = models.CharField(max_length=255, verbose_name='接口参数描述',null=True, blank=True)

    class Meta:
        db_table = "report_interface_field"
        ordering = ('id',)
    
    def __str__(self) -> str:
        return self.interface_para_code

# 数据表信息
class TableInfo(BizBaseModel):
    table_name = models.CharField(max_length=255, verbose_name='表名')
    table_desc = models.CharField(max_length=255, verbose_name='描述')
    table_schema = models.CharField(max_length=255, verbose_name='表模式', null=True, default="")
    schema_type = models.CharField(max_length=255, verbose_name='模式类型', default='')

    class Meta:
        db_table = "report_table_info"
        ordering = ('id',)
        unique_together = (
            ('table_name','table_schema','schema_type')
        )

# 表字段信息
class TableColumnInfo(BizBaseModel):
    # table_id = models.IntegerField(verbose_name='表id')
    table = models.ForeignKey(TableInfo, on_delete=models.CASCADE, null=True)
    column_name = models.CharField(max_length=255, verbose_name='字段名')
    column_desc = models.CharField(max_length=255, verbose_name='字段描述')
    column_order = models.IntegerField(verbose_name='字段排序', default=-1, null=True)
    data_type = models.CharField(max_length=255, verbose_name='字段数据类型')
    data_length = models.IntegerField(verbose_name='字段长度', null=True)
    column_key = models.CharField(max_length=255, verbose_name='字段约束', null=True)
    is_nullable = models.CharField(max_length=255, verbose_name='是否为空', null=True)
    
    class Meta:
        db_table = "report_table_column"
        ordering = ('column_order',)
        unique_together = ('table', 'column_name')

# 表映射关系
class TableMapping(BizBaseModel):
    table_id = models.IntegerField(verbose_name='表id', null=True)
    table_schema = models.CharField(max_length=255, verbose_name='表模式',null=True)
    schema_type = models.CharField(max_length=255, verbose_name='模式类型', null=True)
    table_name = models.CharField(max_length=255, verbose_name='表名',null=True)
    src_table_id = models.IntegerField(verbose_name='源表id', null=True)
    src_table_schema = models.CharField(max_length=255, verbose_name='源表模式', null=True)
    src_schema_type = models.CharField(max_length=255, verbose_name='源模式类型', null=True)
    src_table_name = models.CharField(max_length=255, verbose_name='源表名', null=True)
    class Meta:
        db_table = "report_table_mapping"


# 表字段映射关系
class TableColumnMapping(BizBaseModel):
    table_id = models.IntegerField(verbose_name='表id')
    
    class Meta:
        db_table = "report_table_column_mapping"


# 导入文件信息记录
class UploadFileInfo(BizBaseModel):
    FILE_TYPE_CHOICES = (('1','TXT'),('2', 'Excel'),('3', 'CSV'), ('4', 'JSON'), ('5', 'SQL'))
    BIZ_TYPE_CHOICES = (('1','导入接口文件'),('2', '导入元数据文件'),('3','导入表映射文件'))
    source_file_name = models.CharField(max_length=255, verbose_name='源文件名', default='')
    file_type = models.CharField(max_length=255, verbose_name='文件类型', choices=FILE_TYPE_CHOICES, default='1')
    file_size = models.IntegerField(verbose_name='文件大小',default=0)
    # file_content = models.TextField(verbose_name='文件内容',null=True)
    # file_content = models.BinaryField(verbose_name='文件内容',null=True)
    file = models.FileField(upload_to='upload_files', verbose_name='文件',null=True)
    file_md5 = models.CharField(max_length=255, verbose_name='文件md5',unique=True)  # 校验文件上传是否重复 
    biz_type = models.CharField(max_length=1, verbose_name='业务类型', choices=BIZ_TYPE_CHOICES, default='1')
    class Meta:
        db_table = "report_upload_file_info"


class InterfaceQueryLog(BizBaseModel):
    interface_code = models.CharField(max_length=255, verbose_name='接口编码')
    interface_sql  = models.TextField(verbose_name='接口sql', null=True)
    execute_start_time = models.DateTimeField(verbose_name='开始时间', auto_now_add=True, null=True)
    execute_end_time = models.DateTimeField(verbose_name='结束时间', auto_now_add=True, null=True)
    execute_time = models.IntegerField(verbose_name='执行时间', default=0)
    execute_result = models.TextField(verbose_name='执行结果', null=True)

    class Meta:
        db_table = "report_interface_query_log"
