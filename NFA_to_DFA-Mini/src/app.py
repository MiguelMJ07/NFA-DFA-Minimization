# Punto de entrada de la aplicación.
# Su única responsabilidad es crear el servidor Flask y conectar las rutas.
from flask import Flask
from controllers.automata_controller import automata_bp
from controllers.minimization_controller import minimization_bp  # Asignación 2

app = Flask(__name__)
# Respeta el orden de las llaves en las respuestas JSON (en vez de ordenarlas alfabéticamente).
app.json.sort_keys = False

# Conecta las rutas definidas en el Controller (Blueprint) con la app principal.
app.register_blueprint(automata_bp)       # Asignación 1: /convert, /simulate
app.register_blueprint(minimization_bp)   # Asignación 2: /minimize, /minimize/compare, /minimize/ui

if __name__ == "__main__":
    # debug=True recarga el servidor automáticamente al detectar cambios en el código
    # y muestra errores detallados en el navegador (solo para desarrollo).
    app.run(debug=True, port=5000)
