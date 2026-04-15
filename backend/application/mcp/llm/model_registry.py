from typing import Dict

class ModelRegistry:

    def __init__(self):
        self._models: Dict[str,dict] = {}

    def register(self, llm_id:str,config:dict):
        self._models[llm_id] = config

    def get(self, llm_id:str) -> dict:
        if llm_id not in self._models:
            raise ValueError(f"Modelo {llm_id} não encontrado")
        return self._models[llm_id]
    
    def list_models(self):
        return list(self._models.keys())