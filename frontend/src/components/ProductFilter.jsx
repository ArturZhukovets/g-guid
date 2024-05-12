import DefaultSelect from "./UI/select/defaultSelect.jsx"
import FilterInput from "./UI/input/FilterInput.jsx"


const ProductFilter = ({filter, setFilter}) => {
    return (
        <div className="search-order-group"> 
        <DefaultSelect 
        value={filter.sort}
        onChange={ (sortValue) => setFilter({...filter, sort: sortValue}) }
        defaultValue="Sort products by"
        options={[
          {name: "Product name", value: "title"},
          {name: "Date added", value: "date"},
        ]}
        />
        <FilterInput
          label="Filter records:"
          id="filter-input"
          value={filter.query}
          onChange={(e) => setFilter({...filter, query: e.target.value})}
         />
      </div>
    )
}

export default ProductFilter;