from abc import ABC, abstractmethod

class BaseProduct(ABC):
    @abstractmethod
    def __init__(self, name, description, price, quantity):
        pass

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, new_price):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

class LoggingMixin:
    def __init__(self, *args, **kwargs):
        print(f"Создан объект {self.__class__.__name__} с параметрами: {args}, {kwargs}")
        super().__init__(*args, **kwargs)

class Product(LoggingMixin, BaseProduct):
    def __init__(self, name, description, price, quantity):
        if quantity <= 0:
            raise ValueError("Товар с нулевым или отрицательным количеством не может быть добавлен")
        if price <= 0:
            raise ValueError("Цена товара должна быть положительной")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__(name, description, price, quantity)

    @property
    def price(self):
        """Геттер для приватного атрибута price."""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для приватного атрибута price с проверкой на положительное значение."""
        if new_price <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        self.__price = new_price

    def __str__(self):
        """Строковое представление объекта Product."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Магический метод сложения для объектов Product."""
        if not isinstance(other, Product):
            raise TypeError("Операнд справа должен иметь тип Product или его наследников")
        return self.price * self.quantity + other.price * other.quantity

class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        return f"{self.name}, {self.model}, {self.memory}, {self.color}, {self.price} руб. Остаток: {self.quantity} шт."

class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return f"{self.name}, {self.country}, {self.germination_period}, {self.color}, {self.price} руб. Остаток: {self.quantity} шт."

class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1

    def add_product(self, product):
        """Добавляет продукт в список и увеличивает счетчик продуктов."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты типа Product или его наследников.")
        self.__products.append(product)
        Category.product_count += 1
        print("Товар добавлен")

    @property
    def products(self):
        """Геттер для приватного атрибута products."""
        return "\n".join(str(product) for product in self.__products)

    def __str__(self):
        """Строковое представление объекта Category."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @classmethod
    def new_product(cls, product_data):
        """Создает новый продукт на основе словаря."""
        return Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    def __iter__(self):
        """Возвращает итератор по продуктам категории."""
        return CategoryIterator(self)

    def average_price(self):
        try:
            total_price = sum(product.price for product in self.__products)
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0

class CategoryIterator:
    def __init__(self, category):
        self._category = category
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._category._Category__products):
            product = self._category._Category__products[self._index]
            self._index += 1
            return product
        else:
            raise StopIteration
