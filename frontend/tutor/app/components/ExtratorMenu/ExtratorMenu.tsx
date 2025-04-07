import React, { useCallback, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDropzone } from 'react-dropzone';
import styles from './ExtratorMenu.module.css';
import addImage from "../../assets/add.png"
import Select from 'react-select';
import { s } from 'framer-motion/client';

const ModalExample = () => {
    const [materiasEscolhidas, setmateriasEscolhidas] = useState([])
    const [inputValue, setInputValue] = React.useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const onDrop = useCallback((acceptedFiles: any) => {
        console.log(acceptedFiles);
    }, []);
    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

    const openModal = () => {
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
    };

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(event.target.value);
    };

    return (
        <div className={styles.container}>
            <button onClick={openModal} className={styles.openModalButton}>
                <img src={addImage.src} alt="Logo Bay Area" width={60} height={60} />
            </button>

            <AnimatePresence>
                {isModalOpen && (
                    <>
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 0.8 }}
                            exit={{ opacity: 0 }}
                            className={styles.modalBackdrop}
                        />
                        <motion.div
                            initial={{ opacity: 0, scale: 0.5 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.5 }}
                            transition={{ duration: 0.2 }}
                            className={styles.modalContent}
                        >
                            <div className={styles.extratorContainer}>
                                <div className={styles.infoBar}>
                                    <div className={styles.title}>
                                        <h1>Adicionar arquivos à LLM</h1>
                                    </div>
                                    <button onClick={closeModal} className={styles.closeModalButton}>X</button>
                                </div>

                                <div className={styles.materiaChooseContainer}>
                                    <div className={styles.materiaChoose}>
                                        <h1>Escolha a matéria para indexação:</h1>
                                        <div className={styles.dropDown}>
                                            <Select
                                                defaultValue={["Colocar link para matérias do back aq"]}
                                                isMulti
                                                name="colors"
                                                options={["Colocar link para matérias do back aq"]}
                                                className="basic-multi-select"
                                                classNamePrefix="select"
                                            />
                                        </div>
                                    </div>
                                    <div className={styles.materiasEscolhidas}>
                                        <script>materiasEscolhidas.map()</script>
                                    </div>
                                </div>

                                <div {...getRootProps()} className={`${styles.dragdropContainer} ${isDragActive ? styles.dragActive : ''}`}>
                                    <input {...getInputProps()} />
                                    {isDragActive ? (
                                        <p>Solte os arquivos aqui ...</p>
                                    ) : (
                                        <p><img src={addImage.src} width={100} height={100} /><br />Arraste e solte os arquivos aqui, ou clique para selecionar os arquivos</p>
                                    )}
                                </div>

                                <div className={styles.linkTextoContainer}>
                                    <div className={styles.linkContainer}>
                                        <div className={styles.linkContainerDiv}>
                                            <h1>Link:</h1>
                                            <input
                                                type="link"
                                                value={inputValue}
                                                onChange={handleInputChange}
                                                placeholder="Digite aqui."
                                                className="textInput"
                                            />
                                        </div>
                                        <button>Ok</button>
                                    </div>
                                    <div className={styles.textoContainer}>
                                        <div className={styles.textoContainerDiv}>
                                            <h1>Texto:</h1>
                                            <textarea
                                                placeholder="Digite aqui."
                                                rows={3}
                                                cols={80}
                                                minLength={10} 
                                            />
                                        </div>
                                        <button>Ok</button>
                                    </div>
                                </div>

                                <div className={styles.arqEnviarContainer}>
                                    <div className={styles.statusBarDiv}>
                                        <h1>0/?</h1>
                                        <progress value={100}/>
                                    </div>
                                    <button className={styles.enviar}>Enviar</button>
                                </div>
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </div>
    );
};

export default ModalExample;