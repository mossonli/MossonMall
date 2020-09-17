## drf用户认证(tokenAuthentication)
### settings.py
```python
INSTALLED_APPS = [
    'rest_framework.authtoken'
]

makemigrations
migrate
生成一个表：authtoken_token
```
```python
'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
```
## 在drf中引入用户认证
### 1 urls.py
```python
from rest_framework.authtoken import views
urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
]
```
### 2 在settings.py中添加
```python
REST_FRAMEWORK = {
    # 默认就是使用的AUTHENTICATION_CLASSES(BasicAuthentication SessionAuthentication)
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}
```
### 3 自定义认证
```python
from rest_framework.authentication import TokenAuthentication

class GoodsListViewset():
    ...
    authentication_classes = (TokenAuthentication, )
```
### 4 jwt(json web token)用户认证
> jwt 的特点
```text
1 简洁
2 可以通过url，post参数或者在http header发送，数据小，传输速度快，自包含(self-contained)
3 负载中包含了所有用户所需要的信息，避免了多次查询数据库
```
> jwt的组成
```text
jwt的组成：Header.Payload.Signature

1 header:的组成，加密算法以及token类型
{
    "alg": "HS256",
    "typ": "JWT"
}
header会使用Base64编码组成jwt的一部分，可能会被反解
2 Payload的组成(存放信息：用户的id、签发者、过期时间、面向用户、接收方、签发时间等)
{
    "iss": "luffy JWT", # 签发者
    "iat": "1441595332",    #签发时间
    "exp": "1441595332",    #过期时间
    "aud": "www.luffy.com",    #接收方
    "sub": "luffy@qq.com",    #面向用户
}
3 Signature
前两部分都是使用base64进行编码，前端可以解开知道里面的信息，signature需要使用编码后的header和payload以及我们提供的一个秘钥
然后使用header中指定的签名算法进行签名，签名的作用是保证jwt没有被篡改！
base64url(
    HMACSHA256(
      base64UrlEncode(header) + "." + base64UrlEncode(payload),
      your-256-bit-secret (秘钥加盐)
    )
)
```
### 5 djangorestframework中使用jwt
> 1 安装
```python
pip install djangorestframework-jwt
```
> 2 settings 中REST_FRAMEWORK配置
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
```
> url配置
```python
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    re_path(r'^api-jwt-token-auth/', obtain_jwt_token),
]
```