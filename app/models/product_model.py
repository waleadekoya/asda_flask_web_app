from control.config import BaseConfig
from .product_category_model import ProductCategoryModel
import pandas as pd

con = BaseConfig.con
connection = BaseConfig.connection


class ProductModel:
    def __init__(self, product_name: str, price: int, l3_product_name: str):
        self.l4_product_name = product_name
        self.price = price
        self.l3_product_name = l3_product_name

    @staticmethod
    def total_sales_by(key: str):
        keys = dict(
            L1ProductName="Department",
            L2ProductName="Category",
            L3ProductName="Product",
        )
        query = f"""
        SELECT 
            c.{key} AS {keys.get(key)},
            SUM(o.ProductPrice * o.Quantity) as TotalSales
        FROM asda_project.Order o
        LEFT JOIN asda_project.Product p ON o.L4ProductCode = p.L4ProductCode
        LEFT JOIN asda_project.ProductCategory c ON c.L3ProductCode = p.L3ProductCode
        GROUP BY c.{key} 
        ORDER BY TotalSales
        """
        return pd.read_sql(query, con)

    def add_new_product(self):
        """insert into table_name (col1, col2, col3) values(val1, val2, val3)"""
        query = (
            f"INSERT INTO Product "
            f"(L3ProductName, L3ProductCode, L4ProductName, L4ProductCode, ProductPrice) "
            f"VALUES ("
            f" '{self.l3_product_name}', "
            f" {self.l3_product_code}, "
            f" '{self.l4_product_name}', "
            f"{self.next_l4_product_code}, "
            f"{self.price})"
        )
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()

    @property
    def is_existing_l3_product_names(self):
        return (
            pd.read_sql("select distinct L3ProductName from asda_project.Product", con)
            .squeeze()
            .to_list()
        )

    @staticmethod
    def product_categories():
        return pd.read_sql(
            "select distinct "
            "L0ProductName, L1ProductName, "
            "L2ProductName, L3ProductName "
            "from ProductCategory",
            con,
        )

    @staticmethod
    def products():
        return pd.read_sql("select * from Product", con)

    @property
    def l3_product_code(self) -> pd.DataFrame:
        sql = (
            f"select distinct L3ProductCode from asda_project.ProductCategory "
            f"where L3ProductName = '{self.l3_product_name}' "
        )
        return pd.read_sql(sql, con).iloc[0]["L3ProductCode"]

    @property
    def l3_l4_product_mapping(self) -> pd.DataFrame:
        sql = "select distinct L4ProductCode, L3ProductCode from Product"
        return pd.read_sql(sql, con)

    @property
    def last_l4_product_codes(self) -> int:
        if self.l3_product_name in self.is_existing_l3_product_names:
            sql = (
                f"select distinct L4ProductCode from Product "
                f"where L3ProductName = '{self.l3_product_name}' "
                f"order by L4ProductCode"
            )
            return pd.read_sql(sql, con).tail(1).iloc[0]["L4ProductCode"]

    @property
    def next_l4_product_code(self) -> int:
        parent_code: str = ProductCategoryModel.product_parent_code_from_l3_choice(
            self.l3_product_name
        )
        if self.last_l4_product_codes:
            "for l3 product code with existing l4 product code "
            last_code = int(str(self.last_l4_product_codes).split(parent_code)[1])
            return int(str(parent_code) + str(last_code + 1))
        return int(str(parent_code) + str(100))
