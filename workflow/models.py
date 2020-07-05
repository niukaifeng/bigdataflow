from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models
import uuid

class TempWork(models.Model):

    ticket_id = models.CharField(verbose_name="编号id", primary_key=True,max_length=200,default="111")
    #  该字段为主键

    process_recod = models.CharField('进度', max_length=2048)

# class Users(AbstractUser):
#     username = models.CharField(verbose_name="用户名", max_length=20, default="admin")  # 用户名
#     # login_id=models.IntegerField(verbose_name="登陆id")   #用户登陆id
#     # editable 加上去就不显示
#     password = models.CharField(verbose_name="登陆密码", editable=False, max_length=10000, default="12345678")  # 用户密码
#     user_phone = models.CharField(verbose_name="手机号码", max_length=20, default=1)  # 电话
#     user_mail = models.CharField(verbose_name="邮箱", max_length=20, default=1)  # 邮箱
#     isInform = models.BooleanField(verbose_name="是否推送最新通知", default=True)  # 是否通知
#     isMail = models.BooleanField(verbose_name="是否发邮件", default=True)  # 是否邮件
#     # user_type=models.CharField(max_length=20) # 用户类型
#     USER_TYPE_LIST = (
#         (1, 'user'),
#         (2, 'admin'),
#     )
#     user_type = models.IntegerField(verbose_name="用户类型", choices=USER_TYPE_LIST, default=1)
#     power_type = models.CharField(verbose_name="用户权限", max_length=20)  # 用户权限
#     creator_id = models.IntegerField(verbose_name="创建者id", default=0)  # 创建者id
#     update_id = models.IntegerField(verbose_name="更新者id", default=0)  # 更新者id
#     lastTime = models.DateTimeField(verbose_name="最后更新时间", auto_now=True)
#     createTime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
#     isDel = models.BooleanField(verbose_name="是否能删除", default=True)  # 是否删除
#     # fatheruser_id=models.IntegerField()#父亲用户ID
#     # relevanceKey=models.CharField(max_length=20)#关联Key
#     img = models.ImageField(verbose_name="头像", null=True, blank=True, upload_to="upload")  # 上传图片
#
#     USERNAME_FIELD = 'id'
#
#     REQUIRED_FIELDS = ['username','email']

    # class Meta:
    #     # 指定表名
    #     db_table = 'myApp_users'
    #     verbose_name = '用户管理'
    #     verbose_name_plural = verbose_name

