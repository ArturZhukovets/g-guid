import { useState } from "react";


const ProductForm = ({ onSubmit, buttonName, currentProduct}) => {

    // Use currentProduct if update some product.
    if (!currentProduct) {
        currentProduct = {
            title: '',
            calories: '',
            fat: '',
            proteins: '',
            carbohydrates: '',
        }
    }

    const [productData, setProductData] = useState(currentProduct)
    const [buttonStyle, setButtonStyle] = useState({})
    const [buttonText, setButtonText] = useState(buttonName)

    const handleButtonStyle = (responseType) => {
        if (responseType === "success") {
            setButtonStyle({
                "color": "green",
                "borlderColor": "green",
                "border": "solid 1px",
            })
            setButtonText("✔")
         } else if (responseType === "error") {
            setButtonStyle({
                "color": "red",
                "borlderColor": "red",
                "border": "solid 1px",
            })
            setButtonText("✘")
        }
        setTimeout( () => {
            setButtonStyle({});
            setButtonText(buttonName);
           }, 2000);
        }

    const handleSubmit = (e) => {
        e.preventDefault();
        const formData = {...productData, category_id: 97} 
        // check if update current or create a new one
        if (currentProduct.title) {
            currentProduct = productData;
        }
        onSubmit(formData).then(response => {
            if (response.status >= 200 && response.status < 300) {
                setProductData(currentProduct)
                handleButtonStyle("success")
            } else {
                handleButtonStyle("error")
            }
        }).catch(error => {
            handleButtonStyle("error")
            // TODO ADD ALERT HANDLING
        })
    }


    return (
        <form onSubmit={handleSubmit}>
            <input
            type="text"
            placeholder="Название"
            onChange={e => setProductData({...productData, title: e.target.value})}
            value={productData.title}
            />

            <input
            type="number"
            placeholder="Каллории"
            onChange={e => setProductData({...productData, calories: e.target.value})}
            value={productData.calories}
            />

            <input
            type="number"
            placeholder="Жиры"
            onChange={e => setProductData({...productData, fat: e.target.value})}
            value={productData.fat}
            />

            <input
            type="number"
            placeholder="Белки"
            onChange={e => setProductData({...productData, proteins: e.target.value})}
            value={productData.proteins}
            />


            <input
            type="number"
            placeholder="Углеводы"
            onChange={e => setProductData({...productData, carbohydrates: e.target.value})}
            value={productData.carbohydrates}
            />

            <button
            style={buttonStyle}
            type="submit"
            >{buttonText}</button>
        </form>
    )
}

export default ProductForm;