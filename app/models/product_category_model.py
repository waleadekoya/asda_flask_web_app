from control.config import BaseConfig
import pandas as pd

con = BaseConfig.con


class ProductCategoryModel:
    def __init__(self, main_product):
        self.main_product = main_product

    @staticmethod
    def to_series(sql: str):
        return pd.read_sql(sql, con).squeeze().tolist()

    @staticmethod
    def main_product_categories() -> pd.DataFrame:
        sql = f"select distinct L0ProductName from ProductCategory "
        return ProductCategoryModel.to_series(sql)

    @property
    def is_valid(self):
        return (
            pd.read_sql("select distinct L3ProductName from asda_project.Product", con)
            .squeeze()
            .to_list()
        )

    @property
    def l1_product_categories_based_on_l0_product_name(self) -> pd.DataFrame:
        sql = (
            f"select distinct L1ProductName from ProductCategory "
            f"where L0ProductName = '{self.main_product}' "
            f"order by L1ProductName"
        )
        return ProductCategoryModel.to_series(sql)

    @staticmethod
    def l2_product_categories_based_on_l1_choice(
        l1_product_category: str,
    ) -> pd.DataFrame:
        sql = (
            f"select distinct L2ProductName from ProductCategory "
            f"where L1ProductName = '{l1_product_category}' "
            f"order by L2ProductName"
        )
        return ProductCategoryModel.to_series(sql)

    @staticmethod
    def l3_product_categories_based_on_l2_choice(
        l2_product_category: str,
    ) -> pd.DataFrame:
        sql = (
            f"select distinct L3ProductName from ProductCategory "
            f"where L2ProductName = '{l2_product_category}' "
            f"order by L3ProductName"
        )
        return ProductCategoryModel.to_series(sql)

    @staticmethod
    def product_parent_code_from_l3_choice(l3_product_name: str) -> str:
        sql = (
            f"select distinct CONCAT(L1ProductCode, L2ProductCode, L3ProductCode) as parent_code "
            f"from ProductCategory where L3ProductName = '{l3_product_name}' "
        )
        return pd.read_sql(sql, con).iloc[0]["parent_code"]

    @staticmethod
    def l3_product_categories() -> pd.DataFrame:
        sql = (
            f"select distinct L3ProductName from ProductCategory order by L3ProductName"
        )
        return ProductCategoryModel.to_series(sql)

    @staticmethod
    def l2_product_categories() -> pd.DataFrame:
        sql = (
            f"select distinct L2ProductName from ProductCategory order by L2ProductName"
        )
        return ProductCategoryModel.to_series(sql)

    @classmethod
    def l1_product_categories(cls):
        sql = (
            f"select distinct L1ProductName from ProductCategory order by L1ProductName"
        )
        return ProductCategoryModel.to_series(sql)
