import { Form } from "react-router-dom";
import { useState, useEffect } from 'react';
import axios from "axios";
import {productsBaseUrl} from "../endpoints";
import ProductForm from "../components/ProductForm";
import Product from "../components/Product";
import { IoCloseCircleSharp, IoHammerSharp } from 'react-icons/io5';

function Products() {
  const [products, setProducts] = useState([]);
  const [updateForm, setUpdateForm] = useState(false)

  const fetchProductsList = async () => {
    try {
      const response = await axios.get(productsBaseUrl)
      setProducts(response.data);
    } catch (error) {
      console.log("Error:", error)
    }
  };

  useEffect( () => {
    fetchProductsList();
  }, []);

  const handleCreateProduct = async (formData) => {
    try {
      const response = await axios.post(productsBaseUrl, formData)
      fetchProductsList();
      return response;
    } catch (error) {
      console.error(error);
      throw error
    }
  }

  const handleDeleteProduct = async (product) => {
    try {
      const deleteURL = `${productsBaseUrl}${product.id}`
      const response = await axios.delete(deleteURL);
      fetchProductsList();
    } catch (error) {
      console.error(error);
      alert(error)
    }
  }

  const handleUpdateProduct = async (updateProductData) => {
    try {
      const updateUrl = `${productsBaseUrl}${updateProductData.id}`;
      const response = await axios.put(updateUrl, updateProductData);
      console.log("CALL UPDATE PRODUCT!!!!")
      fetchProductsList();
      return response;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }


  return (
    <div id="products-list">
      <div className="product">
        {products.map(product => (
                <Product 
                product={product}
                onDelete={handleDeleteProduct} 
                onUpdate={handleUpdateProduct}
                key={product.id}
                />
                )
              )}
      </div>
      <aside>
        <ProductForm onSubmit={handleCreateProduct} buttonName="Добавить"/>
      </aside>
    </div>
  )
     
}

export default Products;
