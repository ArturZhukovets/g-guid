import axios from "axios"


// const axios = require('axios').default;

async function getProduct(productId) {
    try {
        const response = await axios.get("");
        return response.data;
    } catch (error) {
        console.error(error.messeage);
    throw error;
    }
} 


async function getProductsList(params) {
    try {
        const response = await axios.get("http://127.0.0.1:8000/products/");
        return response.data;
    } catch (error) {
        console.error(error.messeage);
        throw error;
    }
}

export default getProductsList
