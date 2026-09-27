# NFA to DFA Web Server — extended with DFA Minimization

A REST API for finite automata, built in two stages:

* **Assignment 1:** converts a Nondeterministic Finite Automaton (NFA) into an equivalent DFA with the **Subset Construction** algorithm (Kozen, *Automata and Computability*, Lecture 6), and simulates DFAs.
* **Assignment 2:** receives a DFA and returns its **equivalent states**, using the **minimization algorithm** of Kozen, Lecture 14 (built on the quotient construction of Lecture 13). It also returns the minimized DFA, a step-by-step trace, and a check of whether two DFAs accept the same language.

## Student

- Full name: Miguel Muñoz Jiménez, Juan José Sierra Ocampo
- Class number: 4368

## Environment

- OS: Windows 11
- Python: 3.10 / 3.11 (the test suite was run on Linux with both versions)
- Framework: Flask 3.0.3
- Testing: pytest 8.3.3

## Project structure

```
src/
├── controllers/
│   ├── automata_controller.py      # A1: /convert, /simulate
│   └── minimization_controller.py  # A2: /minimize, /minimize/compare, /minimize/example, /minimize/ui
├── gateways/
│   ├── automata_gateway.py         # A1: orchestration + exception handling
│   └── minimization_gateway.py     # A2: orchestration + exception handling + request limits
├── functions/                      # pure automata algorithms, no HTTP-related code
│   ├── subset_construction.py      # A1: epsilon closure, move, subset construction
│   ├── simulate.py                 # A1: DFA simulation
│   ├── dfa.py                      # A2: DFA model (δ̂, accessible states, JSON/text/DOT output)
│   ├── dfa_parser.py               # A2: course text format + JSON (A1 field names, /convert output)
│   ├── minimization.py             # A2: Kozen L14 marking algorithm, quotient M/≈, DFA equivalence
│   └── minimization_format.py      # A2: assignment text output + JSON view of every step
├── templates/minimization.html     # A2: interactive demo page
└── app.py                          # application entry point
tests/                              # automated tests (pytest)
test_*.json, test_minimize.txt      # sample requests
```

## How to run

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   source .venv/bin/activate       # macOS / Linux
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:

   ```bash
   python src/app.py
   ```

   The server runs on `http://127.0.0.1:5000`. The interactive page is at **http://127.0.0.1:5000/minimize/ui**.

## How to run the tests

```bash
pytest tests/
```

---

# Assignment 1 — Endpoints

### POST /convert

Converts an NFA into its equivalent DFA. Epsilon transitions are written as `"symbol": null`.

**Request body:**
```json
{
    "states": [0, 1, 2, 3],
    "alphabet": ["a", "b"],
    "initial": 0,
    "accepting": [3],
    "transitions": [
        {"from": 0, "symbol": "a", "to": 1}
    ]
}
```

**Response body:**
```json
{
    "dfaStates": ["0", "1", "dead"],
    "transitions": [...],
    "acceptingStates": ["1"]
}
```

### POST /simulate

Runs an input string on a DFA.

**Request body:**
```json
{ "initial": "0", "accepting": ["1"], "input": "ab", "transitions": [...] }
```

**Response body:**
```json
{ "path": ["0", "1"], "accepted": true }
```

---

# Assignment 2 — DFA Minimization

## Endpoints

| Method | Route | Description |
|---|---|---|
| `POST` | `/minimize` | Returns the equivalent states of one or more DFAs (plus the minimized DFA and the trace) |
| `POST` | `/minimize/compare` | Decides whether two DFAs accept the same language; if not, returns a shortest counterexample |
| `GET` | `/minimize/example` | The example from the assignment statement and its expected output |
| `GET` | `/minimize/ui` | Web page that uses `/convert`, `/minimize`, `/minimize/compare` and `/simulate` |

`POST /minimize` accepts two query parameters:

| Parameter | Values | Default | Effect |
|---|---|---|---|
| `format` | `json`, `text` | `json` | `text` returns only the output required by the assignment. `Accept: text/plain` does the same. |
| `steps` | `true`, `false` | `true` for JSON | Includes or omits the step-by-step trace. |

## How the DFA is sent

**1. Course text format** (`Content-Type: text/plain`, section 5.1 of the assignment). The initial state is always `0`, and the final-states line may be empty:

```bash
curl -X POST 'http://127.0.0.1:5000/minimize?format=text' \
     -H 'Content-Type: text/plain' --data-binary @test_minimize.txt
```

```
1
6
a b
1 4 5
0 1 2
1 3 4
2 4 3
3 5 5
4 5 5
5 5 5
```

> Use `--data-binary`. With `curl -d`, the newlines are removed.

**2. JSON with the same field names as Assignment 1** (`Content-Type: application/json`), as in `test_minimize.json`:

```json
{
  "states": [0, 1, 2, 3, 4, 5],
  "alphabet": ["a", "b"],
  "initial": 0,
  "accepting": [1, 4, 5],
  "transitions": [{"from": 0, "symbol": "a", "to": 1}, {"from": 0, "symbol": "b", "to": 2}, "..."]
}
```

**3. The output of `POST /convert`, unchanged.**
* States can be names (`"0-1-3-7"`, `"dead"`).
* `dfaStates` and `acceptingStates` are accepted as aliases.
* A missing `alphabet` is inferred from the transitions.
* A missing `initial` defaults to the first listed state, which is where the subset construction puts the start state.

This gives the full pipeline **NFA → `/convert` → DFA → `/minimize` → minimal DFA**:

```bash
curl -s -X POST http://127.0.0.1:5000/convert -H 'Content-Type: application/json' -d @test_request.json \
 | curl -s -X POST 'http://127.0.0.1:5000/minimize?format=text' -H 'Content-Type: application/json' -d @-
# (5-8, 6-8) (5-8, 8) (6-8, 8)
```

`transitions` may also be an object (`{"0": {"a": 1, "b": 2}}`) or a table of rows in alphabet order (`[[1, 2], [3, 4], ...]`). To send several DFAs at once, use `{"cases": [dfa1, dfa2, ...]}`; to send the course text inside JSON, use `{"input": "<text>"}`.

**Validation.** Invalid input returns **HTTP 400** with a clear message, and text input errors include the **line number**. The server checks:
* the number of cases and of states;
* that symbols are `a`–`z`;
* that there is one row per state and a row for state 0;
* that the DFA is complete and deterministic (no `null` / epsilon symbols; an NFA must go through `/convert` first);
* that every target belongs to Q;
* the size limits: 500 states per DFA, 50 cases, 2 MB body.

```json
{ "error": "Line 6: delta(1, a) = 9 is not a state of Q.", "line": 6 }
```

## Response

**Plain text** (`?format=text`). This is the format required by section 5.2: one line per case with the equivalent pairs in lexicographic order. The line is empty when no states can be collapsed.

```
(4, 5)
```

**JSON** (default):

```jsonc
{
  "algorithm": "Kozen (1997), Lecture 14 - table-filling (marking) minimization",
  "numCases": 1,
  "output": "(4, 5)",
  "cases": [{
    "case": 1,
    "equivalentPairs": [[4, 5]],
    "output": "(4, 5)",
    "isMinimal": false,
    "equivalenceClasses": [[0], [1], [2], [3], [4, 5]],
    "removedInaccessibleStates": [],
    "stats": { "statesOriginal": 6, "statesMinimized": 5, "pairsTotal": 15,
               "pairsMarked": 14, "pairsEquivalent": 1, "rounds": 3 },
    "originalDfa":  { "states": [...], "alphabet": [...], "initial": 0, "accepting": [...], "transitions": [...] },
    "minimizedDfa": { "states": [...], "alphabet": [...], "initial": 0, "accepting": [...], "transitions": [...],
                      "stateLabels": { "4": "{4,5}" }, "stateMap": { "5": 4 },
                      "courseFormat": "1\n5\na b\n1 4\n0 1 2\n..." },
    "dot": { "original": "digraph ...", "minimized": "digraph ..." },
    "steps": {
      "rounds": [ { "round": 2, "description": "...", "marked": [
          { "pair": [0, 2], "round": 2, "symbol": "a", "via": [1, 4], "witness": "aa",
            "reason": "delta(0,a) = 1, delta(2,a) = 4, and {1,4} was already marked" } ] } ],
      "markingTable": { "columns": [...], "rows": [...] },
      "markingTableText": "  1 |  X0 ..."
    }
  }]
}
```

* **`minimizedDfa`** uses the field names of `/simulate` (`initial`, `accepting`, `transitions`), so it can be simulated directly. It can also be sent back to `/minimize`, which then reports `isMinimal: true`.
* **`witness`** is a *shortest* string that distinguishes the pair: from exactly one of the two states, reading it ends in an accepting state.
* **`dot`** holds Graphviz sources. In the original graph, equivalent states share a colour.
* **Large DFAs:** `steps` is only included for DFAs with at most 150 states.

**`POST /minimize/compare`** takes exactly two DFAs (text with `c = 2`, or `{"cases": [dfa1, dfa2]}`) and returns:

```json
{ "equivalent": false, "counterexample": "aaa", "acceptedBy": "first", "rounds": 4,
  "explanation": "The string 'aaa' is accepted by the first DFA only (no shorter string tells them apart), so L(M1) ≠ L(M2)." }
```

---

# Algorithms

## Subset Construction (Assignment 1)

Given an NFA, each state of the resulting DFA represents a *set* of NFA states that could be active at the same time.

1. **Epsilon closure:** for a set of NFA states, compute every state reachable without consuming input.
2. **Move:** for a set of NFA states and a symbol, compute every state reachable by consuming that symbol.
3. Starting from the epsilon closure of the initial state(s), apply `move` followed by `epsilon closure` for every symbol, until no new DFA states appear.
4. A DFA state is accepting if its set contains at least one accepting NFA state.
5. To make the transition function total, a symbol with no reachable states leads to an absorbing `dead` state (the empty set).

## DFA Minimization (Assignment 2)

Let `M = (Q, Σ, δ, s, F)` be a DFA with no inaccessible states. Two states are **equivalent** (`p ≈ q`) iff for every `x ∈ Σ*`, `δ̂(p, x) ∈ F ⇔ δ̂(q, x) ∈ F`. Equivalent states can be **collapsed**.

Kozen, Lecture 14:

1. Write down a table of all pairs `{p, q}`, initially unmarked.
2. Mark `{p, q}` if `p ∈ F` and `q ∉ F`, or vice versa. The empty string `ε` already distinguishes such pairs.
3. Repeat until nothing changes: if an unmarked `{p, q}` has `{δ(p, a), δ(q, a)}` marked for some `a ∈ Σ`, mark `{p, q}`.
4. When done, `p ≈ q` **iff** `{p, q}` is unmarked.

**Why it is correct.**
* *Every marked pair is inequivalent.* If `w` distinguishes `{δ(p,a), δ(q,a)}`, then `aw` distinguishes `{p, q}`. By induction on the order in which pairs are marked, every marked pair is inequivalent.
* *Every inequivalent pair gets marked.* Use induction on the length of a shortest distinguishing string `x`. If `x = ε`, step 2 marks the pair. If `x = ay`, then `y` distinguishes `{δ(p,a), δ(q,a)}`, which is therefore marked, so step 3 marks `{p, q}`.

**Implementation details** (`src/functions/minimization.py`):

* **Synchronous rounds.** Step 3 runs in rounds: round `k` only uses marks from earlier rounds. The final table is exactly Kozen's. In addition, a pair is first marked in round `k` **iff its shortest distinguishing string has length `k`**. This is the `≈ₖ` refinement of Lecture 13, and it is why every recorded witness is a shortest one.
* **Witnesses.** Each marked pair stores the symbol `a` and the pair that caused it. Following that chain rebuilds the witness, e.g. `{0,2} –a→ {1,4} –a→ {3,5}` (marked by ε) gives `aa`.
* **Cost.** At most `|Q| − 1` rounds are needed, because a shortest witness is never longer than `|Q| − 2`. Each round only revisits pairs that are still unmarked. The worst case is `O(|Q|³·|Σ|)`; typical DFAs need about 5 rounds.
* **Classes.** The unmarked pairs form `≈`, and union-find builds its classes `[p]`.
* **Quotient automaton `M/≈`** (Lecture 13): `Q' = {[p]}`, `δ'([p], a) = [δ(p, a)]`, `s' = [s]`, `F' = {[p] | p ∈ F}`. `δ'` is well defined because `≈` is a congruence. The class of `s` becomes state `0`.
* **Inaccessible states.** The assignment guarantees there are none. If some appear anyway, they are removed first (as Kozen requires) and reported.

**Worked example** (from the assignment statement, `F = {1, 4, 5}`):

| Round | Newly marked pairs |
|---|---|
| 0 | `{0,1} {0,4} {0,5} {1,2} {1,3} {2,4} {2,5} {3,4} {3,5}` (accepting vs. non-accepting) |
| 1 | `{0,3}` via `b→{2,5}`, `{1,4}` via `a→{3,5}`, `{1,5}` via `a→{3,5}`, `{2,3}` via `b→{3,5}` |
| 2 | `{0,2}` via `a→{1,4}` |
| 3 | no change, so the algorithm stops |

Only `{4, 5}` stays unmarked. The output is `(4, 5)`, and the minimized DFA has 5 states.

**Equivalence of two DFAs.** `L(M₁) = L(M₂)` iff the two initial states are equivalent in the disjoint union `M₁ ⊎ M₂`. The same marking algorithm decides this, and the witness of `{s₁, s₂}` is a shortest counterexample.

---

# Integration with the Assignment 1 Web Server

The new feature follows the same **Controller → Gateway → Functions** architecture and conventions as Assignment 1:

| Layer | Assignment 1 | Assignment 2 (new, same pattern) |
|---|---|---|
| Controller | `automata_controller.py`: Blueprint, validates input, catches `ValueError` → 400 | `minimization_controller.py`: Blueprint, validates format/params/body, catches `ValueError` → 400 |
| Gateway | `AutomataGateway`: calls Functions, turns internal exceptions into `ValueError` | `MinimizationGateway`: calls Functions, turns internal exceptions into `ValueError`, applies request limits |
| Functions | `subset_construction.py`, `simulate.py` | `dfa.py`, `dfa_parser.py`, `minimization.py`, `minimization_format.py` |

* **Assignment 1 code is untouched.** The only change to existing code is in `src/app.py`: one import, one `app.register_blueprint(minimization_bp)`, and `app.json.sort_keys = False` so JSON keys keep their order.
* **Same JSON conventions** as `/convert` and `/simulate`: `states`, `alphabet`, `initial`, `accepting`, `transitions` as `{from, symbol, to}`, with camelCase response keys.
* **The two assignments chain together.**
  * `/minimize` accepts the output of `/convert` as is.
  * The DFA returned by `/minimize` can be sent directly to `/simulate`.
  * The demo page runs NFA → `/convert` → `/minimize` (e.g. 9 NFA states → 7 DFA states → 5 minimal states), and its string tester calls `/simulate` on both the original and the minimized DFA.
* **Demo page (`/minimize/ui`).**
  * It replays Kozen's table **round by round**: the cells marked in the current round are highlighted, each with its reason and witness.
  * It draws the original and minimized automata, with equivalent states sharing a colour. It uses Graphviz (viz.js) when there is internet access, and otherwise switches to a built-in SVG layout, so the demo also works offline.

# Tests

Run with `pytest tests/`: **907 tests**, 5 from Assignment 1 and 902 from Assignment 2.

**`tests/test_minimization.py`** (Functions layer):
* the statement example, including the pairs marked in each round and their witnesses, plus the same table with `F = {1, 2, 5}` (result `(1, 2) (3, 4)`);
* several cases in one input, numeric ordering, already-minimal and single-state DFAs, inaccessible states, and the `|Q| − 2` witness bound;
* named and subset states;
* every validation error, with its line number;
* **200 random DFAs** compared against a **brute-force evaluation of the definition**. For each one, every witness must distinguish its pair and be a shortest one, the minimized DFA must accept the same language, and running the algorithm on it again must find nothing to collapse;
* **150 random DFA pairs** for `compare`, also checked against brute force.

**`tests/test_minimization_api.py`** (Controller + Gateway):
* every endpoint, input format and query parameter;
* **500 fuzzed malformed requests**, none of which may produce a 500;
* **integration with Assignment 1:**
  * NFA → `/convert` → `/minimize` on the Assignment 1 example;
  * the Kozen Example 6.5 pipeline;
  * `/simulate` on the minimized DFA agreeing with the original on every string of length ≤ 5;
  * the sample request files;
  * the Assignment 1 endpoints still behaving as before.
