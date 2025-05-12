"use client" // Componente de renderização 

import styles from "./paginaInicial.module.css";  // Import os estilos CSS
import userImage from "../../assets/user.png"     // Imagem do usuário
import menuImage from "../../assets/menu.png"     // Ícone de menu
import sairImage from "../../assets/sair.png"     // Ícone de sair
import addImage from "../../assets/add.png"       // Ícone de adicionar/extrair
import React, { useContext, useState } from 'react'; // Importa React e hooks
import { ModalContext } from "../../contexts/contextModal" // Importa o contexto global para controle de estados de menu/modal
import ExtratorWindow from "../../components/ExtratorMenu/ExtratorMenu"; // Componente da janela de extração

export default function PaginaInicial() {
    // Desestrutura funções e variáveis do contexto ModalContext
    const { menuEstaAberto, abrirMenu, fecharMenu, 
            extracaoEstaAberto, abrirMenuExtracao, fecharMenuExtracao, 
            materiaEstaAberto, abrirMenuMateria, fecharMenuMateria, 
            materias } = useContext(ModalContext)!;
    return (
        <div className={styles.containerGlobal}> {/* Container principal da página */}

            {/* Barra superior com título, botão de matéria e perfil */}
            <div className={styles.infoBar}>
                <div className={styles.title}>
                    <h1 className={styles.titulo}>Tutor</h1> {/* Título da aplicação */}
                </div>
                <div className={styles.materia}>
                    {/* Botão que alterna a visualização do menu de matérias */}
                    <button onClick={materiaEstaAberto ? fecharMenuMateria : abrirMenuMateria} className={styles.materiaButton}>
                        <h1>MatériaNomeAqui</h1>
                        <p>TurmaNumAqui</p>
                    </button>
                </div>
                <div className={styles.profile}>
                    {/* Botão de menu do perfil (abre/fecha menu lateral) */}
                    <button className={styles.profileMenu}>
                        <img src={menuImage.src} width={25} height={25} onClick={menuEstaAberto ? fecharMenu : abrirMenu} />
                    </button>
                    {/* Ícone do usuário */}
                    <button className={styles.profileItem}>
                        <img src={userImage.src} width={45} height={45} />
                    </button>
                </div>
            </div>

            {/* Renderiza o menu lateral se estiver aberto */}
            {menuEstaAberto && (
                <div className={styles.optionMenu}>
                    <div className={styles.profileMenuItens}>
                        {/* Botão para abrir/fechar a janela de extração */}
                        <button className={styles.profileMenu}>
                            <img src={addImage.src} width={25} height={25} onClick={extracaoEstaAberto ? fecharMenuExtracao : abrirMenuExtracao} />
                        </button>
                        {/* Botão para fechar o menu */}
                        <button className={styles.profileMenu}>
                            <img src={sairImage.src} width={25} height={25} onClick={fecharMenu} />
                        </button>
                    </div>
                </div>
            )}

            {/* Renderiza a janela de extração se estiver aberta */}
            {extracaoEstaAberto && (
                <div className={styles.containerExtrator}><ExtratorWindow /></div>
            )}

            {/* Renderiza a lista de matérias se o menu estiver aberto */}
            {materiaEstaAberto && (
                <div className={styles.materiadDiv}>
                    <div className={styles.materiaContainer}>
                        {materias.map((item) => (
                            <div key={item.id} className={styles.materiaItem}>
                                {/* Botão que fecha o menu ao selecionar uma matéria */}
                                <button className={styles.materiaItemButton} onClick={fecharMenuMateria}>
                                    <h1>{item.nome}</h1>
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Área principal do chat do usuário */}
            <div className={styles.containerUser}>
                <div className={styles.containerChatMessage}></div> {/* Mensagens do chat (ainda vazio) */}
                <div className={styles.containerChatSend}>
                    <div className={styles.containerChatBox}> 
                        {/* Área de texto para digitação de mensagens */}
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