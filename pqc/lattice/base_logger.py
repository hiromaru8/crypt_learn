import logging
import sys

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(message)s",
#     handlers=[
#         logging.StreamHandler(sys.stdout),
#         logging.FileHandler("log.tmp", encoding="utf-8"),
#     ],
# )


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 標準出力
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # ファイル
    file_handler = logging.FileHandler(
        "log.tmp",
        encoding="utf-8",
        mode="w",
    )
    file_handler.setLevel(logging.DEBUG)

    # 出力フォーマット
    formatter = logging.Formatter(
        "%(message)s"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Handlerを登録
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)