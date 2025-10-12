# main.py
from flask import Flask, render_template, request
from lists_db import create_tables, salvar_lista, listar_listas
from datetime import datetime

app = Flask(__name__)

create_tables()

# ---------- Algoritmos ----------
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
                steps.append((arr[:], (arr[j], arr[j + 1])))
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
            steps.append((arr[:], (arr[i], arr[min_idx])))
    return arr, steps, comparisons, swaps

# ---------- Rotas ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        jogador = request.form.get("player")
        numbers = request.form.get("numbers")
        method = request.form.get("sorting")

        if not jogador or not numbers:
            return render_template("index.html", error="Preencha o nome e a lista de números.")

        try:
            arr = [int(x) for x in numbers.split(",") if x.strip() != ""]
        except ValueError:
            return render_template("index.html", error="Use apenas números inteiros separados por vírgula.")

        # Limite máximo de 20 números
        if len(arr) > 20:
            return render_template("index.html", error="Limite máximo de 20 números por ordenação.")

        salvar_lista(jogador, arr)

        sorted_arr = arr[:]
        steps, comparisons, swaps = [], 0, 0
        complexity = "O(n²)"  # ambos algoritmos

        if method == "bubbleSort":
            sorted_arr, steps, comparisons, swaps = bubble_sort(arr)
            display_method = "Bubble Sort"
        elif method == "selectionSort":
            sorted_arr, steps, comparisons, swaps = selection_sort(arr)
            display_method = "Selection Sort"
        else:
            sorted_arr = sorted(arr)
            display_method = "Sort Padrão (Python)"

        return render_template(
            "sorted.html",
            player=jogador,
            method=display_method,
            originalArr=arr,
            sortedArr=sorted_arr,
            steps=steps,
            complexity=complexity,
            comparisons=comparisons,
            swaps=swaps
        )

    return render_template("index.html")


@app.route("/history")
def history():
    registros = listar_listas(200)
    return render_template("history.html", registros=registros)


if __name__ == "__main__":
    app.run(debug=True)
