import pandas as pd
from flask import Blueprint, render_template

from ..models.product_model import ProductModel

analytics = Blueprint("analytics", __name__)


@analytics.route("/sales_by/<key>", methods=["GET", "POST"])
def total_sales_by(key: str = "department"):
    keys = {
        "department": "L1ProductName",
        "category": "L2ProductName",
        "product": "L3ProductName",
    }
    sales: pd.DataFrame = ProductModel.total_sales_by(keys.get(key))
    return render_template("analytics.html", sales=sales.to_html(), key=key)
