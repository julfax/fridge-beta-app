from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///inventario.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread":False
    }
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()



class Inventario(Base):

    __tablename__="inventario"


    id=Column(
        Integer,
        primary_key=True,
        index=True
    )


    nombre=Column(
        String,
        unique=True
    )


    cantidad=Column(
        Integer,
        default=0
    )


Base.metadata.create_all(
    bind=engine
)