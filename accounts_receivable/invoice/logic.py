from ..models import Invoice, Client
from sqlalchemy import select, insert, update, text
from sqlalchemy.orm import Session
from ..connection import ConnectionDB
from datetime import datetime
import json

class QueryDB(ConnectionDB):
    def __init__(self) -> None:
        super().__init__()
        self.session = Session(self.engine)

    def _process_invoice_(self, object):
        dict_object = object.__dict__
        # client_info = dict_object.get('client_info').__dict__
        dict_object['line_items'] = json.loads(dict_object['line_items'])
        
        # del dict_object['client_info']
        
        # dict_object.update(client_info)
        
        return dict_object
    
    def get_all(self):
        result = self.session.query(Invoice).join(Client).all()
        return [self._process_invoice_(item) for item in result]
    
    def search_invoice(self, query_object):
        for k,v in query_object.dict().items():
            if v:
                raw_sql = text(f'SELECT * FROM invoice WHERE {k} = {v};')
                sub_query_result = self.session.query(Invoice).from_statement(raw_sql)
                invoice_ids = [item.__dict__.get('invoice_id') for item in sub_query_result]
                result = self.session.query(Invoice).join(Client).filter(Invoice.invoice_id.in_(invoice_ids)).all()
                return [self._process_invoice_(item) for item in result]
        
    def create_invoice(self, query_object):
        request = query_object.dict()
        orm_sql = insert(Invoice).values(client_id = request['client_id'], invoice_date = datetime.today().strftime('%Y-%m-%d'),
                                         pay_date = request['pay_date'], line_items = json.dumps(request['line_items']), 
                                         total = request['total'], status = request['status'])
        self.session.execute(orm_sql)
        self.session.commit()
    
    def update_invoice(self, query_object):
        request = query_object.dict()
        orm_sql = update(Invoice).where(Invoice.invoice_id == request['invoice_id']).values(client_id = request['client_id'],
                                    pay_date = request['pay_date'], line_items = json.dumps(request['line_items']), 
                                    total = request['total'], status = request['status'])
        
        self.session.execute(orm_sql)
        self.session.commit()