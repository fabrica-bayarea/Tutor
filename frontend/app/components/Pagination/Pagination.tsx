"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import styles from "./Pagination.module.css";

type PaginationProps = {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
    siblingCount?: number;
};

function buildPageList(current: number, total: number, siblings: number): (number | "...")[] {
    if (total <= 1) return [1];

    const pages: (number | "...")[] = [];
    const left = Math.max(2, current - siblings);
    const right = Math.min(total - 1, current + siblings);

    pages.push(1);
    if (left > 2) pages.push("...");
    for (let i = left; i <= right; i++) pages.push(i);
    if (right < total - 1) pages.push("...");
    if (total > 1) pages.push(total);

    return pages;
}

export default function Pagination({
    currentPage,
    totalPages,
    onPageChange,
    siblingCount = 1,
}: PaginationProps) {
    const pages = buildPageList(currentPage, totalPages, siblingCount);
    const canPrev = currentPage > 1;
    const canNext = currentPage < totalPages;

    return (
        <nav className={styles.pagination} aria-label="Paginação">
            <button
                type="button"
                className={styles.navBtn}
                onClick={() => canPrev && onPageChange(currentPage - 1)}
                disabled={!canPrev}
                aria-label="Página anterior"
            >
                <ChevronLeft size={16} />
                <span className={styles.navLabel}>Anterior</span>
            </button>

            <ul className={styles.pageList}>
                {pages.map((p, i) =>
                    p === "..." ? (
                        <li key={`ellipsis-${i}`} className={styles.ellipsis}>
                            ...
                        </li>
                    ) : (
                        <li key={p}>
                            <button
                                type="button"
                                className={`${styles.pageBtn} ${
                                    p === currentPage ? styles.pageBtnActive : ""
                                }`}
                                onClick={() => onPageChange(p)}
                                aria-current={p === currentPage ? "page" : undefined}
                            >
                                {p}
                            </button>
                        </li>
                    )
                )}
            </ul>

            <button
                type="button"
                className={styles.navBtn}
                onClick={() => canNext && onPageChange(currentPage + 1)}
                disabled={!canNext}
                aria-label="Próxima página"
            >
                <span className={styles.navLabel}>Próximo</span>
                <ChevronRight size={16} />
            </button>
        </nav>
    );
}
