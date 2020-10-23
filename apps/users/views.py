from django.shortcuts import render

# Create your views here
from random import choice
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from .models import VerifyCode
from MossonMall.settings import YunPianSettings

from utils.yunpiancode import Yunpian

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户登录验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            print(e)
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    # 生成四位数的验证码
    @property
    def gennrate_code(self):
        """
        生成四位验证码
        :return:
        """
        seeds = "0123456789"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        yun_pian = Yunpian(YunPianSettings["apikey"])
        code = self.gennrate_code
        sms_status = yun_pian.send_single_sms(code=code, mobile=mobile)
        if sms_status["code"] != 0:
            return Response({"mobile": sms_status["msg"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)


class UserRegViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    用户注册
    """
    # serializer_class = UserRegSerializer # 动态的去获取序列化器
    queryset = User.objects.all()
    # 认证
    # JSONWebTokenAuthentication jwt的认证
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    # 动态获取 serializer
    def get_serializer_class(self):
        """
        重写 get_serializer_class 跟进action的不同选择不同的序列化器
        :return:
        """
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    # 权限
    def get_permissions(self):
        """
        重写 get_permissions 方法，根据action的不同执行不同的权限
        :return:
        """
        # action 放到self里面，只有在 viewsets 里面才有，使用apiView就没有
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    # 前端生成 token 用于用户注册之后直接登录
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        """
        只返回当前的登录的对象，必须是已经登录的状态
        :return:
        """
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
