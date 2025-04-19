import PaginaInicial from "./components/PaginaInicial/paginaInicial";
import { ModalProvider } from "./contexts/contextModal"

export default function Home() {
  return (
    <ModalProvider>
      <PaginaInicial/>
    </ModalProvider>
  );
};