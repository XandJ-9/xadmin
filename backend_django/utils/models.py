from django.db import models
from django.conf import settings


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

class BizBaseModel(models.Model):
    """业务公共字段模型"""
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_creator', null=True, blank=True, verbose_name='创建者')
    updator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_updator', null=True, blank=True, verbose_name='更新者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    del_flag = models.CharField(max_length=1, default='0', choices=[('0', '存在'), ('1', '删除')], verbose_name='删除标志')


    class Meta:
        abstract = True



def get_field_verbose_name(model, field_name):
    """
    获取字段verbose_name
    :param model:
    :param field_name:
    :return:
    """
    field = model._meta.get_field(field_name)
    return field.verbose_name