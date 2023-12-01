import logging
import datetime
# Definir a formatação do log
log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'

# Definir as configurações do log
logging.basicConfig(filename='opcua-tags.log', filemode='a', level=logging.DEBUG, format=log_format)

# Criar uma instância do logger
logger = logging.getLogger('opcua')
logger.setLevel(logging.CRITICAL)

previous_values = {}
def set_log(tags):

    for tag in tags:
        current_value = tag[1]
        tag_name = tag[0]

        if tag_name in previous_values:
            if current_value != previous_values[tag_name]:
                now = datetime.datetime.now()
                logger.critical(f"O valor da tag {tag_name} mudou de {previous_values[tag_name]} para {current_value} em {now}")
                previous_values[tag_name] = current_value
        else:
            previous_values[tag_name] = current_value