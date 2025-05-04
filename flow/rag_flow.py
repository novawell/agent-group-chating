import os
from store import VectorStore
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.docstore.document import Document
from agents.recommend_agent import Agent


class RagFlow:
    def __init__(self, item_path="agents/data/cadedate_items"):
        docs = self.get_docs(item_path)

        self._vector_db = VectorStore()
        # TODO
        self._vector_db.reset_db()
        self._vector_db.add_documents(docs)

        self.vs_retriever = self._vector_db.as_retriever()
        self.bm25_retriever = BM25Retriever.from_texts([t.page_content for t in docs])
        self.retriever = EnsembleRetriever(retrievers=[self.bm25_retriever, self.vs_retriever], weights=[0.5, 0.5])
        self.agent = Agent()

    def get_docs(self, item_path):
        items = os.listdir(item_path)
        item_list = []
        for item in items:
            with open(os.path.join(item_path, item), "r", encoding="utf-8") as file:
                description = file.read()
                subject = item.split(".")[0]
                doc = Document(page_content=description, metadata={"subject": subject})
            item_list.append(doc)
        return item_list

    def run(self, chats):
        docs = self.retriever.get_relevant_documents(chats)
        formatted_docs = "\n\n".join(doc.page_content for doc in docs)

        inp = chats + "\n\n" + formatted_docs
        respond = self.agent.respond(inp)
        return respond
