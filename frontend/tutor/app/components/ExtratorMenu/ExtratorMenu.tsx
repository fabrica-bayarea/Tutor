import React, { useContext, useRef, useState } from 'react';
import styles from './ExtratorMenu.module.css';
import { ModalContext } from "../../contexts/contextModal"
import Select from 'react-select';
import { postLinks } from '@/app/services/link';
import { postUpload } from '@/app/services/upload';

const ExtratorWindow = () => {
    /*Link-Text*/
    const [text, setText] = useState('');
    const [links, setLinks] = useState<string[]>([]);
    const [linkInput, setLinkInput] = useState('');
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
        setLinkInput(event.target.value);
    };

    const addLinkToArray = () => {
        if (linkInput.trim() !== '') {
            setLinks(prevLinks => [...prevLinks, linkInput]);
            setLinkInput('');
            if (linkInputRef.current) {
                linkInputRef.current.value = '';
            }
        }
    };

    const deleteLink = (index: number) => {
        setLinks(prev => prev.filter((_, i) => i !== index));
    };

    /*Drag and Drop*/
    const [arqDragEvent, setArqDragEvent] = useState<File[]>([]);
    const [dragUsado, setDragUsado] = useState(false); //Fazer uma função para escurecer a tela do drag and drop.
    const dropRef = useRef<HTMLDivElement>(null);

    const dragEvent = {
        onDragEnter: (e: React.DragEvent) => {
            e.preventDefault();
            setDragUsado(true);
        },
        onDragOver: (e: React.DragEvent) => {
            e.preventDefault();
            setDragUsado(true);
        },
        onDragLeave: (e: React.DragEvent) => {
            e.preventDefault();
            if (dropRef.current && !dropRef.current.contains(e.relatedTarget as Node)) {
                setDragUsado(false);
            }
        },
        onDrop: (e: React.DragEvent) => {
            e.preventDefault();
            setDragUsado(false);
            const novosArquivos = Array.from(e.dataTransfer.files);
            setArqDragEvent(prev => [...prev, ...novosArquivos]);
        }
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

    const handleEnviar = async () => {
        try {
            console.log('Enviando links:', links);
            if (links.length > 0) {
                const response = await postLinks(links);
                console.log('Resposta do backend:', response);
            }

            if (arqDragEvent.length > 0) {
                await postUpload(arqDragEvent);
            }
            
            setArqDragEvent([]);
            setLinks([]);

            alert('Arquivos enviados com sucesso!');
        } catch (error) {
            console.error('Erro ao enviar os links:', error);
            console.error('Detalhes completo do erro:', error);
            alert('Erro ao enviar os links.');
        }
    }

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
                <div {...dragEvent} 
                ref = {dropRef}
                className={`${styles.dragdropContainer} ${dragUsado ? styles.dragAtivo : ''}`} >
                    <div className={styles.arqList}>
                        {arqDragEvent.map((file: File) => (
                            <li key={file.name}>{file.name}<button className={styles.delArqButton} onClick={() => deleteArq(file)}>X</button></li>
                        ))}
                        {links.map((link, index) => (
                            <li key={index}>{link}<button className={styles.delArqButton} onClick={() => deleteLink(index)}>X</button></li>
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
                            <button onClick={addLinkToArray} className={styles.buttonLinkTextInput}>Adicionar</button>
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
                            <button onClick={addTextAsFileToDrag} className={styles.buttonLinkTextInput}>Adicionar</button>
                        </div>
                    </div>
                </div>

                <div className={styles.arqEnviarContainer}>
                    <div className={styles.statusBarDiv}>
                        <p>Arquivos Selecionados:</p>
                        <progress max={10} value={arqDragEvent.length} />
                        <p>{arqDragEvent.length}/10</p>
                    </div>
                    <button className={styles.enviar} onClick={handleEnviar}>Enviar</button>
                </div>
            </div>
        </div>
    );
};

export default ExtratorWindow;