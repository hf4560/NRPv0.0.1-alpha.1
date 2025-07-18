from flask import Flask, request, jsonify
from nodes.qnode.q_node import QNode

app = Flask(__name__)
q = QNode((0, 0, 0))

@app.route('/', methods=['POST'])
def handle():
    packet = request.get_json()
    result = q.handle_packet(packet)
    return jsonify(result["response"]), result["status"]

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
