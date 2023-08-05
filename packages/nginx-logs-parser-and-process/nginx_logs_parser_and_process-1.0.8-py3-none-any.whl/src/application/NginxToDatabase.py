from typing import List
from tabulate import tabulate

from src.domain.DataProcessor.EliminateUnnecessaryData import EliminateUnnecessaryData
from src.domain.DataProcessor.NormalizeModelData import NormalizeModelData
from src.domain.DataProcessor.PersistIntoDatabase import PersistIntoDatabase
from src.domain.Logs.ReadAllLogsFileIntoMemoryUsingPandas import ReadAllLogsFileIntoMemoryUsingPandas
from src.domain.Server.Server import Server


class NginxToDatabase:
    def __init__(self, data_processor, database):
        self.data_processor = data_processor
        self.database = database

    def process(self, origin_servers: List[Server], destination_server: Server):
        try:
            for remote_server in origin_servers:
                # SynchronizeRemoteNginxLogsWithLocalRepository().process(remote_server, destination_server)
                raw_data = ReadAllLogsFileIntoMemoryUsingPandas(self.data_processor).process(destination_server)
                print(tabulate(raw_data.tail(5), showindex=False, headers="keys"))
                normalized_data = NormalizeModelData(self.data_processor).process(raw_data, remote_server.name)
                print(tabulate(normalized_data.tail(5), showindex=False, headers="keys"))
                clean_data = EliminateUnnecessaryData(self.data_processor).process(normalized_data)
                print(tabulate(clean_data.tail(5), showindex=False, headers="keys"))
                print("Step 4")
                # PersistIntoDatabase(self.database).process(clean_data)
                print("Step 5")
                # InformProcessExecutionStatus(SucessMessage())
                # print(clean_data.info())
                # print(tabulate(clean_data.tail(100), showindex=False, headers="keys"))
                # print(tabulate(raw_data.tail(100)[["UserLogin", "request"]], showindex=False, headers="keys"))
        except Exception as error:
            print(error)
            #     InformProcessExecutionStatus(FailedMessage())
