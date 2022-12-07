'''
    Animated solution for the part 1 of Day 5 of the 2022 Advent of Code challenge.
    The problem can be found here: https://adventofcode.com/2022/day/5

    This time using a more realistic crane with a static arm and a hoist.
'''


import time
import os
import copy

# Color codes
OKGREEN = '\033[92m'
FAIL = '\033[91m'
OKCYAN = '\033[96m'
WARNING = '\033[93m'
BOLD = '\033[1m'
ENDC = '\033[0m'


mx = 15
delay = 0.09 # Delay in seconds between each frame, change this to make the animation faster or slower (/!\ too fast and your terminal may blink)
currentCol = 0
crates = []

# Update max height of drawing (if needed, to avoid resizing everytime)
def updateMax():
    global mx
    if mx - max([len(c) for c in crates]) < 6:
        mx = max([len(c) for c in crates])+8
    elif mx - max([len(c) for c in crates]) > 10:
        mx = max([len(c) for c in crates])+6

# Get height of heightest column in a range
def getLocalMax(b1, b2):
    if b1 > b2:
        b1, b2 = b2, b1
    return max([len(cr) for cr in crates[b1:b2+1]])

# Get height needed to go above the highest column in a range for a given column
def getNeededHeight(current, dest):
    return ((getLocalMax(current, dest))+2)-len(crates[current])

# Move crane claw vertically from ystart to ystop
def goVert(ystart, ystop, col, c):
    # Managing the direction of the movement
    for y in range(ystart, ystop+(-1 if ystart > ystop else 1), -1 if ystart > ystop else 1):
        showCrates(col, y, c)
        time.sleep(delay)

# Move crane claw horizontally from xstart to xstop
def goSlide(xstart, xstop, c):
    # Managing the direction of the movement
    for x in range(xstart, xstop+(-1 if xstart > xstop else 1), -1 if xstart > xstop else 1):
        # We need to stay at the height of the highest column in the range
        showCrates(x, (getLocalMax(xstart, xstop)+2)-len(crates[x])+1, c)
        time.sleep(delay)

# Execute an instruction, move nb crates from column fr to column to
def instruction(fr, nb, to):
    global currentCol
    global mx
    
    # If the crane is not already in the right column
    if fr != currentCol:
        # Go up
        goVert(2, getNeededHeight(currentCol, fr)+1, currentCol, ' ')
        # Slide to the right column
        goSlide(currentCol, fr, ' ')
        # Go Down
        goVert(getNeededHeight(fr, currentCol), 2, fr, ' ')
        
    # Main moving loop
    for i in range(nb):
        # Removing crate from column
        c = crates[fr].pop(0)
        # Go up with the picked crate
        goVert(2, getNeededHeight(fr, to)+1, fr, c)
        # Slide to the destination column
        goSlide(fr, to, c)
        # Go down with the crate
        goVert(getNeededHeight(to, fr), 2, to, c)
        
        # Inserting crate in destination column
        crates[to].insert(0, c)
        # Update max height because the columns have changed
        updateMax()

        currentCol = to
        
        # If there are still crates to move
        if nb > 1 and i < nb-1:
            # Go up
            goVert(2, getNeededHeight(to, fr)+1, to, ' ')
            # Slide to the fr column
            goSlide(to, fr, ' ')
            # Go down with the claw
            goVert(getNeededHeight(fr, to), 2, fr, ' ')
        
        
# Main drawing function to draw the crates and the crane giving it a column, a height and a held crate letter
def showCrates(x, y, letter):
    # Clearing the screen (works on linux and windows)
    # Comment it to see the animation step by step
    os.system('cls' if os.name == 'nt' else 'clear')
    tmpCrates = copy.deepcopy(crates)

    # Height of the highest column
    localMx = max([len(crate) for crate in crates])
    
    # Inserting spaces to make all columns the same height
    for c in tmpCrates:
        while len(c) < mx:
            c.insert(0, ' ')

    # Drawing
    # Rows
    for row in range(mx):
        print("", end='')
        # Columns
        for col in range(l):
            cratePile = tmpCrates[col]
            # Drawing every element
            if row == mx-localMx-5 and col > 0: # Top arm of the crane
                print(f"{WARNING}===={ENDC}", end='')
            elif row == mx-localMx-5 and col == 0: # Tip of the arm
                print(f"{WARNING}/=={ENDC}", end='')
            elif row == mx-localMx-4 and col == x: # Crane hoist
                print(f"{WARNING}\|/ {ENDC}", end='')
            elif row >= mx-localMx-3 and row < mx-len(crates[x])-y and col == x: # Cable
                print(f"{WARNING} |  {ENDC}", end='')
            elif row == mx-len(crates[x])-y and col == x: # Cable-claw thing
                print(f"{WARNING} A  {ENDC}", end='')
            elif row == mx-len(crates[x])-y+1 and col == x: # Claw with crate
                print(f"{WARNING}[{OKGREEN}{letter}{WARNING}]{ENDC} {ENDC}", end='')
            elif cratePile[row] != ' ': # Non-empty crates
                if row == mx-len(crates[col]): # Top crate
                    print(f"{OKGREEN}[{cratePile[row]}]{ENDC} ", end='')
                else: # Other crates
                    print("["+cratePile[row]+"] ", end='')
            else: # Empty crates
                print("    ", end='')
        
        # Drawing the crane
        if row >= mx-localMx-4:
            print(f"{WARNING}          ||   {ENDC}", end='')
        if row == mx-localMx-5:
            print(f"{WARNING}============\==-_{ENDC}", end='')
        print()
        print("  ", end='')

    # Drawing the column numbers
    for i in range(l):
        print(f" {BOLD}{str(i+1)}{ENDC}  ", end='')

    # Drawing the bottom of the crane
    print(f"      {WARNING}{BOLD}_/=[||]=\_{ENDC}  ", end='')
    print()
    print("  ", end='')

    # Drawing top crates of each column
    for i in range(l):
        if len(crates[i]) > 0:
            print(f"{OKCYAN}{BOLD}[{crates[i][0]}]{ENDC} ", end='')
        else:
            print(f"{FAIL}[/]{ENDC} ", end='')
    print()
    
        
# Opening the input file
with open("input.txt") as input_file:
    lines = input_file.readlines()

# Getting the number of columns
emptyLine = lines.index("\n")
l = max([len(line) for line in lines[:emptyLine+1]])//4

# Filing the crates columns
for col in range(1, l*4, 4):
    crates.append([])
    lin = 0
    # While we are not at the base of the column (aka a number)
    while not lines[lin][col].isnumeric():
        char = lines[lin][col]
        if char != ' ':
            crates[col//4].append(char)
        lin += 1

# Initializing the max height
updateMax()

# Getting the instructions
for line in lines[emptyLine+1:]:
    words = line.split(' ')
    instruction(int(words[3])-1, int(words[1]), int(words[5])-1)

# Printing the final result, updating with the last move
showCrates(currentCol, 2, ' ')

# Printing the result
res = ""
for crate in crates:
    res += crate[0]

print()
print(f"{BOLD}              > {res} <{ENDC}")
print()


                          