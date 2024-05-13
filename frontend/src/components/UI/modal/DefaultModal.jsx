import React from 'react';
import cl from "./DefaultModal.module.css";


const DefaultModal = ({children}) => {
    return ( 
        <div className={[cl.defaultModal, cl.active].join(' ')}>
            <div className={cl.defaultModalContent}>
                {children}
            </div>
        </div>
     );
}
 
export default DefaultModal;