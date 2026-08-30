
# 🟢 LEVEL 2 — Multiple Steps

We already know:

```text
START → hello → END
```

Now suppose we want:

```text
START
  ↓
greet
  ↓
introduce
  ↓
END
```

## 1. First write normal Python

We need two operations:

```python
def greet(state):
    return {
        "message": "Hello"
    }


def introduce(state):
    return {
        "message": "I am Vedant"
    }
```

So far, nothing special.

---

## 2. What's missing?

LangGraph knows about the graph, but we haven't told it that these functions are **nodes**.

So:

```python
graph.add_node("greet", greet)
graph.add_node("introduce", introduce)
```

Now we have:

```text
greet
introduce
```

---

## 3. What's still missing?

LangGraph doesn't know the order.

We want:

```text
greet → introduce
```

So:

```python
graph.add_edge("greet", "introduce")
```

And the complete flow:

```python
graph.add_edge(START, "greet")
graph.add_edge("greet", "introduce")
graph.add_edge("introduce", END)
```

---

# Complete code

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str


def greet(state: State):
    return {
        "message": "Hello"
    }


def introduce(state: State):
    return {
        "message": state["message"] + " I am Vedant."
    }


graph = StateGraph(State)

graph.add_node("greet", greet)
graph.add_node("introduce", introduce)

graph.add_edge(START, "greet")
graph.add_edge("greet", "introduce")
graph.add_edge("introduce", END)

app = graph.compile()

result = app.invoke({
    "message": ""
})

print(result)
```

---

# 🧠 New syntax learned

You already knew:

```python
graph.add_node()
graph.add_edge()
```

But now understand that `add_edge()` can connect **any two nodes**:

```python
graph.add_edge("node1", "node2")
```

Meaning:

```text
node1
  ↓
node2
```

---

# 🟡 LEVEL 3 — Decision Making

Now let's make it interesting.

Suppose the user gives:

```python
age = 20
```

We want:

```text
             ┌──→ adult
             │
START → check
             │
             └──→ minor
```

### First question:

Can a normal edge do this?

```python
graph.add_edge("check", "adult")
```

No.

Because we don't always want `adult`.

Sometimes we want `minor`.

So we have a **new problem**:

> The next node depends on the current state.

That's when we need a **conditional edge**.

---

## 1. Create the decision function

```python
def check_age(state):

    if state["age"] >= 18:
        return "adult"

    return "minor"
```

This function decides where to go.

---

## 2. Create the nodes

```python
def adult(state):
    return {
        "result": "Adult"
    }


def minor(state):
    return {
        "result": "Minor"
    }
```

Then:

```python
graph.add_node("adult", adult)
graph.add_node("minor", minor)
```

---

## 3. What's missing?

We need to tell LangGraph:

> "After `check`, use my decision function."

That's:

```python
graph.add_conditional_edges(
    "check",
    check_age,
    {
        "adult": "adult",
        "minor": "minor"
    }
)
```

Read it like English:

```text
After check:

run check_age()

if it returns "adult"
    → go to adult

if it returns "minor"
    → go to minor
```

---

# Complete Level 3 code

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    age: int
    result: str


def check(state: State):
    return {}


def check_age(state: State):

    if state["age"] >= 18:
        return "adult"

    return "minor"


def adult(state: State):
    return {
        "result": "You are an adult"
    }


def minor(state: State):
    return {
        "result": "You are a minor"
    }


graph = StateGraph(State)

graph.add_node("check", check)
graph.add_node("adult", adult)
graph.add_node("minor", minor)

graph.add_edge(START, "check")

graph.add_conditional_edges(
    "check",
    check_age,
    {
        "adult": "adult",
        "minor": "minor"
    }
)

graph.add_edge("adult", END)
graph.add_edge("minor", END)

app = graph.compile()

result = app.invoke({
    "age": 20,
    "result": ""
})

print(result)
```

---

# 🔥 LEVEL 4 — Why do we need `MessagesState`?

Now imagine we're building a chatbot.

The input isn't simply:

```python
{
    "age": 20
}
```

Instead:

```text
User: What is LangGraph?
Assistant: LangGraph is...
User: Why do we use nodes?
```

We need to maintain a **conversation history**.

We could manually create:

```python
class State(TypedDict):
    messages: list
```

But now we have a problem:

> How should messages be added and managed correctly?

Instead of manually handling this, LangGraph provides:

```python
from langgraph.graph import MessagesState
```

Then:

```python
class State(MessagesState):
    pass
```

Or simply:

```python
graph = StateGraph(MessagesState)
```

Now the state contains:

```python
{
    "messages": [...]
}
```

---

# 🧠 The progression is important

You've now learned:

```text
LEVEL 1
StateGraph
   ↓
Node
   ↓
Edge
```

Then:

```text
LEVEL 2
Multiple Nodes
   ↓
Node → Node
```

Then:

```text
LEVEL 3
Conditional Edge
   ↓
Decision
   ↓
Node A / Node B
```

Then:

```text
LEVEL 4
MessagesState
   ↓
Conversation
   ↓
Chatbot
```

### 🚀 Next level

The **big jump** is:

```text
LLM
 ↓
Does LLM want a tool?
 ↓
YES
 ↓
ToolNode
 ↓
LLM
```

That's where we'll introduce **`@tool`, `bind_tools()`, `ToolNode`, and `tools_condition`**—the core syntax behind a real LangGraph agent.
