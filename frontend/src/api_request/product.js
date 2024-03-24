import axios from "axios"
import productListUrl from "../endpoints.js"

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
        const response = await axios.get(productListUrl);
        return await response.data;
    } catch (error) {
        console.error(error.message);
        throw error;
    }
}

export default getProductsList
