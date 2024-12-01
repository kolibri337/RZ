from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)

class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(unique=True, max_length=20)
    shirota = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    dolgota = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'

class ClientsSection(models.Model):
    id_client = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    shirota = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    dolgota = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients_section'

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)

class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class Editor(models.Model):
    id_editor = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    post = models.CharField(max_length=255)
    phone = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'editors'

class FurnitureShopAppClient(models.Model):
    id_client = models.AutoField(primary_key=True)
    type = models.CharField(max_length=1)
    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20)
    shirota = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    dolgota = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'furniture_shop_app_client'

class FurnitureShopAppEditor(models.Model):
    id_editor = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    post = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'furniture_shop_app_editor'

class Good(models.Model):
    id_good = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    price = models.IntegerField()
    mass = models.DecimalField(max_digits=6, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'goods'

    def __str__(self):
        return self.title

class FurnitureShopAppOrder(models.Model):
    id_order = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    data = models.DateField()
    delivery = models.CharField(max_length=10)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    id_client = models.ForeignKey(FurnitureShopAppClient, models.DO_NOTHING)
    id_editor = models.ForeignKey(FurnitureShopAppEditor, models.DO_NOTHING, blank=True, null=True)
    id_good = models.ForeignKey(Good, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'furniture_shop_app_order'

class Order(models.Model):
    id_order = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='id_client', blank=True, null=True)
    id_good = models.ForeignKey(Good, models.DO_NOTHING, db_column='id_good', blank=True, null=True)
    id_editor = models.ForeignKey(Editor, models.DO_NOTHING, db_column='id_editor', blank=True, null=True)
    quantity = models.IntegerField()
    data = models.DateField(blank=True, null=True)
    delivery = models.CharField(max_length=10)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'

class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'