import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.llms.gemini import Gemini
from llama_index.core.settings import Settings
from llama_index.embeddings.gemini import GeminiEmbedding


# load environments variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class Summarizer():
    def __init__(self):
        Settings.llm = Gemini(model="models/gemini-2.5-pro",api_key = GEMINI_API_KEY)
        Settings.embed_model = GeminiEmbedding(model_name="models/embedding-001")  

    def summarize_text(self,text):
        documents = [Document(text=text)]
        index = VectorStoreIndex.from_documents(documents)

        query_engine = index.as_query_engine()

        response = query_engine.query("summarize this text into key points suitable for powerpoint slides")

        return response.response
    
if __name__ == "__main__":
    # test summarizer
    sample_text = """
                    The AI Revolution refers to the rapid growth and integration of artificial intelligence technologies across industries and daily life. It has been fueled by advances in machine learning, deep learning, and neural networks, combined with the availability of massive amounts of data and powerful cloud computing resources. Natural language processing and computer vision breakthroughs have further accelerated the pace, enabling AI systems to understand, generate, and interact with humans in more natural ways.

                The impact of AI is visible across multiple domains. In healthcare, AI assists in diagnostics, drug discovery, and personalized treatments. In finance, it powers fraud detection, algorithmic trading, and customer support chatbots. Education benefits from adaptive learning platforms and AI tutors, while manufacturing and retail make use of robotics, supply chain optimization, and predictive analytics to enhance efficiency and customer experience.

                AI is also transforming the workforce by automating routine tasks while creating new job roles that require advanced digital and analytical skills. This shift highlights the growing need for reskilling and upskilling to prepare people for the AI-driven economy. While the technology presents immense opportunities for efficiency, innovation, and improved decision-making, it also raises challenges such as algorithmic bias, data privacy concerns, ethical dilemmas, and the need for proper governance and regulation.

                Looking ahead, AI is expected to play a central role in shaping the Fourth Industrial Revolution, with progress toward more general-purpose AI (AGI). It holds the potential to redefine economies, societies, and human creativity, making it one of the most transformative forces of our era
                """
    
    summarizer = Summarizer()
    summary = summarizer.summarize_text(sample_text)

    print("\n **summarized text: **\n")
    print(summary)