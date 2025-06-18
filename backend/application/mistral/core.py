from rag_engine import RAGengine
from llm_load import LLMWrapper
from rag_pipeline import RAGPipeline

rag = RAGengine()
rag.load_documents("dados/")

llm = LLMWrapper()

pipeline = RAGPipeline(rag = rag, llm = llm)

query = ""
response = pipeline.run(query)
print(response)