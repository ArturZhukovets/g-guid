import { IoCloseCircleSharp, IoHammerSharp } from 'react-icons/io5';
import ProductForm from './ProductForm';
import { useState } from 'react';


const Product = ({ product, onDelete, onUpdate}) => {

    const [editButton, setEditButton] = useState(false)

    return (
        <div className="product-item">
            <div className="product-title">
            <span>{product.title}</span>
            </div>

            <div className="product-delete">
            <IoCloseCircleSharp product={product} onClick={() => onDelete(product)}/>
            </div>

            <div className="product-edit">
            <IoHammerSharp onClick={() => setEditButton(!editButton)}/>
            </div>

            <div className='product-compound'>
                <p>Calories: {product.calories}</p>
                <p>Fats: {product.fat}</p>
                <p>Proteins: {product.proteins}</p>
                <p>Carbohydrates: {product.carbohydrates}</p>
            </div>

            <div className='product-edit-form'>
                {editButton && <ProductForm buttonName="Изменить" onSubmit={onUpdate} currentProduct={product}/> }
            </div>

        </div>
    )
}

export default Product;