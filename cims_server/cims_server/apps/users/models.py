import datetime

from django.db import models


class BaseUser(models.Model):
    name = models.CharField(max_length=30, verbose_name="姓名")
    gender = models.CharField(max_length=1, verbose_name="性别")
    birth_date = models.DateField(verbose_name="出生年月日")
    issuing_authority = models.CharField(max_length=40, verbose_name="颁发机构")
    valid_from = models.DateField(auto_now_add=True, verbose_name="有效期起始日")
    valid_to = models.DateField(verbose_name="有效期终止日")
    photo = models.ImageField(upload_to='photos/', verbose_name="照片")  # 需要配置MEDIA_ROOT
    document_number = models.CharField(max_length=64, verbose_name="证件编号")  # 当前证件内容(除去照片和指针)字符串拼接后再进行一次sha256的值
    previous_document_number = models.CharField(max_length=64, blank=True, null=True, verbose_name="前证件编号")  # 若没有则为null
    next_document_number = models.CharField(max_length=64, blank=True, null=True, verbose_name="未来证件编号")  # 当前证件编号再次进行一次sha256
    another_document_number = models.CharField(max_length=64, blank=True, null=True, verbose_name="创建当前证件时另一个证件的编号")  # 若没有则为null

    class Meta:
        abstract = True  # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseUser的表

    def save(self, *args, **kwargs):
        current_year = datetime.date.today().year
        birth_year = self.birth_date.year
        age = current_year - birth_year

        if age < 16:
            duration = 5
        elif age < 25:
            duration = 10
        elif age < 45:
            duration = 20
        else:
            duration = 70 - age  # 假设长期有效直至70岁

        # 使用valid_from作为起始点来设置valid_to
        self.valid_to = datetime.date(self.valid_from.year + duration, self.valid_from.month, self.valid_from.day)
        super().save(*args, **kwargs)


class IdentityCard(BaseUser):
    ethnicity = models.CharField(max_length=5, verbose_name="民族")
    address = models.CharField(max_length=70, verbose_name="居住地址")
    id_number = models.CharField(max_length=18, verbose_name="身份证号")

    class Meta:
        db_table = 'ms_identity_card'  # 指定表的名字
        verbose_name = "身份证"
        verbose_name_plural = "身份证"

    # def generate_JWT(self) -> str:
    #     """
    #     生成  JWT
    #     Args:
    #         organization_account: 组织账号
    #     Returns:
    #         JWT
    #     """
    #     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 引用JWT中的jwt_payload_handler函数（生成payload部分）
    #     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 生成JWT
    #
    #     payload = jwt_payload_handler(self)  # 根据user生成用户相关的载荷部分
    #     token = jwt_encode_handler(payload)  # 传入载荷生成完成的JWT
    #     return token

    objects = models.Manager()  # 加上这句就可以了


class Passport(BaseUser):
    nationality = models.CharField(max_length=5, verbose_name="国籍")
    passport_number = models.CharField(max_length=18, verbose_name="护照号码")
    issuing_country = models.CharField(max_length=8, verbose_name="颁发国家")

    class Meta:
        db_table = 'ms_passport'  # 指定表的名字
        verbose_name = "护照"
        verbose_name_plural = "护照"

    objects = models.Manager()  # 加上这句就可以了
