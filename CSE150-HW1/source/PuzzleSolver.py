import argparse




def breadth_first_search():
    pass

def depth_limited_dfs():
    pass

def iterative_deepening_search():
    pass

def a_star_search():
    pass

def greedy_best_first_search():
    pass

def f_value():
    pass

def heuristic_sld():
    pass
    

def heuristic_greedy():
    pass

def heuristic_manhattan():
    pass

def heuristic_alternative():
    pass

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='An N-Puzzle Solver')
    parser.add_argument('file_name', metavar='puzzle_file', help='a puzzle format file')
    parser.add_argument('algorithm', help='the algorithm to be used for computing a solution')
    parser.add_argument('third_parameter',nargs='?',default='NA', help='a third parameter required for some algorithms (e.g. depth, heuristic)')
    
    args = parser.parse_args()
    
    algorithm = args.algorithm
    algorithm_parameter = args.third_parameter
    
    with open(args.file_name, 'r') as fp:
        pass
    
    if algorithm == 'BFS':
        pass
    elif algorithm == 'DFS':
        pass
    elif algorithm == 'ID':
        pass
    elif algorithm == 'A_Star':
        pass
    elif algorithm == 'Greedy':
        pass
    else:
        print '[!] Invalid Algorithm: ' + algorithm
        
        