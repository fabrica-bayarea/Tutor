"use client";

import Header from "./components/Header/Header";
import Aside from "./components/Aside/Aside";
import styles from "./layout.module.css"

export default function LayoutAdmin({children}: { children: React.ReactNode }){
    return (
        <section className={styles.mainSection}>
            <Aside/>
            <section className={styles.pageMediaSection}>
                <Header/>
                {children}
            </section>
        </section>
    )
}