from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavSerializer(serializers.ModelSerializer):
    """"""
    # 获取当前的用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav
        validators = [UniqueTogetherValidator(
            queryset=UserFav.objects.all(),
            fields=("user", "goods"),
            message="已经收藏了",
        )]
        fields = ("user", "goods", "id")


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    # 获取当前的用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")  # read_only 只选择不提交

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")  # read_only 只选择不提交

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")
