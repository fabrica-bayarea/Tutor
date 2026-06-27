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
    listarProfessores,
    desativarProfessor,
    reativarProfessor,
} from "../../../../services/service_professor";
import { Status } from "@/utils/roles";
import { useToast } from "@/contexts/ToastContext";

type ProfessorStatus = "Ativo" | "Desativado";

type Professor = {
    id: string;
    nome: string;
    matricula: string;
    email: string;
    status: ProfessorStatus;
};

const ROW_HEIGHT = 49;
const HEADER_HEIGHT = 47;
const MIN_PAGE_SIZE = 1;

export default function Professores() {
    const router = useRouter();
    const { addToast } = useToast();
    const [professores, setProfessores] = useState<Professor[]>([]);
    const [search, setSearch] = useState("");
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(8);
    const [professorParaDesativar, setProfessorParaDesativar] =
        useState<Professor | null>(null);
    const tableAreaRef = useRef<HTMLDivElement>(null);

    async function carregarProfessores() {
        const lista = await listarProfessores();
        setProfessores(
            lista.map((p) => ({
                id: p.id,
                nome: p.nome,
                matricula: p.matricula,
                email: p.email,
                status: p.status === Status.ATIVO ? "Ativo" : "Desativado",
            }))
        );
    }

    useEffect(() => {
        carregarProfessores();
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

    const filteredProfessores = useMemo(() => {
        const term = search.trim().toLowerCase();
        if (!term) return professores;
        return professores.filter(
            (p) =>
                p.nome.toLowerCase().includes(term) ||
                p.matricula.toLowerCase().includes(term)
        );
    }, [professores, search]);

    const totalPages = Math.max(
        1,
        Math.ceil(filteredProfessores.length / pageSize)
    );
    const currentPage = Math.min(page, totalPages);
    const pagedProfessores = filteredProfessores.slice(
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

    function handleEdit(professor: Professor) {
        const params = new URLSearchParams({
            id: professor.id,
            nome: professor.nome,
            matricula: professor.matricula,
            email: professor.email,
        });
        router.push(
            `/admin/pages/professores/editarProfessor?${params.toString()}`
        );
    }

    function handleDelete(professor: Professor) {
        setProfessorParaDesativar(professor);
    }

    async function confirmarDesativacao() {
        if (!professorParaDesativar) return;
        const resultado = await desativarProfessor(professorParaDesativar.id);
        if (resultado.ok) {
            setProfessores((prev) =>
                prev.map((p) =>
                    p.id === professorParaDesativar.id
                        ? { ...p, status: "Desativado" }
                        : p
                )
            );
            addToast("Professor desativado.", "success");
        }
        setProfessorParaDesativar(null);
    }

    async function handleReactivate(professor: Professor) {
        const resultado = await reativarProfessor(professor.id);
        if (resultado.ok) {
            setProfessores((prev) =>
                prev.map((p) =>
                    p.id === professor.id ? { ...p, status: "Ativo" } : p
                )
            );
            addToast("Professor reativado.", "success");
        }
    }

    const columns: TableColumn<Professor>[] = [
        { key: "nome", title: "Nome", mobileVariant: "stacked" },
        { key: "matricula", title: "Matrícula" },
        { key: "email", title: "E-mail" },
        {
            key: "status",
            title: "Status",
            render: (row) => (
                <span
                    className={`${styles.statusBadge} ${
                        row.status === "Ativo"
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
                    {row.status === "Ativo" ? (
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
                <h1 className={styles.pageTitle}>Professores cadastrados</h1>
                <Button
                    style="filled"
                    action="primary"
                    icon={<Plus size={16} />}
                    label="Novo professor"
                    onClick={() =>
                        router.push("/admin/pages/professores/novoProfessor")
                    }
                />
            </div>

            <div className={styles.searchRow}>
                <SearchInput
                    value={search}
                    onChange={handleSearchChange}
                    placeholder="Buscar professor por nome ou matrícula..."
                />
            </div>

            <div ref={tableAreaRef} className={styles.tableArea}>
                <Table
                    columns={columns}
                    data={pagedProfessores}
                    rowKey={(row) => row.id}
                    emptyMessage="Nenhum professor encontrado."
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
                open={professorParaDesativar !== null}
                onClose={() => setProfessorParaDesativar(null)}
                title="Desativar professor"
                icon={<AlertTriangle size={20} color="#d02b29" />}
                accentColor="#d02b29"
                footer={
                    <>
                        <Button
                            style="ghost"
                            label="Cancelar"
                            onClick={() => setProfessorParaDesativar(null)}
                        />
                        <Button
                            style="filled"
                            action="danger"
                            label="Desativar professor"
                            onClick={confirmarDesativacao}
                        />
                    </>
                }
            >
                <p className={styles.modalText}>
                    Tem certeza que deseja desativar o acesso de{" "}
                    <strong>{professorParaDesativar?.nome}</strong>? Ele não
                    conseguirá mais fazer login.
                </p>
                <div className={styles.modalNote}>
                    O professor pode ser reativado posteriormente, preservando seus
                    dados.
                </div>
            </Modal>
        </div>
    );
}
