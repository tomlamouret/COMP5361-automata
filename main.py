import math

from PySimpleAutomata import automata_IO


def ask_for_states():
    Q = input('''Please enter the finite set of states Q, using a comma as a separation: ''')
    Q = Q.replace('{', '')
    Q = Q.replace('}', '')
    Q = Q.replace(' ', '')
    Q = Q.split(',')
    while '' in Q:
        print("The state names cannot be null.")
        Q = input('''Please enter the finite set of states Q, using a comma as a separation: ''')
        Q = Q.replace('{', '')
        Q = Q.replace('}', '')
        Q = Q.replace(' ', '')
        Q = Q.split(',')
    Q = set(Q)
    Q = list(Q)
    Q.sort()
    return Q


def ask_for_alphabet():
    Σ = input('''Please enter the alphabet Σ, using a comma as a separation: ''')
    Σ = Σ.replace('{', '')
    Σ = Σ.replace('}', '')
    Σ = Σ.replace(' ', '')
    Σ = Σ.split(',')
    invalid = False
    for i in Σ:
        if len(i) > 1:
            invalid = True
    if '' in Σ:
        invalid = True
    while invalid:
        for i in Σ:
            if len(i) > 1:
                print("The alphabet Σ must be composed of characters.")
                break
        if '' in Σ:
            print("The null character cannot be used.")
        Σ = input("Please enter the alphabet Σ, using a comma as a separation: ")
        Σ = Σ.replace('{', '')
        Σ = Σ.replace('}', '')
        Σ = Σ.replace(' ', '')
        Σ = Σ.split(',')
        invalid = False
        for i in Σ:
            if len(i) > 1:
                invalid = True
        if '' in Σ:
            invalid = True
    Σ = set(Σ)
    Σ = list(Σ)
    Σ.sort()
    return Σ


def ask_for_start_states(Q, automaton_type):
    S_message = ''
    if automaton_type == "DFA":
        S_message = "Which of the following states is the start state: "
    else:
        S_message = "Which of the following states constitute the set of start states S: "
    for i in Q:
        S_message += i + ', '
    S_message = S_message[0:len(S_message) - 2]
    S_message += '? '
    S = input(S_message)
    S = S.replace('{', '')
    S = S.replace('}', '')
    S = S.replace(' ', '')
    S = S.split(',')
    S = set(S)
    S = list(S)
    S.sort()
    while '' in S or (len(S) > 1 and automaton_type == "DFA") or not set(S).issubset(set(Q)):
        not_in_Q = []
        for i in S:
            if i not in Q:
                not_in_Q.append(i)
        if len(S) > 1 and automaton_type == "DFA":
            print("A DFA can only have one start state.")
        if not_in_Q is not None:
            if '' in S:
                print("The state names cannot be null.")
            elif len(not_in_Q) == 1:
                print(not_in_Q[0] + " is not part of Q.")
            elif len(not_in_Q) > 1:
                not_in_Q_message = ''
                for i in not_in_Q:
                    not_in_Q_message = not_in_Q_message + i + ', '
                print(not_in_Q_message[0:len(not_in_Q_message) - 2] + " are not part of Q.")
        S = input(S_message)
        S = S.replace('{', '')
        S = S.replace('}', '')
        S = S.replace(' ', '')
        S = S.split(',')
        S = set(S)
        S = list(S)
        S.sort()
    return S


def ask_for_final_states(Q):
    final_states_message = "Which of the following states constitute the set of final states F: "
    for i in Q:
        final_states_message += i + ', '
    final_states_message = final_states_message[0:len(final_states_message) - 2]
    final_states_message += '?\nUse commas as a separation if there are several final states. '
    F = input(final_states_message)
    F = F.replace('{', '')
    F = F.replace('}', '')
    F = F.replace(' ', '')
    F = F.split(',')
    while '' in F or not set(F).issubset(set(Q)):
        not_in_Q = []
        for i in F:
            if i not in Q:
                not_in_Q.append(i)
        if not_in_Q is not None:
            if '' in F:
                print("The state names cannot be null.")
            elif len(not_in_Q) == 1:
                print(not_in_Q[0] + " is not part of Q.")
            elif len(not_in_Q) > 1:
                not_in_Q_message = ''
                for i in not_in_Q:
                    not_in_Q_message = not_in_Q_message + i + ', '
                print(not_in_Q_message[0:len(not_in_Q_message) - 2] + " are not part of Q.")
            F = input(final_states_message)
            F = F.replace('{', '')
            F = F.replace('}', '')
            F = F.replace(' ', '')
            F = F.split(',')
            F = set(F)
            F = list(F)
            F.sort()
    return F


def list_to_set_to_str(list):
    to_return = str(sorted(list))
    to_return = to_return.replace('[', '{')
    to_return = to_return.replace(']', '}')
    to_return = to_return.replace("'", '')
    return to_return


def ask_for_transition_table(Q, Σ, S, F, automaton, automaton_type):
    transition_table = []
    transition_table = [None] * (1 + len(Q))
    transition_table[0] = [None] * (1 + len(Σ))
    transition_table[0][0] = 'δ'
    for i in range(len(Σ)):
        transition_table[0][i + 1] = Σ[i]
    for i in range(len(Q)):
        transition_table[i + 1] = [None] * (1 + len(Σ))
        if Q[i] in S:
            transition_table[i + 1][0] = '→' + Q[i]
        elif Q[i] in F:
            transition_table[i + 1][0] = '*' + Q[i]
        else:
            transition_table[i + 1][0] = Q[i]
    print("Now, we need to fill the following transition table:")
    print_table(transition_table)
    transitions = {}
    counter_i = 0
    for i in transition_table:
        if counter_i > 0:
            counter_j = 0
            for j in i:
                if counter_j > 0:
                    delta_message = "Please enter δ(" + transition_table[counter_i][0] + ',' + \
                                    transition_table[0][counter_j] + ")"
                    delta_message = delta_message.replace('→', '')
                    delta_message = delta_message.replace('*', '')
                    if automaton_type in {"NFA", "DFA B"}:
                        delta_message += ", use commas as a separation if there are " \
                                         "several states and use '{}' to denote the empty set"
                    delta_message += ": "
                    delta = input(delta_message)
                    delta = delta.replace(' ', '')
                    if '{}' in delta:
                        delta = delta.replace('{}', '∅')
                    delta = delta.replace('{', '')
                    delta = delta.replace('}', '')
                    delta = delta.split(',')
                    delta = set(delta)
                    delta = list(delta)
                    delta.sort()
                    while '' in delta or "'" in delta or not set(delta).issubset(set(Q)) or \
                            ('∅' in delta and automaton_type == "DFA") or (len(delta) > 1 and automaton_type == "DFA") \
                            or ('∅' in delta and len(delta) > 1):
                        not_in_Q = []
                        for k in delta:
                            if k not in Q:
                                not_in_Q.append(k)
                        if not_in_Q is not None:
                            if '' in delta:
                                print("The state names cannot be null.")
                            elif "'" in delta:
                                print("Apostrophes are not accepted.")
                            elif '∅' in delta:
                                if automaton_type == "DFA":
                                    print("A δ value of a DFA cannot be the empty set.")
                                elif len(delta) > 1:
                                    print("The empty set should not be combined with another state.")
                                else:
                                    break
                            elif len(delta) > 1 and automaton_type == "DFA":
                                print("A δ value of a DFA cannot be a set with more than one value.")
                            elif len(not_in_Q) == 1:
                                print(not_in_Q[0] + " is not part of Q.")
                            elif len(not_in_Q) > 1:
                                not_in_Q_message = ''
                                for k in not_in_Q:
                                    not_in_Q_message = not_in_Q_message + str(k) + ', '
                                print(not_in_Q_message[0:len(not_in_Q_message) - 2] + " are not part of Q.")
                            delta = input(delta_message)
                            delta = delta.replace(' ', '')
                            if '{}' in delta:
                                delta = delta.replace('{}', '∅')
                            delta = delta.replace('{', '')
                            delta = delta.replace('}', '')
                            delta = delta.split(',')
                            delta = set(delta)
                            delta = list(delta)
                            delta.sort()
                    if delta[0] == '∅':
                        transition_table[counter_i][counter_j] = delta[0]
                    else:
                        transition_table[counter_i][counter_j] = delta
                        a1 = transition_table[counter_i][0]
                        a1 = a1.replace('→', '')
                        a1 = a1.replace('*', '')
                        a2 = transition_table[0][counter_j]
                        a2 = a2.replace('→', '')
                        a2 = a2.replace('*', '')
                        if automaton_type == "DFA":
                            transitions[(a1, a2)] = delta[0]
                        elif automaton_type in {"NFA", "DFA B"}:
                            transitions[(a1, a2)] = set(delta)
                counter_j += 1
            print_table(transition_table)
        counter_i += 1
    if automaton_type == "DFA B":
        incomplete = True
        while incomplete:
            new_states = []
            for l in range(1, len(transition_table)):
                for m in range(1, len(transition_table[0])):
                    temp = str(transition_table[l][m])
                    temp = temp.replace("'", '')
                    temp = temp.replace('[', '{')
                    temp = temp.replace(']', '}')
                    temp2 = temp.split(',')
                    if len(temp2) > 1 and temp not in Q:
                        Q.append(temp)
                        new_states.append(temp)
            if len(new_states) == 0:
                incomplete = False
            else:
                for n in new_states:
                    new_row = [None] * (1 + len(Σ))
                    temp = str(n)
                    temp = temp.replace('[', '{')
                    temp = temp.replace(']', '}')
                    temp = temp.replace("'", '')
                    temp2 = temp.replace('{', '')
                    temp2 = temp2.replace('}', '')
                    temp2 = temp2.replace(' ', '')
                    temp2 = temp2.split(',')
                    for o in temp2:
                        if o in F:
                            temp = '*' + temp
                            break
                    new_row[0] = temp
                    temp = temp.replace('*', '')
                    transition_table.append(new_row)
                    states = str(n)
                    states = states.replace('{', '')
                    states = states.replace('}', '')
                    states = states.replace(' ', '')
                    states = states.split(',')
                    for p in range(1, len(transition_table[0])):
                        temp = set()
                        for o in states:
                            for q in range(1, len(transition_table)):
                                if transition_table[q][p] is not None:
                                    row_header = transition_table[q][0]
                                    row_header = row_header.replace('→', '')
                                    row_header = row_header.replace('*', '')
                                    if row_header == o and type(transition_table[q][p]) is list:
                                        temp = temp.union(transition_table[q][p])
                        temp = list(temp)
                        temp.sort()
                        transition_table[len(transition_table) - 1][p] = temp
                print("The following transition table will allows us to generate the graph for the DFA B:")
                print_table(transition_table)
    automaton["alphabet"] = set(Σ)
    states = []
    if automaton_type == "DFA":
        automaton["initial_state"] = S[0]
    elif automaton_type == "NFA":
        automaton["initial_states"] = set(S)
    if automaton_type in {"DFA", "NFA"}:
        automaton["states"] = set(Q)
        automaton["accepting_states"] = set(F)
        automaton["transitions"] = transitions
    else:
        automaton["initial_state"] = list_to_set_to_str(S)
        states.append(set(S))
    if automaton_type == "DFA B":
        queue = []
        queue.append(set(S))
        accepting_states = []
        if len(states[0].intersection(set(F))) > 0:
            accepting_states.append(list_to_set_to_str(states[0]))
        while queue:
            current = queue.pop(0)
            for a in Σ:
                next = set()
                for state in current:
                    if (state, a) in transitions:
                        for next_state in transitions[state, a]:
                            next.add(next_state)
                if len(next) == 0:
                    continue
                if next not in states:
                    states.append(set(next))
                    queue.append(set(next))
                    if next.intersection(set(F)):
                        accepting_states.append(list_to_set_to_str(next))
                automaton['transitions'][list_to_set_to_str(current), a] = list_to_set_to_str(next)
        states_str = []
        for i in states:
            states_str.append(list_to_set_to_str(list(i)))
        automaton['states'] = set(states_str)
        accepting_states = set(accepting_states)
        automaton['accepting_states'] = set(accepting_states)
    return automaton


def print_table(table):
    max_length = [0] * len(table[0])
    for i in table:
        counter = 0
        for j in i:
            if j is not None:
                if len(str(j)) > max_length[counter] and type(j) is str:
                    max_length[counter] = len(str(j))
                elif len(str(j)) > max_length[counter] and type(j) is list:
                    max_length[counter] = len(str(j)) - len(j) * 2
            counter += 1
    counter_i = 0
    for i in table:
        row = ''
        counter_j = 0
        for j in i:
            if j is not None:
                blank_space = max_length[counter_j] - len(str(j))
                new_entry = ' ' * math.floor(blank_space / 2) + str(j) + ' ' * math.ceil(blank_space / 2)
                new_entry = new_entry.replace("'", '')
                new_entry = new_entry.replace('[', '{')
                new_entry = new_entry.replace(']', '}')
                row += new_entry
                if counter_j == 0:
                    row += '|'
            counter_j += 1
        print(row)
        if counter_i == 0:
            dashes = '-' * sum(max_length) + '-'
            print(dashes)
        counter_i += 1


option = input("If you want the transition diagram for a DFA or NFA A, please enter 1. Otherwise, if you want the\n"
               "transition diagram for a DFA B from a the transition table of a NFA A, please enter 2: ")
while (not option.isdigit()) or int(option) not in {1, 2}:
    option = input("Please enter your choice as either '1' or '2'.\nIf you want the transition diagram for a DFA or NFA"
                   " A, please enter 1. Otherwise, if you want the\ntransition diagram for a DFA B from a the "
                   "transition table of a NFA A, please enter 2: ")
option = int(option)
automaton_type = ''
if option == 1:
    automaton_type = input("Will you input a DFA or a NFA? ")
    while automaton_type not in {"dfa", "DFA", "nfa", "NFA"}:
        automaton_type = input("Please enter your answer as 'DFA' or 'NFA'. "
                               "Will you input a DFA or a NFA? ")
    if automaton_type == "dfa":
        automaton_type = "DFA"
    elif automaton_type == "nfa":
        automaton_type = "NFA"
    DFA = {'alphabet': {}, 'states': {}, 'initial_state': '', 'accepting_states': {}, 'transitions': {}}
    NFA = {'alphabet': {}, 'states': {}, 'initial_states': {}, 'accepting_states': {}, 'transitions': {}}
    Q = ask_for_states()
    Σ = ask_for_alphabet()
    S = ask_for_start_states(Q, automaton_type)
    F = ask_for_final_states(Q)
    if automaton_type == "DFA":
        DFA = ask_for_transition_table(Q, Σ, S, F, DFA, automaton_type)
        automata_IO.dfa_to_dot(DFA, 'DFA', './')
        file_path = '/Users/tomlamouret/Downloads/DFA.dot.svg'
    elif automaton_type == "NFA":
        NFA = ask_for_transition_table(Q, Σ, S, F, NFA, automaton_type)
        automata_IO.nfa_to_dot(NFA, 'NFA', './')
    print("The .svg graph and its corresponding .dot files have been generated in the same directory as this Python "
          "program.")
else:
    automaton_type = "NFA"
    DFA_B = {'alphabet': {}, 'states': {}, 'initial_state': '', 'accepting_states': {}, 'transitions': {}}
    Q = ask_for_states()
    Σ = ask_for_alphabet()
    S = ask_for_start_states(Q, automaton_type)
    F = ask_for_final_states(Q)
    automaton_type = "DFA B"
    DFA_B = ask_for_transition_table(Q, Σ, S, F, DFA_B, automaton_type)
    automata_IO.dfa_to_dot(DFA_B, 'DFA B', './')
    print("The .svg graph and its corresponding .dot files have been generated in the same directory as this Python "
          "program.")
