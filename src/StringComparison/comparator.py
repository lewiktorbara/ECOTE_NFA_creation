from Errors.error_library import get_error_lib
from Errors.log import Log
from Creator.creator import create, conversion

# Matches string to  nfa created by RE
def match(nfa, string, logs, line):

    # The cirrent set of states and tje mext set pf states
    
    currentState = set()
    nextState = set()

    # Add the initial state of the current set of states
    currentState |= followArrowE(nfa.initial)

    # Loop through each character in the string
    for s in string:
        if s == '\n':
            break
        if s.isspace():
            logs.append(Log("w30", line, []))
            break
        if s.isdigit() == False and s.isalpha() == False:
            raise Log("e30", line, [s])
        # Loop through current set of states
        for c in currentState:
            # Check if that state is labbelled 's'
            if c.label == s:
                # Add edge1 state to the next set of states
                nextState |= followArrowE(c.edge1)
        
        # Set currentState to next and clear out nextState
        currentState = nextState
        nextState = set()

    # Check if the accept state is in the current set of states
    return (nfa.accept in currentState)

# Return the set of stetes that can be reached from a state following 'e' arrows
def followArrowE(state):
    # Create a new set, with each state as it's only member
    states = set()
    states.add(state)

    # Check if state has arrows labelled 'e' from it
    if state.label is None:
        # Check if edge1 is a state
        if state.edge1 is not None:
            # If there's edge1, follow it
            states |= followArrowE(state.edge1)
        
        # Check if edge2 is a state
        if state.edge2 is not None:
            # If there's edge2, follow it
            states |= followArrowE(state.edge2)

    # Return the set of states
    return states

def comparison(infix, strings, logs):

    shunt = conversion(infix, logs)
    nfa = create(shunt)
    
    output = []
    output_txt = []

    for i in range(len(strings)):
        result = match(nfa, strings[i], logs, i)
        output.append(result)
        txt = str(result) + " - RE: " + infix + ", String: " + strings[i]
        output_txt.append(txt)
        print(txt)

    print('')
    return output, output_txt