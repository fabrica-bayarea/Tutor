import React, { useCallback, useContext, useState, useRef } from 'react';
import { useDropzone } from 'react-dropzone';
import styles from './ExtratorMenu.module.css';
import addImage from "../../assets/add.png"
import { ModalContext } from "../../contexts/contextModal"
import Select from 'react-select';
import { div, s } from 'framer-motion/client';


const ExtratorWindow = () => {

    /*Drag and Drop*/
    const [arqDragEvent, setArqDragEvent] = useState<File[]>([]);
    const [dragUsado, setDragUsado] = useState(false)
    const dragEvent = {
        onDragEnter: (e: React.DragEvent) => {
            e.preventDefault();
            setDragUsado(true)
        },
        onDragLeave: (e: React.DragEvent) => {
            e.preventDefault();
            setDragUsado(false)
        },
        onDragOver: (e: React.DragEvent) => {
            e.preventDefault();
        },
        onDrop: (e: React.DragEvent) => {
            e.preventDefault();
            setDragUsado(false)
            const novosArquivos = Array.from(e.dataTransfer.files);
            setArqDragEvent(arquivosAnteriores => [...arquivosAnteriores, ...novosArquivos]);
        },
    };
    const deleteArq = (arquivoParaDeletar: File) => {
        setArqDragEvent(arquivosAnteriores =>
            arquivosAnteriores.filter(arquivo => arquivo.name !== arquivoParaDeletar.name)
        );
    };
    const addButtonClick = () => {
        const fileInput = document.getElementById('fileInput') as HTMLInputElement | null;
        if (fileInput) {
            fileInput.click();
        }
    };

    const addArqEvent = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            const novosArquivos = Array.from(event.target.files);
            setArqDragEvent(arquivosAnteriores => [...arquivosAnteriores, ...novosArquivos]);
        }
    };

    /*Matérias*/
    const { fecharMenuExtracao, materias } = useContext(ModalContext)!;
    const options = materias ? materias.map((materia: any) => ({
        value: materia.id,
        label: materia.nome
    })) : [];

    return (
        <div className={styles.container}>
            <div className={styles.extratorContainer}>
                <div className={styles.infoBar}>
                    <div className={styles.title}>
                        <h1>Adicionar arquivos à LLM</h1>
                    </div>
                    <button onClick={fecharMenuExtracao} className={styles.closeModalButton}>X</button>
                </div>

                <div className={styles.materiaChooseContainer}>
                    <div className={styles.materiaChoose}>
                        <h1>Matéria</h1>
                        <div className={styles.dropDown}>
                            <Select
                                isMulti
                                name="colors"
                                className="basic-multi-select"
                                placeholder="Selecione a Matéria"
                                classNamePrefix="Selecione a Matéria"
                                options={options}
                            />
                        </div>
                    </div>
                </div>

                {dragUsado && (
                        <div className={styles.dragUsadoDiv}><h1>Solte os arquivos Aqui.</h1></div>
                    )}
                <div {...dragEvent} className={styles.dragdropContainer}>
                    <div className={styles.arqList}>
                    {arqDragEvent.map((file: File) => (
                        <li  key={file.name}>{file.name}<button className={styles.delArqButton} onClick={() => deleteArq(file)}>X</button></li>
                    ))}
                    </div>
                    <div>
                        <input
                            type="file"
                            id="fileInput"
                            style={{ display: 'none' }}
                            onChange={addArqEvent}
                            multiple
                        />
                    </div>
                    <button className={styles.buttonAddArq} onClick={addButtonClick}>Selecione ou Arraste um Arquivo</button>
                </div>
                <div className={styles.linkTextoContainer}>
                    <div className={styles.linkContainer}>
                        <div className={styles.linkContainerDiv}>
                            <h1>Link:</h1>
                            <input
                                type="text"
                                placeholder="Digite aqui."
                                className="textInput"
                            />
                        </div>
                    </div>
                    <div className={styles.textoContainer}>
                        <div className={styles.textoContainerDiv}>
                            <h1>Texto:</h1>
                            <textarea
                                placeholder="Digite aqui."
                            />
                        </div>
                    </div>
                </div>

                <div className={styles.arqEnviarContainer}>
                    <div className={styles.statusBarDiv}>
                        <p>Arquivos Selecionados:</p>
                        <progress max={10} value={arqDragEvent.length} />
                        <p>{arqDragEvent.length}/10</p>
                    </div>
                    <button className={styles.enviar}>Enviar</button>
                </div>
            </div>
        </div>
    );
};

export default ExtratorWindow;