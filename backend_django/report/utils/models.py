from django.db import models

table_prefix = "report_"

class CoreModel(models.Model):
    """
    核心标准抽象模型模型,可直接继承使用
    """
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id", editable=False)
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间",
                                           verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")
    creator = models.CharField(max_length=255, null=True, blank=True, help_text="创建人", verbose_name="创建人")
    updater = models.CharField(max_length=255, null=True, blank=True, help_text="修改人", verbose_name="修改人")

    class Meta:
        abstract = True
        verbose_name = '核心模型'
        verbose_name_plural = verbose_name