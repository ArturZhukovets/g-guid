import asyncio


from db import get_db
from services.products.management import translate_all_product_titles
from utils.management.create_superuser import manage_create_superuser
from argparse import ArgumentParser

_COMMANDS = [
    "createsuperuser",
    "translate_products",
]

_FUNCTION_MAP = {
    "createsuperuser": manage_create_superuser,
    "translate_products": (translate_all_product_titles, next(get_db()))
}

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="G-guid management",
        usage="python3 manage.py <command_name> [OPTIONS]",
    )
    parser.add_argument(
        "command",
        choices=_COMMANDS,
        help=f"input on of the following commands: {', '.join(_COMMANDS)}",
    )
    args = parser.parse_args()
    command = _FUNCTION_MAP[args.command]
    if isinstance(command, tuple):
        command, *command_args = command
        asyncio.run(command(*command_args))
    elif callable(command):
        asyncio.run(command())
