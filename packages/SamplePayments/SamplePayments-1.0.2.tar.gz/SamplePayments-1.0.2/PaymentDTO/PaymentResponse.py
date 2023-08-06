class PaymentResponse:

    @property
    def paymentTransactionId(self):
        return self.__paymentTransactionId

    @paymentTransactionId.setter
    def paymentTransactionId(self, var):
        self.__paymentTransactionId=var

    @property
    def merchantOrderId(self):
        return self.__merchantOrderId

    @merchantOrderId.setter
    def merchantOrderId(self, var):
        self.__merchantOrderId=var

    @property
    def totalOrderAmount(self):
        return self.__totalOrderAmount

    @totalOrderAmount.setter
    def totalOrderAmount(self, var):
        self.__totalOrderAmount=var

    @property
    def redirectURL(self):
        return self.__redirectURL

    @redirectURL.setter
    def redirectURL(self, var):
        self.__redirectURL=var

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, var):
        self.__amount=var

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, var):
        self.__currency=var

    @property
    def transactionId(self):
        return self.__transactionId

    @transactionId.setter
    def transactionId(self, var):
        self.__transactionId=var

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, var):
        self.__status=var

    @property
    def httpResponseCode(self):
        return self.__httpResponseCode

    @httpResponseCode.setter
    def httpResponseCode(self, var):
        self.__httpResponseCode=var

    @property
    def httpResponseReason(self):
        return self.__httpResponseReason

    @httpResponseReason.setter
    def httpResponseReason(self, var):
        self.__httpResponseReason=var

    @property
    def errorReason(self):
        return self.__errorReason

    @errorReason.setter
    def errorReason(self, var):
        self.__errorReason=var

    @property
    def errorMessage(self):
        return self.__errorMessage

    @errorMessage.setter
    def errorMessage(self, var):
        self.__errorMessage=var

    @property
    def errorField(self):
        return self.__errorField

    @errorField.setter
    def errorField(self, var):
        self.__errorField=var

    @property
    def errorFieldReason(self):
        return self.__errorFieldReason

    @errorFieldReason.setter
    def errorFieldReason(self, var):
        self.__errorFieldReason=var

    @property
    def informationApprovalCode(self):
        return self.__informationApprovalCode

    @informationApprovalCode.setter
    def informationApprovalCode(self, var):
        self.__informationApprovalCode=var

    @property
    def informationResponseCode(self):
        return self.__informationResponseCode

    @informationResponseCode.setter
    def informationResponseCode(self, var):
        self.__informationResponseCode=var

    @property
    def avsCode(self):
        return self.__avsCode

    @avsCode.setter
    def avsCode(self, var):
        self.__avsCode=var

    @property
    def avsCodeRaw(self):
        return self.__avsCodeRaw

    @avsCodeRaw.setter
    def avsCodeRaw(self, var):
        self.__avsCodeRaw=var

    @property
    def reconciliationId(self):
        return self.__reconciliationId

    @reconciliationId.setter
    def reconciliationId(self, var):
        self.__reconciliationId=var

    @property
    def orderSubmitTimeUtc(self):
        return self.__orderSubmitTimeUtc

    @orderSubmitTimeUtc.setter
    def orderSubmitTimeUtc(self, var):
        self.__orderSubmitTimeUtc=var

    @property
    def cardVerificationResultCode(self):
        return self.__cardVerificationResultCode

    @cardVerificationResultCode.setter
    def cardVerificationResultCode(self, var):
        self.__cardVerificationResultCode=var

    @property
    def cvvStatus(self):
        return self.__cvvStatus

    @cvvStatus.setter
    def cvvStatus(self, var):
        self.__cvvStatus=var

    @property
    def refundId(self):
        return self.__refundId

    @refundId.setter
    def refundId(self, var):
        self.__refundId=var

    @property
    def productId(self):
        return self.__productId

    @productId.setter
    def productId(self, var):
        self.__productId=var