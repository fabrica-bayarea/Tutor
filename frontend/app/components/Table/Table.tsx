"use client";

import React from "react";
import styles from "./Table.module.css";

export type TableColumn<T> = {
    key: string;
    title: string;
    align?: "left" | "center" | "right";
    width?: string;
    render?: (row: T, index: number) => React.ReactNode;
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
                            <td colSpan={columns.length} className={styles.emptyCell}>
                                {emptyMessage}
                            </td>
                        </tr>
                    ) : (
                        data.map((row, index) => (
                            <tr key={rowKey ? rowKey(row, index) : index}>
                                {columns.map((col) => (
                                    <td
                                        key={col.key}
                                        style={{ textAlign: col.align ?? "left" }}
                                    >
                                        {col.render
                                            ? col.render(row, index)
                                            : (row[col.key] as React.ReactNode)}
                                    </td>
                                ))}
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
}
