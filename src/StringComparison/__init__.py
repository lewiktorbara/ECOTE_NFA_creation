# Return the set of states that can be reached from a state following 'e' arrows
def followArrowE(state):
    # Create a new set, with each state as it's only member
    
    states = set()
    states.add(state)

    if state.label is None:
        if state.edge1 is not None:
            states |= followArrowE(state.edge1)

        if state.edge2 is not None:
            states |= followArrowE(state.edge2)
    
    return states