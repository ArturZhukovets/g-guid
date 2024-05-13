import { IoCloseCircleSharp, IoHammerSharp } from 'react-icons/io5';
import ProductForm from './ProductForm';
import { useState } from 'react';
import cl from './Product.module.css';


const Product = ({ product, onDelete, onUpdate}) => {

    const [editButton, setEditButton] = useState(false)

    return (
        <div className={cl.productItem}>

            <div className={cl.productFlexElements}>
                <div className={cl.productInfo}>
                    <div>
                        <h5>{product.id}</h5>
                    </div>

                    <div className={cl.productTitle}>
                    <span>{product.title}</span>
                    </div>

                    <div className={cl.productCompound}>
                        <p>Calories: {product.calories}</p>
                        <p>Fats: {product.fat}</p>
                        <p>Proteins: {product.proteins}</p>
                        <p>Carbohydrates: {product.carbohydrates}</p>
                    </div>
                </div>

                <div className={cl.managementIcons}>
                    <div className={cl.productDelete}>
                    <IoCloseCircleSharp product={product} onClick={() => onDelete(product)}/>
                    </div>

                    <div className={cl.productEdit}>
                    <IoHammerSharp onClick={() => setEditButton(!editButton)}/>
                    </div>
                </div>

            </div>

            <div className={cl.productEditForm}>
                {editButton && <ProductForm buttonName="Изменить" onSubmit={onUpdate} currentProduct={product}/> }
            </div>

        </div>
    )
}

export default Product;