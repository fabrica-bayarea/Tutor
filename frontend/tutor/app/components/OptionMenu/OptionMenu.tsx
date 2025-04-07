"use client"

import React, { useState, useRef } from 'react';
import styles from './OptionMenu.module.css';
import menuImage from "../../assets/menu.png"
import sairImage from "../../assets/sair.png"
import ExtratorMenu from '../ExtratorMenu/ExtratorMenu';

const OptionsMenu = () => {
    const [isOpen, setIsOpen] = useState(false);
    const menuRef = useRef<HTMLDivElement>(null);

    const toggleMenu = () => {
        console.log('Button clicked')
        setIsOpen(!isOpen);
    };

    return (
        <div style={{ position: 'relative', display: 'inline-block' }}>
            <button className={styles.menuButton} id="botaoMenu" onClick={toggleMenu}>
                <img src={menuImage.src} alt="Logo Bay Area" width={40} height={40}/>
            </button>
            <div className={`${styles.optionsMenu} ${isOpen ? styles.show : ''}`} id="myMenu" ref={menuRef}>
                <ExtratorMenu/>
                <button className={styles.menuButton} id="botaoSair" >
                    <img src={sairImage.src} alt="Logo Bay Area" width={60} height={60}/>
                </button>
            </div>
        </div>
    );
};

export default OptionsMenu;
