# Documenting graph and orchestrator modules

Read this when documenting a state machine, workflow DAG, agent graph or pipeline orchestrator —
anything where control flow is data rather than a call sequence. Ignore it for ordinary modules.

Prose cannot convey routing. A reader given three paragraphs about a five-node graph still cannot
answer "what happens if this check fails". A diagram can.

## The module header needs a diagram

Under `Graph structure` (or `Tool-call flow`, or `HITL boundary` — name it for what it is):

```text
Graph structure
---------------
START
  │
  ▼
node_a
  │
  ▼
route_x ──yes──► node_b ──► END
  │
  no
  ▼
node_c ──► END
```

ASCII rather than an image: it survives in a terminal, a diff and a code review, and it is edited
where it lives.

## Every node

Include **Position**, **Reads**, **Writes**, **Routes** — the four things a reader needs and
cannot get from the function body alone:

```
Normalise the incoming record, then hand off to the router.

Position: START ──► node_a ──► route_x
Reads:    raw_input, config
Writes:   normalised, reject_count
Routes:   always → route_x
```

`Reads`/`Writes` matter most. Shared mutable state is what makes these systems hard, and nothing
else in the code states which keys a node touches.

## Every router

A decision table — condition → next node. One row per branch, including the fallthrough. A router
whose default case is undocumented is where the silent bug lives.

## Tool catalogs

Show the recommended sequence as an arrow chain, and mark terminating tools distinctly (`⏹`) so a
reader can see which calls end the loop.

## Accuracy

**Drawn arrows must match the compiled graph.** Most frameworks can enumerate their own edges at
runtime — use that to check, rather than reading the builder code and trusting yourself.

A stale diagram is the worst artifact in this skill: it is read as authoritative, it is quicker to
believe than to verify, and it will send someone to the wrong node. When edges change, fix the
diagram in the same commit or delete it.
