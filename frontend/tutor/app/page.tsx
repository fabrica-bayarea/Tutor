import Image from "next/image";
import styles from "./page.module.css";
import PaginaExtracao from "./Extracao/paginaExtracao";
import PaginaChat from "./Chat/paginaChat";

export default function Home() {
  return (
    <div>
      <PaginaExtracao/>
    </div>
  );
}
