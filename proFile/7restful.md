## restful
representational state transfer 资源状态转移
## 网络状态码
```text
1xx：相关信息    api中不需要1xx的状态码
2xx：操作成功
3xx：重定向
4xx：客户端错误
5xx：服务器错误
```
### 2xx
```text
GET: 200 OK
POST: 201 Created   表示生成了新的资源
PUT: 200 OK
PATCH: 200 OK
DELETE: 204 No Content  返回204表示资源已经不存在
202 表示服务器已经收到请求
```
### 3xx
```text
301 永久重定向 api 用不到
302 暂时重定向 api 用不到
303 see other 表示参考另一个url，收到303浏览器不会自动跳转而是让用户去决定应该怎么办

```
### 4xx
```text
4xx状态码表示客户端错误，主要有下面几种。
400 Bad Request：服务器不理解客户端的请求，未做任何处理。
401 Unauthorized：用户未提供身份验证凭据，或者没有通过身份验证。
403 Forbidden：用户通过了身份验证，但是不具有访问资源所需的权限。
404 Not Found：所请求的资源不存在，或不可用。
405 Method Not Allowed：用户已经通过身份验证，但是所用的 HTTP 方法不在他的权限之内。
410 Gone：所请求的资源已从这个地址转移，不再可用。
415 Unsupported Media Type：客户端要求的返回格式不支持。比如，API 只能返回 JSON 格式，但是客户端要求返回 XML 格式。
422 Unprocessable Entity ：客户端上传的附件无法处理，导致请求失败。
429 Too Many Requests：客户端的请求次数超过限额。
```
### 5xx
```text
5xx状态码表示服务端错误。一般来说，API 不会向用户透露服务器的详细信息，所以只要两个状态码就够了。
500 Internal Server Error：客户端请求有效，服务器处理时发生了意外。
503 Service Unavailable：服务器无法处理请求，一般用于网站维护状态。
```