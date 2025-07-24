import React, { useState, useRef, useEffect, KeyboardEventHandler, CSSProperties } from "react";
import styles from "./SourceUpload.module.css";
import { Trash, Link2, FileText, FileVideo, Download, ImageIcon } from "lucide-react";

interface SourceUploadProps {
  onFilesChange?: (files: File[]) => void;
  onLinksChange?: (links: string[]) => void;
  onTextsChange?: (texts: string[]) => void;
}

export default function SourceUpload({ onFilesChange, onLinksChange, onTextsChange }: SourceUploadProps) {
    const [text, setText] = useState(''); // Armazena o texto digitado
    const [arqDragEvent, setArqDragEvent] = useState<File[]>([]); // Lista de arquivos carregados
    const [linkInput, setLinkInput] = useState(''); // Valor atual do input de link
    const [links, setLinks] = useState<string[]>([]); // Lista de links adicionados
    const [texts, setTexts] = useState<string[]>([]); // Lista de textos adicionados
    const linkInputRef = useRef<HTMLInputElement>(null); // Referência ao input de link
    const textareaRef = useRef<HTMLTextAreaElement>(null); // Referência ao textarea de texto
    const [fileType, setFileType] = useState<null | 'arquivo' | 'link' | 'texto'>(null); // Tipo de arquivo selecionado


    // Atualiza o estado do texto digitado
    const addText = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(event.target.value);
    };

    // Adiciona o texto à lista de textos
    const addTextToArray: KeyboardEventHandler<HTMLTextAreaElement> = async (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            if (text.trim() !== '') {
                setTexts(prevTexts => [...prevTexts, text]);
                setText('');
                if (!fileType) setFileType('texto');
                if (onTextsChange) {
                    onTextsChange([...texts, text]);
                }
            }
        }
    };

    // Converte o texto em arquivo e adiciona à lista de arquivos
    const addTextAsFileToDrag: KeyboardEventHandler<HTMLTextAreaElement> = async (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            if (text.trim() !== '') {
                const blob = new Blob([text], { type: 'text/plain' });
                const fileName = `texto${arqDragEvent.length + 1}.txt`;
                const newFile = new File([blob as BlobPart], fileName, { type: 'text/plain' });
                // Store the text content in the File object
                (newFile as any).text = text;
                setArqDragEvent(arquivosAnteriores => [...arquivosAnteriores, newFile]);
                setText('');
                if (!fileType) setFileType('texto'); // Define o tipo de arquivo como 'texto' 
            }
        }
    };

    // Atualiza o valor do input de link
    const addLink = (event: React.ChangeEvent<HTMLInputElement>) => {
        setLinkInput(event.target.value);
    };

    // Adiciona o link digitado à lista de links
    const addLinkToArray: KeyboardEventHandler<HTMLInputElement> = (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            if (linkInput.trim() !== '') {
                setLinks(prevLinks => [...prevLinks, linkInput]);
                setLinkInput('');
                if (linkInputRef.current) {
                    linkInputRef.current.value = '';
                }
                if (!fileType) setFileType('link'); // Define o tipo de arquivo como 'link' se ainda não estiver definido
            }
        }
    };

    // Remove link pelo índice
    const deleteLink = (index: number) => {
        setLinks(prev => {
            const novos = prev.filter((_, i) => i !== index)
            if (novos.length === 0) setFileType(null); // Reseta o tipo de arquivo se não houver mais links
            return novos;
        });

    };

    // Remove texto pelo índice
    const deleteText = (index: number) => {
        setTexts(prev => {
            const novos = prev.filter((_, i) => i !== index);
            if (onTextsChange) {
                onTextsChange(novos);
            }
            if (novos.length === 0) setFileType(null);
            return novos;
        });
    };

    /* Estados e funções para drag and drop */
    const [dragUsado, setDragUsado] = useState(false); //Fazer uma função para escurecer a tela do drag and drop.
    const dropRef = useRef<HTMLDivElement>(null); // Referência para área de drop

    // Eventos do drag and drop
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

    // Remove arquivo da lista
    const deleteArq = (arquivoParaDeletar: File) => {
        setArqDragEvent(arquivosAnteriores => {
            const novos = arquivosAnteriores.filter(arquivo => arquivo.name !== arquivoParaDeletar.name)
            if (novos.length === 0) setFileType(null); // Reseta o tipo de arquivo se não houver mais arquivos
            return novos;
        });
    };

    // Abre seletor de arquivos ao clicar no botão
    const addButtonClick = () => {
        const fileInput = document.getElementById('fileInput') as HTMLInputElement | null;
        if (fileInput) {
            fileInput.click();
        }
    };

    // Adiciona arquivos selecionados via input à lista
    const addArqEvent = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            const novosArquivos = Array.from(event.target.files) as File[]; // Explicitly type as File[]
            setArqDragEvent(arquivosAnteriores => [...arquivosAnteriores, ...novosArquivos]);
            if (!fileType) setFileType('arquivo'); // Define o tipo de arquivo como 'arquivo' se ainda não estiver definido
        }
    };

    const [posicao, setPosicao] = useState<CSSProperties>({
        position: 'absolute',
        left: '288px',
        top: '364px',
        backgroundColor: "red",
        width: "448px",
        height: "5px",
        transition: 'left 0.3s ease-in-out, top 0.3s ease-in-out',
    })

        // Função para formatar o tamanho do arquivo
    const formatFileSize = (size: number): string => {
        if (size < 1024) {
            return `${size} bytes`;
        } else if (size < 1024 * 1024) {
            return `${(size / 1024).toFixed(2)} KB`;
        } else {
            return `${(size / (1024 * 1024)).toFixed(2)} MB`;
        }
    };

    // Estados do link, texto e arquivos
    const [linkopen, setLinkopen] = useState(false)
    const [textoopen, setTextoopen] = useState(false)
    const [arquivosopen, setArquivosopen] = useState(true)

    const trocaTipo = () => {
        if (linkopen) {
            const novaPosicao: CSSProperties = {
                position: 'absolute',
                left: "736px",
                top: '364px',
                backgroundColor: "red",
                width: "448px",
                height: "5px",
                transition: 'left 0.3s ease-in-out, top 0.3s ease-in-out',
            };
            setPosicao(novaPosicao);
        } else if (textoopen) {
            const novaPosicao: CSSProperties = {
                position: 'absolute',
                left: "1184px",
                top: '364px',
                backgroundColor: "red",
                width: "448px",
                height: "5px",
                transition: 'left 0.3s ease-in-out, top 0.3s ease-in-out',
            };
            setPosicao(novaPosicao);
        } else if (arquivosopen) {
            const novaPosicao: CSSProperties = {
                position: 'absolute',
                left: "288px",
                top: '364px',
                backgroundColor: "red",
                width: "448px",
                height: "5px",
                transition: 'left 0.3s ease-in-out, top 0.3s ease-in-out',
            }
            setPosicao(novaPosicao);
        };
    }
    useEffect(() => {
        trocaTipo();
    }, [linkopen, textoopen, arquivosopen]);

    useEffect(() => {
        if (onFilesChange) {
            onFilesChange(arqDragEvent);
        }
    }, [arqDragEvent, onFilesChange]);

    useEffect(() => {
        if (onLinksChange) {
            onLinksChange(links);
        }
    }, [links, onLinksChange]);

    useEffect(() => {
        if (onTextsChange) {
            onTextsChange(texts);
        }
    }, [texts, onTextsChange]);

    const getFileIcon = (file: File) => {
        const fileType = file.type.toLowerCase();
        if (fileType.startsWith('image/')) {
            return <ImageIcon />;
        } else if (fileType === 'application/pdf') {
            return <FileText />;
        } else if (fileType.startsWith('video/')) {
            return <FileVideo />;
        } else if (fileType.startsWith('text/')) {
            return <FileText />;
        } else {
            return <FileText />; // Ícone genérico para outros tipos
        }
    };



    return (
        <div className={styles.SourceUploadContainer}>
            <div className={styles.modeArqDiv}>
                <button 
                    onClick={() => { setArquivosopen(true); setTextoopen(false); setLinkopen(false); }}
                    disabled={fileType !== null && fileType !== 'arquivo'}
                >Arquivos</button>
                <button 
                    onClick={() => { setArquivosopen(false); setTextoopen(false); setLinkopen(true); }}
                    disabled={fileType !== null && fileType !== 'link'}
                >Links</button>
                <button 
                    onClick={() => { setArquivosopen(false); setTextoopen(true); setLinkopen(false); }}
                    disabled={fileType !== null && fileType !== 'texto'}
                >Textos</button>
            </div>

            {/* Área Ativa */}
            {/* <div style={posicao}/> */}


            {/* Área de drag and drop de arquivos */}
            {arquivosopen &&
                <div {...dragEvent}
                    ref={dropRef}
                    className={`${styles.dragdropContainer} ${dragUsado ? styles.dragAtivo : ''}`} >
                    <div>
                        {/* Input oculto para arquivos */}
                        <input
                            type="file"
                            id="fileInput"
                            style={{ display: 'none' }}
                            onChange={addArqEvent}
                            multiple
                        />
                    </div>
                    <Download width={45} height={45} />
                    <p style={{ textAlign: 'center', color: "gray" }}>Arraste e solte aqui arquivos para fazer o upload<br /> ou <a onClick={addButtonClick} style={{ fontWeight: "bold", cursor: "pointer", color: "black" }}>clique aqui</a> para selecioná-los</p>
                    <br /><br /><br /><br />
                    <p style={{ textAlign: 'center', color: "gray" }}>Tipos de arquivos compatíveis: PDF, docx, Planilha(ex: xlxs), Vídeo(ex:mp4), Áudio(ex:mp3)<br />Tamanho máximo por arquivo: 50MB</p>
                </div>
            }
            {/* Seção de entrada de texto */}
            {textoopen &&
                <div className={styles.textoContainer}>
                    <h1>Inserir texto</h1>
                    <textarea
                        ref={textareaRef}
                        onKeyDown={addTextToArray}
                        onChange={addText}
                        id="textareInput"
                        value={text}
                        placeholder="Digite seu texto e pressione Enter para adicionar"
                    />
                    {/*<button onClick={addTextAsFileToDrag} className={styles.buttonLinkTextInput}>Adicionar</button>*/}
                </div>
            }
            {/* Seção de entrada de links */}
            {linkopen &&
                <div className={styles.linkContainer}>
                    <h1>Inserir link</h1>
                    <input
                        onKeyDown={addLinkToArray}
                        type="text"
                        className="textInput"
                        onChange={addLink}
                        ref={linkInputRef}
                    />
                </div>
            }
            <h1 className={styles.addArqh1}>Arquivos Adicionados</h1>
            <div className={styles.arqList}>
                {/* Lista de arquivos, textos e links */}
                {arqDragEvent.map((file: File) => (
                    <li key={file.name}>
                        {getFileIcon(file)}
                        {file.name}
                        <br />
                        {formatFileSize(file.size)}
                        <button className={styles.delArqButton} onClick={() => deleteArq(file)}><Trash /></button>
                    </li>
                ))}
                {links.map((link, index) => (
                    <li key={`link-${index}`}>
                        <Link2 />
                        {link}
                        <button className={styles.delArqButton} onClick={() => deleteLink(index)}><Trash /></button>
                    </li>
                ))}
                {texts.map((text, index) => (
                    <li key={`text-${index}`} className={styles.textItem}>
                        <FileText />
                        <span className={styles.textPreview}>
                            {text.length > 50 ? `${text.substring(0, 50)}...` : text}
                        </span>
                        <button className={styles.delArqButton} onClick={() => deleteText(index)}><Trash /></button>
                    </li>
                ))}
            </div>
        </div>
    )
}
