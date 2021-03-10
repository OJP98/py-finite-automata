from pythomata import SimpleDFA

alphabet = {"a", "b", "c"}
states = {"s1", "s2", "s3"}
initial_state = "s1"
accepting_states = {"s3"}
transition_function = {
    "s1": {
        "b": "s1",
        "a": "s2"
    },
    "s2": {
        "a": "s3",
        "b": "s1"
    },
    "s3": {
        "c": "s3"
    }
}
dfa = SimpleDFA(states, alphabet, initial_state,
                accepting_states, transition_function)

graph = dfa.minimize().trim().to_graphviz()
graph.render("./test")
