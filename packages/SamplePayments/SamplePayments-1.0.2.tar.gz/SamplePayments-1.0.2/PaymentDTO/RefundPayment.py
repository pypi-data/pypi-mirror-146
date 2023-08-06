class RefundPayment:

    @property
    def paymentTransactionId(self):
        return self.__paymentTransactionId

    @paymentTransactionId.setter
    def paymentTransactionId(self, var):
        self.__paymentTransactionId=var

    @property
    def merchantId(self):
        return self.__merchantId

    @merchantId.setter
    def merchantId(self, var):
        self.__merchantId=var

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, var):
        self.__currency=var

    @property
    def refundAmount(self):
        return self.__refundAmount

    @refundAmount.setter
    def refundAmount(self, var):
        self.__refundAmount=var

    @property
    def paymentMethodType(self):
        return self.__paymentMethodType

    @paymentMethodType.setter
    def paymentMethodType(self, var):
        self.__paymentMethodType=var