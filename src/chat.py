import sys
from search import search_prompt


def main():
    try:
        ask = sys.argv[1] if len(sys.argv) > 1 else "Qual a empresa com o menor faturamento?"
        chain = search_prompt(ask)

        print("Resposta do Chat:")
        print(chain)
    except IndexError:
        print("Erro: Argumento inválido.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
