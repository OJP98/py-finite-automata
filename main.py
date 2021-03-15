from reader import Reader
from parsing import Parser
from nfa import NFA
from dfa import DFA
from direct_dfa import DDFA
from direct_reader import DirectReader

program_title = '''

#        FINITE AUTOMATA        #

Generate NFA's of DFA's based on a regular epression and compare times simulating a string!
'''

main_menu = '''
What would you like to do?
1. Set a regular expression
2. Test a string with the given regular expression
0. Exit out of the program
'''

submenu = '''
Select one of the above to test your regular expression:

    1. Use Thompson to generate a NFA and Powerset construction to generate a DFA.
    2. Use direct DFA method.
    0. Back to main menu.
'''
thompson_msg = '''
    # THOMPSON AND POWERSET CONSTRUCION # '''
direct_dfa_msg = '''
    # DIRECT DFA CONSTRUCION # '''
invalid_opt = '''
Err: That's not a valid option!
'''
generate_diagram_msg = '''
Would you like to generate and view the diagram? [y/n] (default: n)'''
type_regex_msg = '''
Type in a regular expression '''
type_string_msg = '''
Type in a string '''

if __name__ == "__main__":
    print(program_title)
    opt = None
    regex = None
    method = None

    while opt != 0:
        print(main_menu)
        opt = input('> ')

        if opt == '1':
            print(type_regex_msg)
            regex = input('> ')

            reader = Reader(regex)
            tokens = reader.CreateTokens()
            parser = Parser(tokens)
            tree = parser.Parse()

            direct_reader = DirectReader(regex)
            direct_tokens = direct_reader.CreateTokens()
            direct_parser = Parser(direct_tokens)
            direct_tree = direct_parser.Parse()
            print('\n\tParsed tree:', tree)

        if opt == '2':
            if not regex:
                print('\nERR: You need to set a regular expression first!')
                opt = None
            else:
                print(submenu)
                method = input('> ')

                if method == '1':
                    print(thompson_msg)
                    print(type_string_msg)
                    regex_input = input('> ')
                    nfa = NFA(tree, reader.GetSymbols(), regex_input)
                    nfa_regex = nfa.EvalRegex()
                    print('Does the string belongs to the regex (NFA)?')
                    print('>', nfa_regex)

                    dfa = DFA(nfa.trans_func, nfa.symbols,
                              nfa.curr_state, nfa.final_states)
                    dfa.TransformNFAToDFA()
                    dfa_regex = 'TODO'
                    print('Does the string belongs to the regex (DFA)?')
                    print('>', dfa_regex)

                    print(generate_diagram_msg)
                    generate_diagram = input('> ')

                    if generate_diagram == 'y':
                        nfa.WriteNFADiagram()
                        dfa.GraphDFA()

                elif method == '2':
                    print(direct_dfa_msg)
                    print(type_string_msg)
                    regex_input = input('> ')
                    ddfa = DDFA(direct_tree, direct_reader.GetSymbols())
                    ddfa_regex = 'TODO'
                    print('Does the string belongs to the regex?')
                    print('>', nfa_regex)

                    print(generate_diagram_msg)
                    generate_diagram = input('> ')

                    if generate_diagram == 'y':
                        ddfa.GraphDFA()

                elif method == '3':
                    continue

                else:
                    print(invalid_opt)

        elif opt == '0':
            print('See you later!')
            exit(1)


# if __name__ == "__main__":
#     string = 'abb(a|b)*'
#     regex = 'abbab'
#     print('EXPRESIÓN:', string)

#     print(f'''
#             Parsed tree: {tree}
#             ''')

#     ddfa = DDFA(tree, reader.GetSymbols())
#     ddfa.GraphDFA()

    # NFA
    # _nfa = NFA(tree, reader.GetSymbols(), regex)
    # _nfa.WriteNFADiagram()
    # nfa_regex = _nfa.EvalRegex()
    # print(nfa_regex)

    # DFA
    # _dfa = DFA(_nfa.trans_func, _nfa.symbols,
    #            _nfa.curr_state, _nfa.final_states)

    # _dfa.TransformNFAToDFA()
    # _dfa.GraphDFA()

    # DIRECT DFA
    # reader = DirectReader(string)
    # tokens = reader.CreateTokens()
    # parser = Parser(tokens)
    # tree = parser.Parse()
    # ddfa = DDFA(tree, reader.GetSymbols())
    # ddfa.GraphDFA()
