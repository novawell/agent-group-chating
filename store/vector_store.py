import logging
import os
from typing import List


import os
import sys

# DuckDB로 강제 설정
os.environ["CHROMA_DB_IMPL"] = "duckdb"
os.environ["PYTHONNOUSERSITE"] = "1"

from langchain_openai import OpenAIEmbeddings
from langchain_chroma.vectorstores import Chroma

from setkeys import init_keys

from time import sleep

EMBED_DELAY = 0.02  # 20 milliseconds

class EmbeddingProxy:
    def __init__(self, embedding):
        self.embedding = embedding

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        sleep(EMBED_DELAY)
        return self.embedding.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        sleep(EMBED_DELAY)
        return self.embedding.embed_query(text)


class VectorStore:
    def __init__(self, path="vectordb_instance/", collection_name="chroma", embeddings=None):
        # TODO: Add More Embedding Options
        openai_api_key = init_keys()
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-3-small")

        self._proxy_embeddings = EmbeddingProxy(embeddings)
        self._vector_db = Chroma(collection_name=collection_name, embedding_function=self._proxy_embeddings, persist_directory=os.path.join(path, collection_name))

    def as_retriever(self):
        return self._vector_db.as_retriever()

    def reset_db(self):
        self._vector_db.reset_collection()

    def add_documents(self, documents):
        if not documents:
            return
        self._vector_db.add_documents(documents)

    def is_document_exists(self, document):
        results = self._vector_db.similarity_search(document, k=1)
        return len(results) > 0 and results[0].page_content == document

    def find_similar(vs, query):
        docs = vs.similarity_search(query)
        return docs
