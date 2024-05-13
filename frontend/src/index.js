import React from 'react';
import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import reportWebVitals from './reportWebVitals';
import Root from "./routes/root";
import "./css/index.css";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import ErrorPage from "./error-page";
import Products from "./routes/products"
import About from "./routes/about"


const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "products/",
        element: <Products />,
      },
      // {
      //   path: "about/",
      //   element: <About/>,
      // }
    ]
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // <StrictMode>
    <RouterProvider router={router} />
  // </StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
