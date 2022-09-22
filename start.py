from logging import getLogger
from logging import StreamHandler
from logging import Formatter
from logging import INFO
from waitress import serve
from dotenv import load_dotenv
from app import create_app

logger = getLogger()


def init_logger():
    logger.setLevel(INFO)
    handler = StreamHandler()
    handler.setFormatter(fmt=Formatter("%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(hdlr=handler)


def get_app():
    try:
        from paste.translogger import TransLogger
        app = TransLogger(create_app())
    except ImportError:
        app = create_app()
        logger.info("TransLogger is disabled")

    return app


def main():
    host, port = "127.0.0.1", 18282
    serve(app=get_app(), host=host, port=port)


if __name__ == "__main__":
    load_dotenv()
    init_logger()
    main()
