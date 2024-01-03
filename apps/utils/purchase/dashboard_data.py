import locale

from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.utils import timezone

from apps.utils import querys


def get_last_day(**kwargs):
    date_now = timezone.now()
    return (date_now - relativedelta(**kwargs)).date()


def get_total_price(models):
    return models.aggregate(total=Sum('total_price'))['total']


def get_models_range_date(minimal_date, max_date):
    return querys.get_purchases(
        create_at__range=[minimal_date, max_date]
    )


def get_model_date(date):
    return querys.get_purchases(create_at__date=date)


def get_date_values(time, format: str, timedelta_field: str):
    date_now = timezone.now()
    dashboard_data = {}
    labels = []
    values = []
    data = []

    locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')
    for i in range(time, -1, -1):
        # Labels
        date = get_last_day(**{timedelta_field: i})
        day = date.strftime(format)
        labels.append(day.title())

        # List Values
        model = get_model_date(date)
        value = 0

        if model is not None:
            value = get_total_price(model)
        values.append(value)

        # Data
        data.append({
            "date": date.strftime("%d/%m/%Y"),
            "value": value if value is not None else 0
        })

    minimal_date = get_last_day(**{timedelta_field: i})
    models = querys.get_purchases(
        create_at__range=[minimal_date, date_now]
    )

    total = get_total_price(models)

    dashboard_data = {
        "labels": labels,
        "values": values,
        "total": total,
        "data": data
    }

    locale.setlocale(locale.LC_TIME, '')
    return dashboard_data
