import logging


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        filename='app_log.log',
        filemode='a',
        format='[%(asctime)s] %(levelname)s - %(message)s'
    )

    return logging
