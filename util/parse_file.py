import re

class ParseFile:
    def parse_filename(filename:str) -> dict:
        pattern = r'^INMET_(\w{1,2})_(\w{2})_(\w{4})_([^_]+?)_(\d{2}-\d{2}-\d{4})_A_(\d{2}-\d{2}-\d{4})\.CSV$'
        
        match = re.fullmatch(pattern, filename)
        
        if match:
            return {
            'region': match.group(1),
            'state': match.group(2),
            'station_code': match.group(3),
            'station_name': match.group(4),
            'start_date': match.group(5),
            'end_date': match.group(6)
        }
        return None