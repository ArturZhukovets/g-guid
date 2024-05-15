import DefaultModal from "./UI/modal/DefaultModal";
import { GrAddCircle } from "react-icons/gr";
import ProductForm from "./product/ProductForm";


const AddProductBlock = (props) => {
    return ( 
        <div className="formProduct">
            <button type="button" onClick={() => props.setModalVisible(true)}>
              <GrAddCircle/> Добавить
            </button>
            <DefaultModal
                modalVisible={props.modalVisible}
                setModalVisible={props.setModalVisible} 
                >
            <ProductForm 
                onSubmit={props.handleCreateProduct} 
                buttonName="Добавить"
            />
            </DefaultModal>
        </div>
     );
}
 
export default AddProductBlock;