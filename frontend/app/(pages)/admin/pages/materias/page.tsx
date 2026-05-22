"use client";

import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Pencil, Trash2, RotateCw, Plus, AlertTriangle } from "lucide-react";
import styles from "./page.module.css";
import Table, { TableColumn } from "../../../../components/Table/Table";
import Button from "../../../../components/Button/Button";
import SearchInput from "../../../../components/SearchInput/SearchInput";
import Pagination from "../../../../components/Pagination/Pagination";
import Modal from "../../../../components/Modal/Modal";
import {
    listarMaterias,
    desativarMateria,
    reativarMateria,
} from "../../../../services/service_materia";
import { listarTurmas } from "../../../../services/service_turma";
import { obterVinculosTurmaMateria } from "../../../../services/service_vinculos";
import { useToast } from "@/contexts/ToastContext";

type MateriaStatus = "Ativa" | "Desativada";

type Materia = {
    id: string;
    codigo: string;
    nome: string;
    status: MateriaStatus;
    turmasVinculadas: number;
};

const ROW_HEIGHT = 49;
const HEADER_HEIGHT = 47;
const MIN_PAGE_SIZE = 1;

export default function Materias() {
    const router = useRouter();
    const { addToast } = useToast();
    const [materias, setMaterias] = useState<Materia[]>([]);
    const [search, setSearch] = useState("");
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(8);
    const [materiaParaDesativar, setMateriaParaDesativar] =
        useState<Materia | null>(null);
    const tableAreaRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        let cancelled = false;
        (async () => {
            const [lista, turmas] = await Promise.all([
                listarMaterias(),
                listarTurmas(),
            ]);
            if (cancelled) return;

            const turmasAtivas = turmas.filter((t) => t.status === "ATIVO");
            const vinculosPorTurma = await Promise.all(
                turmasAtivas.map((t) =>
                    obterVinculosTurmaMateria(t.id).catch(() => [])
                )
            );
            if (cancelled) return;

            const contagemPorMateria: Record<string, number> = {};
            vinculosPorTurma.flat().forEach((v) => {
                contagemPorMateria[v.materia_id] =
                    (contagemPorMateria[v.materia_id] ?? 0) + 1;
            });

            setMaterias(
                lista.map((m) => ({
                    id: m.id,
                    codigo: m.codigo,
                    nome: m.nome,
                    status: m.status === "ATIVO" ? "Ativa" : "Desativada",
                    turmasVinculadas: contagemPorMateria[m.id] ?? 0,
                }))
            );
        })();
        return () => {
            cancelled = true;
        };
    }, []);

    useLayoutEffect(() => {
        const el = tableAreaRef.current;
        if (!el) return;

        const compute = () => {
            const available = el.clientHeight - HEADER_HEIGHT;
            const rows = Math.max(MIN_PAGE_SIZE, Math.floor(available / ROW_HEIGHT));
            setPageSize(rows);
        };

        compute();
        const ro = new ResizeObserver(compute);
        ro.observe(el);
        return () => ro.disconnect();
    }, []);

    const filteredMaterias = useMemo(() => {
        const term = search.trim().toLowerCase();
        if (!term) return materias;
        return materias.filter(
            (m) =>
                m.codigo.toLowerCase().includes(term) ||
                m.nome.toLowerCase().includes(term)
        );
    }, [materias, search]);

    const totalPages = Math.max(1, Math.ceil(filteredMaterias.length / pageSize));
    const currentPage = Math.min(page, totalPages);
    const pagedMaterias = filteredMaterias.slice(
        (currentPage - 1) * pageSize,
        currentPage * pageSize
    );

    useEffect(() => {
        if (page > totalPages) setPage(totalPages);
    }, [page, totalPages]);

    function handleSearchChange(value: string) {
        setSearch(value);
        setPage(1);
    }

    function handleEdit(materia: Materia) {
        const params = new URLSearchParams({
            id: materia.id,
            codigo: materia.codigo,
            nome: materia.nome,
            status: materia.status === "Ativa" ? "ATIVO" : "INATIVO",
        });
        router.push(`/admin/pages/materias/editarMateria?${params.toString()}`);
    }

    function handleDelete(materia: Materia) {
        setMateriaParaDesativar(materia);
    }

    async function confirmarDesativacao() {
        if (!materiaParaDesativar) return;
        if (materiaParaDesativar.turmasVinculadas > 0) {
            setMateriaParaDesativar(null);
            return;
        }
        const resultado = await desativarMateria(materiaParaDesativar.id);
        if (resultado.ok) {
            setMaterias((prev) =>
                prev.map((m) =>
                    m.id === materiaParaDesativar.id ? { ...m, status: "Desativada" } : m
                )
            );
            addToast("Matéria desativada.", "success");
        } else if (resultado.status === 409) {
            addToast(
                resultado.message ?? "Matéria não pode ser desativada.",
                "error"
            );
        }
        setMateriaParaDesativar(null);
    }

    async function handleReactivate(materia: Materia) {
        const resultado = await reativarMateria(
            materia.id,
            materia.codigo,
            materia.nome
        );
        if (resultado.ok) {
            setMaterias((prev) =>
                prev.map((m) => (m.id === materia.id ? { ...m, status: "Ativa" } : m))
            );
            addToast("Matéria reativada.", "success");
        }
    }

    const columns: TableColumn<Materia>[] = [
        { key: "codigo", title: "Código", mobileVariant: "stacked" },
        { key: "nome", title: "Nome" },
        {
            key: "turmasVinculadas",
            title: "Turmas vinculadas",
            render: (row) => <span>{row.turmasVinculadas}</span>,
        },
        {
            key: "status",
            title: "Status",
            render: (row) => (
                <span
                    className={`${styles.statusBadge} ${
                        row.status === "Ativa"
                            ? styles.statusAtivo
                            : styles.statusDesativado
                    }`}
                >
                    {row.status}
                </span>
            ),
        },
        {
            key: "acoes",
            title: "Ações",
            align: "right",
            mobileVariant: "actions",
            render: (row) => (
                <div className={styles.actions}>
                    {row.status === "Ativa" ? (
                        <>
                            <button
                                type="button"
                                className={styles.iconBtn}
                                onClick={() => handleEdit(row)}
                                aria-label={`Editar ${row.nome}`}
                            >
                                <Pencil size={18} color="#0d9488" />
                            </button>
                            <button
                                type="button"
                                className={styles.iconBtn}
                                onClick={() => handleDelete(row)}
                                aria-label={`Desativar ${row.nome}`}
                            >
                                <Trash2 size={18} color="#d02b29" />
                            </button>
                        </>
                    ) : (
                        <button
                            type="button"
                            className={styles.iconBtn}
                            onClick={() => handleReactivate(row)}
                            aria-label={`Reativar ${row.nome}`}
                        >
                            <RotateCw size={18} color="#0d9488" />
                        </button>
                    )}
                </div>
            ),
        },
    ];

    return (
        <div className={styles.cadastro}>
            <div className={styles.headerRow}>
                <h1 className={styles.pageTitle}>Matérias cadastradas</h1>
                <Button
                    style="filled"
                    action="primary"
                    icon={<Plus size={16} />}
                    label="Nova matéria"
                    onClick={() => router.push("/admin/pages/materias/novaMateria")}
                />
            </div>

            <div className={styles.searchRow}>
                <SearchInput
                    value={search}
                    onChange={handleSearchChange}
                    placeholder="Buscar matéria por código ou nome..."
                />
            </div>

            <div ref={tableAreaRef} className={styles.tableArea}>
                <Table
                    columns={columns}
                    data={pagedMaterias}
                    rowKey={(row) => row.id}
                    emptyMessage="Nenhuma matéria encontrada."
                />
            </div>

            <div className={styles.paginationRow}>
                <Pagination
                    currentPage={currentPage}
                    totalPages={totalPages}
                    onPageChange={setPage}
                />
            </div>

            <Modal
                open={materiaParaDesativar !== null}
                onClose={() => setMateriaParaDesativar(null)}
                title={
                    materiaParaDesativar && materiaParaDesativar.turmasVinculadas > 0
                        ? "Não é possível desativar"
                        : "Desativar matéria"
                }
                icon={<AlertTriangle size={20} color="#d02b29" />}
                accentColor="#d02b29"
                footer={
                    materiaParaDesativar && materiaParaDesativar.turmasVinculadas > 0 ? (
                        <Button
                            style="filled"
                            action="primary"
                            label="Entendi"
                            onClick={() => setMateriaParaDesativar(null)}
                        />
                    ) : (
                        <>
                            <Button
                                style="ghost"
                                label="Cancelar"
                                onClick={() => setMateriaParaDesativar(null)}
                            />
                            <Button
                                style="filled"
                                action="danger"
                                label="Desativar matéria"
                                onClick={confirmarDesativacao}
                            />
                        </>
                    )
                }
            >
                {materiaParaDesativar && materiaParaDesativar.turmasVinculadas > 0 ? (
                    <>
                        <p className={styles.modalText}>
                            A matéria <strong>{materiaParaDesativar.nome}</strong> não pode ser desativada porque está vinculada a{" "}
                            <strong>
                                {materiaParaDesativar.turmasVinculadas}{" "}
                                {materiaParaDesativar.turmasVinculadas === 1 ? "turma" : "turmas"}
                            </strong>
                            .
                        </p>
                        <div className={styles.modalNote}>
                            Remova o vínculo da matéria com as turmas antes de desativá-la.
                        </div>
                    </>
                ) : (
                    <>
                        <p className={styles.modalText}>
                            Tem certeza que deseja desativar a matéria{" "}
                            <strong>{materiaParaDesativar?.nome}</strong>?
                        </p>
                        <div className={styles.modalNote}>
                            A matéria fica inacessível para chat e gerenciamento de materiais. Todo o histórico é preservado e pode ser restaurado ao reativar
                        </div>
                    </>
                )}
            </Modal>
        </div>
    );
}
