from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired

from app.models.product_category_model import ProductCategoryModel

main_product_categories = [
    (item, item) for item in ProductCategoryModel.main_product_categories()
]
l1_products = [(item, item) for item in ProductCategoryModel.l1_product_categories()]
l2_products = [(item, item) for item in ProductCategoryModel.l2_product_categories()]
l3_products = [(item, item) for item in ProductCategoryModel.l3_product_categories()]


class ProductForm(FlaskForm):

    product_group = SelectField("1. Product Group", choices=main_product_categories)
    l1_product_category = SelectField("2. Product Classification", choices=l1_products)
    l2_product_category = SelectField("3. Product Category", choices=l2_products)
    l3_product_category = SelectField("4. Product Subcategory", choices=l3_products)
    name = StringField("5. Product Name", validators=[DataRequired()])
    price = FloatField("6. Product Price", validators=[DataRequired()])
    submit = SubmitField("Submit")
