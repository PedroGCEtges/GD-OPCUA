import logging
import datetime
import copy
# Definir a formatação do log
log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'

# Definir as configurações do log
logging.basicConfig(filename='opcua-tags.log', filemode='a', level=logging.DEBUG, format=log_format)

# Criar uma instância do logger
logger = logging.getLogger('opcua')
logger.setLevel(logging.CRITICAL)

previous_values = {}
def set_log(tags):
    tags_bckup = copy.deepcopy(tags)

    for tag in tags_bckup:
        tag_name = tag["name"]
        current_value = tag["value"]

        if tag_name in previous_values:
            if current_value != previous_values[tag_name]:
                now = datetime.datetime.now()
                logger.critical(f"O valor da tag {tag_name} mudou de {previous_values[tag_name]} para {current_value} em {now}")
                previous_values[tag_name] = current_value
        else:
            previous_values[tag_name] = current_value