import os
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core import PromptTemplate

from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent

PERSIST_DIR_ALBUMS = "./storage/albums"
PERSIST_DIR_SONGS = "./storage/songs"
PERSIST_DIR_BIOGRAPHIES = "./storage/biographies"

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

class RAGService:

    def __init__(self) -> None:
        Settings.llm = OpenAI(model='gpt-4o-mini', api_key=openai_api_key)
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002", api_key=openai_api_key)

        self.albums_parser = SentenceSplitter(chunk_size=256, chunk_overlap=30)
        self.songs_parser = SentenceSplitter(chunk_size=256, chunk_overlap=30)
        self.bio_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        
        self.albums_index = self.load_or_create_index(PERSIST_DIR_ALBUMS, "./albums.txt", self.albums_parser)
        self.songs_index = self.load_or_create_index(PERSIST_DIR_SONGS, "./songs.txt", self.songs_parser)
        self.biographies_index = self.load_or_create_index(PERSIST_DIR_BIOGRAPHIES, "./biographies.txt", self.bio_parser)

        self.engine = self.initialize_engine()
        self.prompt = self.initialize_prompt()
        self.agent = OpenAIAgent.from_tools(self.engine, verbose=True, system_prompt=self.prompt)
        

 

    # Função para verificar e carregar índice se existir, ou criar novo se não existir
    def load_or_create_index(self, persist_dir, data_path, parser):
        """Inicializa oou cria índice vetorial."""
        if not os.path.exists(persist_dir):
            documents = SimpleDirectoryReader(input_files=[data_path]).load_data()
            nodes = parser.get_nodes_from_documents(documents, show_progress=True)
            index = VectorStoreIndex(nodes, show_progress=True)
            index.storage_context.persist(persist_dir=persist_dir)
            return index
        else:
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
            return load_index_from_storage(storage_context)

    def initialize_prompt(self):
        text_qa_template_str = """As informações de contexto estão abaixo.
        \n---------------------\n{context_str}\n---------------------\n
        Instruções:
        - Usando apenas as informações fornecidas no contexto, responda a pergunta: {query_str}.
        - Sempre responda de maneira clara, gentil e solícita.
        - Se você não entender completamente a pergunta, peça ao usuário que reformule.
        - Se o contexto não for útil, diga que você não tem informações suficientes para responder.
        - Se a palavra "quais" for mencionada, liste todas as ocorrências de maneira organizada 
        (exemplo: "Quais são os álbuns de Taylor Swift?" deve listar todos os álbuns com nomes e datas).
        - Se a pergunta envolver listar músicas ou álbuns, forneça a lista completa.
        - Para artistas conhecidos por mais de um nome, use as informações fornecidas na biografia para reconhecer todos os nomes.
        - Apenas use as informações fornecidas no contexto, não utilize alguma informação que não esteja lá.
        Importante: Não mencione que está usando informações recuperadas do contexto, apenas forneça a resposta educadamente."""
        
        return text_qa_template_str

    def initialize_engine(self):
        """Inicializa o motor de consulta."""
       
        albums_engine = self.albums_index.as_query_engine(similarity_top_k=5)
        songs_engine = self.songs_index.as_query_engine(similarity_top_k=5)
        biographies_engine = self.biographies_index.as_query_engine(similarity_top_k=5)
        
        query_engine_tools = [
            QueryEngineTool(
                query_engine=albums_engine,
                metadata=ToolMetadata(
                    name="albums_info",
                    description="Fornece informações sobre os álbuns do artista."
                ),
            ),
            QueryEngineTool(
                query_engine=songs_engine,
                metadata=ToolMetadata(
                    name="songs_info",
                    description="Fornece informações sobre as músicas do artista."
                ),
            ),
            QueryEngineTool(
                query_engine=biographies_engine,
                metadata=ToolMetadata(
                    name="biographies_info",
                    description="Fornece informações pessoais e sobre a carreira do artista."
                ),
            )
        ]
        return query_engine_tools

    def generate_answer(self, query):
        """Gera uma resposta para a consulta."""
        try:
            response = self.agent.chat(query) 
            return response.response  
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta: {str(e)}")
