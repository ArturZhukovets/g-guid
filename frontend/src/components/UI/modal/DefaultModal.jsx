import React from 'react';
import cl from "./DefaultModal.module.css";


const DefaultModal = ({children, modalVisible, setModalVisible}) => {

    const rootClasses = [cl.defaultModal]

    if (modalVisible) {
        rootClasses.push(cl.active)
    }

    return ( 
        <div className={rootClasses.join(' ')} onClick={ () => setModalVisible(false)}>
            <div className={cl.defaultModalContent} onClick={(e) => e.stopPropagation()}>
                {children}
            </div>
        </div>
     );
}
 
export default DefaultModal;