import os
from sqlalchemy.sql import text as sa_text
from sqlalchemy import create_engine

# import psycopg2
from src.infrastructure.Database import Database


class CanadaThreeDatabase(Database):
    def __init__(self):
        self.engine = None
        super().__init__()

    def connect(self):
        if not self.engine:
            print("Connecting")
            self.engine = create_engine(os.environ.get('DESTINATION_DATABASE_URI'))
        return self.engine

    def get_table_name(self) -> str:
        return "temporal_logs"

    def get_destination_table_name(self) -> str:
        return "logs"

    def truncate_table(self):
        if self.engine:
            print("Truncating table")
            self.engine.execute(sa_text(f"""TRUNCATE TABLE {self.get_table_name()}""").execution_options(autocommit=True))

    def pass_temporal_to_final_logs_table(self):
        if self.engine:
            print("Passing from temporal to logs table")
            self.engine.execute(
                sa_text(
                    f"""
                DELETE FROM {self.get_table_name()} WHERE uniqueid in (SELECT uniqueid from {self.get_destination_table_name()});
                
                INSERT INTO {self.get_destination_table_name()} (ip, str_datetime, request, status, "size", referer, 
                    user_agent, log_datetime, log_date, log_time, logged, data_from_server, uniqueid)
                SELECT ip, str_datetime, request, status, "size", referer, 
                    user_agent, log_datetime, log_date, log_time, logged, data_from_server, uniqueid
                FROM {self.get_table_name()};
                """
                ).execution_options(autocommit=True)
            )
