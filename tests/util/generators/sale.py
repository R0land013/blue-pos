from datetime import date
from model.entity.models import Sale, Product
from model.util.monetary_types import CUPMoney


class SaleGenerator:

    DEFAULT_DATE = date.today()
    DEFAULT_MONEY = CUPMoney('1.00')

    @staticmethod
    def generate_sales_from_product(product: Product, quantity: int):
        sales = []

        for _ in range(quantity):
            sale = SaleGenerator.generate_one_sale_from_product(product)
            sales.append(sale)
        return sales

    @staticmethod
    def generate_one_sale_from_product(product: Product) -> Sale:
        sale = Sale()
        sale.date = SaleGenerator.DEFAULT_DATE
        sale.product_id = product.id
        sale.product = product
        sale.price = product.price
        sale.profit = product.profit

        return sale

    @staticmethod
    def generate_one_sale_without_product() -> Sale:
        sale = Sale()
        sale.date = SaleGenerator.DEFAULT_DATE
        sale.price = SaleGenerator.DEFAULT_MONEY
        sale.profit = SaleGenerator.DEFAULT_MONEY
        return sale