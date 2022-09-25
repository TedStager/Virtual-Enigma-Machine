# Virtual Enigma Machine
# Ted Stager
# Will emulate the German encryption device

#Import statements (using tkinter for the GUI)
import tkinter as tk 
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

# ============================ CODE FOR THE ENIGMA MACHINE ==============================

# 3 dimensional array for the rotors: 3 rotors, which each have 26 pairs of letters
rotors = [[['a', 'j'], ['b', 'g'], ['c', 'd'], ['d', 'q'], ['e', 'o'], ['f', 'x'], ['g', 'u'], ['h', 's'], ['i', 'c'], ['j', 'a'], ['k', 'm'], ['l', 'i'], ['m', 'f'], ['n', 'r'], ['o', 'v'], ['p', 't'], ['q', 'p'], ['r', 'n'], ['s', 'e'], ['t', 'w'], ['u', 'k'], ['v', 'b'], ['w', 'l'], ['x', 'z'], ['y', 'y'], ['z', 'h']],
          [['a', 'n'], ['b', 't'], ['c', 'z'], ['d', 'p'], ['e', 's'], ['f', 'f'], ['g', 'b'], ['h', 'o'], ['i', 'k'], ['j', 'm'], ['k', 'w'], ['l', 'r'], ['m', 'c'], ['n', 'j'], ['o', 'd'], ['p', 'i'], ['q', 'v'], ['r', 'l'], ['s', 'a'], ['t', 'e'], ['u', 'y'], ['v', 'u'], ['w', 'x'], ['x', 'h'], ['y', 'g'], ['z', 'q']],
          [['a', 'j'], ['b', 'v'], ['c', 'i'], ['d', 'u'], ['e', 'b'], ['f', 'h'], ['g', 't'], ['h', 'c'], ['i', 'd'], ['j', 'y'], ['k', 'a'], ['l', 'k'], ['m', 'e'], ['n', 'q'], ['o', 'z'], ['p', 'p'], ['q', 'o'], ['r', 's'], ['s', 'g'], ['t', 'x'], ['u', 'n'], ['v', 'r'], ['w', 'm'], ['x', 'w'], ['y', 'f'], ['z', 'l']]]

# Copy of the above array to ensure that when we shift the letters, we're always shifting them from the same spot
baseRotors = [[['a', 'j'], ['b', 'g'], ['c', 'd'], ['d', 'q'], ['e', 'o'], ['f', 'x'], ['g', 'u'], ['h', 's'], ['i', 'c'], ['j', 'a'], ['k', 'm'], ['l', 'i'], ['m', 'f'], ['n', 'r'], ['o', 'v'], ['p', 't'], ['q', 'p'], ['r', 'n'], ['s', 'e'], ['t', 'w'], ['u', 'k'], ['v', 'b'], ['w', 'l'], ['x', 'z'], ['y', 'y'], ['z', 'h']],
              [['a', 'n'], ['b', 't'], ['c', 'z'], ['d', 'p'], ['e', 's'], ['f', 'f'], ['g', 'b'], ['h', 'o'], ['i', 'k'], ['j', 'm'], ['k', 'w'], ['l', 'r'], ['m', 'c'], ['n', 'j'], ['o', 'd'], ['p', 'i'], ['q', 'v'], ['r', 'l'], ['s', 'a'], ['t', 'e'], ['u', 'y'], ['v', 'u'], ['w', 'x'], ['x', 'h'], ['y', 'g'], ['z', 'q']],
              [['a', 'j'], ['b', 'v'], ['c', 'i'], ['d', 'u'], ['e', 'b'], ['f', 'h'], ['g', 't'], ['h', 'c'], ['i', 'd'], ['j', 'y'], ['k', 'a'], ['l', 'k'], ['m', 'e'], ['n', 'q'], ['o', 'z'], ['p', 'p'], ['q', 'o'], ['r', 's'], ['s', 'g'], ['t', 'x'], ['u', 'n'], ['v', 'r'], ['w', 'm'], ['x', 'w'], ['y', 'f'], ['z', 'l']]]

# Lists for the connected letters on the plugboard
plugboard = [['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', '']]

# Lists for the reflector (13 pairs of letters) and the rotor positions
reflector = [('a', 'b'), ('c', 'd'), ('e', 'f'), ('g', 'h'), ('i', 'j'), ('k', 'l'), ('m', 'n'), ('o', 'p'), ('q', 'r'), ('s', 't'), ('u', 'v'), ('w', 'x'), ('y', 'z')]
rotorPos = [0, 0, 0]

# Function to encode a single character through a single rotor
def rotorEncode(c, R):
    rotor = rotors[R-1]
    
    # Goes through every letter until it finds the right input (left letter in the pair), then gives the output of that letter (right letter)
    for x in range(26):
        if rotor[x][0] == c:
            rotorOut = rotor[x][1]
            break            
    return rotorOut

# Does the exact same thing as rotorEncode, but in reverse (takes in the right letter in the pair and outputs the left)
def rotorEncodeInv(c, R):
    rotor = rotors[R-1]
    
    for x in range(26):
        if rotor[x][1] == c:
            rotorOut = rotor[x][0]
            break
    return rotorOut

# Updates the rotor positions
# Programmed like hands on a clock, once the first rotor hits 26, it'll go back to 0 and the next will increase by 1
def rotorSpin():
    global rotorPos
    
    rotorPos[2] += 1
    if rotorPos[2] == 26:
        rotorPos[1] += 1
        rotorPos[2] = 0
    if rotorPos[1] == 26:
        rotorPos[0] += 1
        rotorPos[1] = 0
    if rotorPos[0] == 26:
        rotorPos = [0, 0, 0]
    
    # This is written as a separate function because it is also necessary to call this at the beginning of the program
    accountForSpin()

# Shifts all the letters down accordingly
def accountForSpin():
    global rotors
    # Nested for loop, we go through every pair in each rotor
    for x in range(3):
        for y in range(26):
            # This block essentially turns a letter into its corresponding number, adding the shift, and turns it back into a letter
            shift = rotorPos[x]
            num = ord(baseRotors[x][y][0]) # Note that we always use the same base to make sure that the shift is uniform
            shifted = num + shift
            if shifted > 122: shifted -= 26
            rotors[x][y][0] = chr(shifted)

# The reflecter pairs of letters, and turns them into each other to be sent back into the rotors in retrograde
# This ensures that if put on the same settings, the ciphertext will output the plaintext
def reflect(c):
    for x in range(13):
        if reflector[x][0] == c:
            return reflector[x][1]
        elif reflector[x][1] == c:
            return reflector[x][0]

# If the letter is connected to anything on the plugboard, it'll swap it for the one it's connected to
def plugboardPass(c):
    for x in range(10):
        if plugboard[x][0] == c:
            return plugboard[x][1]
        elif plugboard[x][1] == c:
            return plugboard[x][0]
    return c

# Puts all of the above together, and encodes a full string 
def enigmaEncode(s):
    s = s.lower()
    result = ""
    accountForSpin()
    for x in range(len(s)):
        c = s[x]
        letter = False
        # Checking to see if it's a letter or not
        for y in range(26):
            if c == baseRotors[0][y][0]: #Using the base rotors for the alphabet
                letter = True
                break
        if letter == False:
            result = result + c
            continue
        
        # Sending the letter through the machine
        c = plugboardPass(c)
        c = rotorEncode(c, 1)
        c = rotorEncode(c, 2)
        c = rotorEncode(c, 3)
        c = reflect(c)
        c = rotorEncodeInv(c, 3)
        c = rotorEncodeInv(c, 2)
        c = rotorEncodeInv(c, 1)
        c = plugboardPass(c)
        rotorSpin()
        
        # Adding the encoded letter onto the result string
        result = result + c

    return result.upper()

# ============================= CODE FOR THE GUI =============================

# Declaring the functions that the buttons will trigger

# This function will pair two letters off on the plugboard
def pair():
    # Checks if we have an empty slot for a connection
    emptyPair = -1
    for x in range(10):
        if plugboard[x] == ['', '']:
            emptyPair = x
            break
    if emptyPair == -1:
        msgbox.showinfo('Connections Full', 'Oops, you seem to have already used all 10 connections.\nTry clearing the plugboard.')
        return

    # Checks if the letters that are in the comboboxes have already been used
    letterI = comboPlugboardI.get()
    letterII = comboPlugboardII.get()
    for x in range(10):
        for y in range(2):
            if plugboard[x][y] == letterI.lower() or plugboard[x][y] == letterII.lower():
                msgbox.showinfo('Letter Already Used', 'Oops, you\'ve already used one of those letters.\nTry using different letters or clearing the plugboard.')
                return
    
    # Checks if the letters are the same
    if letterI == letterII:
        msgbox.showinfo('Letter Paired With Itself', 'Oops, you can\'t pair a letter to itself.')
        return
    
    # Assigning the letters to the plugboard and the Connections label
    plugboard[emptyPair][0] = letterI.lower()
    plugboard[emptyPair][1] = letterII.lower()
    paired = letterI + letterII
    
    # Displaying the connection on the window
    labelTextCurrent = labelConnections.cget('text')
    newlabelText = labelTextCurrent.replace('--', paired, 1)
    labelConnections.configure(text=newlabelText)
    

# This function clears the plugboard
def clear():
    #Clears the list for the connections
    for x in range(10):
        plugboard[x] = ['', '']
    
    #Clears the label for the connections
    labelConnections.configure(text='Connections\n --  -- \n --  -- \n --  -- \n --  -- \n --  -- ')

# This function encodes whatever is in the entry box, and outputs the ciphertext
def encode():
    rotorPos[0] = int(comboRotorI.get())
    rotorPos[1] = int(comboRotorII.get())
    rotorPos[2] = int(comboRotorIII.get())
    
    plaintext = textboxInput.get()
    ciphertext = enigmaEncode(plaintext)

    # In order to insert the text into the output textbox, we need to set it off of readonly, delete what's inside and insert the text, then put it back on readonly    
    textboxOutput.configure(state='normal')
    boxtext = textboxOutput.get()
    textboxOutput.delete(0, len(boxtext))
    textboxOutput.insert(0, ciphertext)
    textboxOutput.configure(state='readonly')
    
# This function brings up the help window
def helpBox():
    helpFile = open('Instructions.txt', 'r') # I wrote the help guide in a .txt file because I didn't want a really long string literal
    instructions = helpFile.read()
    helpFile.close()
    
    msgbox.showinfo('Help', instructions)


# Setting up the basic layout of the GUI
# Setting up the window
root = tk.Tk()
root.geometry('500x400')
root.title("Virtual Enigma Machine")
root.iconbitmap('typewriter.ico') # Adding a little typewriter icon instead of the default feather

# Rotor setting labels and options
comboRotorI = ttk.Combobox(root, width=4, state="readonly")
comboRotorI['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26)
comboRotorI.grid(column=0, row=1)
comboRotorI.current(0)

comboRotorII = ttk.Combobox(root, width=4, state="readonly")
comboRotorII['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26)
comboRotorII.grid(column=0, row=3)
comboRotorII.current(0)

comboRotorIII = ttk.Combobox(root, width=4, state="readonly")
comboRotorIII['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26)
comboRotorIII.grid(column=0, row=5)
comboRotorIII.current(0)

labelRotorI = tk.Label(root, text="Rotor I Setting")
labelRotorI.grid(column=0, row=0)

labelRotorII = tk.Label(root, text="Rotor II Setting")
labelRotorII.grid(column=0, row=2)

labelRotorIII = tk.Label(root, text="Rotor III Setting")
labelRotorIII.grid(column=0, row=4)

# Plugboard settings
labelPlugboard = tk.Label(root, text='\nPlugboard Settings')
labelPlugboard.grid(column=0, row=6, pady=10)

comboPlugboardI = ttk.Combobox(root, width=4, state="readonly")
comboPlugboardI['values'] = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
comboPlugboardI.grid(column=0, row=7)
comboPlugboardI.current(0)

comboPlugboardII = ttk.Combobox(root, width=4, state="readonly")
comboPlugboardII['values'] = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
comboPlugboardII.grid(column=0, row=8)
comboPlugboardII.current(1)

buttonPair = tk.Button(root, text=' Pair ', command=pair)
buttonPair.grid(column=1, row=7, padx=10)

buttonClear = tk.Button(root, text='Clear', command=clear)
buttonClear.grid(column=1, row=8, padx=10)

labelConnections = tk.Label(root, text='Connections\n --  -- \n --  -- \n --  -- \n --  -- \n --  -- ')
labelConnections.grid(column=0, row=9, pady=10)

# Input and ouput boxes
textboxInput = tk.Entry(root, width=40)
textboxInput.grid(column=3, row=4, padx=50)

labelInput = tk.Label(root, text='Input')
labelInput.grid(row=3, column=3)

labelOutput = tk.Label(root, text='Output')
labelOutput.grid(column=3, row=8)

textboxOutput = tk.Entry(root, width=40, state='readonly')
textboxOutput.grid(column=3, row=7)

buttonEncode = tk.Button(root, text='Encode', command=encode)
buttonEncode.grid(column=3, row=6)
              
buttonHelp = tk.Button(root, text='Help', command=helpBox)
buttonHelp.grid(column=3, row=10, sticky='E', padx=20, pady=10)


# Running the loop on the window so that it won't immediately close
root.mainloop()