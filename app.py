from flask import Flask, render_template, redirect
from logic.models import *
from flask_peewee.db import Database
from views.base import BaseView
from views.restaurant import RestaurantView, RestaurantInfoView, TableView
from views.staff import StaffView, WaiterView, OrderView, PositionView
from flask.app import request

app = Flask(__name__)
DATABASE = {
    'name': 'db1.sqlite3',
    'engine': 'peewee.SqliteDatabase',
}
app.config.from_object(__name__)
DEBUG = True
SECRET_KEY = 'ssshhhh'
db = Database(app)

register_models = {
    'restaurant': RestaurantView(),
    'restaurantinfo': RestaurantInfoView(),
    'table': TableView(),
    'staff': StaffView(),
    'waiter': WaiterView(),
    'order': OrderView(),
    'position': PositionView()
}


@app.route('/')
def index_view():
    return render_template('index.html', register_models=register_models.keys())


@app.route('/<instance_name>/', methods=['GET'])
def model_view(instance_name: str):
    for name, model in register_models.items():
        if name == instance_name:
            return model.view(request)
    return redirect('/')


@app.route('/<instance_name>/create/', methods=["GET"])
def form_view(instance_name: str):
    for name, model in register_models.items():
        if name == instance_name:
            return model.view_form(request, 'create')
    return redirect('/')


@app.route('/<instance_name>/create/', methods=["POST"])
def save_view(instance_name: str):
    for name, model in register_models.items():
        if name == instance_name:
            return model.create(request)
    return redirect('/')


@app.route('/<instance_name>/edit/<pk>', methods=["GET"])
def form_edit_view(instance_name: str, pk: int):
    for name, model in register_models.items():
        if name == instance_name:
            return model.view_form(request, 'edit', pk)
    return redirect('/')


@app.route('/<instance_name>/edit/<pk>', methods=["POST"])
def edit_view(instance_name: str, pk: int):
    for name, model in register_models.items():
        if name == instance_name:
            return model.edit(request, pk)
    return redirect('/')


@app.route('/<instance_name>/delete/<pk>', methods=["get"])
def delete_view(instance_name: str, pk: int):
    for name, model in register_models.items():
        if name == instance_name:
            return model.delete(request, pk)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
