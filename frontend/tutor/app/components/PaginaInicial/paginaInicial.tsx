"use client"

import styles from "./paginaInicial.module.css";
import userImage from "../../assets/user.png"
import menuImage from "../../assets/menu.png"
import sairImage from "../../assets/sair.png"
import addImage from "../../assets/add.png"
import React, { useContext, useState } from 'react';
import { ModalContext } from "../../contexts/contextModal"
import ExtratorWindow from "../../components/ExtratorMenu/ExtratorMenu";

export default function PaginaInicial() {
    const { menuEstaAberto, abrirMenu, fecharMenu, 
            extracaoEstaAberto, abrirMenuExtracao, fecharMenuExtracao, 
            materiaEstaAberto, abrirMenuMateria, fecharMenuMateria, 
            materias } = useContext(ModalContext)!;
    return (
        <div className={styles.containerGlobal}>


            <div className={styles.infoBar}>
                <div className={styles.title}>
                    <h1 className={styles.titulo}>Tutor</h1>
                </div>
                <div className={styles.materia}>
                    <button onClick={materiaEstaAberto ? fecharMenuMateria : abrirMenuMateria} className={styles.materiaButton}>
                        <h1>MatériaNomeAqui</h1>
                        <p>TurmaNumAqui</p>
                    </button>
                </div>
                <div className={styles.profile}>
                    <button className={styles.profileMenu}><img src={menuImage.src} width={25} height={25} onClick={menuEstaAberto ? fecharMenu : abrirMenu} /></button>
                    <button className={styles.profileItem}><img src={userImage.src} width={45} height={45} /></button>
                </div>
            </div>

            {menuEstaAberto && (
                <div className={styles.optionMenu}>
                    <div className={styles.profileMenuItens}>
                        <button className={styles.profileMenu}><img src={addImage.src} width={25} height={25} onClick={extracaoEstaAberto ? fecharMenuExtracao : abrirMenuExtracao} /></button>
                        <button className={styles.profileMenu}><img src={sairImage.src} width={25} height={25} onClick={fecharMenu} /></button>
                    </div>
                </div>
            )}

            {extracaoEstaAberto && (
                <div className={styles.containerExtrator}><ExtratorWindow /></div>
            )}


            {materiaEstaAberto && (
                <div className={styles.materiadDiv}>
                    <div className={styles.materiaContainer}>
                        {materias.map((item) => (
                            <div key={item.id} className={styles.materiaItem}>
                                <button className={styles.materiaItemButton} onClick={fecharMenuMateria}><h1>{item.nome}</h1></button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <div className={styles.containerUser}>
                <div className={styles.containerChatMessage}></div>
                <div className={styles.containerChatSend}>
                    <div className={styles.containerChatBox}>
                        <textarea
                            placeholder="Digite aqui."
                            minLength={10}
                        />
                    </div>
                </div>
            </div>


        </div>
    );
};