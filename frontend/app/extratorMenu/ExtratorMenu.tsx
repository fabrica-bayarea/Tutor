import React, { useEffect, useRef, useState, KeyboardEventHandler, CSSProperties } from 'react';
import styles from './ExtratorMenu.module.css';
import Select from 'react-select';
import { postLinks } from '@/app/services/service_link';
import { postUpload } from '@/app/services/service_arquivo';
import SourceUpload from '../professor/components/SourceUpload/SourceUpload';
import { getVinculosProfessorTurmaMateria } from '@/app/services/service_professor_turma_materia';

// Componente principal da janela de extração
function ExtratorWindow() {
    /* Estados relacionados a links e texto */
    const [text, setText] = useState(''); // Armazena o texto digitado
    const [matricula_professor, setMatricula_professor] = useState<string>('1');// Matrícula fixa do professor
    const [vinculos, setVinculos] = useState([]); // Lista de vínculos do professor (turma/matéria)
    const [links, setLinks] = useState<string[]>([]); // Lista de links adicionados
    const [arqDragEvent, setArqDragEvent] = useState<File[]>([]); // Lista de arquivos carregados
    


    /*Matérias*/

    // Opções para o componente Select com base nos vínculos do professor
    const options = vinculos.map((vinculo: any, index: number) => ({
        value: index,
        label: `${vinculo.codigo_turma} - ${vinculo.codigo_materia}`
    }));

        // Adiciona arquivos selecionados via input à lista
        const addArqEvent = (event: React.ChangeEvent<HTMLInputElement>) => {
            if (event.target.files && event.target.files.length > 0) {
                const novosArquivos = Array.from(event.target.files) as File[]; // Explicitly type as File[]
                setArqDragEvent(arquivosAnteriores => [...arquivosAnteriores, ...novosArquivos]);
            }
        };
    

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

    // Função para obter o ícone do arquivo com base no tipo

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

                <SourceUpload/>

                <button className={styles.enviar} onClick={handleEnviar}>Enviar</button>
            </div>
        </div>
    );
};

export default ExtratorWindow;
