from peewee import *

conn = SqliteDatabase('db2.sqlite3')


class BaseModel(Model):

    class Meta:
        database = conn

    def get_all_values(self):
        pass

    def get_table_name(self):
        return self._meta.table_name


class RestaurantInfo(BaseModel):
    id = AutoField(primary_key=True, column_name='id')
    address = CharField(column_name='address', max_length=255, null=True)
    phone = CharField(column_name='phone', max_length=20, null=True)

    def __str__(self):
        return f"{self.address} {self.phone}"

    def get_all_values(self):
        return [self.id, self.address, self.phone]


class Restaurant(BaseModel):
    id = AutoField(primary_key=True, column_name='id')
    name = CharField(column_name='name', max_length=255)
    info = ForeignKeyField(RestaurantInfo, related_name='restaurant', unique=True, on_delete='CASCADE')

    def __str__(self):
        return f'{self.name} {self.info if self.info else ""}'

    def get_all_values(self):
        return [self.id, self.name, self.info]


class Position(BaseModel):
    id = AutoField(primary_key=True, column_name='id')
    name = CharField(column_name='name', max_length=255)
    salary = DecimalField(max_digits=10, decimal_places=2)

    def get_all_values(self):
        return [self.id, self.name, self.salary]

    def __str__(self):
        return f'{self.name}'


class Staff(BaseModel):
    id = AutoField(primary_key=True, column_name='id')
    FIO = CharField(column_name='FIO', max_length=512)
    phone = CharField(column_name='phone', max_length=20)
    position = ForeignKeyField(Position, related_name='staffs', on_delete='CASCADE')

    def get_all_values(self):
        return [self.id, self.FIO, self.phone, self.position]

    def __str__(self):
        return f"{self.FIO} {self.position}"


class Table(BaseModel):
    id = AutoField(primary_key=True, column_name='id')
    number = IntegerField()
    status = IntegerField()

    def get_all_values(self):
        return [self.id, self.number, self.status]

    def __str__(self):
        return f"Table {self.number}"


class Waiter(BaseModel):
    id = AutoField(primary_key=True, column_name='id')
    staff = ForeignKeyField(Staff, related_name='waiters', on_delete='CASCADE')
    tables = ManyToManyField(Table, backref='waiters')

    def get_all_values(self):
        return [self.id, self.staff, self.tables_to_view()]

    def tables_to_view(self):
        result = ""
        for table in self.tables:
            result += f"{table}\n"
        return result

    def __str__(self):
        return f'{self.staff}'


class Order(BaseModel):
    id = AutoField(primary_key=True, column_name='id')
    waiter = ForeignKeyField(Waiter, related_name='waiters', on_delete='CASCADE')
    table = ForeignKeyField(Table, related_name='tables', on_delete='CASCADE')
    price = DecimalField(max_digits=10, default=2)

    def get_all_values(self):
        return [self.id, self.waiter, self.table, self.price]

    def __str__(self):
        return f"{self.waiter} {self.table} {self.price}"


# class WaiterTable(BaseModel):
#     waiter = ForeignKeyField(Waiter)
#     table = ForeignKeyField(Table)
#
#     class Meta:
#         db_table = 'waiter_table_through'


if __name__ == '__main__':
    print(1)
    RestaurantInfo.create_table()
    Restaurant.create_table()
    Position.create_table()
    Staff.create_table()
    Table.create_table()
    Waiter.create_table()
    Waiter.tables.get_through_model().create_table()
    Order.create_table()
    conn.commit()

