import argparse
import operator
import Queue
import sets
import string

class Puzzle:
    direction = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    
    # Each index corresponds to a digit and the zero index is the blank tile.
    # The elements of the lists are tuples of (row, column) that represents the
    # location of that digit on the puzzle board
    initial_state = []
    current_state = []
    frontier = []
    explored = []
    goal_state = []
    total_columns = 0
    total_rows = 0
    
    def __init__(self, file_name):
        with open(file_name, 'r') as fp:
            self._create_initial_states(fp)

    def breadth_first_search(self):
        paths = Queue.Queue()
        paths.put([[0,self.initial_state]])
        self.frontier.append(self.initial_state)
        
        while paths.not_empty:
            current_path = paths.get()
            current_state = current_path[-1][1]
            self.frontier.remove(current_state)
            print current_state
            self.explored.append(current_state)
            
            if self._goal_test(current_state):
#                print current_path
#                print current_state
#                print 'goal: ' + str(self.goal_state)
                 return  self._print_solution(current_path, self.explored)
            
                
            children = self._get_children(current_state)
            
            for child in children:
                if (child not in self.explored) and (child not in self.frontier):
                    self.frontier.append(child[1])
                    new_path = list(current_path)
                    new_path.append(child)
                    paths.put(new_path)
        return  '[!] No solution found'
            
    
    def depth_limited_dfs(self):
        pass
    
    def iterative_deepening_search(self):
        pass
    
    def a_star_search(self):
        pass
    
    def greedy_best_first_search(self):
        pass
    
    def _state_transition(self, direction, input_state):
        next_state = input_state[:]
        try:
#            print input_state[0]
#            print self.direction[direction]
            idx = input_state.index(self._add_tuples(input_state[0], self.direction[direction]))
        except ValueError as e:
            raise e
        next_state[0], next_state[idx] = next_state[idx], next_state[0]
        return next_state
    
    def _f_value(self, input_state, current_path_length):
        return current_path_length + self._heuristic_manhattan(input_state)
    
    def _heuristic_manhattan(self, input_state):
        # calculate the manhattan heuristic for current state
        distance_list = map(self._manhattan_distance, input_state, self.goal_state)
        return sum(distance_list)
    
    def _heuristic_alternative(self):
        pass
    
    def _manhattan_distance(self, start_tuple, end_tuple):
        # calculate the manhattan distance between two tile positions
        return abs(end_tuple[0] - start_tuple[0]) + abs(end_tuple[1] - start_tuple[1])
    
    def _create_initial_states(self, input_puzzle_fp):
    # generate the initial state and goal state from an input puzzle file
        current_row_idx = 1
        current_column_idx = 1
        
        input_puzzle_list = input_puzzle_fp.readlines()
        
        current_state_matrix = [row.rstrip('\n').split(',') for row in input_puzzle_list]
        
        self.initial_state = [0] * sum(sum(1 for i in row) for row in current_state_matrix)
        
        for row in current_state_matrix:
            self.total_rows = current_row_idx
            for element in row:
                self.initial_state[int(element)] = (current_row_idx, current_column_idx)
                self.goal_state.append((current_row_idx, current_column_idx))
                current_column_idx += 1
            self.total_columns = current_column_idx - 1
            current_column_idx = 1
            current_row_idx += 1
            
    def _add_tuples(self, tuple_a, tuple_b):
        return tuple(map(operator.add, tuple_a, tuple_b))
    
    def _goal_test(self, input_state):
        return input_state == self.goal_state
    
    def _get_children(self, input_state):
        # return a list of child states
        children = []
        for key in self.direction.iterkeys():
            try:
                children.append([key, self._state_transition(key, input_state)])
            except ValueError:
                continue
        return children
    
    def _print_solution(self, solution_path, expanded_list):
        print 'solution length: ' + str(len(solution_path) - 1)
        print 'nodes expanded: ' + str(len(expanded_list) - 1)
        print string.join([state[0] for state in solution_path if state[0]], '')
            
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='An N-Puzzle Solver')
    parser.add_argument('file_name', metavar='puzzle_file', help='a puzzle format file')
    parser.add_argument('algorithm', help='the algorithm to be used for computing a solution')
    parser.add_argument('third_parameter',nargs='?',default='NA', help='a third parameter required for some algorithms (e.g. depth, heuristic)')
    
    args = parser.parse_args()
    
    algorithm = args.algorithm
    algorithm_parameter = args.third_parameter
    
    
    puzzle = Puzzle(args.file_name)
    
    if algorithm == 'BFS':
        puzzle.breadth_first_search()
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
        
        