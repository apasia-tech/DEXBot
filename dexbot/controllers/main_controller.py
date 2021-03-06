from dexbot.bot import BotInfrastructure

from ruamel.yaml import YAML
from bitshares.instance import set_shared_bitshares_instance


class MainController:

    bots = dict()

    def __init__(self, bitshares_instance):
        self.bitshares_instance = bitshares_instance
        set_shared_bitshares_instance(bitshares_instance)
        self.bot_template = BotInfrastructure

    def create_bot(self, botname, config, view):
        bot = self.bot_template(config, self.bitshares_instance, view)
        bot.start()
        self.bots[botname] = bot

    def stop_bot(self, bot_name):
        self.bots[bot_name].terminate()
        self.bots.pop(bot_name, None)

    def remove_bot(self, bot_name):
        if bot_name in self.bots:
            self.bots[bot_name].terminate()

        # Todo: Add some threading here so that the GUI doesn't freeze
        config = self.get_bot_config(bot_name)
        self.bot_template.remove_bot(config, bot_name)
        self.remove_bot_config(bot_name)

    @staticmethod
    def load_config():
        yaml = YAML()
        with open('config.yml', 'r') as f:
            return yaml.load(f)

    @staticmethod
    def get_bots_data():
        """
        Returns dict of all the bots data
        """
        with open('config.yml', 'r') as f:
            yaml = YAML()
            return yaml.load(f)['bots']

    @staticmethod
    def get_latest_bot_config():
        """
        Returns config file data with only the latest bot data
        """
        with open('config.yml', 'r') as f:
            yaml = YAML()
            config = yaml.load(f)
            latest_bot = list(config['bots'].keys())[-1]
            config['bots'] = {latest_bot: config['bots'][latest_bot]}
            return config

    @staticmethod
    def get_bot_config(botname):
        """
        Returns config file data with only the data from a specific bot
        """
        with open('config.yml', 'r') as f:
            yaml = YAML()
            config = yaml.load(f)
            config['bots'] = {botname: config['bots'][botname]}
            return config

    @staticmethod
    def remove_bot_config(bot_name):
        yaml = YAML()
        with open('config.yml', 'r') as f:
            config = yaml.load(f)

        config['bots'].pop(bot_name, None)

        with open("config.yml", "w") as f:
            yaml.dump(config, f)
