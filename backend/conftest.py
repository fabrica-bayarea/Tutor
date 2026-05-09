import sys
import os

# Garante que o diretório raiz do backend esteja no PYTHONPATH,
# permitindo que todos os testes encontrem os módulos 'app' e 'application'.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))