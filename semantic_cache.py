import os
from sqlalchemy import create_engine, Column, Integer, String, Float, select
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class CacheAtaque(Base):
    __tablename__ = 'cache_ataques'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(String)
    prompt_texto = Column(String)
    embedding = Column(Vector(384))
    origem = Column(String)
    risco_nota = Column(Float, nullable=True) 
    motivo = Column(String, nullable=True)

class SemanticCacheManager:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL")
        
        if db_url:
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            self.engine = create_engine(db_url)
        else:
            dbname = os.getenv("PG_DBNAME", "semantic_cache")
            user = os.getenv("PG_USER", "admin")
            password = os.getenv("PG_PASSWORD", "adminpassword")
            host = os.getenv("PG_HOST", "localhost")
            port = os.getenv("PG_PORT", "5432")
            
            db_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
            self.engine = create_engine(db_url)
            
        self.Session = sessionmaker(bind=self.engine)
        
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
    def _obter_embedding(self, texto: str) -> list:
        return self.embeddings.embed_query(texto)

    def verificar_ataque(self, texto: str, threshold: float = 0.15) -> tuple[bool, str]:
        vetor = self._obter_embedding(texto)
        
        with self.Session() as session:
            distancia_expr = CacheAtaque.embedding.cosine_distance(vetor).label('distancia')
            
            stmt = select(CacheAtaque.categoria, distancia_expr)\
                .order_by(distancia_expr.asc()).limit(1)
                
            resultado = session.execute(stmt).first()
            
            if resultado:
                categoria = resultado.categoria
                distancia = resultado.distancia
                
                if distancia < threshold:
                    return False, categoria
                    
        return True, None

    def registrar_ataque(self, texto: str, categoria: str, risco_nota: float = 0.0, motivo: str = None, origem: str = "llm_judge"):
        vetor = self._obter_embedding(texto)
        
        with self.Session() as session:
            novo_ataque = CacheAtaque(
                categoria=categoria,
                prompt_texto=texto,
                embedding=vetor,
                origem=origem,
                risco_nota=risco_nota,
                motivo=motivo
            )
            session.add(novo_ataque)
            session.commit()

    def __del__(self):
        if hasattr(self, 'engine') and self.engine:
            self.engine.dispose()
