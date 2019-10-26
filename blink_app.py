import yaml

APP_NAME = 'blink // =_='
COMPANY_NAME = 'C.R.E.D.'

secrets = yaml.load(open("secrets.yaml", "r"), Loader = yaml.FullLoader)
config = yaml.load(open("config.yaml", "r"), Loader = yaml.FullLoader)