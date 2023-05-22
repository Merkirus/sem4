import logging, sys

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

console_handler_err = logging.StreamHandler(sys.stderr)
console_handler_cri = logging.StreamHandler(sys.stderr)
console_handler_debug = logging.StreamHandler(sys.stdout)
console_handler_info = logging.StreamHandler(sys.stdout)
console_handler_warning = logging.StreamHandler(sys.stdout)

console_handler_err.setLevel(logging.ERROR)
console_handler_cri.setLevel(logging.CRITICAL)
console_handler_debug.setLevel(logging.DEBUG)
console_handler_info.setLevel(logging.INFO)
console_handler_warning.setLevel(logging.WARNING)

formatter = logging.Formatter('%(levelname)s: %(message)s')

console_handler_err.setFormatter(formatter)
console_handler_cri.setFormatter(formatter)
console_handler_debug.setFormatter(formatter)
console_handler_info.setFormatter(formatter)
console_handler_warning.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console_handler_err)
logger.addHandler(console_handler_cri)
logger.addHandler(console_handler_info)
logger.addHandler(console_handler_warning)
logger.addHandler(console_handler_debug)
