from database import CollectInmetData
from download_inmet_data import DownloadInmetData
from collect_inmet_data import CollectInmetData
from database import MongoDB

mongo = MongoDB('mongodb://localhost:27017/')
downloader = DownloadInmetData()
collect = CollectInmetData("data/years")

for year in range(2024, 2025):
    downloader.download_data_by_year(year)
    mongo.create_collections(year)
    json = collect.extract_inmet_data(2024, "NE", "PB")
    mongo.insert_data_inmet(str(year), json)
