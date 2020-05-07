import abc

class Customer():
    def __init__(self, username, password):
        self.__username = username
        self._password = password
        self._pizza = None

    def get_username(self):
        return self.__username
    def get_password(self):
        return self._password
  
    def set_pizza(self,pizza):
        self._pizza = pizza


class Pizza(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_price(self):
        pass

    @abc.abstractmethod
    def get_status(self):
        pass


class Pepperoni(Pizza):
    __pizza_price = 1.0

    def get_price(self):
        return self.__pizza_price

    def get_status(self):
        return "Pepperoni"


class Supreme(Pizza):
    __pizza_price = 1.5

    def get_price(self):
        return self.__pizza_price

    def get_status(self):
        return "Supreme"


class PizzaDecorator(Pizza):
    def __init__(self, pizza):
        self.pizza = pizza

    def get_price(self):
        return self.pizza.get_price()

    def get_status(self):
        return self.pizza.get_status()


class Tomato(PizzaDecorator):
    def __init__(self, pizza):
        super(Tomato, self).__init__(pizza)
        self.__tomato_price = 2.0

    @property
    def price(self):
        return self.__tomato_price

    def get_price(self):
        return super(Tomato, self).get_price() + self.__tomato_price

    def get_status(self):
        return super(Tomato, self).get_status() + " Tomato"


class Cheese(PizzaDecorator):
    def __init__(self, pizza):
        super(Cheese, self).__init__(pizza)
        self.__cheese_price = 1.5

    @property
    def price(self):
        return self.__cheese_price

    def get_price(self):
        return super(Cheese, self).get_price() + self.__cheese_price

    def get_status(self):
        return super(Cheese, self).get_status() + " Cheese"


# =========================Buisnes Layer ===================================================


class NewPizza(Pizza):
    def __init__(self,pizzaName,pizzaPrice):
        self.__name = pizzaName
        self.__price = pizzaPrice
        
    def get_price(self):
        return self.__price
    def get_status(self):
        return self.__name

class NewExtention(PizzaDecorator):
    def __init__(self, pizza,name,price):
        super(NewExtention,self).__init__(pizza)
        self.__name = name
        self.__price = price
    
    def get_price(self):
        return super(NewExtention,self).get_price() + self.__price
    def get_status(self):
        return super(NewExtention,self).get_status() + " " + self.__name



class PizzaBuilder:
    def __init__(self, pizza_type,pizza_price):
        self.pizza_type = pizza_type
        self.pizza_price = pizza_price
        self.pizza = NewPizza(pizza_type,pizza_price)
        self.extentions_list = []
        self.price_list = []

    def add_extention(self, extention,extention_price):
    
        self.pizza = NewExtention(self.pizza,extention,extention_price)
        self.extentions_list.append(extention)
        self.price_list.append(extention_price)

    def remove_extention(self, extention):

        if extention in self.extentions_list:
            index = self.extentions_list.index(extention)
            self.extentions_list.remove(extention)
            self.price_list.remove(self.price_list[index])

        temp_pizza = NewPizza(self.pizza_type,self.pizza_price)
        for ex in self.extentions_list:
            temp_pizza = NewExtention(temp_pizza,ex,self.price_list[self.extentions_list.index(ex)])

        self.pizza = temp_pizza

    def get_price(self):
        return self.pizza.get_price()

    def get_status(self):
        return self.pizza.get_status()






