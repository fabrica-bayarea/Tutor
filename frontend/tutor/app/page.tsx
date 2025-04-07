import React from "react";
import styles from "./page.module.css";
import bayImage from "./assets/bayImage.png";
import userImage from "./assets/user.png"
import OptionsMenu from "./components/OptionMenu/OptionMenu";

export default function Home() {
  return (
    <div className={styles.containerGlobal}>


      <div className={styles.infoBar}>
        <div className={styles.title}>
          <img src={bayImage.src} alt="Logo Bay Area" width={70} height={70}/>
          <h1 className={styles.titulo}>Tutor</h1>
        </div>
        <div className={styles.profile}>
          <OptionsMenu/>
          <button className={styles.profileItem}><img src={userImage.src} alt="Logo Bay Area" width={90} height={90}/></button>
        </div>
      </div>

      <div className={styles.optionMenu}></div>

      <div className={styles.ContainerExtrator}></div>


      <div className={styles.containerUser}>
        <div className={styles.turmaMateria}>
          <div className={styles.turma}></div>
          <div className={styles.materia}></div>
        </div>
        <div className={styles.containerChat}></div>
      </div>


    </div>
  );
};