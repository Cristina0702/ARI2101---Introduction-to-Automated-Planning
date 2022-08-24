#!/usr/bin/env python
# coding: utf-8

# In[1]:


import heapq as hq # Heap used to represent priority queue
import copy
from time import perf_counter
from collections import deque

def calc_misplaced_tiles(state, goal):
    # Calculating the number of misplaced tiles whilst ignoring 0.
    # Flattening the list of lists for easy comparison
    state = [item for sublist in state for item in sublist]
    goal = [item for sublist in goal for item in sublist]
    
    count = 0
    
    for i in range(0, len(goal)):
        if state[i] == 0:
            continue
        if (state[i] != goal[i]):
            count += 1
            
    return count

def calc_manhattan_dist(state, goal):
    dist = []

    for i in range(0, len(state)):
        for j in range(0, len(state[i])):
            if (state[i][j] == goal[i][j]):
                continue
                
            if (state[i][j] == 0):
                continue
            
            else:
                # Finding where this tile is in the goal state
                i_of_goal_tile, j_of_goal_tile = find_in_sublists(state[i][j], goal)
                
                distance = abs(i - i_of_goal_tile) + abs(j - j_of_goal_tile)
                dist.append(distance)
    
    return sum(dist)

def check_states_equal(state_a, state_b):
    # Checking if the given two states are equal.
    # Flattening the list of lists for easy comparison
    flat_list_a = [item for sublist in state_a for item in sublist]
    flat_list_b = [item for sublist in state_b for item in sublist]
    
    return flat_list_a == flat_list_b


def find_in_sublists(val, lst):
    # Finding the given value in a list of lists
    for i, sub_list in enumerate(lst):
        try:
            j = sub_list.index(val)
        except ValueError:
            continue
        return i, j
            
    return None, None


class Node:
    # Creating node class
    def __init__(self,prog, parent=None, state=0):
        # Initialising node variables
        self.prog=prog
        self.parent = parent
        self.state = state
        if prog != 2:
            self.cost_from_start = 0
            self.cost_to_goal = 0
        self.children = []
        
    def __eq__(self, other):
        #comparing the given nodes
        return self.state == other.state
    
    def __lt__(self, other): 
        # This is a very vital function as it decides how the f-value of each search algorithm is calculated
        if(self.prog==2):
            # Doesn't use f-value
            return 0
        elif(self.prog==0): 
            # Calculate the f-val = g(n) + h(n)
            return (self.cost_from_start + self.cost_to_goal) < (other.cost_from_start + other.cost_to_goal)
        elif(self.prog==1):
            # Calculate the f-val = h(n) 
            return (self.cost_to_goal) < (other.cost_to_goal)
        elif(self.prog==3):
            ## Calculate the f-val = g(n) + h(n)
            return (self.cost_from_start + self.cost_to_goal) < (other.cost_from_start + other.cost_to_goal)
        
    def add_child(self, node, cost_to_expand=1):
        # Adds a child node to the list of this node's children
        if(self.prog !=2 and self.prog !=3):
            # Extending the child's cost from start to goal
            node.cost_from_start = self.cost_from_start + cost_to_expand 
        # Setting the node's parent
        node.parent = self
        # Appending the node to the current node's children array
        self.children.append(node)
        
    def get_f_val(self):
        # Returning the cost from start and the cost to goal
        return (self.cost_from_start + self.cost_to_goal)
    
    def traceback(self):
        # Traversing all parents to display the nodes of the valid plan
        print(self.state)
        
        forValidation = []
        forValidation.append(self.state)
        
        p = self.parent
        count = 1
        
        while p:
            count += 1
            print(p.state)
            forValidation.append(p.state)
            p = p.parent
            
        print(str(count) + " nodes traced.\n")
        
        # Calling the validation function to perform validation on final plan moves
        validation(forValidation, count)
        
    def print_state(self):
        # Printing the node
        for i in self.state:
            print(i)
        
    def expand(self):
        # Performing the up, down , left and right moves from the given state and returning the list of moves
        
        # Finding the index of the 0 value in the state
        i_zero, j_zero = find_in_sublists(0, self.state)
        
        state_len = len(self.state)
        
        states_to_return = []
        
        # Move Up: Swapping zero with the element above it if such element exists
        if (i_zero != 0):
            tmp_state = copy.deepcopy(self.state)
            tmp_state[i_zero][j_zero] = tmp_state[i_zero - 1][j_zero]
            tmp_state[i_zero - 1][j_zero] = 0
            
            # Add only if the parent does not have the same expanded state
            if self.parent and check_states_equal(tmp_state, self.parent.state):
                states_to_return.append(None) 
            else:
                states_to_return.append(tmp_state)
        
        # Move Right: Swapping zero with the element on its right if possible
        if (j_zero != (state_len - 1)):
            tmp_state = copy.deepcopy(self.state)
            tmp_state[i_zero][j_zero] = tmp_state[i_zero][j_zero + 1]
            tmp_state[i_zero][j_zero + 1] = 0
            
            # Add only if the parent does not have the same expanded state
            if self.parent and check_states_equal(tmp_state, self.parent.state):
                states_to_return.append(None) 
            else:
                states_to_return.append(tmp_state)
                
        # Move Down: Swapping zero with the element below it if possible
        if (i_zero != (state_len - 1)):
            tmp_state = copy.deepcopy(self.state)
            tmp_state[i_zero][j_zero] = tmp_state[i_zero + 1][j_zero]
            tmp_state[i_zero + 1][j_zero] = 0
            
            # Add only if the parent does not have the same expanded state
            if self.parent and check_states_equal(tmp_state, self.parent.state):
                states_to_return.append(None) 
            else:
                states_to_return.append(tmp_state)
        
        # Move Left: Swapping zero with the element on its left if possible
        if (j_zero != 0):
            tmp_state = copy.deepcopy(self.state)
            tmp_state[i_zero][j_zero] = tmp_state[i_zero][j_zero - 1]
            tmp_state[i_zero][j_zero - 1] = 0
            
            # Add only if the parent does not have the same expanded state
            if self.parent and check_states_equal(tmp_state, self.parent.state):
                states_to_return.append(None)
            else:
                states_to_return.append(tmp_state)
            
        return states_to_return

def validation(forValidation, count):
    # Function to check that all moves from the plan were valid
    print("\nValidating plan:\n")
    
    # Setting index to be count-1 to start from the initial state and loop till the goal state
    index = count-1
    while(index > 0):
        
        # Getting the indexes of the 0 node from both states
        i_zero, j_zero = find_in_sublists(0, forValidation[index])
        i_zero2, j_zero2 = find_in_sublists(0, forValidation[index-1])

        if(i_zero == i_zero2 and (j_zero == j_zero2+1 or j_zero == j_zero2-1)):
            # Checking to see if 0 was moved left or right
            print(forValidation[index], "--> ", forValidation[index-1], " is Valid.\n")
        elif(j_zero == j_zero2 and (i_zero == i_zero2+1 or i_zero == i_zero2-1)):
            # Checking to see if 0 was moved up or down
            print(forValidation[index], "--> ", forValidation[index-1], " is Valid.\n")
        else:
            # Otherwise move was not valid
            print(forValidation[index], "--> ", forValidation[index-1], " is not Valid.\n")

        index = index - 1
            
def tree_search(start_state, goal_state, heuristic, prog):
    root = Node(state=start_state,prog=(int(prog)))
    
    # Used as a heapq
    h = [] 
    hq.heappush(h, root)
    explored = []
    
    max_nodes = 1
    expanded = 0
    
    # Looping whilst heapq is not empty
    while h:
        max_nodes = max(len(h), max_nodes)
        
        current = hq.heappop(h)
        
        print("\nThe best state to expand with g(n) = " + str(int(current.cost_from_start))
                  + " and h(n) = " + str(int(current.cost_to_goal)) + " is...")
        current.print_state()
        
        # Calling traceback function if states are equal
        if (check_states_equal(current.state, goal_state)):
            print("\nFound a solution!")
            print("Traceback:")
            current.traceback()
            print("To solve this problem the search algorithm expanded a total of " + str(expanded) + " nodes.") 
            print("The maximum number of nodes in the queue at any one time: " + str(max_nodes))
            
            return expanded, max_nodes
        
        else:
            # Appending the current state to the explored array
            explored.append(current)
            
            # Filtering out the none states
            expanded_states_list = [non_none_state for non_none_state in current.expand() if non_none_state]
            
            # If expanded_states_list is empty after we filter all none, continue
            if expanded_states_list == []:
                continue
            
            for expanded_state in expanded_states_list:
                new_node = Node(state=expanded_state,prog=(int(prog)))

                # If h is not empty and new_node already exists in h or
                # If explored is not empty and new_node already exists in explored, continue
                if ((h and new_node in h) or (explored and new_node in explored)):
                    # already seen
                    continue

                # Calling the functions to calculate costs depending on the heuristic 
                if (heuristic == "misplaced"):
                    new_node.cost_to_goal = calc_misplaced_tiles(new_node.state, goal_state)

                if (heuristic == "manhattan"):
                    new_node.cost_to_goal = calc_manhattan_dist(new_node.state, goal_state)
                
                # Adding the new_node as the current's child node
                current.add_child(node=new_node)
                # Pushing the new_node in h
                hq.heappush(h, new_node)
        
            expanded += 1
        
    print("Couldn't find a solution :(")            
    return -1


def enf_hill_climb_search(start_state, goal_state, heuristic, prog):
    root = Node(state=start_state, prog=(int(prog)))
    
    explored = []
    
    # Using deque as it is faster than list
    h = deque()
    h.append(root)
    
    max_nodes = 1
    expanded = 0
    
    # Looping whilst heapq is not empty
    while h:
        
        max_nodes = max(len(h), max_nodes)
        
        current = h.popleft()
        
        # Calling traceback function if states are equal
        if (check_states_equal(current.state, goal_state)):
            print("\nFound a solution!")
            print("Traceback:")
            current.traceback()
            print("To solve this problem the search algorithm expanded a total of " + str(expanded) + " nodes.") 
            print("The maximum number of nodes in the queue at any one time: " + str(max_nodes))
            
            return expanded, max_nodes
        
        else:
            # Compare states with their heursitics
            explored.append(current)
            
            # Filter out None states
            expanded_states_list = [non_none_state for non_none_state in current.expand() if non_none_state]

            # If expanded_states_list is empty after we filter all none, continue
            if expanded_states_list == []:
                continue

            for expanded_state in expanded_states_list:
                new_node = Node(state=expanded_state,prog=(int(prog)))

                # If h is not empty and new_node already exists in h or
                # If explored is not empty and new_node already exists in explored, continue
                if ((h and new_node in h) or (explored and new_node in explored)):
                    # already seen
                    continue

                # Calling the functions to calculate costs depending on the heuristic 
                if (heuristic == "misplaced"):
                    new_node.cost_to_goal = calc_misplaced_tiles(new_node.state, goal_state)
                
                if (heuristic == "manhattan"):
                    new_node.cost_to_goal = calc_manhattan_dist(new_node.state, goal_state)
            
                # Calling Breadth First Search to expand the state
                if not ((h and new_node in h) or (explored and new_node in explored)):
                    current.add_child(node=new_node)
                    h.append(new_node)
                
                # Comparing f-values of the current and new_node to expand the best one
                if(current.get_f_val()>=new_node.get_f_val()):
                    h.clear()
                    current.add_child(node=new_node)
                    h.append(new_node)
                    break
                else:
                    current.add_child(node=new_node)
                    h.append(new_node)

            expanded += 1
        
    print("Couldn't find a solution :(")            
    return -1

def bts_search(start_state, goal_state, prog):
    root = Node(state=start_state, prog=(int(prog)))

    explored = []
    
    # Using deque as it is faster than list
    h = deque()
    
    h.append(root)
    explored.append(root)
    
    max_nodes = 1
    expanded = 0
    
    # Looping whilst heapq is not empty
    while h:
        max_nodes = max(len(h), max_nodes)
        
        current = h.popleft()
        
        # Calling traceback function if states are equal
        if (check_states_equal(current.state, goal_state)):
            print("\nFound a solution!")
            print("Traceback:")
            current.traceback()
            print("To solve this problem the search algorithm expanded a total of " + str(expanded) + " nodes.") 
            print("The maximum number of nodes in the queue at any one time: " + str(max_nodes))
            
            return expanded, max_nodes
        
        else:
            explored.append(current)
            
            # Filtering out the none states
            expanded_states_list = [non_none_state for non_none_state in current.expand() if non_none_state]
            
            # If expanded_states_list is empty after we filter all none, continue
            if expanded_states_list == []:
                continue
        
            for expanded_state in expanded_states_list:
                new_node = Node(state=expanded_state, prog=(int(prog)))

                # If h is not empty and new_node already exists in h or
                # If explored is not empty and new_node already exists in explored, continue
                if not ((h and new_node in h) or (explored and new_node in explored)):
                    current.add_child(node=new_node)
                    h.append(new_node)
        
            expanded += 1
        
    print("Couldn't find a solution :(")            
    return -1


def get_algorithm():
    # Displaying the hueristic options
    
    print("Select algorithm:\n"
          + " 1  Misplaced Tile Heuristic" + "\n"
          + " 2  Manhattan Distance Heuristic" + "\n"
         )
    
    alg_input_dict = {
                "1": ("misplaced", "Misplaced Tile Heuristic"),
                "2": ("manhattan", "Manhattan Distance Heuristic"),
            }
    
    while True:
        try:
            selection = input() or str(len(alg_input_dict))
            
            if (int(selection) < 1) or (int(selection) > len(alg_input_dict)):
                print("Error: input " + selection + " is not within range.\n")
                raise ValueError
            
            break
        except(ValueError):
            print("Error: please input a number in the valid range or press enter for default!")
        
    print("Selected " + alg_input_dict[selection][1])
    
    return alg_input_dict[selection][0]

    
def init_default_puzzle():
    # Displaying the puzzle options
    
    puzzle_list = [
        ("Example 1", [[8, 6, 7], [2, 5, 4], [3, 0, 1]]),
        ("Example 2", [[1, 2, 3], [8, 4, 6], [7, 5, 0]]),
        ("Example 3", [[6, 4, 7], [8, 5, 0], [3, 2, 1]]),
    ]
    
    list_len = len(puzzle_list)

    print("Choose default puzzle: (1 to " + str(list_len) + "):\n")
    
    # Looping to display the puzzle options
    print("[1] " + puzzle_list[0][0])
    for i in range(1, len(puzzle_list)):
        print(" " + str(i + 1) + "  " + puzzle_list[i][0])
    
    while True:
        try:
            selected_example = int(input() or 1)

            if ((selected_example < 1) or (selected_example > list_len)):
                print("Error: input " + str(selected_example) + " is not within range.\n")
                raise ValueError

            break
        except(ValueError):
            print("Error: please input a number or press enter for default!")

    print("Selected " + puzzle_list[selected_example - 1][0] + "\n")
    return puzzle_list[selected_example - 1][1]


def main():
    print("Welcome to 8-puzzle solver.")
    print("Default 3x3 puzzle" + "\n")
    
    # Initialising goal state
    init_state = []
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    
    init_state = init_default_puzzle()
    
    # Getting user input for Algorithm
    prog = input("Choose which Search you want to use \n"  + "0 : Astar\n" +"1 : For Greedy Best First Search \n"+"2 : Breadth First Search\n" + "3 : Enforced Hill Climbing \n ")
    
    # Calling algorithm functions for choosen function and starting the time function
    if(prog=="1" or prog=="0"):
        alg = get_algorithm()
        t1_start = perf_counter()
        tree_search(init_state, goal_state, alg, prog)
    elif(prog=="2"):
        print("\nSelected Breadth First Search\n")
        t1_start = perf_counter()
        bts_search(init_state, goal_state, prog)
    elif(prog=="3"):
        alg = get_algorithm()
        t1_start = perf_counter()
        enf_hill_climb_search(init_state, goal_state, alg, prog)
     
    # Stoping the time function and displaying the time
    t1_stop = perf_counter()
    ms = (t1_stop - t1_start)
    print("--- %s seconds ---" % ms)
        
    return


# In[3]:


main() #Figure 3 A* Manhattan


# In[4]:


main()#Figure 4 A* Manhattan


# In[5]:


main() #Figure 3 Greedy Misplaced


# In[6]:


main() #Figure 3 Greedy Manhattan


# In[7]:


main() #Figure 4 Greedy Misplaced


# In[8]:


main() #Figure 4 Greedy Manhattan


# In[9]:


main() #Example 2 Breadth First Search


# In[4]:


main() # Figure 3 A star Misplaced Tiles


# In[3]:


main() #Figure 4 A star Misplaced Tiles


# In[2]:


main() #Figure 4 Breadth First Search


# In[2]:


main() #Figure 3 Enf Hill Climbing Manhattan


# In[3]:


main() #Figure 4 Enf Hill Climbing Manhattan


# In[4]:


main() #Figure 3 Enf Hill Climbing Misplaced


# In[5]:


main() #Figure 4 Enf Hill Climbing Misplaced


# In[2]:


main() #Figure 3 Breadth First Search


# In[ ]:




