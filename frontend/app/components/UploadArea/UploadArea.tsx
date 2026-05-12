'use client';

import { useDropzone } from 'react-dropzone';
import { Upload } from 'lucide-react';
import StatusBadge, { StatusBadgeVariant } from '../StatusBadge/StatusBadge';
import ProgressBar from '../ProgressBar/ProgressBar';
import styles from './UploadArea.module.css';

export type UploadFile = {
    name: string;
    size: string;
    progress: number;
    status: StatusBadgeVariant;
};

type UploadAreaProps = {
    onDrop: (files: File[]) => void;
    accept?: Record<string, string[]>;
    hint?: string;
    files?: UploadFile[];
};

export default function UploadArea({
    onDrop,
    accept,
    hint = 'PDF, DOCX, PPTX, MP4, MP3 — máx. 100 MB',
    files = [],
}: UploadAreaProps) {
    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept });

    return (
        <div className={styles.wrapper}>
            <div
                {...getRootProps()}
                className={[styles.dropzone, isDragActive ? styles.dragActive : ''].filter(Boolean).join(' ')}
            >
                <input {...getInputProps()} />
                <div className={styles.uploadIcon}>
                    <Upload size={20} color="#737373" />
                </div>
                <p className={styles.instruction}>
                    {isDragActive ? 'Solte os arquivos aqui' : 'Arraste arquivos aqui ou clique para selecionar'}
                </p>
                <p className={styles.hint}>{hint}</p>
            </div>

            {files.length > 0 && (
                <ul className={styles.fileList}>
                    {files.map((file, index) => (
                        <li key={index} className={styles.fileItem}>
                            <span className={styles.fileName}>{file.name}</span>
                            <span className={styles.fileSize}>{file.size}</span>
                            <StatusBadge variant={file.status} />
                            <div className={styles.fileProgress}>
                                <ProgressBar value={file.progress} height={6} />
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
