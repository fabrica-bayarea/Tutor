'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import styles from './page.module.css';

import Button from '../../../../../components/Button/Button';
import CardMediaContent from '../../../components/CardMediaContent/CardMediaContent';
import { InterfaceProfessor, InterfaceTurma, InterfaceMateria, InterfaceArquivo, InterfaceArquivoTurmaMateria } from '../../../../../types';
import { ArrowLeft, Plus } from 'lucide-react';
import { obterTurma } from '../../../../../services/service_turma';
import { obterMateria } from '../../../../../services/service_materia';
import { obterVinculosArquivoTurmaMateria } from '../../../../../services/service_vinculos';
import { obterArquivo, obterArquivoDownload, deletarArquivo } from '../../../../../services/service_arquivo';

export default function Materia() {
    const params = useParams();
    const [professor, setProfessor] = useState<InterfaceProfessor | null>(null);
    const [turmaId, materiaId] = (params.materiaId as string).split('_');

    const [turma, setTurma] = useState<InterfaceTurma>({
        id: turmaId,
        codigo: '',
        semestre: '',
        turno: ''
    });
    const [materia, setMateria] = useState<InterfaceMateria>({
        id: materiaId,
        codigo: '',
        nome: ''
    });
    const [arquivos, setArquivos] = useState<InterfaceArquivo[]>([]);

    useEffect(() => {
        const professorData = localStorage.getItem("professor");
        if (professorData) {
            try {
                const parsedProfessor = JSON.parse(professorData);
                setProfessor(parsedProfessor);
                handleGetTurma(turmaId);
                handleGetMateria(materiaId);
                handleGetArquivos(turmaId, materiaId);
            } catch (error) {
                console.error("Erro ao fazer parse dos dados do professor:", error);
            }
        }
    }, []);

    const handleGetTurma = async (turma_id: string) => {
        try {
            const turmaData: InterfaceTurma = await obterTurma(turma_id);
            setTurma(turmaData);
        } catch (error) {
            console.error("Erro ao buscar turma:", error);
        }
    };

    const handleGetMateria = async (materia_id: string) => {
        try {
            const materiaData: InterfaceMateria = await obterMateria(materia_id);
            setMateria(materiaData);
        } catch (error) {
            console.error("Erro ao buscar matéria:", error);
        }
    };

    const handleGetArquivos = async (turma_id: string, materia_id: string) => {
        try {
            // Busca os arquivos que tem vínculo com essa turma-matéria
            // Recebe uma lista de dicionários, onde cada dicionário contém 'arquivo_id', 'turma_id' e 'materia_id'
            const responseVinculos: InterfaceArquivoTurmaMateria[] = await obterVinculosArquivoTurmaMateria(turma_id, materia_id);

            // Pega apenas os IDs dos arquivos em cada vínculo
            const filteredArquivosIds = responseVinculos.map(({ arquivo_id }) => arquivo_id);

            // Busca os arquivos usando cada um dos IDs obtidos
            const responseArquivos: InterfaceArquivo[] = await Promise.all(
                filteredArquivosIds.map(async (arquivo_id: string) => {
                    const responseArquivo: InterfaceArquivo = await obterArquivo(arquivo_id);
                    return responseArquivo;
                })
            );
            setArquivos(responseArquivos);
        } catch (error) {
            console.error("Erro ao buscar arquivos:", error);
        }
    };

    // Abre o arquivo
    // NÃO ESTÁ FUNCIONANDO CORRETAMENTE
    const handleOpenArquivo = async (arquivo_id: string) => {
        try {
            const responseArquivo: InterfaceArquivo = await obterArquivoDownload(arquivo_id);
            console.log(responseArquivo);
        } catch (error) {
            console.error("Erro ao buscar arquivo:", error);
        }
    };

    // Baixa o arquivo
    // NÃO ESTÁ FUNCIONANDO CORRETAMENTE
    const handleDownloadArquivo = async (arquivo_id: string) => {
        try {
            const responseArquivo: InterfaceArquivo = await obterArquivoDownload(arquivo_id);
            console.log(responseArquivo);
        } catch (error) {
            console.error("Erro ao baixar arquivo:", error);
        }
    };

    // Exclui o arquivo
    const handleDeleteArquivo = async (arquivo_id: string) => {
        try {
            const responseArquivo: {
                "arquivo_deletado": boolean;
                "arquivo_real_deletado": boolean;
            } = await deletarArquivo(arquivo_id);
            console.log(responseArquivo);

            if (responseArquivo.arquivo_deletado && responseArquivo.arquivo_real_deletado) {
                setArquivos((prevArquivos) => prevArquivos.filter((arquivo) => arquivo.id !== arquivo_id));
            }
        } catch (error) {
            console.error("Erro ao excluir arquivo:", error);
        }
    };

    return (
        <div className={styles.midColumn}>
            <div className={styles.header}>
                <Button
                    icon={<ArrowLeft size={24} />}
                    label="Voltar"
                    onClick={() => window.history.back()}
                />
                <h1>{materia.nome}</h1>
                <div className={styles.materiaInfo}>
                    <p><strong>Turma:</strong> {turma.codigo}</p>
                    <p><strong>Código da matéria:</strong> {materia.codigo}</p>
                </div>
            </div>
            <div className={styles.fontesAdicionadas}>
                <div className={styles.fontesAdicionadasHeader}>
                    <h2>Fontes adicionadas</h2>
                    <Button
                        style="filled"
                        icon={<Plus size={24} />}
                        label="Adicionar fonte"
                        onClick={() => { }}
                    />
                </div>
                <div className={styles.fontesAdicionadasList}>
                    <div className={styles.fontesAdicionadasListHeader}>
                        <div className={styles.headerLeft}>
                            <span>Nome</span>
                        </div>
                        <div className={styles.headerRight}>
                            <div>
                                <span>Adicionado em</span>
                            </div>
                            <div>
                                <span>Tamanho</span>
                            </div>
                            <div>
                                <span>Ações</span>
                            </div>
                        </div>
                    </div>
                    <div className={styles.fontesAdicionadasContent}>
                        {arquivos.map((arquivo) => (
                            <CardMediaContent
                                arquivo={arquivo}
                                onOpen={() => handleOpenArquivo(arquivo.id)}
                                onDownload={() => handleDownloadArquivo(arquivo.id)}
                                //onEdit={() => handleEditArquivo(arquivo.id)}
                                onDelete={() => handleDeleteArquivo(arquivo.id)}
                            />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
