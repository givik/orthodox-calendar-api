"""
Orthodox Liturgical Calendar Application Entrypoint.
Usage:
    python3 -m app.main              # Run standard server on port 8000
    python3 -m app.main 8080         # Run standard server on custom port
    python3 -m app.main cli [args]   # Run CLI
"""

import sys

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        from app.cli import main as cli_main
        sys.argv.pop(1)
        cli_main()
    else:
        from app.server import run_server
        port = 8000
        if len(sys.argv) > 1:
            try:
                port = int(sys.argv[1])
            except ValueError:
                pass
        run_server(port=port)

if __name__ == "__main__":
    main()
