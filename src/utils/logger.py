import logging


def init_logger(name: str, level: str) -> logging.Logger:
    """
    Logger를 생성하는 함수
    Args:
        name(str): 현재 파일의 이름
        level(str): 에러 레벨
    Return:
        logger(Logger)
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter('|%(asctime)s|==|%(levelname)s| %(funcName)s | %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    # 부모 로거로의 전파 방지
    logger.propagate = False

    return logger