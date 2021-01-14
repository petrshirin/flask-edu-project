from flask import Request, render_template, redirect
from peewee import Field, CharField, TextField, IntegerField, \
    ForeignKeyField, AutoField, DecimalField, ManyToManyField, \
    ModelSelect

from logic.models import BaseModel
from jinja2 import Template
from typing import List


class BaseView(object):
    model = BaseModel
    fields = []
    register_models = [
        'restaurant',
        'restaurantinfo',
        'table',
        'staff',
        'waiter',
        'order',
        'position'
    ]
    form_fields = {}

    def render_form(self, main_obj: BaseModel):
        form_fields = {}
        form_fields.update(self.model()._meta.fields)
        form_fields.update(self.model()._meta.manytomany)
        form_fields = self.form_fields if self.form_fields else form_fields
        form = ""
        for name, field_type in form_fields.items():
            print(name, field_type)
            form += self._generate_html(name, field_type, main_obj) + '\n'
        return form


    @staticmethod
    def _generate_html(name: str, field_type: Field, main_obj: BaseModel = None) -> str:

        def generate_options(option_objects: ModelSelect, selected_options: ModelSelect):
            html_for_options = '<option></option>\n'
            for obj in option_objects:
                if selected_options:
                    try:
                        selected = "selected" if obj in selected_options else ""
                    except TypeError:
                        selected = "selected" if obj in [selected_options] else ""
                else:
                    selected = ''
                html_for_options += f'<option value="{obj.id}" {selected}>{obj}</option>\n'
            return html_for_options

        html = ''
        if isinstance(field_type, AutoField):
            return html

        elif isinstance(field_type, IntegerField) or isinstance(field_type, DecimalField):
            html = f'''<label for="{name}">
    {name}
    <input type="number" class="form-control" 
name="{name}" id="{name}" value="{getattr(main_obj, name, '') if getattr(main_obj, name, '') else ''}">
</label>'''

        elif isinstance(field_type, CharField) or isinstance(field_type, TextField):
            html = f'''<label for="{name}">
    {name}
    <input type="text" class="form-control" 
name="{name}" id="{name}" value="{getattr(main_obj, name, '') if getattr(main_obj, name, '') else ''}">
</label>'''

        elif isinstance(field_type, ForeignKeyField):
            objects = field_type.rel_model.select()
            html = f'''<label>
    {name}
<select name="{name}" id="{name}" class="form-control">
    {generate_options(objects, getattr(main_obj, name, None) if main_obj.id else None)}
</select>
</label>'''
        elif isinstance(field_type, ManyToManyField):
            objects = field_type.rel_model.select()
            html = f'''<label>
                {name}
            <select name="{name}[]" id="{name}" multiple class="form-control">
                {generate_options(objects, getattr(main_obj, name, None))}
            </select>
            </label>'''
        print(html)
        return html

    def view(self, request: Request):
        table_name = self.model._meta.table_name
        objects = self.model.select()
        return render_template('view_list.html',
                               objects=objects,
                               fields=self.fields,
                               model_name=table_name,
                               register_models=self.register_models)

    def view_form(self, request: Request, method: str, pk: int = None):
        model_name = self.model._meta.table_name
        obj = self.model() if method == 'create' else self.model.select().where(self.model.id == pk).first()

        return render_template('model_form.html',
                               model_name=model_name,
                               method=method,
                               obj=obj,
                               form=self.render_form(obj))

    def create(self, request: Request):
        model_name = self.model._meta.table_name
        self.model.create(**request.form)
        return redirect(f'/{model_name}/')

    def edit(self, request: Request, pk: int):
        print(request.form)
        model_name = self.model._meta.table_name
        md = self.model.get_by_id(pk)
        for key, value in request.form.items():
            if getattr(md, key, '`') is not '`':
                setattr(md, key, value)
        md.save()
        return redirect(f'/{model_name}/')

    def delete(self, request: Request, pk: int):
        md = self.model.get_by_id(pk)
        model_name = self.model._meta.table_name
        md.delete_instance()
        return redirect(f'/{model_name}/')






