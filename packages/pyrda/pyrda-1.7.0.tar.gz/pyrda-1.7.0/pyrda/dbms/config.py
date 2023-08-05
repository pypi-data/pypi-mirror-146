from rdconfig.config import Config
from rdoss.rds import File
file = File(regionName='ap-shanghai',bucketName='rdconfig-1251945645',key='pyrda/db.json')
file_name = file.url()
cfg = Config(file_name=file_name)
cfg_setting = cfg.read_jsonUrl(node_name='mssql')
# print(cfg_setting)

