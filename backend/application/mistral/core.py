import os
from .rag_engine import RAGEngine
from .llm_load import LLMWrapper
from .rag_pipeline import RAGPipeline

rag = RAGEngine(collection_name="documentos")
llm = LLMWrapper(model_name="mistral")
pipeline = RAGPipeline(rag=rag, llm=llm)
