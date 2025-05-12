import PaginaInicial from "./components/PaginaInicial/paginaInicial";
import { ModalProvider } from "./contexts/contextModal"

// Página inicial da aplicação com contexto de modais aplicado
export default function Home() {
  return (
    <ModalProvider>
      <PaginaInicial/>
    </ModalProvider>
  );
};