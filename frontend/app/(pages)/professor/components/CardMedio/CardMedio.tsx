import styles from './CardMedio.module.css';
import { Shapes, Brain, ChartNoAxesColumnIncreasing, GraduationCap, ChevronRight } from 'lucide-react';
import BarraDeProgresso from '../BarraDeProgresso/BarraDeProgresso';

interface ItemDuvida {
  duvida: string;
  materia: string;
  volume: string;
  porcentagem: string;
}

interface CardPequenoProps {
  titulo: string;
  tipo: 'RankingDeDuvidas' | 'RankingDeMaterias' | 'InsightTutor' | 'MateriasEnsinadas';
  itens?: ItemDuvida[];
}

export default function CardPequeno({ titulo, tipo, itens = [] }: CardPequenoProps) {

  const renderHeader = () => {
    switch(tipo) {
      case 'RankingDeDuvidas':
        return <ChartNoAxesColumnIncreasing />;
      case 'RankingDeMaterias':
        return <Shapes />;
      case 'InsightTutor':
        return <Brain />;
      case 'MateriasEnsinadas':
        return <GraduationCap />;
      default:
        return null;
    }
  }

  const renderContent = () => {
    switch(tipo) {
      case 'RankingDeDuvidas':
        return itens.map((el, idx) => (
          <div key={idx} className={styles.itemRankeadoPerguntas}>
            <div className={styles.perguntasInfos}>
              <p>{el.duvida}</p>
              <p>{el.materia}</p>
            </div>
            <div className={styles.perguntasInfos}>
              <p className={styles.bolderText}>{el.volume}</p>
              <p className={styles.legendBottomPercentage}>{el.porcentagem}%</p>
            </div>
          </div>
        ));
      case 'RankingDeMaterias':
        return itens.map((el, idx) => (
          <div key={idx} className={styles.itemRankeadoVolume}>
            <div className={styles.volumeInfos}>
              <p>{el.materia}</p>
              <p>{el.volume} dúvidas</p>
            </div>
            <BarraDeProgresso porcentagem={Number(el.porcentagem)} />
          </div>
        ));
      case 'InsightTutor':
        return (
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Ducimus dicta sit quia assumenda inventore, 
            porro eius qui atque ratione blanditiis earum sint illo consectetur incidunt! Quo explicabo quidem 
            eveniet dolore.
          </p>
        );
      case 'MateriasEnsinadas':
        return itens.map((el, idx) => (
          <div key={idx} className={styles.itemRankeadoVolume}>
            <div className={styles.itemDireitoMateria}>
              <p>{el.materia}</p>
              <ChevronRight />
            </div>
          </div>
        ));
      default:
        return null;
    }
  }

  return (
    <div className={styles.itemEstatisticaRanking}>
      <div className={styles.headerEstatisticaRanking}>
        {renderHeader()}
        <p className={styles.bolderText}>
          {tipo === 'InsightTutor' ? 'Insights do Tutor' :
           tipo === 'MateriasEnsinadas' ? 'Matérias ensinadas' :
           titulo}
        </p>
      </div>
      <div>
        {renderContent()}
      </div>
    </div>
  );
}
