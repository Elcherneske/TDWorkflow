import os
import configparser

class Setting:
    def __init__(self):
        self.config_path = './setting.config'
        if os.path.exists(self.config_path):
            self.config = configparser.ConfigParser()
            self.config.read(self.config_path)
        else:
            self.new_config()
    
    def get_config(self, section, option):
        return self.config[section][option]
    
    def save_config(self):
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

    def set_config(self, section, option, value, is_save = True):
        if section not in self.config:
            self.config.add_section(section)
        self.config[section][option] = value
        if is_save:
            self.save_config()

    def new_config(self):
        self.config = configparser.ConfigParser()
        self.set_config('Tools', 'msconvert', '', is_save = False)
        self.set_config('Tools', 'toppic', '', is_save = False)
        self.set_config('Tools', 'topfd', '', is_save = False)
        self.set_config('Tools', 'informed_proteomics', '', is_save = False)
        self.set_config('Tools', 'spectator', '', is_save = False)
        self.set_config('Fasta', 'fasta_path', '', is_save = False)
        self.set_config('Output', 'output_dir', '', is_save = False)
        self.save_config()

