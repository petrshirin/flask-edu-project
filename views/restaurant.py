from flask import Request, render_template, redirect
from .base import BaseView
from logic.models import Restaurant, RestaurantInfo, Table


class RestaurantView(BaseView):

    model = Restaurant
    fields = ['name', 'info']

    def create(self, request: Request):
        if request.form['info']:
            try:
                super().create(request)
            except Exception as err:
                print(err)

        else:
            data = request.form.copy()
            del data['info']
            inf = RestaurantInfo.create(address='Address1', phone="+79999999999")
            Restaurant.create(**data, info=inf)
        return redirect('/restaurant/')


class RestaurantInfoView(BaseView):

    model = RestaurantInfo
    fields = ['address', 'phone']


class TableView(BaseView):

    model = Table
    fields = ['number', 'status']
    print(Table.number.field_type)
    form_fields = {'number': Table.number,
                   "status": Table.status}



