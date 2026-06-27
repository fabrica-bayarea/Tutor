"use client";

import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Pencil, Trash2, RotateCw, Plus, AlertTriangle } from "lucide-react";
import styles from "./page.module.css";
import Table, { TableColumn } from "../../../../components/Table/Table";
import Button from "../../../../components/Button/Button";
import SearchInput from "../../../../components/SearchInput/SearchInput";
import Pagination from "../../../../components/Pagination/Pagination";
import Modal from "../../../../components/Modal/Modal";
import { listarAlunosPaginado, desativarAluno, reativarAluno } from "../../../../services/service_aluno";
import { Status } from "@/utils/roles";
import { useToast } from "@/contexts/ToastContext";

type AlunoStatus = "Ativo" | "Desativado";

type Aluno = {
    id: string;
    nome: string;
    matricula: string;
    email: string;
    status: AlunoStatus;
};

const ROW_HEIGHT = 49;
const HEADER_HEIGHT = 47;
const MIN_PAGE_SIZE = 1;

export default function Alunos() {
    const router = useRouter();
    const { addToast } = useToast();
    const [alunos, setAlunos] = useState<Aluno[]>([]);
    const [search, setSearch] = useState("");
    const [debouncedSearch, setDebouncedSearch] = useState("");
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(8);
    const [totalPages, setTotalPages] = useState(1);
    const [alunoParaDesativar, setAlunoParaDesativar] = useState<Aluno | null>(null);
    const tableAreaRef = useRef<HTMLDivElement>(null);

    // Debounce da busca: evita uma requisição por tecla e volta para a 1ª página.
    useEffect(() => {
        const t = setTimeout(() => {
            setDebouncedSearch(search);
            setPage(1);
        }, 300);
        return () => clearTimeout(t);
    }, [search]);

    // Busca a página atual no servidor (paginação + filtro server-side — GAP-02-D).
    const carregar = useCallback(async () => {
        if (pageSize < 1) return;
        const r = await listarAlunosPaginado(page, pageSize, debouncedSearch);
        setAlunos(
            r.usuarios.map((u) => ({
                id: u.id,
                nome: u.nome,
                matricula: u.matricula,
                email: u.email,
                status: u.status === Status.ATIVO ? "Ativo" : "Desativado",
            }))
        );
        setTotalPages(Math.max(1, r.pages));
        if (r.pages >= 1 && page > r.pages) setPage(r.pages);
    }, [page, pageSize, debouncedSearch]);

    useEffect(() => {
        carregar();
    }, [carregar]);

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

    function handleSearchChange(value: string) {
        setSearch(value);
    }

    function handleEdit(aluno: Aluno) {
        const params = new URLSearchParams({
            id: aluno.id,
            nome: aluno.nome,
            matricula: aluno.matricula,
            email: aluno.email,
        });
        router.push(`/admin/pages/alunos/editarAluno?${params.toString()}`);
    }

    function handleDelete(aluno: Aluno) {
        setAlunoParaDesativar(aluno);
    }

    async function confirmarDesativacao() {
        if (!alunoParaDesativar) return;
        const resultado = await desativarAluno(alunoParaDesativar.id);
        if (resultado.ok) {
            addToast("Aluno desativado.", "success");
            carregar();
        }
        setAlunoParaDesativar(null);
    }

    async function handleReactivate(aluno: Aluno) {
        const resultado = await reativarAluno(aluno.id);
        if (resultado.ok) {
            addToast("Aluno reativado.", "success");
            carregar();
        }
    }

    const columns: TableColumn<Aluno>[] = [
        { key: "nome", title: "Nome", mobileVariant: "stacked" },
        { key: "matricula", title: "Matrícula" },
        { key: "email", title: "E-mail" },
        {
            key: "status",
            title: "Status",
            render: (row) => (
                <span
                    className={`${styles.statusBadge} ${
                        row.status === "Ativo" ? styles.statusAtivo : styles.statusDesativado
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
            <div className={styles.buttonContainer}>
                <Button
                    style="filled"
                    action="primary"
                    icon={<Plus size={16} />}
                    label="Novo Aluno"
                    onClick={() => router.push("/admin/pages/alunos/novoAluno")}
                />
            </div>

            <div className={styles.searchRow}>
                <SearchInput
                    value={search}
                    onChange={handleSearchChange}
                    placeholder="Buscar aluno por nome, matrícula ou e-mail..."
                />
            </div>

            <div ref={tableAreaRef} className={styles.tableArea}>
                <Table
                    columns={columns}
                    data={alunos}
                    rowKey={(row) => row.id}
                    emptyMessage="Nenhum aluno encontrado."
                />
            </div>

            <div className={styles.paginationRow}>
                <Pagination
                    currentPage={page}
                    totalPages={totalPages}
                    onPageChange={setPage}
                />
            </div>

            <Modal
                open={alunoParaDesativar !== null}
                onClose={() => setAlunoParaDesativar(null)}
                title="Desativar usuário"
                icon={<AlertTriangle size={20} color="#d02b29" />}
                accentColor="#d02b29"
                footer={
                    <>
                        <Button
                            style="ghost"
                            label="Cancelar"
                            onClick={() => setAlunoParaDesativar(null)}
                        />
                        <Button
                            style="filled"
                            action="danger"
                            label="Desativar aluno"
                            onClick={confirmarDesativacao}
                        />
                    </>
                }
            >
                <p className={styles.modalText}>
                    Tem certeza que deseja desativar o acesso de{" "}
                    <strong>{alunoParaDesativar?.nome}</strong>? Ele não conseguirá mais
                    fazer login.
                </p>
                <div className={styles.modalNote}>
                    O histórico de conversas e matrículas são preservados e podem ser
                    restaurados quando o aluno for reativado.
                </div>
            </Modal>
        </div>
    );
}
