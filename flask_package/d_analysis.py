from flask_package.models import Inventory, Sales, Transaction
# from datetime import date, datetime, timedelta
import datetime
from dateutil.relativedelta import relativedelta


def t_income():
    income = 0
    all_sales = Sales.query.all()
    for sale in all_sales:
        income += sale.t_price
    return income


def t_investment():
    investment = 0
    all_inv = Inventory.query.all()
    for inv in all_inv:
        investment += inv.t_price
    return investment


def t_inv_remaining():
    remaining = 0
    all_inv = Inventory.query.filter(Inventory.remaining > 0).order_by(Inventory.id.desc())
    for inv in all_inv:
        remaining += inv.remaining
    return remaining


def remain_cash():
    cash_out = 0
    transactions = Transaction.query.all()
    for trans in transactions:
        cash_out += trans.amount
    cash = t_income() - cash_out
    return cash


def operation_cost():
    cost = 0
    transactions = Transaction.query.filter_by(type=2).all()
    for trans in transactions:
        cost += trans.amount
    return cost


def trans_type_one():
    cost = 0
    transactions = Transaction.query.filter_by(type=1).all()
    for trans in transactions:
        cost += trans.amount
    return cost


def PL():
    return t_income() - t_investment() - operation_cost()


def month_sale(x,y=0):
    day = datetime.datetime.now().day
    if x != 0:
        date1 = datetime.datetime.combine(datetime.date.today() - relativedelta(months=x, days=day),
                                          datetime.time(0, 0))

        date2 = datetime.datetime.combine(datetime.date.today() - relativedelta(months=y,days=day),
                                          datetime.time(0, 0))
    else:
        date1 = datetime.datetime.combine(datetime.date.today() - relativedelta(months=x, days=day),
                                          datetime.time(0, 0))

        date2 = datetime.datetime.combine(datetime.date.today(),
                                          datetime.time(0, 0))

    # print(date1, date2)
    trans = Sales.query.filter(Sales.date > date1).filter(Sales.date <= date2)
    return trans


def month_income(x, y):
    income = 0
    sales = month_sale(x, y)
    for sale in sales:
        income += sale.t_price
    return income


def month_trans(x):
    day = datetime.datetime.now().day
    if x != 0:
        date1 = datetime.datetime.combine(datetime.date.today() - relativedelta(months=x, days=day),
                                          datetime.time(0, 0))

        date2 = datetime.datetime.combine(datetime.date.today() - relativedelta(days=day),
                                          datetime.time(0, 0))
    else:
        date1 = datetime.datetime.combine(datetime.date.today() - relativedelta(months=x, days=day),
                                          datetime.time(0, 0))

        date2 = datetime.datetime.combine(datetime.date.today(),
                                          datetime.time(0, 0))

    # print(date1, date2)
    trans = Transaction.query.filter(Sales.date > date1).filter(Sales.date <= date2)
    return trans


def month_trans_amount(x):
    amount = 0
    transactions = month_trans(x)
    for trans in transactions:
        amount += trans.amount
    return amount


def month_inv(x, y):
    day = datetime.datetime.now().day
    if x != 0:
        date1 = datetime.datetime.combine(datetime.date.today() - relativedelta(months=x, days=day),
                                          datetime.time(0, 0))

        date2 = datetime.datetime.combine(datetime.date.today() - relativedelta(months=y, days=day),
                                          datetime.time(0, 0))
    else:

        date1 = datetime.datetime.combine(datetime.date.today() - relativedelta(months=x, days=day),
                                          datetime.time(0, 0))

        date2 = datetime.datetime.combine(datetime.date.today(),
                                          datetime.time(0, 0))

    # print(date1, date2)
    trans = Inventory.query.filter(Inventory.date > date1).filter(Inventory.date <= date2)
    return trans


def month_inv_amount(x, y):
    amount = 0
    investment = month_inv(x, y)

    for inv in investment:
        amount += inv.t_price
    # print(x, y, amount)
    return amount


