// REFACTOR products.jsx. Decomposite ProductList to this component

import Product from "./Product";

const ProductList = (props) => {
    if (! props.sortedAndFilteredProducts.length) {
        return (
            <div className="productsNotFound">
                    <h2>No products found</h2>
            </div>
        )
    }

    return ( 
        <div className="productsList">
            <div className="product">
            {props.sortedAndFilteredProducts.map(product => (
                <Product 
                product={product}
                onDelete={props.handleDeleteProduct} 
                onUpdate={props.handleUpdateProduct}
                key={product.id}
                />
                )
                )}
            </div>
        </div>
     );

}
 
export default ProductList;