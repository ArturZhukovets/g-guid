import { Form } from "react-router-dom";
import { useState, useEffect, useMemo } from 'react';
import axios from "axios";
import {productsBaseUrl} from "../endpoints";
import ProductForm from "../components/ProductForm";
import Product from "../components/Product";
import DefaultSelect from "../components/UI/select/defaultSelect";
import FilterInput from "../components/UI/input/FilterInput";
import { PER_PAGE } from "../constants";
import { IoCloseCircleSharp, IoHammerSharp } from 'react-icons/io5';

function Products() {
  const [products, setProducts] = useState([]);

  // ===================== PAGINATION STATES ===============================
  const [currentPage, setCurrentPage] = useState(1);
  const [fetching, setFetching] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  // =======================================================================

  // ===================== FILTER & ORDER STATES ===========================
  const [selectedSort, setSelectedSort] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  // =======================================================================

  // const [updateForm, setUpdateForm] = useState(false)
  
  // ===================== PAGINATION ===================
  // https://www.youtube.com/watch?v=J2MWOhV8T6o&t=1s

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

  // =======================================================================


  // =========================== CRUD HANDLERS =============================


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
      const updateUrl = `${productsBaseUrl}/${updateProductData.id}`;
      const response = await axios.put(updateUrl, updateProductData);
      console.log("CALL UPDATE PRODUCT")
      // TODO Realize without loading page!
      fetchProductsList();
      return response;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  // =======================================================================

  // ====================== FILTERING & SORTING & ORDERING

  const sortedProducts = useMemo( () => {
    // call this func every time when update products or 'selectSort' value
    console.log("Call sort or filtering callback")
    if (selectedSort) {
      if (selectedSort === "title") {
        return [...products].sort( (a, b) => a[selectedSort].localeCompare(b[selectedSort]))
      } else if (selectedSort === 'date') {
        return [...products].sort( (a, b) => a["id"] - b["id"]);
      }
    }
    return products;
  }, [selectedSort, products])


  const sortedAndFilteredProducts = useMemo( () => {
    return sortedProducts.filter( product => product.title.toLowerCase().includes(searchQuery.toLocaleLowerCase()))
  }, [searchQuery, sortedProducts])

  // =======================================================================


  return (
    <div className="content">
      <div className="search-order-group"> 
        <DefaultSelect 
        value={selectedSort}
        onChange={ (sortValue) => setSelectedSort(sortValue) }
        defaultValue="Sort products by"
        options={[
          {name: "Product name", value: "title"},
          {name: "Date added", value: "date"},
        ]}
        />
        <FilterInput
          label="Filter records:"
          id="filter-input"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
         />
      </div>
      <div id="products-list">
        <div className="product">
          {sortedAndFilteredProducts.map(product => (
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
    </div>
  )
     
}

export default Products;
