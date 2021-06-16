const productGroup = document.getElementById("l0_product_category");
const ProductClassification = document.getElementById("l1_product_category");
const productCategory = document.getElementById("l2_product_category");
const productSubCategory = document.getElementById("l3_product_category");

productGroup.onchange = () => setOptions(productGroup, ProductClassification, "L1ProductName", "/products_category_l1/")
ProductClassification.onchange = () => setOptions(ProductClassification, productCategory, "L2ProductName", "/products_category_l2/")
productCategory.onchange = () => setOptions(productCategory, productSubCategory, "L3ProductName", "/products_category_l3/")


const setOptions = (parent, child, key, endpoint) => {
    let value =  parent.value;
    console.log(value)
    // console.log(endpoint)
    // console.log($SCRIPT_ROOT)
    fetch( endpoint + value).then(result => {
        result.json().then(data => {
            let optionHtml = '';
            for (let option of data[key]) {
                optionHtml += `<option value ="${option}">${option}</option>`;
            }
            child.innerHTML = optionHtml;
        });
    });

}