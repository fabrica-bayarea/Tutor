import React, { useContext, useRef, useState } from 'react';
import styles from './ExtratorMenu.module.css';
import { ModalContext } from "../../contexts/contextModal"
import Select from 'react-select';

const ExtratorWindow = () => {
    /*Link-Text*/
    const [text, setText] = useState('');
    const [linkText, setLinkText] = useState('');
    const linkInputRef = useRef<HTMLInputElement>(null);

    const addText = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(event.target.value);
    };

    const addTextAsFileToDrag = () => {
        if (text.trim() !== '') {
            const blob = new Blob([text], { type: 'text/plain' });
            const fileName = `texto${arqDragEvent.length + 1}.txt`;
            const newFile = new File([blob], fileName, { type: 'text/plain' });
            setArqDragEvent(arquivosAnteriores => [...arquivosAnteriores, newFile]);
            setText('');
        }
    };

    const addLink = (event: React.ChangeEvent<HTMLInputElement>) => {
        setLinkText(event.target.value);
    };

    const addLinkAsFileToDrag = () => {
        if (linkText.trim() !== '') {
            const blob = new Blob([linkText], { type: 'text/plain' });
            const fileName = `link${arqDragEvent.length + 1}.txt`;
            const newFile = new File([blob], fileName, { type: 'text/plain' });
            setArqDragEvent(arquivosAnteriores => [...arquivosAnteriores, newFile]);
            setLinkText('');
            if (linkInputRef.current) {
                linkInputRef.current.value = '';
            }
        }
    };

    /*Drag and Drop*/
    const [arqDragEvent, setArqDragEvent] = useState<File[]>([]);
    const [dragUsado, setDragUsado] = useState(false); //Fazer uma função para escurecer a tela do drag and drop.
    const dragEvent = {
        onDragEnter: (e: React.DragEvent) => {
            e.preventDefault();
            setDragUsado(true);
        },
        onDragOver: (e: React.DragEvent) => { 
            e.preventDefault();
        },
        onDragLeave: (e: React.DragEvent) => {
            e.preventDefault();
            setDragUsado(false);
        },
        onDrop: (e: React.DragEvent) => {
            e.preventDefault();
            setDragUsado(false);
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
                <div {...dragEvent} className={styles.dragdropContainer}>
                    <div className={styles.arqList}>
                        {arqDragEvent.map((file: File) => (
                            <li key={file.name}>{file.name}<button className={styles.delArqButton} onClick={() => deleteArq(file)}>X</button></li>
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
                                onChange={addLink}
                                ref={linkInputRef}
                            />
                            <button onClick={addLinkAsFileToDrag} className={styles.buttonLinkTextInput}>Enviar</button>
                        </div>
                    </div>
                    <div className={styles.textoContainer}>
                        <div className={styles.textoContainerDiv}>
                            <h1>Texto:</h1>
                            <textarea
                                placeholder="Digite aqui."
                                onChange={addText}
                                id="textareInput"
                                value={text}
                            />
                            <button onClick={addTextAsFileToDrag} className={styles.buttonLinkTextInput}>Enviar</button>
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