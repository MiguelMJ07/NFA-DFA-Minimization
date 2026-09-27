# CAPA CONTROLLER
# Responsabilidad: recibir peticiones HTTP, validar el formato de entrada,
# y devolver respuestas HTTP. NO contiene lógica del algoritmo de autómatas.
from flask import Blueprint, request, jsonify
from gateways.automata_gateway import AutomataGateway

# Blueprint agrupa las rutas relacionadas con "automata" en un solo módulo.
automata_bp = Blueprint("automata", __name__)

# Una sola instancia del Gateway, reutilizada en todas las peticiones
# (no guarda estado entre peticiones, así que es seguro compartirla).
gateway = AutomataGateway()


@automata_bp.route("/convert", methods=["POST"])
def convert():
    # Parsea el body JSON de la petición a un diccionario de Python.
    data = request.get_json()

    # Validación de forma: confirma que existan los campos obligatorios
    # antes de siquiera intentar ejecutar el algoritmo.
    required_fields = ["states", "alphabet", "initial", "accepting", "transitions"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        # Delega la ejecución del algoritmo al Gateway.
        result = gateway.convert_nfa_to_dfa(data)
        return jsonify(result), 200
    except ValueError as e:
        # Si el Gateway detecta un error de negocio (ej. estado inicial inválido),
        # lo traduce en una respuesta HTTP 400.
        return jsonify({"error": str(e)}), 400


@automata_bp.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()

    # Validación de forma para /simulate: confirma los campos que
    # necesita simulate_dfa (transitions, initial, accepting, input).
    required_fields = ["transitions", "initial", "accepting", "input"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        result = gateway.simulate(data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400