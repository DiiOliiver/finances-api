#!/usr/bin/env python3
import re
import subprocess
import sys

pattern = r'^(feature|refactor|bugfix|hotfix|test)/[a-z0-9]+(-[a-z0-9]+)*$'


def main():
    result = subprocess.run(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        capture_output=True,
        text=True,
        check=False,
    )
    branch = result.stdout.strip()

    if not re.match(pattern, branch):
        print(f"[ERRO] Nome da branch '{branch}' inválido.")
        print("Padrão esperado: tipo/nome-da-atividade")
        print("(ex: feature/criar-endpoint-login)")
        sys.exit(1)


if __name__ == '__main__':
    main()
