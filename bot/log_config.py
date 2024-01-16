from loguru import logger

logger.add('info.log', format='{time} {level} {message}', level='INFO', rotation='10 KB', compression='zip')

logger.info('INFO (debug)')
logger.debug('BUG (debug)')
logger.error('ERROR (debug)')
