// Navbar.js
"use client";
import React, { useContext, useState, CSSProperties, useEffect } from 'react';
import { Link } from 'react-router-dom';
import styles from "./mainNavigator.module.css";
import { ModalContext } from "../contexts/contextModal"
import { Menu, House, Plus, GraduationCap, BookMarked } from "lucide-react";

function MainNavigator() {
  const { menuEstaAberto, abrirMenu, fecharMenu } = useContext(ModalContext)!;

  return (
    <div>
      <button className={styles.buttonMenu} onClick={menuEstaAberto ? fecharMenu : abrirMenu}>
        <Menu />
      </button>
      {menuEstaAberto && (
        <nav className={styles.navbar}>
          <ul className={`nav-links ${menuEstaAberto ? 'open' : ''}`}>
            <li className={styles.cabecalhoNavbar}>
              <h1></h1>
              <button onClick={menuEstaAberto ? fecharMenu : abrirMenu} >
                <Menu />
              </button>
            </li>
            <li className={styles.navbarItem}>
              <Link  to="/pagina inicial" onClick={fecharMenu} className={styles.linkNavbar}>
                <House />
                Chat
              </Link>
            </li>
            <li className={styles.navbarItem}>
              <Link  to="/" onClick={fecharMenu} className={styles.linkNavbar}>
                <GraduationCap />
                Minhas Turmas
              </Link>
            </li>
            <li className={styles.navbarItem}>
              <Link  to="/" onClick={fecharMenu} className={styles.linkNavbar}>
                <BookMarked />
                Minhas Matérias
              </Link>
            </li>
            <li className={styles.navbarItem}>
              <Link to="/pagina de extracao" onClick={fecharMenu} className={styles.linkNavbar}>
                <Plus />
                Adicionar Fontes
              </Link>
            </li>
          </ul>
        </nav>
      )}
    </div>
  );
}

export default MainNavigator;