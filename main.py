from flask import Flask, render_template, request

app = Flask(__name__)

def bubble_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]       
                steps.append((arr[:], (arr[j], arr[j+1])))
    return arr, steps

def selection_sort(arr):
    size = len(arr)
    steps = []
    for ind in range(size):
        min_index = ind

        for j in range(ind + 1, size):
            if arr[j] < arr[min_index]:
                min_index = j

        if min_index != ind:
            arr[ind], arr[min_index] = arr[min_index], arr[ind]
            steps.append((arr[:], (arr[ind], arr[min_index])))

    return arr, steps

@app.route("/", methods=["GET", "POST"])
def index():
    originalArr = []
    sortedArr = []
    steps = []

    if request.method == "POST":
        numbers = request.form.get("numbers")
        sorting = request.form.get("sorting")
        if numbers:
            originalArr = [int(x) for x in numbers.split(",") if x.strip().isdigit()]
            if sorting == "bubbleSort":
                sortedArr, steps = bubble_sort(originalArr[:])
                method = "Bubble Sort"
            elif sorting == "selectionSort":
                sortedArr, steps = selection_sort(originalArr[:])
                method = "Selection Sort"

        return render_template("sorted.html",
                            originalArr=originalArr,
                            sortedArr=sortedArr,
                            steps=steps, method=method)
    
    else:
        return render_template("index.html")
@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)