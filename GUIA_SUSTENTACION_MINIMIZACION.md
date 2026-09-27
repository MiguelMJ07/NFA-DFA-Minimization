# Guía de sustentación — Minimización de AFD (Kozen, Lecture 14)

Este documento sirve para estudiar antes de sustentar; no es para leerlo durante la sustentación.
Estás listo si puedes explicar las secciones siguientes **sin mirar el código**.

---

## ¿Qué hace el proyecto en una frase?

Recibe un autómata determinista (AFD) y encuentra qué estados son **equivalentes**, es decir, cuáles
se comportan igual para cualquier cadena. Esos estados se juntan en uno solo para obtener el **AFD mínimo**
que acepta el mismo lenguaje. Usa el algoritmo de marcado de Kozen, Lecture 14, y se integra al servidor de la Asignación 1.

---

## Los 6 conceptos que te pueden preguntar

### 1. Estados equivalentes (p ≈ q)

**En una frase:** dos estados son equivalentes si **ninguna cadena** puede distinguirlos. Para
toda cadena x, o las dos rutas terminan en aceptación, o ninguna termina.

**Analogía:** son dos puertas distintas que dan al mismo edificio. Por fuera se ven diferentes,
pero todo lo que puedes hacer después de entrar por una lo puedes hacer después de entrar por la otra.

**Si preguntan "¿cómo sabes que dos estados NO son equivalentes?":**
> "Porque existe una cadena, que llamamos testigo, con la que uno de los dos llega a aceptación
> y el otro no. El servidor devuelve ese testigo para cada par marcado."

---

### 2. El algoritmo de marcado (el corazón del tema)

**Los 4 pasos (Kozen, Lecture 14):**
1. Hacer una tabla con todos los pares {p, q}, sin marcar.
2. Marcar los pares donde **exactamente uno** de los dos estados es final. ε ya los distingue.
3. Repetir: si {p, q} no está marcado pero con algún símbolo `a` se llega a un par
   {δ(p,a), δ(q,a)} que **ya está marcado**, marcar {p, q}.
4. Al terminar, los pares **sin marcar** son exactamente los equivalentes.

**Analogía:** es como un contagio. Primero se "contagian" los pares que ya se ven distintos
(final contra no final). Después, un par se contagia si con una letra lleva a un par contagiado.
Lo que nunca se contagia son los estados que de verdad se comportan igual.

**Si preguntan "¿por qué termina?":**
> "Porque en cada ronda se marca al menos un par o el algoritmo se detiene, y hay un número finito de pares:
> n(n−1)/2. En el peor caso bastan n−1 rondas."

---

### 3. ¿Por qué es correcto? (la demostración)

**Dirección 1: si se marca, no son equivalentes.** Si {δ(p,a), δ(q,a)} se distingue con la cadena `w`,
entonces {p, q} se distingue con `a·w`. Por inducción sobre el orden en que se marcan los pares, todo par marcado es distinguible.

**Dirección 2: si no son equivalentes, se marca.** Se hace inducción sobre la longitud de la cadena más corta `x`
que los distingue:
- Si `x = ε`, uno es final y el otro no, así que se marca en el paso 2.
- Si `x = a·y`, entonces `y` distingue a {δ(p,a), δ(q,a)}, que por hipótesis de inducción ya está marcado,
  así que el paso 3 marca {p, q}.

---

### 4. El autómata cociente M/≈ (Lecture 13)

**En una frase:** cada clase de estados equivalentes se convierte en **un solo estado** del AFD mínimo.

- Q' = {[p]}, δ'([p], a) = [δ(p, a)], s' = [s], F' = {[p] | p ∈ F}.

**Si preguntan "¿por qué δ' está bien definida si elijo cualquier estado de la clase?":**
> "Porque ≈ es una **congruencia**: si p ≈ q, entonces δ(p,a) ≈ δ(q,a). Da igual qué representante
> de la clase use; siempre llego a la misma clase."

---

### 5. Estados inaccesibles

**En una frase:** son estados a los que no se llega desde el inicial con ninguna cadena.

**Si preguntan "¿por qué Kozen pide quitarlos primero?":**
> "Porque el marcado solo junta estados equivalentes. Un estado inaccesible puede no ser equivalente
> a ninguno y quedaría en el AFD 'mínimo' sin servir para nada. El enunciado garantiza que no hay,
> pero el servidor igual los detecta, los quita y lo reporta."

---

### 6. Nuestra decisión de diseño: rondas y testigos

**En una frase:** el paso 3 se ejecuta por **rondas**, y una marca nueva solo se tiene en cuenta
a partir de la ronda siguiente.

**Si preguntan "¿eso cambia el algoritmo de Kozen?":**
> "No. La tabla final es exactamente la misma. Lo que se gana es que la ronda k corresponde a la
> relación ≈k de la Lecture 13: un par se marca en la ronda k si y solo si la cadena más corta que lo distingue
> mide k. Por eso cada testigo que devuelve el servidor es el más corto posible."

---

## Ejemplo para hacer en vivo (el del enunciado)

AFD: estados 0 a 5, alfabeto {a, b}, F = {1, 4, 5}.

| Ronda | Pares que se marcan | ¿Por qué? |
|---|---|---|
| 0 | {0,1} {0,4} {0,5} {1,2} {1,3} {2,4} {2,5} {3,4} {3,5} | uno es final y el otro no |
| 1 | {0,3} {1,4} {1,5} {2,3} | p. ej. {0,3} con `b` va a {2,5}, ya marcado |
| 2 | {0,2} | con `a` va a {1,4}, marcado en la ronda 1 (testigo: `aa`) |
| 3 | ninguno | el algoritmo termina |

**Resultado:** solo {4, 5} queda sin marcar, así que la salida es `(4, 5)` y el AFD pasa de 6 a 5 estados.

**Para mostrarlo en vivo:** abre `/minimize/ui`, pulsa **⏮ Start** y avanza con **Next ▶**. En cada ronda se
resaltan las celdas nuevas, con su razón y su testigo. Si no hay internet, los grafos se dibujan igual.

**Segundo ejemplo para el tablero:** la misma tabla con F = {1, 2, 5} da `(1, 2) (3, 4)`. Los pares {1,2} y {3,4}
nunca llevan a un par marcado: con `a` y con `b`, {1,2} va a {3,4}, y {3,4} va a {5,5}.

**Ejemplo con la Asignación 1:** el NFA de la Asignación 1 tiene 9 estados. `/convert` lo transforma en un AFD de 7 estados, y
`/minimize` lo reduce a 5, porque `8`, `5-8` y `6-8` son equivalentes: desde los tres se acepta exactamente b*.

---

## Preguntas frecuentes y respuesta corta

**¿Cómo se integró con la Asignación 1?**
> "Con la misma arquitectura Controller → Gateway → Functions, en archivos nuevos. Del código viejo
> solo cambió `app.py`, para registrar el nuevo Blueprint. Además `/minimize` recibe tal cual la salida de
> `/convert`, y el AFD mínimo se puede mandar directo a `/simulate`."

**¿Qué formatos de entrada acepta?**
> "El formato de texto del enunciado y JSON con los mismos campos de la Asignación 1. Si los estados
> tienen nombre, como `0-1-3-7`, la respuesta usa esos mismos nombres."

**¿Qué devuelve?**
> "Con `?format=text`, exactamente lo que pide el enunciado: los pares en orden lexicográfico, una línea
> por caso. En JSON devuelve además las clases, el AFD mínimo, la tabla de marcado, las rondas y el testigo de cada par."

**¿Cuál es la complejidad?**
> "Hay O(n²) pares y cada ronda los revisa con |Σ| símbolos. Con hasta n−1 rondas, el peor caso es
> O(n³·|Σ|). En la práctica se necesitan pocas rondas."

**¿Cómo sabes que funciona?**
> "Hay 907 pruebas. Sobre 200 AFD aleatorios se compara el resultado con la definición evaluada
> por fuerza bruta. También se verifica que el AFD mínimo acepta el mismo lenguaje y que no se puede
> minimizar más."

**¿Qué es `/minimize/compare`?**
> "Una funcionalidad extra. Dos AFD aceptan el mismo lenguaje si y solo si sus estados iniciales son
> equivalentes en la unión de los dos autómatas. Se usa el mismo algoritmo de marcado, y si no son
> equivalentes, el testigo es el contraejemplo más corto."

---

## Mapa rápido: teoría → código

| Concepto | Dónde está |
|---|---|
| Pasos 1-4 de Kozen (tabla, marcado, rondas) | `mark_pairs()` en `src/functions/minimization.py` |
| Testigo (cadena que distingue un par) | `Marking.witness()` |
| Clases de ≈ | `_equivalence_classes()` (union-find) |
| Cociente M/≈ | `_quotient()` |
| Quitar estados inaccesibles | `DFA.accessible_states()` + `minimize()` |
| Equivalencia de dos AFD | `compare()` |
| Lectura del formato del curso y del JSON | `src/functions/dfa_parser.py` |
| Salida `(p, q)` en orden lexicográfico | `format_output()` en `src/functions/minimization_format.py` |
| Endpoint y validación HTTP | `src/controllers/minimization_controller.py` |
| Orquestación y manejo de errores | `MinimizationGateway` en `src/gateways/minimization_gateway.py` |
