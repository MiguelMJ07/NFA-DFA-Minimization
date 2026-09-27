# Asignación 2 — Auditoría y guion de sustentación

## Veredicto de la auditoría

El proyecto cumple el enunciado y el algoritmo es correcto. Coincide con un algoritmo independiente en 3.000 AFD aleatorios, y las pruebas detectan los errores introducidos a propósito. En el proyecto final (`NFA-DFA-Minimization-main`) ya están el README completo y la carpeta limpia. Queda un pendiente: contrastar con el texto de la Lecture 14. Además, conviene copiar las 3 correcciones de la auditoría (hallazgos 10 a 12), que no están en esa versión.

Cómo se verificó:

- **Enunciado, punto por punto:** secciones 3, 4, 5.1 y 5.2, y los entregables 2 a 6.
- **Oráculo independiente:** 3.000 AFD aleatorios (1 a 40 estados, 1 a 4 símbolos, con y sin estados inaccesibles) se compararon contra el algoritmo de Moore. Dieron los mismos pares equivalentes y el mismo tamaño mínimo en todos los casos.
- **Mutation testing:** se metieron 11 errores a propósito en el algoritmo y en el lector de entrada. Las pruebas detectaron 10. Se reforzó la prueba que faltaba y ahora detectan los 11.
- **Análisis estático (pyflakes):** cero advertencias en el código de la Asignación 2.
- **Rendimiento y tamaño de respuesta:** medidos por HTTP con AFD de 6 a 500 estados.
- **Asignación 1 dentro del servidor integrado:** se probaron `/convert` y `/simulate` con entradas válidas e inválidas.
- **Pruebas automáticas:** las 907 pasan con Flask 3.0.3 y pytest 8.3.3, en Python 3.10 y 3.11 (Linux, y también en la VM Linux de la Mac).

## Hallazgos

Se encontraron 12 hallazgos y ninguno afecta la corrección del algoritmo. En el proyecto final ya están resueltos 2: el README y la limpieza de la carpeta. Las 3 correcciones de la auditoría (10 a 12) están en el .zip, pero no en ese proyecto.

| # | Hallazgo | Severidad | Estado |
| --- | --- | --- | --- |
| 1 | Al README le faltaban nombre, número de clase y SO. En el proyecto final ya están; solo convendría poner la versión exacta de Python con la que corren. | Alta | Corregido |
| 2 | El algoritmo no se ha contrastado con el texto de la Lecture 14: el PDF no está en el proyecto y la vista previa de Springer no cargó. | Media | Abierto: ustedes |
| 3 | Archivos innecesarios (`.DS_Store`, `__pycache__`). El proyecto final no los tiene y su `.gitignore` ya los excluye. | Media | Corregido |
| 4 | El formato `(p, q)` y el orden numérico de los pares son una interpretación del enunciado, no algo que diga textualmente. | Baja | Abierto: ustedes |
| 5 | `/convert` con `"states": 5` responde 500, porque `_validate_nfa` se ejecuta fuera del `try`. | Media | Abierto: Asignación 1 |
| 6 | `/convert` con un body que no es JSON devuelve una página HTML 415 en vez de un JSON. | Baja | Abierto: Asignación 1 |
| 7 | `/convert` ordena los nombres de estado como texto: {2, 10} sale como `10-2`. | Baja | Abierto: Asignación 1 |
| 8 | Hay un import sin usar (`move`) en `tests/test_subset_construction.py`. | Baja | Abierto: Asignación 1 |
| 9 | Un método HTTP incorrecto (por ejemplo `GET /minimize`) devuelve HTML 405, igual que en la Asignación 1. | Baja | Abierto: ustedes |
| 10 | Prueba débil: si el código dejara de eliminar los estados inaccesibles, ninguna prueba fallaría. Está reforzada en el .zip, pero no en el proyecto final. | Media | Abierto: ustedes |
| 11 | La traza paso a paso pesa 3,2 MB con 150 estados. El .zip la limita a 60 estados; el proyecto final mantiene 150. | Media | Abierto: ustedes |
| 12 | Un comentario dice "pocos segundos" para 500 estados, pero el peor caso mide \~9 s. Está corregido en el .zip, no en el proyecto final. | Baja | Abierto: ustedes |

Sin hallazgos en:

- Seguridad: no hay inyección de HTML, porque Jinja escapa el texto, la página escribe con `textContent` y los nombres se escapan en el DOT.
- Concurrencia: el Gateway no guarda estado entre peticiones.
- Compatibilidad con Python 3.10 y 3.11.
- Tiempo de un AFD aleatorio de 500 estados: 0,25 s.

## Cumplimiento del enunciado

El proyecto final, `NFA-DFA-Minimization-main`, cumple los 10 requisitos. Lo único que conviene reforzar es contrastar el algoritmo con el texto de la Lecture 14.

| Requisito (enunciado) | Cómo se cumple | Estado |
| --- | --- | --- |
| Extender el servidor de la Asignación 1 (secciones 3 y 4) | Un Blueprint nuevo registrado en `src/app.py`. El código de la Asignación 1 no se modificó. | Cumple |
| Aplicar el algoritmo de la Lecture 14 (req. 3) | `mark_pairs()` implementa los pasos 1 a 4 al pie de la letra, por rondas. Falta contrastarlo con el PDF (hallazgo 2). | Cumple |
| Endpoint diseñado por el estudiante (sección 4) | `POST /minimize`, más `/minimize/compare`, `/minimize/example` y `/minimize/ui` | Cumple |
| Entrada en el formato 5.1: c casos, n, alfabeto, finales, filas; s = 0; letras a–z | `parse_cases()` informa los errores con número de línea. Ejemplo en `test_minimize.txt`. | Cumple |
| Salida 5.2: pares equivalentes en orden lexicográfico | `?format=text` devuelve una línea por caso. Con el ejemplo del enunciado da `(4, 5)`. | Cumple |
| AFD minimizado (opcional, 5.2) | `minimizedDfa` en JSON y en el formato del curso | Cumple |
| Integración con la Asignación 1 (req. 2) | Mismas capas. El recorrido NFA → `/convert` → `/minimize` → `/simulate` está probado. | Cumple |
| README en inglés con los 9 puntos (req. 4) | Completo en el proyecto final: estudiantes, número de clase, SO, instrucciones, endpoint, entrada, respuesta, algoritmo e integración. | Cumple |
| Sin archivos innecesarios (req. 5) | El proyecto final no tiene `.DS_Store` ni `__pycache__`, y el `.gitignore` los excluye. | Cumple |
| Funcionalidad adicional (req. 6 y sección 4.1) | Comparación de dos AFD, tabla ronda por ronda, testigos, grafos y recorrido desde un NFA | Cumple |

## Estructura del video (6:00)

&#91;embedded content: guion de 6:00 · 8 bloques, 2 personas\]

Los 8 bloques alternan de persona y ninguno pasa de 60 s. Así la explicación teórica nunca va más de un minuto seguido sin que se vea el sistema en pantalla. Cada persona habla 3:00 exactos.

- **Persona A:** intro, ejemplo en vivo, arquitectura y pruebas.
- **Persona B:** teoría, por qué funciona, demo de la API y cierre.

## Guion completo

Son 811 palabras: unos 5:25 a 150 palabras por minuto. Los 35 s que sobran son para las acciones en pantalla. Lo que va entre corchetes es la acción en pantalla y no se lee en voz alta. El bloque más cargado es el de teoría (0:30–1:30, 162 palabras por minuto). Si se pasan, recorten su última frase.

### 0:00–0:30 · Intro — Persona A

**En pantalla:** la página `/minimize/ui` abierta.

> Hola. En la Asignación 2 extendimos el servidor web de la Asignación 1, el que convierte un AFN en AFD, con una funcionalidad nueva. Ahora el servidor recibe un autómata finito determinista y encuentra sus estados equivalentes con el algoritmo de minimización de Kozen, Lecture 14. Al juntar esos estados se obtiene el AFD mínimo. Vamos a mostrar la teoría, el algoritmo en vivo, cómo lo integramos y cómo lo verificamos.

### 0:30–1:30 · Equivalencia y algoritmo — Persona B

**En pantalla:** el README, en la sección *DFA Minimization*, con la definición y los 4 pasos.

> Dos estados p y q son equivalentes si ninguna cadena los distingue: para toda cadena x, δ̂(p, x) está en F si y solo si δ̂(q, x) está en F. El algoritmo de Kozen busca justamente los pares que *no* son equivalentes. Paso 1: se escribe una tabla con todos los pares {p, q}, sin marcar. Paso 2: se marcan los pares donde exactamente uno de los dos es final, porque la cadena vacía ya los distingue. Paso 3: se repite lo siguiente. Si un par sin marcar lleva, con algún símbolo a, a un par {δ(p, a), δ(q, a)} que ya está marcado, también se marca. Paso 4: cuando una ronda no marca nada, los pares sin marcar son exactamente los equivalentes. Nosotros ejecutamos el paso 3 por rondas, y una marca nueva solo cuenta desde la ronda siguiente. El resultado es el mismo de Kozen, pero así la ronda k marca los pares cuya cadena distinguidora más corta mide k.

### 1:30–2:30 · Ejemplo en vivo — Persona A

**En pantalla:** `/minimize/ui` con el ejemplo del enunciado; se usan los botones ⏮ Start y Next ▶.

> Este es el ejemplo del enunciado: seis estados, alfabeto a y b, y finales 1, 4 y 5. \[⏮ Start\] En la ronda 0 se marcan los nueve pares de un final contra un no final. \[Next ▶\] En la ronda 1 caen cuatro pares. Por ejemplo, {0, 3}: con la letra b, 0 va a 2 y 3 va a 5, y {2, 5} ya estaba marcado. Su testigo es b. \[Next ▶\] En la ronda 2 cae {0, 2}: con a va a {1, 4}, que se marcó en la ronda anterior. Su testigo es aa. \[Next ▶\] En la ronda 3 no cambia nada y el algoritmo termina. Solo {4, 5} queda sin marcar. La salida es (4, 5) y el AFD pasa de 6 a 5 estados. \[señalar el grafo\] Por eso en el grafo el 4 y el 5 tienen el mismo color.

### 2:30–3:15 · Por qué funciona y M/≈ — Persona B

**En pantalla:** el README, en la sección *Why it is correct*.

> ¿Por qué es correcto? En una dirección: si w distingue a {δ(p, a), δ(q, a)}, entonces a·w distingue a {p, q}, así que todo par marcado es distinguible. En la otra, por inducción sobre la longitud de la cadena más corta que distingue a p y q. Si es la cadena vacía, el paso 2 marca el par. Si es a·y, el par al que se llega con a ya estaba marcado, y el paso 3 marca este. Además termina, porque hay a lo sumo n(n−1)/2 pares. Con los pares sin marcar formamos las clases de equivalencia, que son los estados del cociente M/≈ de la Lecture 13. δ′ está bien definida porque ≈ es una congruencia.

### 3:15–4:15 · Arquitectura e integración — Persona A

**En pantalla:** el árbol de `src/` en el editor, y después `app.py`, `minimization_controller.py`, `minimization_gateway.py` y `mark_pairs()` en `functions/minimization.py`.

> Mantuvimos la arquitectura de la Asignación 1: Controller, Gateway y Functions. El controller recibe la petición HTTP, valida el formato y devuelve la respuesta. Si algo falla, responde 400 con un mensaje claro y, cuando la entrada es texto, con el número de línea. El Gateway coordina: lee la entrada, aplica límites de tamaño, llama a las funciones y traduce los errores. En Functions está el algoritmo puro, sin nada de HTTP. mark\_pairs implementa los pasos de Kozen y \_quotient construye M/≈. El único archivo de la Asignación 1 que cambió es app.py, donde registramos el nuevo Blueprint. Además, /minimize acepta tal cual la salida de /convert, y el AFD mínimo se puede mandar directo a /simulate.

### 4:15–5:15 · Demo de la API — Persona B

**En pantalla:** una terminal con `curl`, y después el panel *Or start from an NFA* de la página.

> El endpoint es POST /minimize. Recibe el formato del enunciado como texto plano, o JSON con los mismos campos de la Asignación 1. \[curl con test\_minimize.txt y ?format=text\] Con format=text devuelve exactamente la salida pedida: (4, 5). Sin ese parámetro devuelve JSON con los pares, las clases, el AFD minimizado y cada ronda con su razón y su testigo. \[página, panel del AFN\] Ahora el recorrido completo. Este es el AFN de la Asignación 1, con nueve estados. /convert lo convierte en un AFD de siete, y /minimize lo reduce a cinco, porque 8, 5-8 y 6-8 son equivalentes: desde los tres se acepta exactamente b\*. \[escribir abb\] Y esta cadena, simulada con /simulate en los dos autómatas, da el mismo resultado.

### 5:15–5:45 · Pruebas y verificación — Persona A

**En pantalla:** la terminal con `pytest tests/` y el resultado `907 passed`.

> Para verificarlo tenemos 907 pruebas automáticas. En 200 AFD aleatorios comparamos el resultado con la definición de equivalencia evaluada por fuerza bruta. También comprobamos que cada testigo sea el más corto y que el AFD mínimo acepte el mismo lenguaje. Hay pruebas de integración con /convert y /simulate, y 500 peticiones mal formadas que nunca deben tumbar el servidor.

### 5:45–6:00 · Cierre — Persona B

**En pantalla:** la página con el AFD mínimo.

> En resumen: implementamos el algoritmo de la Lecture 14, lo integramos al servidor de la Asignación 1 sin romper nada, la salida sigue el formato del enunciado y hay una interfaz para verlo paso a paso. Gracias.

## Antes de grabar

El guion se verificó sobre el proyecto final, `NFA-DFA-Minimization-main`, y coincide en todo: 907 pruebas, salida `(4, 5)`, 9, 4, 1 y 0 pares marcados por ronda, testigo `aa` y el recorrido de 9 → 7 → 5 estados. Los comandos de abajo son para Windows 11 y se corren desde la carpeta raíz del proyecto.

- [ ] Preparar el entorno: `python -m venv .venv`, luego `.venv\Scripts\activate` y `pip install -r requirements.txt`.
- [ ] Correr `pytest tests/`. Debe salir `907 passed`.
- [ ] Correr `python src/app.py`, abrir `http://127.0.0.1:5000/minimize/ui` y confirmar que se dibujan los grafos.
- [ ] Dejar abiertos el README (secciones *DFA Minimization* y *Why it is correct*) y el editor con `src/`.
- [ ] Tener otra terminal con el curl ya escrito. En PowerShell usen `curl.exe` y comillas dobles, porque `curl` sin `.exe` es otro comando y una `@` sin comillas da error: `curl.exe -X POST "http://127.0.0.1:5000/minimize?format=text" -H "Content-Type: text/plain" --data-binary "@test_minimize.txt"`
- [ ] Poner la tabla en ⏮ Start antes del bloque de 1:30.
- [ ] Ensayar una vez con cronómetro, bloque por bloque.

## Preguntas probables

| Pregunta | Respuesta corta |
| --- | --- |
| ¿Por qué por rondas y no marcando todo en la misma pasada? | La tabla final es la misma. Las rondas corresponden a ≈k de la Lecture 13, y por eso cada testigo es el más corto posible. |
| ¿Y los estados inaccesibles? | Kozen pide quitarlos primero. El enunciado garantiza que no hay, pero el servidor los detecta, los quita y lo reporta. |
| ¿Cuál es la complejidad? | O(n²) pares × \|Σ\| por ronda × hasta n−1 rondas, o sea O(n³·\|Σ\|) en el peor caso. Un AFD aleatorio de 500 estados tarda 0,25 s. |
| ¿Qué significa "orden lexicográfico" en la salida? | Cada par se escribe (p, q) con p < q. Se ordenan primero por p y luego por q, numéricamente. |
| ¿Cómo saben que el resultado es mínimo? | Las pruebas lo vuelven a minimizar y no queda nada por colapsar, y verifican que acepta el mismo lenguaje. El AFD mínimo es único salvo renombrar estados (Myhill–Nerode). |
| ¿Por qué casi no tocaron el código de la Asignación 1? | Se extendió con archivos nuevos en cada capa. Solo `app.py` cambió, para registrar el Blueprint. |
| ¿Qué hace `/minimize/compare`? | Dos AFD aceptan el mismo lenguaje si y solo si sus estados iniciales son equivalentes en la unión disjunta. Usa el mismo algoritmo, y si no son equivalentes, el testigo es el contraejemplo más corto. |
