from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI


class QASystem:
    def __init__(self, vector_store):
        self.llm = VertexAI(model_name="gemini-1.5-pro-001", temperature=0.2)
        self.retriever = vector_store.as_retriever()
        template = """Provide a concise and specific answer using the references below:

Question: {question}

References:
{context}

Answer:"""
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            chain_type_kwargs={
                "prompt": PromptTemplate(template=template, input_variables=["context", "question"])
            }
        )

    # Updated ask_question in QASystem
    def ask_question(self, question):
        try:
            result = self.qa.invoke({"query": question})
            if result is None:
                return "Sorry, I couldn't find any relevant information for your query."
            return result
        except IndexError:
            return "No relevant documents were found in the database."
        except Exception as e:
            return f"An error occurred: {str(e)}"
