import { Form } from "react-router-dom";
import getProductsList from "../api_request/product";

function Products() {
  const product = {
    title: "Yogurt",
    fat: "A LOT",
    avatar: "https://placekitten.com/g/200/200",

  };
  const products = getProductsList();
  console.log(products)

  return (
    <div id="product">
      <div>
        <img
          key={product.avatar}
          src={product.avatar || null}
          className="productImage"
        />
      </div>

      <div>
        <h1>
              {product.title}
        </h1>

          <p>
            
              {product.fat}
          </p>

        {/* <div>
          <Form action="edit">
            <button type="submit">Edit</button>
          </Form>
          <Form
            method="post"
            action="destroy"
            onSubmit={(event) => {
              if (
                !confirm(
                  "Please confirm you want to delete this record."
                )
              ) {
                event.preventDefault();
              }
            }}
          >
            <button type="submit">Delete</button>
          </Form>
        </div> */}
      </div>
    </div>
  );
}


export default Products;
