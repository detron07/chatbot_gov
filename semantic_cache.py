import os
import psycopg2
from pgvector.psycopg2 import register_vector
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

class SemanticCacheManager:
    def __init__(self):
        # Conexão com o banco PostgreSQL
        db_url = os.getenv("DATABASE_URL")
        
        if db_url:
            self.conn = psycopg2.connect(db_url)
        else:
            self.conn = psycopg2.connect(
                dbname=os.getenv("PG_DBNAME", "semantic_cache"),
                user=os.getenv("PG_USER", "admin"),
                password=os.getenv("PG_PASSWORD", "adminpassword"),
                host=os.getenv("PG_HOST", "localhost"),
                port=os.getenv("PG_PORT", "5432")
            )
        
        register_vector(self.conn)
        
        # Modelo de embeddings (usa GPU se disponível)
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': device}
        )
        
    def _obter_embedding(self, texto: str) -> list:
        # Gera o vetor usando o modelo do Google
        return self.embeddings.embed_query(texto)

    def verificar_ataque(self, texto: str, threshold: float = 0.15) -> tuple[bool, str]:
        """
        Verifica se a entrada é similar a algum ataque armazenado no cache.
        Retorna (True, None) se for seguro.
        Retorna (False, categoria) se for detectado um ataque.
        """
        vetor = self._obter_embedding(texto)
        
        with self.conn.cursor() as cur:
            # Faz a busca pelo vizinho mais próximo usando pgvector
            # O operador <=> representa a distância do cosseno
            cur.execute(
                """
                SELECT categoria, embedding <=> %s::vector AS distancia 
                FROM cache_ataques 
                ORDER BY distancia ASC 
                LIMIT 1
                """,
                (vetor,)
            )
            
            resultado = cur.fetchone()
            
            if resultado:
                categoria, distancia = resultado
                # Se a distância for menor que o threshold, significa que é muito similar a um ataque conhecido
                if distancia < threshold:
                    return False, categoria
                    
        return True, None

    def registrar_ataque(self, texto: str, categoria: str, origem: str = "llm_judge", motivo: str = None):
        """
        Registra um novo ataque no cache semântico.
        """
        vetor = self._obter_embedding(texto)
        
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cache_ataques (categoria, prompt_texto, embedding, origem, motivo) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (categoria, texto, vetor, origem, motivo)
            )
            self.conn.commit()

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
