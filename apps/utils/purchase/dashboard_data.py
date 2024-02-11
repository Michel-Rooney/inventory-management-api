import calendar
# import locale
from dateutil.relativedelta import relativedelta

from django.db.models import Sum, Max
from django.utils import timezone

from rest_framework.response import Response

from apps.utils import querys


def get_last_day(**kwargs):
    date_now = timezone.now()
    return (date_now - relativedelta(**kwargs)).date()


def get_total_price(models):
    total = models.aggregate(total=Sum('total_price'))['total']
    return round(total, 2) if total is not None else total


def get_total_purchase_price(models):
    total = models.aggregate(total=Sum('total_purchase_price'))['total']
    return round(total, 2) if total is not None else total


def get_gain(sale_price, purchase_price):
    if (sale_price is None) or (purchase_price is None):
        return 0

    return (sale_price - purchase_price)


def get_models_range_date(company, minimal_date, max_date):
    return querys.get_purchases(
        company=company,
        create_at__range=[minimal_date, max_date],
    )


def get_model_date(date):
    return querys.get_purchases(create_at__date=date)


def get_labels(date, labels: list, format: str):
    day = date.strftime(format)
    labels.append(day.title())

    return labels


def get_list_values(date, is_year, company, values):
    model = get_model_date(date)
    value = 0

    if is_year:
        minimal_date = timezone.datetime(date.year, date.month, 1)
        last_day_month = calendar.monthrange(date.year, date.month)[1]
        max_date = timezone.datetime(date.year, date.month, last_day_month)

        model = get_models_range_date(company, minimal_date, max_date)

    if model is not None:
        value = get_total_price(model)
        value = value if value is not None else 0

        purchase_price = get_total_purchase_price(model)
        if purchase_price is None:
            purchase_price = 0

        gain = get_gain(value, purchase_price)

    values.append(value)

    return values, value, gain


def append_data(data, date, value, gain):
    data.append({
        "date": date.strftime("%d/%m/%Y"),
        "total_price": value,
        "gain": gain
    })

    return data


def get_most_sold_product(company, minimal_date, date_now):
    products = querys.get_log_products(
        company=company,
        create_at__range=[minimal_date, date_now],
    )
    most_sold_product = products.values('name').annotate(
        total_quantity_sold=Sum('purchase__log_products__quantity')
    ).order_by('-total_quantity_sold').first()

    if most_sold_product is None:
        most_sold_product = {}
        most_sold_product['name'] = 'Não há produto mais vendido'

        return most_sold_product

    most_sold_products = querys.get_log_products(
        name=most_sold_product.get('name')
    )

    total_sale = 0
    for product in most_sold_products:
        total_sale += (product.quantity * product.sale_price)

    most_sold_product['total_sale'] = total_sale

    return most_sold_product


def get_biggest_sale_date(models):
    biggest_sale = models.annotate(
        biggest_price=Max('total_price')
    ).order_by('-biggest_price').first()

    if biggest_sale is None:
        return 'Não há o dia mais vedido'

    return biggest_sale.create_at


def get_date_values(
    company, time, format: str, timedelta_field: str, is_year=False
):
    date_now = timezone.now()
    dashboard_data = {}
    labels = []
    values = []
    data = []

    # locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')
    for i in range(time, -1, -1):
        date = get_last_day(**{timedelta_field: i})

        # Labels
        labels = get_labels(date, labels, format)

        # List Values
        values, value, gain = get_list_values(date, is_year, company, values)

        # Data
        data = append_data(data, date, value, gain)

    minimal_date = get_last_day(**{timedelta_field: time})
    models = querys.get_purchases(
        company=company,
        create_at__range=[minimal_date, date_now],
    )

    total_price = get_total_price(models)
    total_purcahse_price = get_total_purchase_price(models)
    gain = get_gain(total_price, total_purcahse_price)

    biggest_sale_date = get_biggest_sale_date(models)
    most_sold_product = get_most_sold_product(company, minimal_date, date_now)

    dashboard_data = {
        "labels": labels,
        "values": values,
        "total_price": total_price,
        "gain": gain,
        "data": data,
        "biggest_sale": {
            'data': biggest_sale_date,
            'value': total_price,
        },
        "most_sold_product": most_sold_product,
    }

    # locale.setlocale(locale.LC_TIME, '')
    return dashboard_data


def get_dashboard_data(request: any) -> dict:
    types = ["week", "month", "year"]
    request_type = request.query_params.get("type", "")

    if request_type not in types:
        return Response({"detail": "Tipo de atributo da url inválido."})

    company = request.user.id

    if request_type == "week":
        data = get_date_values(company, 6, "%A", "days")

    elif request_type == "month":
        data = get_date_values(company, 30, "%d/%b", "days")

    elif request_type == "year":
        data = get_date_values(
            company, 11, "%B", "months", is_year=True
        )

    return data
