#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

    from django.core.management import execute_from_command_line

    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        host = os.getenv("HOST", "127.0.0.1")
        port = os.getenv("PORT", "8000")
        sys.argv[2:] = [f"{host}:{port}"]

    execute_from_command_line(sys.argv)
