import importlib

def run_all_exercises():
    for i in range(1, 11):
        module_name = f"exercicios_resolucoes.exercicio_{i:02d}"
        print(f"\nExecutando {module_name}...")
        module = importlib.import_module(module_name)
        if hasattr(module, "main"):
            module.main()
        else:
            print(f"⚠️ O módulo {module_name} não possui uma função main()")

if __name__ == "__main__":
    run_all_exercises()
