import argparse
import operator
import Queue
import string
import sys
from heapq import *

class Puzzle:
    direction = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    
    # Each index corresponds to a digit and the zero index is the blank tile.
    # The elements of the lists are tuples of (row, column) that represents the
    # location of that digit on the puzzle board
    initial_state = []
    current_state = []
    frontier = []
    explored = []
    lifo = []
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
            self.explored.append(current_state)
            
            for child in self._get_children(current_state):
                if (child[1] not in self.explored) and (child[1] not in self.frontier):
                    self.frontier.append(child[1])
                    new_path = list(current_path)
                    new_path.append(child)
                    if self._goal_test(child[1]):
                         return  self._print_solution(new_path, self.explored)
                    paths.put(new_path)
        return  '[!] No solution found'
            
    def depth_limited_dfs(self, depth_limit):
        result = self._recursive_dfs([0, self.initial_state], depth_limit)
        if result:
            self._print_solution(self.lifo[::-1], self.explored)
        return result
    
    def _recursive_dfs(self, current_state, depth_limit):
            self.explored.append(current_state)
            if self._goal_test(current_state[1]):
                self.lifo.append(current_state)
                return True
            elif depth_limit == 0:
                return False
            else:
                cutoff_occurred = False;
                
                for child in self._get_children(current_state[1]):
                    result = self._recursive_dfs(child, depth_limit - 1)
                    if not result:
                        cutoff_occurred = True;
                    elif result:
                        self.lifo.append(current_state)
                        return True
                if cutoff_occurred:
                    return False
                     
            print  '[!] No solution found'
            return False
            
    def iterative_deepening_search(self, depth_limit):
        for limit in range(1, depth_limit + 1):
            result = self.depth_limited_dfs(limit)
            if result:
                break
    
    def a_star_search(self, heuristic):
        paths = []
        heappush(paths, (self._f_value(self.initial_state, 0, heuristic),[[ 0, self.initial_state]]))
        self.frontier.append(self.initial_state)
        
        while len(paths):
            current_path = heappop(paths)
            current_state = current_path[1][-1][1]
            self.frontier.remove(current_state)
            self.explored.append(current_state)
            
            if self._goal_test(current_state):
                return  self._print_solution(current_path[1], self.explored)
            
            for child in self._get_children(current_state):
                if (child[1] not in self.explored) and (child[1] not in self.frontier):
                    self.frontier.append(child[1])
                    new_path = list(current_path[1])
                    new_path.append(child)
                    heappush(paths, (self._f_value(child[1], len(new_path), heuristic), new_path))
        return  '[!] No solution found'
    
    def greedy_best_first_search(self, heuristic):
        paths = []
        heappush(paths, (self._heuristic(self.initial_state, heuristic),[[ 0, self.initial_state]]))
        self.frontier.append(self.initial_state)
        
        while len(paths):
            current_path = heappop(paths)
            current_state = current_path[1][-1][1]
            self.frontier.remove(current_state)
            self.explored.append(current_state)
            
            if self._goal_test(current_state):
                return  self._print_solution(current_path[1], self.explored)
            
            for child in self._get_children(current_state):
                if (child[1] not in self.explored) and (child[1] not in self.frontier):
                    self.frontier.append(child[1])
                    new_path = list(current_path[1])
                    new_path.append(child)
                    heappush(paths, (self._heuristic(child[1], heuristic), new_path))
        return  '[!] No solution found'
    
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
    
    def _f_value(self, input_state, current_path_length, heuristic):
        return current_path_length + self._heuristic(input_state, heuristic)
    
    def _heuristic(self, input_state, type_of_heuristic):
        # calculate the heuristic for current state
        if type_of_heuristic == 'Manhattan':
            distance_list = map(self._manhattan_distance, input_state, self.goal_state)
            return sum(distance_list)
        elif type_of_heuristic == 'Blank':
            print self.goal_state 
            print input_state
            misplaced_tiles = 0
            for x, y in zip(input_state, self.goal_state):
                if x != y:
                    misplaced_tiles += 1
            print misplaced_tiles
            return misplaced_tiles
            
        else:
            print '[!] Invalid Heuristic: ' + type_of_heuristic
            sys.exit()
    
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
        puzzle.depth_limited_dfs(int(algorithm_parameter))
    elif algorithm == 'ID':
        puzzle.iterative_deepening_search(int(algorithm_parameter))
    elif algorithm == 'A_Star':
        puzzle.a_star_search(algorithm_parameter)
    elif algorithm == 'Greedy':
        puzzle.greedy_best_first_search(algorithm_parameter)
    else:
        print '[!] Invalid Algorithm: ' + algorithm
        
        
