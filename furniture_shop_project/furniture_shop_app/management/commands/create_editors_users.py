from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from furniture_shop_app.models import Editor

class Command(BaseCommand):
    help = 'Создает пользователей на основе данных из таблицы editors и добавляет их в группу Managers'

    def handle(self, *args, **kwargs):
        # Получаем группу Managers
        managers_group, created = Group.objects.get_or_create(name='Managers')

        # Получаем всех редакторов из базы данных
        editors = Editor.objects.all()

        for editor in editors:
            # Формируем имя пользователя на основе фамилии и имени
            username = f"{editor.surname.lower()}_{editor.name.lower()}"

            # Проверяем, существует ли уже пользователь с таким именем
            if not User.objects.filter(username=username).exists():
                # Создаем пользователя
                user = User.objects.create_user(
                    username=username,
                    password='password'  # Установите здесь пароль по умолчанию
                )
                # Добавляем пользователя в группу Managers
                user.groups.add(managers_group)
                self.stdout.write(self.style.SUCCESS(f'Создан пользователь {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Пользователь {username} уже существует'))