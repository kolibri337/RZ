from django.contrib import admin
from django.contrib.auth.models import Group

# Регистрация модели Group
admin.site.register(Group)

# Отмена регистрации модели Group
admin.site.unregister(Group)

class ClientGroup(Group):
    class Meta:
        proxy = True
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

class ManagerGroup(Group):
    class Meta:
        proxy = True
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'

admin.site.register(ClientGroup)
admin.site.register(ManagerGroup)