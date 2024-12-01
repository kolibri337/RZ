from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from furniture_shop_app.models import Client

class Command(BaseCommand):
    help = 'Создает пользователей на основе данных из таблицы clients и добавляет их в группу Clients'

    def handle(self, *args, **kwargs):
        # Получаем группу Clients
        clients_group, created = Group.objects.get_or_create(name='Clients')

        # Получаем всех клиентов из базы данных
        clients = Client.objects.all()

        for client in clients:
            # Формируем имя пользователя на основе фамилии и имени
            username = f"{client.surname.lower()}_{client.name.lower()}"

            # Проверяем, существует ли уже пользователь с таким именем
            if not User.objects.filter(username=username).exists():
                # Создаем пользователя
                user = User.objects.create_user(
                    username=username,
                    password='password'  # Установите здесь пароль по умолчанию
                )
                # Добавляем пользователя в группу Clients
                user.groups.add(clients_group)
                self.stdout.write(self.style.SUCCESS(f'Создан пользователь {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Пользователь {username} уже существует'))