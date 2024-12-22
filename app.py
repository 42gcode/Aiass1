from flask import Flask, request, render_template
from queue import PriorityQueue

app = Flask(__name__)

graph = {
    'Gujranwala': ['Sialkot', 'Kamoke', 'Wazirabad', 'Daska'],
    'Sialkot': ['Gujranwala', 'Daska', 'Sambrial', 'Wazirabad'],
    'Gujrat': ['Gujranwala', 'Jhelum'],
    'Jhelum': ['Gujrat'],
    'Wazirabad': ['Gujranwala', 'Sialkot', 'Hafizabad', 'Alipur Chatha', 'Gujrat'],
    'Sheikhupura': ['Gujranwala', 'Hafizabad'],
    'Hafizabad': ['Wazirabad', 'Sheikhupura', 'Alipur Chatha'],
    'Kamoke': ['Gujranwala', 'Sheikhupura'],
    'Daska': ['Sialkot', 'Sambrial'],
    'Sambrial': ['Daska', 'Sialkot'],
    'Alipur Chatha': ['Wazirabad', 'Hafizabad']
}



def bfs(start, end):
    visited = set()
    queue = [(start, [start])]
    while queue:
        (current, path) = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor == end:
                return path + [end], len(visited)
            queue.append((neighbor, path + [neighbor]))
    return None, len(visited)

def dfs(start, end):
    visited = set()
    stack = [(start, [start])]
    while stack:
        (current, path) = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor == end:
                return path + [end], len(visited)
            stack.append((neighbor, path + [neighbor]))
    return None, len(visited)

def ucs(start, end):
    visited = set()
    pq = PriorityQueue()
    pq.put((0, start, [start]))
    while not pq.empty():
        (_, current, path) = pq.get()
        if current in visited:
            continue
        visited.add(current)
        if current == end:
            return path, len(visited)
        for neighbor in graph[current]:
            pq.put((0, neighbor, path + [neighbor]))
    return None, len(visited)

@app.route('/')
def index():
    cities = list(graph.keys())  # Get the list of all cities
    return render_template('index.html', cities=cities)

@app.route('/search', methods=['POST'])
def search():
    start = request.form['start']
    end = request.form['end']
    algorithm = request.form['algorithm']

    if algorithm == 'BFS':
        path, steps = bfs(start, end)
    elif algorithm == 'DFS':
        path, steps = dfs(start, end)
    elif algorithm == 'UCS':
        path, steps = ucs(start, end)
    else:
        path, steps = None, 0

    return render_template('result.html', algorithm=algorithm, path=path, steps=steps)

if __name__ == '__main__':
    app.run(debug=True)
