import sys
import os
from unittest.mock import MagicMock

# Garante que o diretório raiz do backend esteja no PYTHONPATH,
# permitindo que todos os testes encontrem os módulos 'app' e 'application'.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# IMPORTANTE: este conftest fica FORA do pacote `application`, então é carregado
# pelo pytest antes de qualquer módulo de teste importar `application`. Stubamos
# aqui `application.config.vector_database`, cujo corpo roda no import
# `os.makedirs("/data/chroma")` + `PersistentClient(...)`. No CI (Linux, usuário
# sem permissão em `/`) esse makedirs levanta PermissionError e, como o módulo
# está na cadeia `application → routes → service_arquivo → vector_database`,
# derruba a coleta de TODOS os testes que importam `application`/`app`.
# Substituindo o módulo inteiro por um mock, o corpo nunca executa.
sys.modules["application.config.vector_database"] = MagicMock()
sys.modules.setdefault("chromadb", MagicMock())
sys.modules.setdefault("ollama", MagicMock())