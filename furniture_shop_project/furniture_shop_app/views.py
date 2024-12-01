from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from psycopg2 import IntegrityError, errors
from .models import Good, Order, Client
from .db_utils import get_db_connection
from .forms import GoodForm, OrderForm, ClientForm
import re, datetime
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

def is_manager(user):
    return user.groups.filter(name='Managers').exists()

def welcome(request):
    return render(request, 'welcome.html')

def check_manager_access(user):
    if not user.groups.filter(name='Managers').exists():
        return render(None, 'access_denied.html')
    return None

def list_goods(request):
    goods = Good.objects.all()
    is_manager = request.user.groups.filter(name='Managers').exists()
    is_client = request.user.groups.filter(name='Clients').exists()
    
    context = {
        'goods': goods,
        'is_manager': is_manager,
        'is_client': is_client,
    }
    return render(request, 'list_goods.html', context)

@login_required
def create_order(request, id_good):
    good = get_object_or_404(Good, id_good=id_good)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.id_client = Client.objects.get(id_client=request.user.id)  # Получаем клиента по id_client
            order.id_good = good
            order.data = datetime.date.today()  # Убедитесь, что поле data заполняется
            order.total = good.price * form.cleaned_data['quantity']  # Рассчитываем total
            order.save()
            return redirect('confirm_order', order_id=order.id_order)
        else:
            print("Form is not valid")
            print(form.errors)  # Вывод ошибок валидации в консоль
    else:
        form = OrderForm(initial={'id_good': good})
    return render(request, 'create_order.html', {'form': form, 'id_good': id_good})

@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id_order=order_id)
    if request.method == 'POST':
        if 'confirm' in request.POST:
            return redirect('list_goods')
        elif 'cancel' in request.POST:
            order.delete()
            return redirect('list_goods')
    return render(request, 'confirm_order.html', {'order': order})

@login_required
@user_passes_test(is_manager)
def list_orders(request):
    if request.user.groups.filter(name='Managers').exists():
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(id_client=request.user.id)
    return render(request, 'list_orders.html', {'orders': orders})

@login_required
def update_order(request, id_order):
    order = get_object_or_404(Order, id_order=id_order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('list_orders')
    else:
        form = OrderForm(instance=order)
    return render(request, 'update_order.html', {'form': form, 'order': order})

@login_required
def delete_order(request, id_order):
    order = get_object_or_404(Order, id_order=id_order)
    if request.method == 'POST':
        order.delete()
        return redirect('list_orders')
    return render(request, 'delete_order.html', {'order': order})

@login_required
def insert_good(request):
    if request.method == 'POST':
        form = GoodForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            mass = form.cleaned_data['mass']

            try:
                with get_db_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute('CALL insert_good(%s, %s, %s, %s)', [title, description, price, mass])
                        connection.commit()
                return redirect('list_goods')
            except IntegrityError as e:
                return render(request, 'insert_good.html', {'form': form, 'error': str(e)})
    else:
        form = GoodForm()
    return render(request, 'insert_good.html', {'form': form})

@login_required
def update_good(request, id_good):
    good = get_object_or_404(Good, id_good=id_good)
    if request.method == 'POST':
        form = GoodForm(request.POST, instance=good)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            mass = form.cleaned_data['mass']

            try:
                with get_db_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute('CALL update_good(%s, %s, %s, %s, %s)', [id_good, title, description, price, mass])
                        connection.commit()
                return redirect('list_goods')
            except Exception as e:
                return render(request, 'update_good.html', {'form': form, 'good': good, 'error': str(e)})
    else:
        form = GoodForm(instance=good)
    return render(request, 'update_good.html', {'form': form, 'good': good})

@login_required
def delete_good(request, id_good):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('CALL delete_good(%s)', [id_good])
                connection.commit()
        return redirect('list_goods')
    except errors.ForeignKeyViolation as e:
        return HttpResponse("Невозможно удалить товар - сначала нужно завершить заказы с этим товаром", status=400)

@login_required
@user_passes_test(is_manager)
def list_clients(request):
    clients = Client.objects.all()
    return render(request, 'list_clients.html', {'clients': clients})

@login_required
@user_passes_test(is_manager)
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_clients')
    else:
        form = ClientForm()
    return render(request, 'create_client.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def update_client(request, id_client):
    client = get_object_or_404(Client, id_client=id_client)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('list_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'update_client.html', {'form': form, 'client': client})

@login_required
@user_passes_test(is_manager)
def delete_client(request, id_client):
    client = get_object_or_404(Client, id_client=id_client)
    client.delete()
    return redirect('list_clients')

@login_required
def latest_orders(request):
    with get_db_connection().cursor() as cursor:
        cursor.callproc('get_latest_orders')
        result = cursor.fetchall()

    orders = []
    for row in result:
        order_data = row[0]
        pattern = re.compile(r'id_order: (\d+), id_client: (\d+), id_good: (\d+), id_editor: (None|\d+), quantity: (\d+), data: (\d{4}-\d{2}-\d{2}), delivery: (\w+), total: (\d+\.\d+)')
        matches = pattern.findall(order_data)
        for match in matches:
            order = {
                'id_order': int(match[0]),
                'id_client': int(match[1]),
                'id_good': int(match[2]),
                'id_editor': None if match[3] == 'None' else int(match[3]),
                'quantity': int(match[4]),
                'data': match[5],
                'delivery': match[6],
                'total': float(match[7])
            }
            orders.append(order)

    return render(request, 'latest_orders.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        client_form = ClientForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            client = client_form.save(commit=False)
            client.id_client = user.id  # Связываем id_client с id пользователя
            client.save()

            # Добавление пользователя в группу Clients
            group = Group.objects.get(name='Clients')
            user.groups.add(group)

            return redirect('login')
    else:
        user_form = UserCreationForm()
        client_form = ClientForm()
    return render(request, 'register.html', {'user_form': user_form, 'client_form': client_form})