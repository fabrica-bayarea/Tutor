// Navbar.js
"use client";
import React, { useContext, useState, CSSProperties, useEffect} from 'react';
import { Link } from 'react-router-dom';
import styles from "./mainNavigator.module.css";
import { ModalContext } from "../contexts/contextModal"
import menuImage from "../assets/menu.png"

function MainNavigator() {
  const { menuEstaAberto, abrirMenu, fecharMenu } = useContext(ModalContext)!;

  return (
    <div>
      <button className={styles.buttonMenu} onClick={menuEstaAberto ? fecharMenu : abrirMenu}>
        <img src={menuImage.src} width={25} height={25} alt="Menu" />
      </button>
      {menuEstaAberto && (
        <nav className={styles.navbar}>
          <ul className={`nav-links ${menuEstaAberto ? 'open' : ''}`}>
            <li>
              <Link className={styles.linkPagIni} to="/pagina inicial" onClick={fecharMenu}>
                Chat
              </Link>
            </li>
            <li>
              <Link className={styles.linkPagExt} to="/pagina de extracao" onClick={fecharMenu}>
                Extração
              </Link>
            </li>
            <li>
              <button className={styles.buttonMenuSair} onClick={() => { fecharMenu() }}>
                Sair
              </button>
            </li>
          </ul>
        </nav>
      )}
    </div>
  );
}

export default MainNavigator;