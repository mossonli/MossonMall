from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "用户"

    def ready(self):
        # 加载自定义的信号
        import users.signals
