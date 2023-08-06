class Product:

    @property
    def orderItemId(self):
        return self.__orderItemId

    @orderItemId.setter
    def orderItemId(self, var):
        self.__orderItemId=var

    @property
    def productId(self):
        return self.__productId

    @productId.setter
    def productId(self, var):
        self.__productId=var

    @property
    def productName(self):
        return self.__productName

    @productName.setter
    def productName(self, var):
        self.__productName=var

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, var):
        self.__price=var

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, var):
        self.__quantity=var

    @property
    def itemdescription(self):
        return self.__itemdescription

    @itemdescription.setter
    def itemdescription(self, var):
        self.__itemdescription=var