'use client';

import React, { useEffect, useRef, useState, KeyboardEventHandler, CSSProperties } from 'react';
import styles from './page.module.css';
import Select from 'react-select';
import { InterfaceProfessor, InterfaceTurma, InterfaceMateria, InterfaceProfessorTurmaMateria } from '@/app/types';
import { postLinks } from '@/app/services/service_link';
import { uploadArquivos, uploadLinks, uploadTextos } from '@/app/services/service_arquivo';
import SourceUpload from '../components/SourceUpload/SourceUpload';
import { obterVinculosProfessorTurmaMateria } from '@/app/services/service_vinculos';
import { obterTurma } from '@/app/services/service_turma';
import { obterMateria } from '@/app/services/service_materia';

function ExtratorWindow() {
    const [professor, setProfessor] = useState<InterfaceProfessor | null>(null);
    const [matricula_professor, setMatricula_professor] = useState<string>('1');
    const [turmas, setTurmas] = useState<InterfaceTurma[]>([]);
    const [materias, setMaterias] = useState<InterfaceMateria[]>([]);
    const [vinculos, setVinculos] = useState<InterfaceProfessorTurmaMateria[]>([]);
    const [links, setLinks] = useState<string[]>([]);
    const [arqDragEvent, setArqDragEvent] = useState<File[]>([]);

    useEffect(() => {
        if (typeof window !== 'undefined') {
            const professorData = localStorage.getItem("professor");
            if (professorData) {
                try {
                    const parsedProfessor = JSON.parse(professorData);
                    setProfessor(parsedProfessor);
                    handleGetTurmasMaterias(parsedProfessor.id);
                } catch (error) {
                    console.error("Erro ao fazer parse dos dados do professor:", error);
                }
            }
        }
    }, []);
    
    // Busca os vínculos do professor com turmas e matérias
    const handleGetTurmasMaterias = async (professor_id: string) => {
        try {
            const responseVinculos: InterfaceProfessorTurmaMateria[] = await obterVinculosProfessorTurmaMateria(professor_id);
            setVinculos(responseVinculos);

            const responseTurmas: InterfaceTurma[] = await Promise.all(
                responseVinculos.map(async (vinculo: InterfaceProfessorTurmaMateria) => {
                    const responseTurma: InterfaceTurma = await obterTurma(vinculo.turma_id);
                    return responseTurma;
                })
            );
            setTurmas(responseTurmas);

            const responseMaterias: InterfaceMateria[] = await Promise.all(
                responseVinculos.map(async (vinculo: InterfaceProfessorTurmaMateria) => {
                    const responseMateria: InterfaceMateria = await obterMateria(vinculo.materia_id);
                    return responseMateria;
                })
            );
            setMaterias(responseMaterias);
        } catch (error) {
            console.error('Erro ao buscar vínculos:', error);
            setVinculos([]);
        }
    };


    /*Matérias*/

    // Opções para o componente Select com base nos vínculos do professor
    const options = vinculos.map((vinculo: InterfaceProfessorTurmaMateria, index: number) => {
        const turma = turmas.find(t => t.id === vinculo.turma_id);
        const materia = materias.find(m => m.id === vinculo.materia_id);
        if (turma && materia) {
            return {
                value: index,
                label: `${turma.codigo} - ${materia.codigo} (${materia.nome})`
            };
        }
        return { value: index, label: 'Vínculo não encontrado' };
    });

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

            const response = await uploadArquivos(
                arqDragEvent,
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
    // useEffect(() => {
    //     handleGetTurmasMaterias();
    // }, []);

    // Função para obter o ícone do arquivo com base no tipo

    // Só é possível customizar o componente Select do React com estilos inline.
    // CSS Modules não funcionam.
    const customDropDownStyles = {
        control: (base: any, state: any) => ({
            ...base,
            borderRadius: "8px",
            boxShadow: "none",
            border: state.isFocused ? "1px solid #D92F35" : state.isHovered ? "1px solid rgba(0, 0, 0, 0.15)" : "1px solid transparent",
            outline: "1px solid transparent",
            '&:not(:focus):hover': {
                border: "1px solid rgba(0, 0, 0, 0.15)",
            },
            transition: "border ease-out 0.15s",
        }),
        menu: (base: any) => ({
            ...base,
        }),
        option: (base: any, state: any) => ({
            ...base,
            backgroundColor: state.isFocused ? "rgba(217, 47, 53, 0.05)" : "transparent",
            color:"#666666",
            '&:hover': {
                backgroundColor: "rgba(217, 47, 53, 0.05)",
            },
        }),
        placeholder: (base: any) => ({
            ...base,
            color: "#999999",
        }),
    }

    return (
        <div className={styles.midColumn}>
            {/* Container principal */}

            <div className={styles.header}>
                <h1>Adicionar fontes</h1>
                <p>Adicione materiais (arquivos, links e textos personalizados) à sua base de conteúdos para que o modelo de IA gere respostas mais precisas para seus alunos com base neles.</p>
            </div>
            <div className={styles.selectMaterias}>
                <div className={styles.title}>
                    <h2>Matérias</h2>
                    <p>Selecione as matérias para as quais você quer adicionar os arquivos</p>
                </div>
                <Select
                    styles={customDropDownStyles}
                    isMulti
                    placeholder="Selecione a Matéria"
                    options={options}
                />
            </div>
            <div className={styles.extratorContainer}>
                <SourceUpload/>
                <button className={styles.enviar} onClick={handleEnviar}>Enviar</button>
            </div>
        </div>
    );
};

export default ExtratorWindow;
