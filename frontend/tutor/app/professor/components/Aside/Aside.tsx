import { useState } from 'react';
import styles from './Aside.module.css';
import { Menu, House, GraduationCap, LibraryBig, Plus } from 'lucide-react';
import AsideMainButton from '../../../components/AsideMainButton/AsideMainButton';

type AsideProfessorProps = {
  selected: 'home' | 'turmas' | 'materias' | 'addFontes';
};

export default function Aside({ selected }: AsideProfessorProps) {
  return (
    <div className={styles.asideContainer}>
      <div className={styles.asideHeader}>
        <img src="" alt="" />
        <Menu size={24} />
      </div>
      <div className={styles.asideMainButtons}>
        <AsideMainButton
          icon={<House />}
          label="Início"
          isCollapsed={false}
          isSelected={selected === 'home'}
        />
        <AsideMainButton
          icon={<GraduationCap />}
          label="Minhas turmas"
          isCollapsed={false}
          isSelected={selected === 'turmas'}
        />
        <AsideMainButton
          icon={<LibraryBig />}
          label="Minhas matérias"
          isCollapsed={false}
          isSelected={selected === 'materias'}
        />
        <AsideMainButton
          icon={<Plus />}
          label="Adicionar fontes"
          isCollapsed={false}
          isSelected={selected === 'addFontes'}
        />
      </div>
    </div>
  );
}
