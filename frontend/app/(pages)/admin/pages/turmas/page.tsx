"use client";

import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Pencil, Trash2, RotateCw, Plus, AlertTriangle } from "lucide-react";
import styles from "./page.module.css";
import Table, { TableColumn } from "../../../../components/Table/Table";
import Button from "../../../../components/Button/Button";
import SearchInput from "../../../../components/SearchInput/SearchInput";
import Pagination from "../../../../components/Pagination/Pagination";
import Modal from "../../../../components/Modal/Modal";
import Select, { SelectOption } from "../../../../components/Select/Select";
import {
    listarTurmas,
    desativarTurma,
    reativarTurma,
} from "../../../../services/service_turma";
import { useToast } from "@/contexts/ToastContext";
import {
    TURNO_DISPLAY_OPTIONS,
    turnoApiToDisplay,
    turnoDisplayToApi,
} from "@/utils/turno";

type TurmaStatus = "Ativa" | "Desativada";

type Turma = {
    id: string;
    codigo: string;
    semestre: string;
    turno: string;
    turnoApi: string;
    status: TurmaStatus;
};

const ROW_HEIGHT = 49;
const HEADER_HEIGHT = 47;
const MIN_PAGE_SIZE = 1;
const SEARCH_DEBOUNCE_MS = 300;

const TURNO_FILTER_OPTIONS: SelectOption[] = [
    { value: "", label: "Todos os turnos" },
    ...TURNO_DISPLAY_OPTIONS.map((t) => ({ value: t, label: t })),
];

export default function Turmas() {
    const router = useRouter();
    const { addToast } = useToast();
    const [turmas, setTurmas] = useState<Turma[]>([]);
    const [search, setSearch] = useState("");
    const [debouncedSearch, setDebouncedSearch] = useState("");
    const [semestreFiltro, setSemestreFiltro] = useState("");
    const [debouncedSemestre, setDebouncedSemestre] = useState("");
    const [turnoFiltro, setTurnoFiltro] = useState("");
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(8);
    const [totalPages, setTotalPages] = useState(1);
    const [loading, setLoading] = useState(false);
    const [turmaParaDesativar, setTurmaParaDesativar] = useState<Turma | null>(
        null
    );
    const tableAreaRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handle = setTimeout(
            () => setDebouncedSearch(search.trim()),
            SEARCH_DEBOUNCE_MS
        );
        return () => clearTimeout(handle);
    }, [search]);

    useEffect(() => {
        const handle = setTimeout(
            () => setDebouncedSemestre(semestreFiltro.trim()),
            SEARCH_DEBOUNCE_MS
        );
        return () => clearTimeout(handle);
    }, [semestreFiltro]);

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

    useEffect(() => {
        setPage(1);
    }, [debouncedSearch, debouncedSemestre, turnoFiltro]);

    useEffect(() => {
        let cancelled = false;
        (async () => {
            setLoading(true);
            const resultado = await listarTurmas({
                search: debouncedSearch || undefined,
                semestre: debouncedSemestre || undefined,
                turno: turnoFiltro ? turnoDisplayToApi(turnoFiltro) : undefined,
                page,
                limit: pageSize,
            });
            if (cancelled) return;
            setTurmas(
                resultado.turmas.map((t) => ({
                    id: t.id,
                    codigo: t.codigo,
                    semestre: t.semestre,
                    turno: turnoApiToDisplay(t.turno),
                    turnoApi: t.turno,
                    status: t.status === "ATIVO" ? "Ativa" : "Desativada",
                }))
            );
            setTotalPages(Math.max(1, resultado.pagination.pages));
            setLoading(false);
        })();
        return () => {
            cancelled = true;
        };
    }, [debouncedSearch, debouncedSemestre, turnoFiltro, page, pageSize]);

    function handleSearchChange(value: string) {
        setSearch(value);
    }

    function handleEdit(turma: Turma) {
        const params = new URLSearchParams({
            id: turma.id,
            codigo: turma.codigo,
            semestre: turma.semestre,
            turno: turma.turnoApi,
            status: turma.status === "Ativa" ? "ATIVO" : "INATIVO",
        });
        router.push(`/admin/pages/turmas/editarTurma?${params.toString()}`);
    }

    function handleDelete(turma: Turma) {
        setTurmaParaDesativar(turma);
    }

    async function recarregar() {
        const resultado = await listarTurmas({
            search: debouncedSearch || undefined,
            semestre: debouncedSemestre || undefined,
            turno: turnoFiltro ? turnoDisplayToApi(turnoFiltro) : undefined,
            page,
            limit: pageSize,
        });
        setTurmas(
            resultado.turmas.map((t) => ({
                id: t.id,
                codigo: t.codigo,
                semestre: t.semestre,
                turno: turnoApiToDisplay(t.turno),
                turnoApi: t.turno,
                status: t.status === "ATIVO" ? "Ativa" : "Desativada",
            }))
        );
        setTotalPages(Math.max(1, resultado.pagination.pages));
    }

    async function confirmarDesativacao() {
        if (!turmaParaDesativar) return;
        const resultado = await desativarTurma(turmaParaDesativar.id);
        if (resultado.ok) {
            addToast("Turma desativada.", "success");
            await recarregar();
        } else if (resultado.status === 409) {
            addToast(
                resultado.message ?? "Turma não pode ser desativada.",
                "error"
            );
        } else {
            addToast(
                resultado.message ?? "Erro ao desativar a turma.",
                "error"
            );
        }
        setTurmaParaDesativar(null);
    }

    async function handleReactivate(turma: Turma) {
        const resultado = await reativarTurma(
            turma.id,
            turma.codigo,
            turma.semestre,
            turma.turnoApi
        );
        if (resultado.ok) {
            addToast("Turma reativada.", "success");
            await recarregar();
        } else {
            addToast(resultado.message ?? "Erro ao reativar a turma.", "error");
        }
    }

    const turnoFiltroValue =
        TURNO_FILTER_OPTIONS.find((opt) => opt.value === turnoFiltro) ??
        TURNO_FILTER_OPTIONS[0];

    const columns: TableColumn<Turma>[] = [
        { key: "codigo", title: "Código", mobileVariant: "stacked" },
        { key: "semestre", title: "Semestre" },
        { key: "turno", title: "Turno" },
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
                                aria-label={`Editar ${row.codigo}`}
                            >
                                <Pencil size={18} color="#0d9488" />
                            </button>
                            <button
                                type="button"
                                className={styles.iconBtn}
                                onClick={() => handleDelete(row)}
                                aria-label={`Desativar ${row.codigo}`}
                            >
                                <Trash2 size={18} color="#d02b29" />
                            </button>
                        </>
                    ) : (
                        <button
                            type="button"
                            className={styles.iconBtn}
                            onClick={() => handleReactivate(row)}
                            aria-label={`Reativar ${row.codigo}`}
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
                <h1 className={styles.pageTitle}>Turmas cadastradas</h1>
                <Button
                    style="filled"
                    action="primary"
                    icon={<Plus size={16} />}
                    label="Nova turma"
                    onClick={() => router.push("/admin/pages/turmas/novaTurma")}
                />
            </div>

            <div className={styles.filtersRow}>
                <div className={styles.searchCell}>
                    <SearchInput
                        value={search}
                        onChange={handleSearchChange}
                        placeholder="Buscar turma por código..."
                    />
                </div>
                <input
                    type="text"
                    className={styles.filterInput}
                    value={semestreFiltro}
                    onChange={(e) => setSemestreFiltro(e.target.value)}
                    placeholder="Filtrar por semestre (ex: 2026.1)"
                    maxLength={6}
                />
                <div className={styles.filterSelect}>
                    <Select
                        instanceId="turnoFiltro"
                        options={TURNO_FILTER_OPTIONS}
                        value={turnoFiltroValue}
                        onChange={(opt) => {
                            const selected = opt as SelectOption | null;
                            setTurnoFiltro(selected?.value ?? "");
                        }}
                        placeholder="Filtrar por turno"
                        isSearchable={false}
                    />
                </div>
            </div>

            <div ref={tableAreaRef} className={styles.tableArea}>
                <Table
                    columns={columns}
                    data={turmas}
                    rowKey={(row) => row.id}
                    emptyMessage={
                        loading ? "Carregando..." : "Nenhuma turma encontrada."
                    }
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
                open={turmaParaDesativar !== null}
                onClose={() => setTurmaParaDesativar(null)}
                title="Desativar turma"
                icon={<AlertTriangle size={20} color="#d02b29" />}
                accentColor="#d02b29"
                footer={
                    <>
                        <Button
                            style="ghost"
                            label="Cancelar"
                            onClick={() => setTurmaParaDesativar(null)}
                        />
                        <Button
                            style="filled"
                            action="danger"
                            label="Desativar turma"
                            onClick={confirmarDesativacao}
                        />
                    </>
                }
            >
                <p className={styles.modalText}>
                    Tem certeza que deseja desativar a turma{" "}
                    <strong>{turmaParaDesativar?.codigo}</strong>?
                </p>
                <div className={styles.modalNote}>
                    A turma fica inacessível para novos vínculos. Todo o histórico é
                    preservado e pode ser restaurado ao reativar.
                </div>
            </Modal>
        </div>
    );
}
