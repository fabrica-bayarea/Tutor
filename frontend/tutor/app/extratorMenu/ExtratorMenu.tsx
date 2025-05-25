import React, { useEffect, useRef, useState, KeyboardEventHandler, CSSProperties } from 'react';
import styles from './ExtratorMenu.module.css';
import Select from 'react-select';
import { postLinks } from '@/app/services/link';
import { postUpload } from '@/app/services/upload';
import { getVinculosProfessorTurmaMateria } from '@/app/services/professor_turma_materia';
import exportImage from "../assets/exportImage.png";
import arqImage from "../assets/arqImage.png";
import delImage from "../assets/delImage.png";
import linkImage from "../assets/linkImage.png";

// Componente principal da janela de extração
export default function ExtratorWindow() {
    /* Estados relacionados a links e texto */
    const [text, setText] = useState(''); // Armazena o texto digitado
    const [links, setLinks] = useState<string[]>([]); // Lista de links adicionados
    const [linkInput, setLinkInput] = useState(''); // Valor atual do input de link 
    const linkInputRef = useRef<HTMLInputElement>(null); // Referência ao input de link
    const [matricula_professor, setMatricula_professor] = useState<string>('1');// Matrícula fixa do professor
    const [vinculos, setVinculos] = useState([]); // Lista de vínculos do professor (turma/matéria)

    // Atualiza o estado do texto digitado
    const addText = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(event.target.value);
    };

    // Converte o texto em arquivo e adiciona à lista de arquivos
    const addTextAsFileToDrag: KeyboardEventHandler<HTMLTextAreaElement> = (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            if (text.trim() !== '') {
                const blob = new Blob([text], { type: 'text/plain' });
                const fileName = `texto${arqDragEvent.length + 1}.txt`;
                const newFile = new File([blob], fileName, { type: 'text/plain' });
                setArqDragEvent(arquivosAnteriores => [...arquivosAnteriores, newFile]);
                setText('');
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
                const response = await postLinks(links, matricula_professor, vinculos); // Envia os links para o backend
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

    // Estados do link, texto e arquivos
    const [linkopen, setLinkopen] = useState(false)
    const [textoopen, setTextoopen] = useState(false)
    const [arquivosopen, setArquivosopen] = useState(true)

    const [posicao, setPosicao] = useState<CSSProperties>({
        position: 'absolute',
        left: '288px',
        top: '364px',
        backgroundColor: "red",
        width: "448px",
        height: "5px",
        transition: 'left 0.3s ease-in-out, top 0.3s ease-in-out',
    })

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

    return (
        <div className={styles.container}>
            {/* Container principal */}

            <div className={styles.extratorContainer}>
                {/* Barra de título */}
                <div className={styles.infoBar}>
                    <div className={styles.title}>
                        <h1>Adicionar arquivos à LLM<br /><p style={{ fontWeight: "normal", fontSize: 18, color: "gray", letterSpacing: 0 }}>Adicione materiais(arquivos, links, textos personalizados) à sua base de conteúdos para que o modelo de IA gere respostas mais precisas para seus alunos com base neles.</p></h1>
                    </div>
                </div>

                {/* Seletor de matéria */}
                <div className={styles.materiaChooseContainer}>
                    <div className={styles.materiaChoose}>
                        <h1>Matéria<br /><p style={{ fontWeight: "normal", fontSize: 18, color: "gray", letterSpacing: 0 }}>Selecione as matérias para as quais você quer adicionar os arquivos</p></h1>
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


                <div className={styles.modeArqDiv}>
                    <button onClick={() => { setArquivosopen(true); setTextoopen(false); setLinkopen(false);}}>Arquivos</button>
                    <button onClick={() => { setArquivosopen(false); setTextoopen(false); setLinkopen(true);}}>Links</button>
                    <button onClick={() => { setArquivosopen(false); setTextoopen(true); setLinkopen(false);}}>Textos</button>
                </div>

                {/* Área Ativa */}
                <div style={posicao}></div>


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
                        <img src={exportImage.src} width={50} height={50} />
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
                            onKeyDown={addTextAsFileToDrag}
                            onChange={addText}
                            id="textareInput"
                            value={text}
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
                    {/* Lista de arquivos e links */}
                    {arqDragEvent.map((file: File) => (
                        <li key={file.name}><img className={styles.arqImage} src={arqImage.src} width={30} height={30} />{file.name}<br />{file.size}<button className={styles.delArqButton} onClick={() => deleteArq(file)}><img src={delImage.src} width={30} height={30} /></button></li>
                    ))}
                    {links.map((link, index) => (
                        <li key={index}><img className={styles.arqImage} src={linkImage.src} width={30} height={30} />{link}<button className={styles.delArqButton} onClick={() => deleteLink(index)}><img src={delImage.src} width={30} height={30} /></button></li>
                    ))}
                </div>
                <button className={styles.enviar} onClick={handleEnviar}>Enviar</button>
            </div>
        </div>
    );
};
