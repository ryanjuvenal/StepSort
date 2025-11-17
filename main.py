from flask import Flask, render_template, request
from lists_db import create_tables, salvar_lista, listar_listas, limpar_listas, atualizar_nome, deletar_registro
from time import perf_counter

# Cria a aplicação Flask
app = Flask(__name__)

# Garante que as tabelas do banco existem ao iniciar o app
create_tables()
#limpar_listas()  # Função opcional para limpar o histórico (comentada para evitar apagar tudo)


# -----------------------------------------------
# Função BUBBLE SORT com contagem e passos
# -----------------------------------------------
def bubble_sort(arr):
    steps = []          # Armazena os passos (usado apenas quando a lista tem até 20 itens)
    arr = arr[:]         # Copia a lista para evitar modificar a original
    n = len(arr)
    comparisons = 0      # Contador de comparações
    swaps = 0            # Contador de trocas

    # Loop externo controla quantas passadas serão feitas
    for i in range(n - 1):
        # Loop interno faz comparações entre pares adjacentes
        for j in range(n - i - 1):
            comparisons += 1

            # Se o elemento atual for maior que o próximo, troca
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

                # Armazena o passo somente se a lista for pequena
                if n <= 20:
                    steps.append((arr[:], (arr[j + 1], arr[j])))

    return arr, steps, comparisons, swaps


# -----------------------------------------------
# Função SELECTION SORT com contagem e passos
# -----------------------------------------------
def selection_sort(arr):
    steps = []
    arr = arr[:]
    n = len(arr)
    comparisons = 0
    swaps = 0

    # Cada posição "i" buscará o menor elemento à frente
    for i in range(n - 1):
        min_idx = i

        # Encontra o menor item no restante da lista
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j

        # Se achou um menor, troca
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1

            # Registra o passo se a lista for pequena
            if n <= 20:
                steps.append((arr[:], (arr[min_idx], arr[i])))

    return arr, steps, comparisons, swaps


# -----------------------------------------------
# ROTA PRINCIPAL: página inicial
# -----------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    # Se o método for POST, o usuário enviou dados para ordenação
    if request.method == "POST":
        jogador = request.form.get("player")
        numbers = request.form.get("numbers")
        method = request.form.get("sorting")

        # Validação do nome e lista
        if not jogador or not numbers:
            return render_template("index.html", error="Preencha o nome e a lista de números.")

        # Verifica se o jogador escolheu um algoritmo
        if not method:
            return render_template("index.html", error="Selecione um algoritmo de ordenação antes de continuar.")

        # Tenta converter a lista de números
        try:
            arr = [int(x) for x in numbers.split(",") if x.strip() != ""]
        except ValueError:
            return render_template("index.html", error="Use apenas números inteiros separados por vírgula.")

        # Limite máximo definido
        if len(arr) > 20:
            return render_template("index.html", error="Limite máximo de 20 números por ordenação.")

        # Salva a lista no banco
        salvar_lista(jogador, arr)

        # Variáveis padrão
        sorted_arr = arr[:]
        steps, comparisons, swaps = [], 0, 0
        complexity = "O(n²)"
        display_method = ""

        # Cronometragem da ordenação escolhida
        start_main = perf_counter()

        # Execução do algoritmo escolhido
        if method == "bubbleSort":
            sorted_arr, steps, comparisons, swaps = bubble_sort(arr)
            display_method = "Bubble Sort"

        elif method == "selectionSort":
            sorted_arr, steps, comparisons, swaps = selection_sort(arr)
            display_method = "Selection Sort"

        else:
            sorted_arr = sorted(arr)  # fallback para ordenação nativa do Python
            display_method = "Sort Padrão (Python)"
            complexity = "O(n log n)"

        elapsed_main = perf_counter() - start_main

        # Remove steps se a lista for grande
        if len(arr) > 20:
            steps = []

        # -----------------------------------------
        # Comparação automática entre algoritmos
        # -----------------------------------------
        # Tempo Bubble Sort com mesma entrada
        start_bubble = perf_counter()
        _, _, bubble_comp, bubble_swap = bubble_sort(arr)
        bubble_time = perf_counter() - start_bubble

        # Tempo Selection Sort com mesma entrada
        start_selection = perf_counter()
        _, _, selection_comp, selection_swap = selection_sort(arr)
        selection_time = perf_counter() - start_selection

        comparison_data = {
            "bubble": {"time": f"{bubble_time:.8f}", "comp": bubble_comp, "swap": bubble_swap},
            "selection": {"time": f"{selection_time:.8f}", "comp": selection_comp, "swap": selection_swap},
        }

        # -----------------------------------------
        # Cenários de Melhor Caso e Pior Caso
        # -----------------------------------------
        best_case_arr = sorted(arr)
        worst_case_arr = sorted(arr, reverse=True)

        best_case_results = {}
        worst_case_results = {}

        # Melhor e pior caso do Bubble Sort
        if method == "bubbleSort":
            start = perf_counter()
            _, _, c, s = bubble_sort(best_case_arr)
            best_case_results = {'time': f"{perf_counter() - start:.8f}", 'comp': c, 'swap': s}

            start = perf_counter()
            _, _, c, s = bubble_sort(worst_case_arr)
            worst_case_results = {'time': f"{perf_counter() - start:.8f}", 'comp': c, 'swap': s}

        # Melhor e pior caso do Selection Sort
        elif method == "selectionSort":
            start = perf_counter()
            _, _, c, s = selection_sort(best_case_arr)
            best_case_results = {'time': f"{perf_counter() - start:.8f}", 'comp': c, 'swap': s}

            start = perf_counter()
            _, _, c, s = selection_sort(worst_case_arr)
            worst_case_results = {'time': f"{perf_counter() - start:.8f}", 'comp': c, 'swap': s}

        scenario_data = {
            "best_arr": best_case_arr,
            "worst_arr": worst_case_arr,
            "best_results": best_case_results,
            "worst_results": worst_case_results
        }

        # Renderiza a página de resultados
        return render_template(
            "sorted.html",
            player=jogador,
            method=display_method,
            originalArr=arr,
            sortedArr=sorted_arr,
            steps=steps,
            complexity=complexity,
            comparisons=comparisons,
            swaps=swaps,
            elapsed_time=f"{elapsed_main:.8f}",
            comparison_data=comparison_data,
            scenario_data=scenario_data,
            show_steps=(len(arr) <= 20)
        )

    # Se for GET, apenas mostra a página inicial
    return render_template("index.html")


# -----------------------------------------------
# Histórico de listas salvas no banco de dados
# -----------------------------------------------
@app.route("/history")
def history():
    registros = listar_listas(200)  # busca até 200 registros
    return render_template("history.html", registros=registros)


# -----------------------------------------------
# Editar nome de um registro (AJAX)
# -----------------------------------------------
@app.route("/edit/<int:id>", methods=["POST"])
def editar(id):
    novo_nome = request.form.get("novo_nome")

    if not novo_nome:
        return "Nome inválido", 400

    atualizar_nome(id, novo_nome)
    return ("", 204)  # Sucesso sem conteúdo


# -----------------------------------------------
# Deletar registro por ID
# -----------------------------------------------
@app.route("/delete/<int:id>", methods=["POST"])
def deletar(id):
    deletar_registro(id)
    return ("", 204)


# -----------------------------------------------
# Inicia o servidor Flask em modo debug
# -----------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
