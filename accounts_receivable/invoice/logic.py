from ..models import Invoice
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from ..connection import ConnectionDB

class QueryDB(ConnectionDB):
    def __init__(self) -> None:
        super().__init__()
        self.session = Session(self.engine)
        
    def search_invoice(self, query_object):
        for k,v in query_object.dict().items():
            if v:
                sql_query = text(f"SELECT * FROM invoice WHERE {k} ='{v}';")
                orm_sql = select(Invoice).from_statement(sql_query)
                result = self.session.execute(orm_sql).scalars().all()
                return [item.__dict__ for item in result]
            
            