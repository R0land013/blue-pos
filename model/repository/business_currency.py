from sqlalchemy.orm import Session
from model.entity.models import BusinessCurrency


class BusinessCurrencyRepository:

    def __init__(self, session: Session):
        super().__init__()
        self.__session = session
    
    def exists_business_currency(self) -> bool:
        """
        Returns True if there is at least one currency in the database, False otherwise.
        """
        return self.__session.query(BusinessCurrency).count() > 0

    def set_business_currency(self, currency_code: str):
        """
        Sets the business currency. If no currency exists yet, creates a new one. 
        If a currency already exists, updates the first one.
        """
        currency = self.__session.query(BusinessCurrency).first()
        
        if currency is None:
            currency = BusinessCurrency(currency_code=currency_code)
            self.__session.add(currency)
        else:
            currency.currency_code = currency_code
        
        self.__session.commit()
