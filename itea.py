from sqlalchemy import MetaData,Table, Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship

engine = create_engine("mysql+pymysql://listener:localhost@192.168.1.100/python")
Base = declarative_base()
Session = sessionmaker(bind=engine)
metadata = MetaData()

class Klass(Base):
    __tablename__ = 'Masynyn_klasy'
    id = Column(Integer(), primary_key=True)
    name = Column(String(200), nullable=False, unique=True)

class Currencies(Base):
    __tablename__ = "Pul_birligi" #TMT, Rubl ya-da Dollar
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

class CarName(Base):
    __tablename__ = "Masynyn_ady"
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False, unique=True)

class OperationTypes(Base):
    __tablename__ = "Opeasiyalryn_gornusi"
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

class Products(Base):
    __tablename__ = "Harytlar"
    id = Column(Integer(), primary_key=True)
    price = Column(Float(), nullable=False, default=0)
    quantity = Column(Float(), nullable=False, default=0)
    klass = Column(Integer(), ForeignKey('Masynyn_klasy.id'))
    currencies = Column(Integer(), ForeignKey('Pul_birligi.id'))
    car_name =Column(Integer(), ForeignKey('Masynyn_ady.id'))
    klass= relationship('Klass')
    currency = relationship('Currencies')
    name = relationship('CarName')

    def __str__(self):
        return f'Product[id={self.id}, price={self.price}, quantity={self.quantity}, klass={self.unit.name}, currencies={self.currency.name}, car_name={self.name.name}]'

class IncoomeExpense(Base):
    __tablename__ = 'Girdeyji-Cykdayjy'
    id = Column(Integer(), primary_key=True)
    quantity = Column(Float(), nullable=False, default=0)
    operation_types = Column(Integer(), ForeignKey('OperationTypes.id'))
    products = Column(Integer(), ForeignKey('Products.id'))

Base.metadata.create_all(engine)

def get_klass(klass:str)->int:
    session = Session()
    if session.query(Klass).filter(Klass.name==klass).count()>0:
        return session.query(Klass).filter(Klass.name==klass).first().id
    _klass = Klass(name=klass)
    session.add(_klass)
    session.commit()
    return _klass.id

def get_currency(currency:str)->int:
    session= Session()
    if session.query(Currencies).filter(Currencies.name==currency).count()>0:
        return session.query(Currencies).filter(Currencies.name==currency).first().id
    _currency = Currencies(name=currency)
    session.add(_currency)
    session.commit()
    return _currency.id

def get_operation_types(types:str)->int:
    session= Session()
    if session.query(OperationTypes).filter(OperationTypes.name==types).count()>0:
        return session.query(OperationTypes).filter(OperationTypes.name==types).first().id
    _types = OperationTypes(name=types)
    session.add(_types)
    session.commit()
    return _types.id

def get_name(name:str)->int:
    session = Session()
    if session.query(CarName).filter(CarName.name==name).count()>0:
        return session(CarName).filter(CarName.name==name).first().id
    car_name=CarName(name=name)
    session.add(car_name)
    session.commit()
    return car_name.id

def  add_product():
    try:
        name =input("Enter car name: ")
        price = float(input(f"Enter priceof {name}: "))
        quantity= float(input(f"Enter quantity of {name}: "))
        klass = input(f'Enter class of {name}')
        currency = input(f'Enter currency of {name}')
        product = Products(price=price,quantity=quantity, klass=get_klass(klass), currencies= get_currency(currency), car_name= get_name(name))
        session = Session()
        session.add(product)
        session.commit()
        id = product.id
        session = Session()
        income_expence = IncoomeExpense(products=id, operation_types= get_operation_types('income'), quantity=quantity)
        session.add(income_expence)
        session.commit()
    except Exception as e:
        print(e)

def list_products():
    session = Session()
    for product in session.query(Products).all():
        print((product))

def delate_product():
    list_products()
    id = int(input("Enter id of product: "))
    session = Session()
    product = session.query(Products).get(id)
    name = input("enter the name: ")
    product.price = float(input(f"Enter price of {name}: "))
    product.quantity = float(input(f"Enter quantity of {name}: "))
    product.klass = get_klass(input(f"Enter the class of {name}: "))
    product.currencies = get_currency(input(f'Enter currency of {name}: '))
    product.car_name = get_name(name)
    session.add(product)
    session.commit()

def update_product():
    list_products()
    id = int(input("Enter the product: "))
    session = Session()
    product = session.query(Products).get(id)
    name = input("Enter the product name: ")
    product.price = float(input(f'Enter the price of {name}: '))
    product.quantity = float(input(f'Enter quantity of {name}: '))
    product.klass = get_klass(input(f"Enter class of {name}: "))
    product.currencies = get_currency(input(f'Enter currency of {name}: '))
    product.car_name = get_name(name)
    session.add(product)
    session.commit()

def expense_product():
    list_products()
    id = int(input("Enter id of product: "))
    session = Session ()
    real_id, real_quantity = session.query(IncoomeExpense.products, func.sum(IncoomeExpense.quantity)).filter(IncoomeExpense.products==id).group_by(IncoomeExpense.products).one()
    if real_quantity>0:
        while True:
            quantity = float(input(f'Enter expensed product quantity(max:{real_quantity}): '))
            if quantity<= real_quantity and quantity>=0:
                income_expence = IncoomeExpense(products=id, operation_types= get_operation_types('expence'), quantity=quantity)
                session.add(income_expence)
                break
    else:
        print("can not be expensed!".center(30,"-"))
    session.commit()

def list_products():
    session = Session()
    for product in session.query(Products).all():
        print(product)

def menu()->str:
    return input("1. Add product\n2. List of products\n3. Delate product\n4. Update product\n5. Expense product\n0. Exit\n-> ")

is_exit = False
while is_exit==False:
    ans = menu()
    match(ans):
        case '0':
            is_exit= True
        case '1':
            add_product()
        case '2':
            list_products()
        case '3':
            delate_product()
        case '4':
            update_product()
        case '5':
            expense_product()
        case '6':
            print('nothing')