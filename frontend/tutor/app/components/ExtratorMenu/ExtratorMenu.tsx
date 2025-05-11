import React, { useContext, useEffect, useRef, useState } from 'react';
import styles from './ExtratorMenu.module.css';
import { ModalContext } from "../../contexts/contextModal"
import Select from 'react-select';
import { postLinks } from '@/app/services/link';
import { postUpload } from '@/app/services/upload';
import { getVinculosProfessorTurmaMateria } from '@/app/services/professor_turma_materia';

// Componente principal da janela de extração
const ExtratorWindow = () => {
    /* Estados relacionados a links e texto */
    const [text, setText] = useState(''); // Armazena o texto digitado
    const [links, setLinks] = useState<string[]>([]); // Lista de links adicionados
    const [linkInput, setLinkInput] = useState(''); // Valor atual do input de link 
    const linkInputRef = useRef<HTMLInputElement>(null); // Referência ao input de link
    const [matricula_professor, setMatricula_professor] = useState('1');// Matrícula fixa do professor
    const [vinculos, setVinculos] = useState([]); // Lista de vínculos do professor (turma/matéria)

    // Atualiza o estado do texto digitado
    const addText = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(event.target.value);
    };

    // Converte o texto em arquivo e adiciona à lista de arquivos
    const addTextAsFileToDrag = () => {
        if (text.trim() !== '') {
            const blob = new Blob([text], { type: 'text/plain' });
            const fileName = `texto${arqDragEvent.length + 1}.txt`;
            const newFile = new File([blob], fileName, { type: 'text/plain' });
            setArqDragEvent(arquivosAnteriores => [...arquivosAnteriores, newFile]);
            setText('');
        }
    };

    // Atualiza o valor do input de link
    const addLink = (event: React.ChangeEvent<HTMLInputElement>) => {
        setLinkInput(event.target.value);
    };

    // Adiciona o link digitado à lista de links
    const addLinkToArray = () => {
        if (linkInput.trim() !== '') {
            setLinks(prevLinks => [...prevLinks, linkInput]);
            setLinkInput('');
            if (linkInputRef.current) {
                linkInputRef.current.value = '';
            }
        }
    };

    // Remove link pelo índice
    const deleteLink = (index: number) => {
        setLinks(prev => prev.filter((_, i) => i !== index));
    };

    /* Estados e funções para drag and drop */
    const [arqDragEvent, setArqDragEvent] = useState<File[]>([]); // Lista de arquivos carregados
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
        setArqDragEvent(arquivosAnteriores =>
            arquivosAnteriores.filter(arquivo => arquivo.name !== arquivoParaDeletar.name)
        );
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
            const novosArquivos = Array.from(event.target.files);
            setArqDragEvent(arquivosAnteriores => [...arquivosAnteriores, ...novosArquivos]);
        }
    };

    /*Matérias*/
    const { fecharMenuExtracao, materias } = useContext(ModalContext)!;

    // Opções para o componente Select com base nos vínculos do professor
    const options = vinculos.map((vinculo: any, index: number) => ({
        value: index,
        label: `${vinculo.codigo_turma} - ${vinculo.codigo_materia}`
    }));    

    // Função chamada ao clicar em "Enviar"
    const handleEnviar = async () => {
        try {
            console.log('Enviando links:', links);
            if (links.length > 0) {
                const response = await postLinks(links); // Envia os links para o backend
                console.log('Resposta do backend:', response);
            }

            if (arqDragEvent.length > 0) {
                await handleUpload(); // Envia os arquivos para o backend
            }
            
            setLinks([]); // Limpa os links após envio

            alert('Arquivos enviados com sucesso!');
        } catch (error) {
            console.error('Erro ao enviar os dados:', error);
            console.error('Detalhes completo do erro:', error);
            alert('Erro ao enviar os dados.');
        }
    }

    // Busca os vínculos do professor com turmas e matérias
    const handleGetTurmasMaterias = async () => {
        try {
            const response = await getVinculosProfessorTurmaMateria(matricula_professor);
            console.log('Resposta do backend:', response);
            setVinculos(response);
        } catch (error) {
            console.error('Erro ao buscar os vínculos do professor:', error);
            alert('Erro ao buscar os vínculos do professor.');
        }
    }    

    // Realiza o upload dos arquivos
    const handleUpload = async () => {
        try {
            if (arqDragEvent.length === 0) {
                alert('Por favor, selecione arquivos para upload');
                return;
            }
            if (vinculos.length === 0) {
                alert('Por favor, selecione os vínculos de turma e matéria');
                return;
            }

            const response = await postUpload(
                arqDragEvent, 
                matricula_professor, 
                vinculos
            );

            console.log('Upload successful:', response);
            fecharMenuExtracao(); // Fecha o menu após upload
            setArqDragEvent([]); // Limpa os arquivos
        } catch (error) {
            console.error('Erro no upload:', error);
            alert('Erro no upload. Por favor, tente novamente.');
        }
    };

    // Executa busca dos vínculos ao montar o componente
    useEffect(() => {
        handleGetTurmasMaterias();
    }, []);

    return (
        <div className={styles.container}>
            {/* Container principal */}
            <div className={styles.extratorContainer}>
                {/* Barra de título */}
                <div className={styles.infoBar}>
                    <div className={styles.title}>
                        <h1>Adicionar arquivos à LLM</h1>
                    </div>
                    <button onClick={fecharMenuExtracao} className={styles.closeModalButton}>X</button>
                </div>

                {/* Seletor de matéria */}
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

                {/* Área de drag and drop de arquivos */}
                <div {...dragEvent} 
                ref = {dropRef}
                className={`${styles.dragdropContainer} ${dragUsado ? styles.dragAtivo : ''}`} >
                    <div className={styles.arqList}>
                        {/* Lista de arquivos e links */}
                        {arqDragEvent.map((file: File) => (
                            <li key={file.name}>{file.name}<button className={styles.delArqButton} onClick={() => deleteArq(file)}>X</button></li>
                        ))}
                        {links.map((link, index) => (
                            <li key={index}>{link}<button className={styles.delArqButton} onClick={() => deleteLink(index)}>X</button></li>
                        ))}
                    </div>
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
                    <button className={styles.buttonAddArq} onClick={addButtonClick}>Selecione ou Arraste um Arquivo</button>
                </div>
                {/* Seção de entrada de texto e links */}
                <div className={styles.linkTextoContainer}>
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
                </div>

                {/* Seção de envio */}
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
