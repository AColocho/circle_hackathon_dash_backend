from ..models import Client
from sqlalchemy import select, text, insert, update
from sqlalchemy.orm import Session
from ..connection import ConnectionDB

class QueryDB(ConnectionDB):
    def __init__(self) -> None:
        super().__init__()
        self.session = Session(self.engine)
    
    def search_client(self, query_object):
        for k,v in query_object.dict().items():
            if v:
                sql_query = text(f"SELECT * FROM client_list WHERE {k} ='{v}';")
                orm_sql = select(Client).from_statement(sql_query)
                result = self.session.execute(orm_sql).scalars().all()
                return [item.__dict__ for item in result]
    
    def create_client(self, query_object):
        request = query_object.dict()
        orm_sql = insert(Client).values(name = request['name'], phone = request['phone'],
                                        address_1 = request['address_1'], address_2 = request['address_2'],
                                        city = request['city'], state = request['state'], 
                                        email = request['client_email'], zipcode = request['zipcode'])
        self.session.execute(orm_sql)
        self.session.commit()
    
    def update_client(self, query_object):
        request = query_object.dict()
        orm_sql = update(Client).where(Client.client_id == request['client_id']).values(name = request['name'], phone = request['phone'],
                                                            address_1 = request['address_1'], address_2 = request['address_2'],
                                                            city = request['city'], state = request['state'], 
                                                            email = request['client_email'], zipcode = request['zipcode'])
        self.session.execute(orm_sql)
        self.session.commit()