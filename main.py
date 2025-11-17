from flask import Flask, render_template, request
from lists_db import create_tables, salvar_lista, listar_listas, limpar_listas, atualizar_nome, deletar_registro
from time import perf_counter

app = Flask(__name__)

create_tables()
#limpar_listas()


def bubble_sort(arr):
    steps = []
    arr = arr[:]
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        for j in range(n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                if n <= 20:
                    steps.append((arr[:], (arr[j + 1], arr[j])))
    return arr, steps, comparisons, swaps


def selection_sort(arr):
    steps = []
    arr = arr[:]
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
            if n <= 20:
                steps.append((arr[:], (arr[min_idx], arr[i])))
    return arr, steps, comparisons, swaps


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        jogador = request.form.get("player")
        numbers = request.form.get("numbers")
        method = request.form.get("sorting")

        if not jogador or not numbers:
            return render_template("index.html", error="Preencha o nome e a lista de números.")

        # 🚨 AQUI está a verificação pedida:
        if not method:
            return render_template("index.html", error="Selecione um algoritmo de ordenação antes de continuar.")

        try:
            arr = [int(x) for x in numbers.split(",") if x.strip() != ""]
        except ValueError:
            return render_template("index.html", error="Use apenas números inteiros separados por vírgula.")

        if len(arr) > 20:
            return render_template("index.html", error="Limite máximo de 20 números por ordenação.")

        salvar_lista(jogador, arr)

        sorted_arr = arr[:]
        steps, comparisons, swaps = [], 0, 0
        complexity = "O(n²)"
        display_method = ""

        start_main = perf_counter()
        if method == "bubbleSort":
            sorted_arr, steps, comparisons, swaps = bubble_sort(arr)
            display_method = "Bubble Sort"
        elif method == "selectionSort":
            sorted_arr, steps, comparisons, swaps = selection_sort(arr)
            display_method = "Selection Sort"
        else:
            sorted_arr = sorted(arr)
            display_method = "Sort Padrão (Python)"
            complexity = "O(n log n)"
        elapsed_main = perf_counter() - start_main

        if len(arr) > 20:
            steps = []

        start_bubble = perf_counter()
        _, _, bubble_comp, bubble_swap = bubble_sort(arr)
        bubble_time = perf_counter() - start_bubble

        start_selection = perf_counter()
        _, _, selection_comp, selection_swap = selection_sort(arr)
        selection_time = perf_counter() - start_selection

        comparison_data = {
            "bubble": {"time": f"{bubble_time:.8f}", "comp": bubble_comp, "swap": bubble_swap},
            "selection": {"time": f"{selection_time:.8f}", "comp": selection_comp, "swap": selection_swap},
        }

        best_case_arr = sorted(arr)
        worst_case_arr = sorted(arr, reverse=True)

        best_case_results = {}
        worst_case_results = {}

        if method == "bubbleSort":
            start = perf_counter()
            _, _, c, s = bubble_sort(best_case_arr)
            best_case_results = {'time': f"{perf_counter() - start:.8f}", 'comp': c, 'swap': s}

            start = perf_counter()
            _, _, c, s = bubble_sort(worst_case_arr)
            worst_case_results = {'time': f"{perf_counter() - start:.8f}", 'comp': c, 'swap': s}

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

    return render_template("index.html")


@app.route("/history")
def history():
    registros = listar_listas(200)
    return render_template("history.html", registros=registros)

@app.route("/edit/<int:id>", methods=["POST"])
def editar(id):
    novo_nome = request.form.get("novo_nome")
    if not novo_nome:
        return "Nome inválido", 400

    atualizar_nome(id, novo_nome)
    return ("", 204)  # retorna vazio, ideal para AJAX


@app.route("/delete/<int:id>", methods=["POST"])
def deletar(id):
    deletar_registro(id)
    return ("", 204)

if __name__ == "__main__":
    app.run(debug=True)