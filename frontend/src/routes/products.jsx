import { Form } from "react-router-dom";
import { useState, useEffect } from 'react';
import axios from "axios";
import {productsBaseUrl} from "../endpoints";
import ProductForm from "../components/ProductForm";
import Product from "../components/Product";
import { PER_PAGE } from "../constants";
import { IoCloseCircleSharp, IoHammerSharp } from 'react-icons/io5';

function Products() {
  const [products, setProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [fetching, setFetching] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  const [updateForm, setUpdateForm] = useState(false)
  
  useEffect( () => {
    if (fetching) {
      axios.get(`${productsBaseUrl}?page=${currentPage}&per_page=${PER_PAGE}`)
      .then(response => {
        setProducts([...products, ...response.data.items])
        setCurrentPage(prevState => prevState + 1);
        setTotalCount(response.data.count)
      }).finally( () => setFetching(false));
    }
  }, [fetching]);

  useEffect( () => {
    document.addEventListener("scroll", scrollHandler)
    return function() {
      document.removeEventListener('scroll', scrollHandler)
    }
  })

  const scrollHandler = (e) => {
    let fullPageHeight = e.target.documentElement.scrollHeight;
    let scrollTop = e.target.documentElement.scrollTop;
    if (fullPageHeight - (scrollTop + window.innerHeight) < 100 && products.length < totalCount) {
      console.log("loading...")
      setFetching(true)
    } 
  }

  const fetchProductsList = async () => {
    try {
      const response = await axios.get(`${productsBaseUrl}?page=${currentPage}&per_page=${PER_PAGE}&order=desc`)
      setProducts([...products, ...response.data.items]);
      setCurrentPage(prevState => prevState + 1);
      setTotalCount(response.data.count)
    } catch (error) {
      console.log("Error:", error)
    } finally { setFetching(false) };
  };

  const handleCreateProduct = async (formData) => {
    try {
      const response = await axios.post(productsBaseUrl, formData)
      const productData = response.data
      setProducts([productData, ...products])
      // fetchProductsList();
      return response;
    } catch (error) {
      console.error(error);
      throw error
    }
  }

  const handleDeleteProduct = async (product) => {
    try {
      const deleteURL = `${productsBaseUrl}/${product.id}`
      await axios.delete(deleteURL);
      const updatedProducts = products.filter(el => el.id !== product.id);
      setProducts(updatedProducts);
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
