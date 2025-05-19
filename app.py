from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Route for the homepage, serves the index.html template
@app.route("/")
def index():
    return render_template("index.html")

# FIFO Page Replacement Algorithm implementation
def fifo(reference, frames):
    memory = []      # List to store current pages in memory frames
    steps = []       # To record memory state and hit/miss for each step
    pointer = 0      # Points to the frame to replace next (FIFO order)
    faults = 0       # Counts page faults

    for page in reference:
        if page not in memory:
            # Page fault occurred
            if len(memory) < frames:
                memory.append(page)  # Add page if memory not full
            else:
                memory[pointer] = page  # Replace oldest page
                pointer = (pointer + 1) % frames  # Move pointer circularly
            faults += 1
            hit = False
        else:
            # Page hit, no replacement needed
            hit = True
        # Save a copy of current memory state + hit/miss marker
        steps.append(memory.copy() + ['✔' if hit else '✘'])
    return {"faults": faults, "steps": steps}

# LRU Page Replacement Algorithm implementation
def lru(reference, frames):
    memory = []      # Pages currently in memory
    recent = {}      # Dictionary to track last used index for each page
    steps = []       # To record memory state and hit/miss per step
    faults = 0       # Page fault count

    for i, page in enumerate(reference):
        if page in memory:
            hit = True
        else:
            hit = False
            if len(memory) < frames:
                memory.append(page)  # Add page if frame available
            else:
                # Find least recently used page to replace
                lru_page = min(memory, key=lambda p: recent.get(p, -1))
                memory[memory.index(lru_page)] = page
            faults += 1
        # Update last used index for current page
        recent[page] = i
        steps.append(memory.copy() + ['✔' if hit else '✘'])
    return {"faults": faults, "steps": steps}

# Optimal Page Replacement Algorithm implementation
def optimal(reference, frames):
    memory = []      # Current pages in memory
    steps = []       # Record memory states and hit/miss
    faults = 0       # Page faults count

    for i in range(len(reference)):
        page = reference[i]
        if page in memory:
            hit = True
        else:
            hit = False
            if len(memory) < frames:
                memory.append(page)  # Add if space available
            else:
                # Look into future references to decide which page to replace
                future = reference[i+1:]
                # For each page in memory, find when it will be used next
                indexes = [future.index(p) if p in future else float('inf') for p in memory]
                # Replace the page not used for longest time (or never again)
                replace_index = indexes.index(max(indexes))
                memory[replace_index] = page
            faults += 1
        steps.append(memory.copy() + ['✔' if hit else '✘'])
    return {"faults": faults, "steps": steps}

# API endpoint to simulate the page replacement algorithms
@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()                 # Get JSON data from POST request
    frame_count = data.get("frameCount", 3)  # Extract frame count, default to 3

    # Generate a random reference string of 20 pages (0 to 9)
    ref_string = [random.randint(0, 9) for _ in range(20)]

    # Run each algorithm with the reference string and frame count
    fifo_result = fifo(ref_string, frame_count)
    lru_result = lru(ref_string, frame_count)
    opt_result = optimal(ref_string, frame_count)

    # Return JSON response with reference string, faults, and step-by-step visualization
    return jsonify({
        "referenceString": ref_string,
        "fifo": fifo_result["faults"],
        "lru": lru_result["faults"],
        "opt": opt_result["faults"],
        "fifoSteps": fifo_result["steps"],
        "lruSteps": lru_result["steps"],
        "optSteps": opt_result["steps"]
    })

# Run the Flask app in debug mode when the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
