import pandas as pd
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify

from ..forms.product_registration_form import ProductForm
from ..models.product_model import ProductModel

product = Blueprint("products", __name__)


@product.route("/products/label/<label>", methods=["GET", "POST"])
def find_products_by_search_string(label):
    df = ProductModel.products()
    products = (
        df[["L4ProductName", "ProductPrice"]]
        .loc[df["L4ProductName"].astype(str).str.lower().str.contains(label)]
        .reset_index(drop=True)
    )
    products.index = products.index + 1
    return render_template("products.html", products=products.to_html())


@product.route("/products")
def list_all_products():
    products = (
        ProductModel.products()[["L4ProductName", "ProductPrice", "L3ProductName"]]
        .rename(
            columns={
                "L4ProductName": "Product Name",
                "ProductPrice": "Price",
                "L3ProductName": "Category",
            }
        )
        .sort_values(by=["Product Name"])
        .reset_index(drop=True)
    )
    products.index = products.index + 1
    return render_template("products.html", products=products.to_html())


@product.route("/products/create", methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    if form.validate_on_submit() and request.method == "POST":
        product_name = form.name.data
        price = form.price.data
        product_sub_category = form.l3_product_category.data
        ProductModel(product_name, price, product_sub_category).add_new_product()
        flash("Data received...", "success")
        return redirect(url_for("products.list_all_products"))
    return render_template("register_product.html", form=form)


@product.route("/products_category_l1/<l0>")
def get_l1_product_subcategory(l0: str):
    return get_product_category_level("L0ProductName", "L1ProductName", l0)


@product.route("/products_category_l2/<l1>")
def get_l2_product_subcategory(l1: str):
    return get_product_category_level("L1ProductName", "L2ProductName", l1)


@product.route("/products_category_l3/<l2>")
def get_l3_product_subcategory(l2: str):
    return get_product_category_level("L2ProductName", "L3ProductName", l2)


def get_product_category_level(lower_level: str, higher_level: str, value: str):
    product_categories: pd.DataFrame = ProductModel.product_categories().set_index(
        lower_level
    )
    filtered = product_categories.loc[value, higher_level]
    if isinstance(filtered, pd.Series):
        result: list = (
            product_categories.loc[value, higher_level].drop_duplicates().tolist()
        )
    else:
        result: list = [filtered]
    return jsonify({f"{higher_level}": sorted(result)})



