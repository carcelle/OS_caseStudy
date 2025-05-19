from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def fifo(reference, frames):
    memory = []
    steps = []
    pointer = 0
    faults = 0

    for page in reference:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory[pointer] = page
                pointer = (pointer + 1) % frames
            faults += 1
            hit = False
        else:
            hit = True
        steps.append(memory.copy() + ['✔' if hit else '✘'])
    return {"faults": faults, "steps": steps}

def lru(reference, frames):
    memory = []
    recent = {}
    steps = []
    faults = 0

    for i, page in enumerate(reference):
        if page in memory:
            hit = True
        else:
            hit = False
            if len(memory) < frames:
                memory.append(page)
            else:
                lru_page = min(memory, key=lambda p: recent.get(p, -1))
                memory[memory.index(lru_page)] = page
            faults += 1
        recent[page] = i
        steps.append(memory.copy() + ['✔' if hit else '✘'])
    return {"faults": faults, "steps": steps}

def optimal(reference, frames):
    memory = []
    steps = []
    faults = 0

    for i in range(len(reference)):
        page = reference[i]
        if page in memory:
            hit = True
        else:
            hit = False
            if len(memory) < frames:
                memory.append(page)
            else:
                future = reference[i+1:]
                indexes = [future.index(p) if p in future else float('inf') for p in memory]
                replace_index = indexes.index(max(indexes))
                memory[replace_index] = page
            faults += 1
        steps.append(memory.copy() + ['✔' if hit else '✘'])
    return {"faults": faults, "steps": steps}

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    frame_count = data.get("frameCount", 3)

    ref_string = [random.randint(0, 9) for _ in range(20)]
    fifo_result = fifo(ref_string, frame_count)
    lru_result = lru(ref_string, frame_count)
    opt_result = optimal(ref_string, frame_count)

    return jsonify({
        "referenceString": ref_string,
        "fifo": fifo_result["faults"],
        "lru": lru_result["faults"],
        "opt": opt_result["faults"],
        "fifoSteps": fifo_result["steps"],
        "lruSteps": lru_result["steps"],
        "optSteps": opt_result["steps"]
    })

if __name__ == "__main__":
    app.run(debug=True)
