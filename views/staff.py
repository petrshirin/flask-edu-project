from flask import Request, render_template, redirect
from .base import BaseView
from logic.models import Staff, Waiter, Order, Position, Table


class StaffView(BaseView):

    model = Staff
    fields = ['FIO', 'phone', 'position', ]


class PositionView(BaseView):

    model = Position
    fields = ['name', 'salary']


class WaiterView(BaseView):

    model = Waiter
    fields = ['staff', 'tables']

    def create(self, request: Request):
        data = request.form.copy()
        waiter = Waiter()
        for name, value in data.items():
            if name == 'staff':
                waiter.staff_id = value
        waiter.save()
        for value in request.form.getlist('tables[]'):
            waiter.tables.add(Table.get_by_id(int(value)))

        return redirect('/waiter/')

    def edit(self, request: Request, pk: int):
        data = request.form.copy()
        waiter = self.model.get_by_id(pk)
        try:
            waiter.staff_id = int(data['staff'])
            waiter.tables.clear()
            tables = []
            for value in request.form.getlist('tables[]'):
                tables.append(Table.get_by_id(int(value)))
            waiter.tables.add(tables)
            waiter.save()
        except ValueError:
            pass
        return redirect('/waiter/')


class OrderView(BaseView):

    model = Order
    fields = ['waiter', 'table', 'price']

