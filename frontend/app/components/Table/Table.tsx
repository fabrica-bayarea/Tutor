"use client";

import React from "react";
import styles from "./Table.module.css";

export type TableColumn<T> = {
    key: string;
    title: string;
    align?: "left" | "center" | "right";
    width?: string;
    render?: (row: T, index: number) => React.ReactNode;
    /**
     * Como a coluna se comporta no layout de card (mobile).
     * - "stacked": empilha o conteúdo sem mostrar o label da coluna (ex: bloco de identidade).
     * - "inline": mostra "Label: valor" (padrão).
     * - "actions": fica no canto superior direito do card, sem label.
     * - "hidden": não aparece no card.
     */
    mobileVariant?: "stacked" | "inline" | "actions" | "hidden";
};

type TableProps<T> = {
    columns: TableColumn<T>[];
    data: T[];
    rowKey?: (row: T, index: number) => string | number;
    emptyMessage?: string;
    className?: string;
};

export default function Table<T extends Record<string, any>>({
    columns,
    data,
    rowKey,
    emptyMessage = "Nenhum registro encontrado.",
    className,
}: TableProps<T>) {
    const renderCellContent = (col: TableColumn<T>, row: T, index: number) =>
        col.render ? col.render(row, index) : (row[col.key] as React.ReactNode);

    return (
        <div className={`${styles.tableWrapper} ${className ?? ""}`}>
            <table className={styles.table}>
                <thead>
                    <tr>
                        {columns.map((col) => (
                            <th
                                key={col.key}
                                style={{
                                    textAlign: col.align ?? "left",
                                    width: col.width,
                                }}
                            >
                                {col.title}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.length === 0 ? (
                        <tr>
                            <td
                                colSpan={columns.length}
                                className={styles.emptyCell}
                            >
                                {emptyMessage}
                            </td>
                        </tr>
                    ) : (
                        data.map((row, index) => (
                            <tr key={rowKey ? rowKey(row, index) : index}>
                                {columns.map((col) => {
                                    const variant = col.mobileVariant ?? "inline";
                                    return (
                                        <td
                                            key={col.key}
                                            data-label={col.title}
                                            data-variant={variant}
                                            style={{ textAlign: col.align ?? "left" }}
                                            className={
                                                variant === "hidden"
                                                    ? styles.mobileHidden
                                                    : undefined
                                            }
                                        >
                                            <span className={styles.cellLabel}>
                                                {col.title}
                                            </span>
                                            <span className={styles.cellValue}>
                                                {renderCellContent(col, row, index)}
                                            </span>
                                        </td>
                                    );
                                })}
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
}