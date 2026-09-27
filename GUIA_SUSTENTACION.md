 Guía de sustentación — NFA a DFA (Construcción de subconjuntos)

Este documento es para estudiar antes de sustentar, no para leer en la sustentación.
Si puedes explicar las 4 secciones siguientes **sin mirar el código**, estás listo.

---

## ¿Qué hace el proyecto en una frase?

Recibe un autómata no determinista (NFA), y construye un autómata determinista (DFA)
equivalente — es decir, uno que acepta exactamente las mismas cadenas — usando el
algoritmo de **construcción de subconjuntos** (Kozen, Lecture 6).

---

## Los 4 conceptos que te pueden preguntar

### 1. Clausura-ε (`epsilon_closure`)

**En una frase:** son los estados a los que el autómata puede "deslizarse" sin
consumir ningún símbolo de entrada.

**Analogía:** imagina puertas que se abren solas, sin que tengas que dar un paso.
Antes de leer la siguiente letra de la palabra, primero cruzas todas las puertas
que se abren solas y ves en qué habitaciones podrías estar.

**Si preguntan "¿por qué la necesitas?":**
> "Porque un NFA con transiciones-ε puede cambiar de estado sin leer nada. Si no
> las tuviera en cuenta, el DFA se perdería estados a los que el NFA sí podría
> llegar."

---

### 2. Construcción de subconjuntos (`Q_M = 2^Q`) — el corazón del tema

**En una frase:** cada estado del DFA **no es un estado del NFA**, es un **conjunto**
de estados en los que el NFA podría estar simultáneamente.

**Analogía:** el NFA es como una persona indecisa que va por varios caminos a la
vez. El DFA en vez de elegir un camino, en cada paso se queda con "la lista de
todos los caminos posibles en los que podría estar ahora mismo". Esa lista completa
ES el nuevo estado del DFA.

**Si preguntan "¿por qué el DFA a veces tiene más estados que el NFA?":**
> "Porque en el peor caso hay que representar cada combinación posible de estados
> del NFA — hasta 2^n combinaciones para n estados. Por eso el algoritmo se llama
> 'construcción de subconjuntos': cada estado del DFA es un subconjunto de estados
> del NFA."

---

### 3. Estado `dead` (función de transición total)

**En una frase:** cuando el NFA no tiene a dónde ir con cierto símbolo, el DFA no
se queda "sin definir" — llega a un estado especial que ya no tiene salida.

**Analogía:** es como un cajón vacío: si abres cualquier cajón vacío, sigues
encontrando un cajón vacío. Nunca "sales" de ahí.

**Si preguntan "¿por qué agregaste eso?":**
> "Porque formalmente la función de transición de un DFA debe estar definida para
> *todo* estado y *todo* símbolo (es decir, ser total). Cuando el NFA no tiene
> transición, matemáticamente eso corresponde al conjunto vacío — que sigue siendo
> un subconjunto válido — y de ahí ya no se sale nunca."

---

### 4. Estado inicial como **conjunto** (no un solo estado)

**En una frase:** la definición formal de NFA permite *varios* estados de arranque
a la vez, no solo uno.

**Analogía:** es como poder empezar un laberinto por dos puertas de entrada
distintas al mismo tiempo, en vez de una sola.

**Si preguntan "¿por qué lo generalizaste?":**
> "Porque la definición formal de NFA es N = (Q, Σ, Δ, S, F), donde S es un
> *conjunto* de estados iniciales, no un solo estado. Un solo estado inicial es
> simplemente el caso particular donde ese conjunto tiene un solo elemento."

---

## Ejemplo para hacer en vivo si te lo piden

Este es el ejemplo tal cual aparece en la lectura (Kozen, Example 6.5), y ya está
probado en `tests/test_subset_construction.py`.

**NFA:** alfabeto `{b}`, estado inicial `s`, aceptación `{p, q, r}`

s --ε--> t --ε--> u
p --ε--> t q --ε--> u
s --b--> p t --b--> q u --b--> r


**Traza paso a paso (para dibujar en el tablero):**

| Paso | Estado del DFA (conjunto de estados NFA) | ¿Acepta? |
|---|---|---|
| Inicio | clausura-ε({s}) = **{s, t, u}** | No |
| Lee `b` | {p,q,r} ∪ clausura-ε = **{p, q, r, t, u}** | Sí → acepta `"b"` |
| Lee `b` otra vez | **{q, r, u}** | Sí → acepta `"bb"` |
| Lee `b` otra vez | **{r}** | Sí → acepta `"bbb"` |
| Lee `b` otra vez | **∅ (dead)** | No → rechaza `"bbbb"` |

**Conclusión que dice el PDF:** el lenguaje aceptado es exactamente `{b, bb, bbb}`.
Esto es justo lo que valida el test `test_example_6_5_accepts_exactly_b_bb_bbb`.

---

## Preguntas frecuentes y respuesta corta

**¿Por qué usaste `frozenset` en vez de listas o strings para los estados del DFA?**
> Porque cada estado del DFA es un *conjunto* de estados del NFA, y necesito poder
> compararlos y usarlos como llave (los sets normales de Python no se pueden usar
> como llave porque son mutables; `frozenset` sí).

**¿Cómo decides si un estado del DFA es de aceptación?**
> Si el conjunto de estados del NFA que representa tiene *al menos uno* que sea de
> aceptación en el NFA original (intersección no vacía con F).

**¿Qué pasa si el NFA no tiene transiciones-ε?**
> El algoritmo funciona igual: la clausura-ε de un estado sin transiciones-ε es
> el mismo estado, así que simplemente no cambia nada.

**¿Cuál es la complejidad en el peor caso?**
> Exponencial en el número de estados del NFA: hasta 2^n estados en el DFA, porque
> cada subconjunto de Q es un estado posible.

---

## Mapa rápido: teoría → código

| Concepto del PDF | Función / archivo |
|---|---|
| `Δ̂(A, ε)` | `epsilon_closure()` en `src/functions/subset_construction.py` |
| `Δ(A, a)` | `move()` |
| Construcción completa `M = (Q_M, Σ, δ_M, s_M, F_M)` | `subset_construction()` |
| `F_M = {A \| A ∩ F ≠ ∅}` | línea `accepting_states = [s for s in dfa_states if s & set(accepting)]` |
| Simulación de una cadena sobre el DFA | `simulate_dfa()` en `src/functions/simulate.py` |
| Ejemplo 6.5 como prueba automatizada | `tests/test_subset_construction.py` |
