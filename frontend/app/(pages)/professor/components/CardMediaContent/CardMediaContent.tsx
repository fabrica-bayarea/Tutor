import { useState } from 'react';
import styles from './CardMediaContent.module.css';
import { File, Music, Play, Text, Trash2, Download, SquareArrowOutUpRight, Pencil } from 'lucide-react';
import IconButton from '@/app/components/IconButton/IconButton';
import { TIPOS_ARQUIVO } from '@/constants';
import { InterfaceArquivo } from '@/app/types';

export default function CardMediaContent({
    arquivo: {
        titulo,
        data_upload,
        tamanho_arquivo,
        tipo_arquivo
    },
    onOpen,
    onDownload,
    //onEdit,
    onDelete
}: {
    arquivo: {
        titulo: InterfaceArquivo["titulo"];
        data_upload: InterfaceArquivo["data_upload"];
        tamanho_arquivo?: string;
        tipo_arquivo?: string;
    },
    onOpen?: () => void,
    onDownload?: () => void,
    //onEdit?: () => void,
    onDelete?: () => void
}) {
    const [isHovered, setIsHovered] = useState(false);

    const handleMouseEnter = () => {
        setIsHovered(true);
    };

    const handleMouseLeave = () => {
        setIsHovered(false);
    };

    const toggleActions = (e: React.MouseEvent) => {
        e.stopPropagation();
    };

    const tipoArquivo = titulo.split('.').pop() || ''
    return (
        <div 
            className={styles.cardMediaContent}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            <div className={styles.cardMediaContentStateLayer}>
                <div className={styles.cardMediaContentLeft}>
                    <div className={styles.cardMediaContentIconContainer}>
                        {TIPOS_ARQUIVO.documento.includes(`.${tipoArquivo}`) ? <File size={24} /> :
                        TIPOS_ARQUIVO.video.includes(`.${tipoArquivo}`) ? <Play size={24} /> :
                        TIPOS_ARQUIVO.audio.includes(`.${tipoArquivo}`) ? <Music size={24} /> :
                        TIPOS_ARQUIVO.texto.includes(`.${tipoArquivo}`) ? <Text size={24} /> : null}
                    </div>
                    <span>{titulo}</span>
                </div>
                <div className={styles.cardMediaContentRight}>
                    <div><span>{data_upload.toString()}</span></div>
                    <div><span>{tamanho_arquivo || '2.64MB'}</span></div>
                    <div className={styles.actionsContainer}>
                        <IconButton
                            icon={<SquareArrowOutUpRight size={20} />}
                            title="Abrir arquivo"
                            aria-label="Abrir arquivo"
                            onClick={onOpen}
                        />
                        <IconButton
                            icon={<Download size={20} />}
                            title="Baixar arquivo"
                            aria-label="Baixar arquivo"
                            onClick={onDownload}
                        />
                        <IconButton
                            icon={<Pencil size={20} />}
                            title="Editar arquivo"
                            aria-label="Editar arquivo"
                            //onClick={onEdit}
                        />
                        <IconButton
                            icon={<Trash2 size={20} color="#D92F35" />}
                            title="Excluir arquivo"
                            aria-label="Excluir arquivo"
                            onClick={onDelete}
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}
