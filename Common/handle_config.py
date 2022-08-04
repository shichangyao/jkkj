from configparser import ConfigParser
from Common.handle_path import conf_dir

class HandleConfig(ConfigParser):
    def __init__(self,filepath):
        super().__init__()
        self.read(filepath,encoding='utf-8')

conf = HandleConfig(conf_dir+'/conf.ini')

if __name__ == "__main__":
    conf = HandleConfig(conf_dir+'/conf.ini')
    conf.get("log","name")
