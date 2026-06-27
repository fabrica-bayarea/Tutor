"use client";

import React, { useState, useRef, useEffect, KeyboardEventHandler, CSSProperties } from "react";
import styles from "./SourceUpload.module.css";
import { Trash, Link2, FileText, FileVideo, Download, ImageIcon, SendHorizonal } from "lucide-react";

interface SourceUploadProps {
  onFilesChange?: (files: File[]) => void;
  onLinksChange?: (links: string[]) => void;
  onTextsChange?: (texts: string[]) => void;
}

export default function SourceUpload({ onFilesChange, onLinksChange, onTextsChange }: SourceUploadProps) {
    const [text, setText] = useState('');
    const [arqDragEvent, setArqDragEvent] = useState<File[]>([]);
    const [linkInput, setLinkInput] = useState('');
    const [links, setLinks] = useState<string[]>([]);
    const [texts, setTexts] = useState<string[]>([]);
    const linkInputRef = useRef<HTMLInputElement>(null);
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const [fileType, setFileType] = useState<null | 'arquivo' | 'link' | 'texto'>(null);

    const addText = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(event.target.value);
    };

    const addTextToArray: KeyboardEventHandler<HTMLTextAreaElement> = (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            if (text.trim() !== '') {
                setTexts(prev => [...prev, text]);
                setText('');
                if (!fileType) setFileType('texto');
                onTextsChange?.([...texts, text]);
            }
        }
    };

    const addTextAsFileToDrag: KeyboardEventHandler<HTMLTextAreaElement> = async (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            if (text.trim() !== '') {

                if (typeof window !== "undefined") {
                    const blob = new Blob([text], { type: 'text/plain' });
                    const fileName = `texto${arqDragEvent.length + 1}.txt`;
                    const newFile = new File([blob], fileName, { type: 'text/plain' });

                    (newFile as any).text = text;

                    setArqDragEvent(prev => [...prev, newFile]);
                    setText('');
                    if (!fileType) setFileType('texto');
                }
            }
        }
    };

    const addLink = (event: React.ChangeEvent<HTMLInputElement>) => {
        setLinkInput(event.target.value);
    };

    const addLinkToArray: KeyboardEventHandler<HTMLInputElement> = (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            if (linkInput.trim() !== '') {
                setLinks(prev => [...prev, linkInput]);
                setLinkInput('');
                linkInputRef.current!.value = '';
                if (!fileType) setFileType('link');
            }
        }
    };

    const deleteLink = (index: number) => {
        setLinks(prev => {
            const novos = prev.filter((_, i) => i !== index);
            if (novos.length === 0) setFileType(null);
            return novos;
        });
    };

    const deleteText = (index: number) => {
        setTexts(prev => {
            const novos = prev.filter((_, i) => i !== index);
            onTextsChange?.(novos);
            if (novos.length === 0) setFileType(null);
            return novos;
        });
    };

    const [dragUsado, setDragUsado] = useState(false);
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

    const deleteArq = (arquivo: File) => {
        setArqDragEvent(prev => {
            const novos = prev.filter(a => a.name !== arquivo.name);
            if (novos.length === 0) setFileType(null);
            return novos;
        });
    };

    const addButtonClick = () => {
        const fileInput = document.getElementById('fileInput') as HTMLInputElement;
        fileInput?.click();
    };

    const addArqEvent = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files?.length) {
            const novosArquivos = Array.from(event.target.files);
            setArqDragEvent(prev => [...prev, ...novosArquivos]);
            if (!fileType) setFileType('arquivo');
        }
    };

    const formatFileSize = (size: number): string => {
        if (size < 1024) return `${size} bytes`;
        else if (size < 1024 * 1024) return `${(size / 1024).toFixed(2)} KB`;
        else return `${(size / 1024 / 1024).toFixed(2)} MB`;
    };

    useEffect(() => onFilesChange?.(arqDragEvent), [arqDragEvent]);
    useEffect(() => onLinksChange?.(links), [links]);
    useEffect(() => onTextsChange?.(texts), [texts]);

    const getFileIcon = (file: File) => {
        const t = file.type.toLowerCase();
        if (t.startsWith('image/')) return <ImageIcon />;
        if (t === 'application/pdf') return <FileText />;
        if (t.startsWith('video/')) return <FileVideo />;
        if (t.startsWith('text/')) return <FileText />;
        return <FileText />;
    };

    return (
        <div className={styles.SourceUploadContainer}>
            <h1>Inserir link</h1>
            <div className={styles.linkContainer}>
                <input
                    onKeyDown={addLinkToArray}
                    type="text"
                    onChange={addLink}
                    placeholder="Digite seu link"
                    ref={linkInputRef}
                />
                <SendHorizonal />
            </div>

            <h1>Inserir texto</h1>
            <div className={styles.textoContainer}>
                <textarea
                    ref={textareaRef}
                    onKeyDown={addTextToArray}
                    onChange={addText}
                    value={text}
                    placeholder="Digite seu texto"
                />
                <SendHorizonal />
            </div>

            <h1>Fontes Adicionadas</h1>
            <p>
                Arraste e solte aqui arquivos para fazer o upload ou{" "}
                <a onClick={addButtonClick} style={{ fontWeight: "bold", cursor: "pointer", color: "black" }}>
                    clique aqui
                </a>
            </p>

            <div {...dragEvent} ref={dropRef} className={`${styles.dragdropContainer} ${dragUsado ? styles.dragAtivo : ''}`}>
                <input type="file" id="fileInput" style={{ display: 'none' }} onChange={addArqEvent} multiple />

                <div className={styles.arqList}>
                    {arqDragEvent.map((file) => (
                        <li key={file.name}>
                            {getFileIcon(file)}
                            {file.name}
                            <br />
                            {formatFileSize(file.size)}
                            <button className={styles.delArqButton} onClick={() => deleteArq(file)}>
                                <Trash />
                            </button>
                        </li>
                    ))}

                    {links.map((link, index) => (
                        <li key={`link-${index}`}>
                            <Link2 /> {link}
                            <button className={styles.delArqButton} onClick={() => deleteLink(index)}>
                                <Trash />
                            </button>
                        </li>
                    ))}

                    {texts.map((text, index) => (
                        <li key={`text-${index}`}>
                            <FileText />
                            {text.length > 50 ? `${text.substring(0, 50)}...` : text}
                            <button className={styles.delArqButton} onClick={() => deleteText(index)}>
                                <Trash />
                            </button>
                        </li>
                    ))}
                </div>
            </div>
        </div>
    );
}
