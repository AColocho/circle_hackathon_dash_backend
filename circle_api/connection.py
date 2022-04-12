from sqlalchemy import create_engine

class ConnectionDB:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///accounts_receivable/prod.db")
