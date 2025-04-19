import React, { useCallback, useContext } from 'react';
import { useDropzone } from 'react-dropzone';
import styles from './ExtratorMenu.module.css';
import addImage from "../../assets/add.png"
import { ModalContext} from "../../contexts/contextModal"
import Select from 'react-select';

const ExtratorWindow = () => {
    const onDrop = useCallback((acceptedFiles: any) => { }, []);
    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });
    const {fecharMenuExtracao} = useContext(ModalContext)!;

    return (
        <div className={styles.container}>
            <div className={styles.extratorContainer}>
                <div className={styles.infoBar}>
                    <div className={styles.title}>
                        <h1>Adicionar arquivos à LLM</h1>
                    </div>
                    <button  onClick={fecharMenuExtracao}  className={styles.closeModalButton}>X</button>
                </div>

                <div className={styles.materiaChooseContainer}>
                    <div className={styles.materiaChoose}>
                        <h1>Matéria</h1>
                        <div className={styles.dropDown}>
                            <Select
                                /*defaultValue={["Colocar link para matérias do back aq"]}*/
                                isMulti
                                name="colors"
                                /*options={["Colocar link para matérias do back aq"]} */
                                className="basic-multi-select"
                                placeholder="Selecione a Matéria"
                                classNamePrefix="Selecione a Matéria"
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
                        <p><img src={addImage.src} width={100} height={100} style={{ opacity: 0.5 }} /><br />clique ou arraste arquivos aqui</p>
                    )}
                </div>

                <div className={styles.linkTextoContainer}>
                    <div className={styles.linkContainer}>
                        <div className={styles.linkContainerDiv}>
                            <h1>Link:</h1>
                            <input
                                type="link"
                                placeholder="Digite aqui."
                                className="textInput"
                            />
                        </div>
                    </div>
                    <div className={styles.textoContainer}>
                        <div className={styles.textoContainerDiv}>
                            <h1>Texto:</h1>
                            <textarea
                                placeholder="Digite aqui."
                            />
                        </div>
                    </div>
                </div>

                <div className={styles.arqEnviarContainer}>
                    <div className={styles.statusBarDiv}>
                        <p>Arquivos Selecionados</p>
                        <progress value={100} />
                        <p>0/10</p>
                    </div>
                    <button className={styles.enviar}>Enviar</button>
                </div>
            </div>
        </div>
    );
};

export default ExtratorWindow;