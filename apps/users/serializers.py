import re
import datetime
from datetime import timedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import VerifyCode

User = get_user_model()
from MossonMall.settings import REGEX_MOBILE


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码（验证谁就要返回谁）
        :param mobile:
        :return:
        """
        # 1 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号格式不正确请重新输入")
        # 2 手机号是否已经注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经注册")
        # 3 限制验证码的发送频率
        one_min_ago = datetime.datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_min_ago, mobile=mobile).count():
            raise serializers.ValidationError("发送时间间隔较短请稍后再发")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """

    """
    # code 并不是User表中的一个字段，在保存的时候 要剔除掉这个字段
    # write_only=True serializer 对字段进行序列化的时候 就是排除 code
    code = serializers.CharField(required=True, write_only=True, min_length=4, max_length=4,label="验证码", error_messages={
        "blank": True,
        "required": "请输入验证码",
        "max_length": "验证码格式错误",
        "min_length": "验证码格式错误",
    }, help_text="验证码")  # help_text  rest api 的提示内容
    username = serializers.CharField(required=True, allow_blank=False,label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    # 方式1 重写create  方式2 利用信号量
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):
        # self.initial_data 是前端传来的form表单的内容
        # verify_records该手机号获取验证码的左右记录
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_min_ago = datetime.datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_min_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        """
        作用于serializer所有的字段之上
        :return:
        """
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        # 执行create创建的时候 会对serializer.data [也就是fields进行序列化]进行序列化
        # 如果不想某一个字段被序列化 只需要加上write_only=True 即可
        fields = ("username", "code", "mobile", "password")
