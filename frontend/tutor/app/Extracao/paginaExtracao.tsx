"use client";

import Image from "next/image";
import React, { useState } from "react";
import Dropzone from "../../componentes/Dropzone";
import styles from "../Extracao/estilosExtracao.module.css"

export default function PaginaExtracao() {
  const [selectedFiles, setSelectedFiles] = useState([]);

  const handleFilesSelected = (files) => {
    setSelectedFiles(files);
    console.log("Arquivos selecionados na página:", files);
  };

  return (
      <div className={styles.container}>
        <div className={styles.BarDiv}>
            <h1 className={styles.barItem}>Chat</h1>
        </div>

        <div className={styles.extrairDiv}>
        <h1>Extrair arquivos aqui</h1>

        <div className={styles.extratorDiv}>
          <Dropzone />
        </div>
        </div>

        <div className={styles.buttonDiv}>
          <button className="button" onClick={() => console.log("Arquivos para extrair:", selectedFiles)}>
            Extrair
          </button>
        </div>
      </div>
  );
}