from django.db import models
from django.utils.translation import gettext_lazy as _

from cims_server.utils.utils import encrypt_message


class Base(models.Model):
    class GENDER(models.TextChoices):
        MALE = 'm', _('男')
        FEMALE = 'f', _('女')

    name = models.CharField(max_length=30, verbose_name="姓名")
    gender = models.CharField(max_length=1, choices=GENDER.choices, verbose_name="性别")
    birth_date = models.DateField(verbose_name="出生年月日")
    issuing_authority = models.CharField(max_length=40, verbose_name="颁发机构")
    valid_from = models.DateField(verbose_name="有效期起始日")
    valid_to = models.DateField(verbose_name="有效期终止日")
    photo = models.ImageField(upload_to='photos/',verbose_name="照片")  # 需要配置MEDIA_ROOT
    document_number = models.CharField(max_length=64, verbose_name="证件编号")  # 当前证件内容(除去照片和指针)字符串拼接后再进行一次sha256的值
    previous_document_number = models.CharField(max_length=64, blank=True, null=True, verbose_name="前证件编号")  # 若没有则为null
    next_document_number = models.CharField(max_length=64, blank=True, null=True, verbose_name="未来证件编号")  # 当前证件编号再次进行一次sha256
    another_document_number = models.CharField(max_length=64, blank=True, null=True, verbose_name="创建当前证件时另一个证件的编号")  # 若没有则为null
    ordinary_user = models.ForeignKey('OrdinaryUser', on_delete=models.CASCADE, verbose_name="用户id")  # 外键关联到OrdinaryUser模型

    class Meta:
        abstract = True  # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseUser的表


class IdentityCard(Base):
    ethnicity = models.CharField(max_length=5, verbose_name="民族")
    address = models.CharField(max_length=70, verbose_name="居住地址")
    id_number = models.CharField(max_length=18, verbose_name="身份证号")

    # 定义类属性fields
    fields = ['id', 'name', 'gender', 'ethnicity', 'address', 'id_number',
              'birth_date', 'issuing_authority', 'valid_from', 'valid_to', 'photo',
              'previous_document_number', 'next_document_number', 'another_document_number']

    class Meta:
        db_table = 'ms_identity_card'  # 指定表的名字
        verbose_name = "身份证"
        verbose_name_plural = "身份证"

    @classmethod
    def create_from_list(cls, elements):
        identity_card = cls(**dict(zip(cls.fields, elements)))
        return identity_card

    def get_func_param(self):
        arr = [getattr(self, field) for field in self.fields]
        arr = [encrypt_message(str(i), self.ordinary_user.public_key) for i in arr]
        res = '"' + '","'.join(map(str, arr)) + '"'
        return res

    def __str__(self):
        _ = [str(self.id), self.name, self.ethnicity, self.id_number, str(self.valid_to)]
        return '  '.join(_)  # 用空格连接

    objects = models.Manager()


class Passport(Base):
    nationality = models.CharField(max_length=5, verbose_name="国籍")
    passport_number = models.CharField(max_length=18, verbose_name="护照号码")
    issuing_country = models.CharField(max_length=8, verbose_name="颁发国家")

    # 定义类属性fields
    fields = [
        'id', 'name', 'gender', 'birth_date', 'nationality', 'passport_number',
        'issuing_country', 'issuing_authority', 'valid_from', 'valid_to', 'photo',
        'previous_document_number', 'next_document_number', 'another_document_number'
    ]

    class Meta:
        db_table = 'ms_passport'  # 指定表的名字
        verbose_name = "护照"
        verbose_name_plural = "护照"

    @classmethod
    def create_from_list(cls, elements):
        if len(elements) != len(cls.fields):
            raise ValueError("元素数量必须与字段数量一致")
        passport = cls(**dict(zip(cls.fields, elements)))
        return passport

    def get_func_param(self):
        arr = [getattr(self, field) for field in self.fields]
        arr = [encrypt_message(str(i), self.ordinary_user.public_key) for i in arr]
        res = '"' + '","'.join(map(str, arr)) + '"'
        return res

    def __str__(self):
        _ = [str(self.id), self.name, self.nationality, self.passport_number, str(self.valid_to)]
        return '  '.join(_)  # 用空格连接

    objects = models.Manager()


class OrdinaryUser(models.Model):
    public_key = models.TextField(verbose_name="公钥")
    private_key = models.TextField(verbose_name="私钥")

    class Meta:
        db_table = 'ms_ordinary_user'  # 指定表的名字
        verbose_name = "普通用户"
        verbose_name_plural = "普通用户"

    objects = models.Manager()


class GovernmentUser(models.Model):
    public_key = models.TextField(verbose_name="公钥")
    private_key = models.TextField(verbose_name="私钥")

    class Meta:
        db_table = 'ms_government_user'  # 指定表的名字
        verbose_name = "政府用户"
        verbose_name_plural = "政府用户"

    objects = models.Manager()
