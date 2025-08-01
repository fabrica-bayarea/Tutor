'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import styles from './page.module.css';

import Button from '../../../../../components/Button/Button';
import IconButton from '@/app/components/IconButton/IconButton';
import { InterfaceProfessor, InterfaceTurma, InterfaceMateria, InterfaceArquivo, InterfaceArquivoTurmaMateria } from '../../../../../types';
import { ArrowLeft, Download, File, Play, Music, Text, Pencil, Plus, SquareArrowOutUpRight, Trash2 } from 'lucide-react';
import { obterTurma } from '../../../../../services/service_turma';
import { obterMateria } from '../../../../../services/service_materia';
import { obterVinculosArquivoTurmaMateria } from '../../../../../services/service_vinculos';
import { obterArquivo, obterArquivoDownload, deletarArquivo } from '../../../../../services/service_arquivo';
import { deletarVinculoArquivoTurmaMateria } from '../../../../../services/service_vinculos';
import { TIPOS_ARQUIVO } from '@/constants';

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
    const [arquivos, setArquivos] = useState<{
        id: InterfaceArquivo["id"];
        titulo: InterfaceArquivo["titulo"];
        data_upload: InterfaceArquivo["data_upload"];
        tamanho?: string;
        tipo_arquivo?: string;
    }[]>([]);

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
            const responseArquivo: boolean = await deletarVinculoArquivoTurmaMateria(arquivo_id, turmaId, materiaId);
            console.log(responseArquivo);

            if (responseArquivo) {
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
                    <table>
                        <thead>
                            <tr>
                                <th>Nome</th>
                                <th></th>
                                <th>Adicionado em</th>
                                <th>Tamanho</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {arquivos.map((arquivo) => (
                                <tr key={arquivo.id}>
                                    <td>
                                        <div className={styles.iconContainer}>
                                            {TIPOS_ARQUIVO.documento.includes(`.${arquivo.titulo.split('.').pop()}`) ? <File size={24} /> :
                                            TIPOS_ARQUIVO.video.includes(`.${arquivo.titulo.split('.').pop()}`) ? <Play size={24} /> :
                                            TIPOS_ARQUIVO.audio.includes(`.${arquivo.titulo.split('.').pop()}`) ? <Music size={24} /> :
                                            TIPOS_ARQUIVO.texto.includes(`.${arquivo.titulo.split('.').pop()}`) ? <Text size={24} /> : null}
                                        </div>
                                    </td>
                                    <td>{arquivo.titulo}</td>
                                    <td>{arquivo.data_upload as String}</td>
                                    <td>{arquivo.tamanho || "--"}</td>
                                    <td className={styles.actionsContainer}>
                                        <IconButton
                                            icon={<SquareArrowOutUpRight size={20} />}
                                            title="Abrir arquivo"
                                            onClick={() => handleOpenArquivo(arquivo.id)}
                                        />
                                        <IconButton
                                            icon={<Download size={20} />}
                                            title="Baixar arquivo"
                                            onClick={() => handleDownloadArquivo(arquivo.id)}
                                        />
                                        <IconButton
                                            icon={<Pencil size={20} />}
                                            title="Editar nome do arquivo"
                                            //onClick={() => handleEditArquivo(arquivo.id)}
                                        />
                                        <IconButton
                                            icon={<Trash2 size={20} color="#D92F35" />}
                                            title="Excluir arquivo para esta matéria"
                                            onClick={() => handleDeleteArquivo(arquivo.id)}
                                        />
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}
