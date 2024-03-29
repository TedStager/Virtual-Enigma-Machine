# Virtual-Enigma-Machine
A program that encrypts and decrypts messages based on the mechanisms of the Enigma Machine. All programmed by Ted Stager.
NOTE: The GUI will only function properly on a Windows OS.

Instructions:

Welcome to the Virtual Enigma Machine. This program is designed to imitate the WW2-era German encryption device.

There are two areas you can change to alter the ciphertext that the machine outputs:

First are the rotors. These are the beating heart of the Enigma Machine, and are what do all the work in scrambling the letters. Each rotor swaps out the inputted letter for a different letter, and then passes the signal onto the next rotor, until it has gone through all three rotors, through the reflector*, and back through the rotors in reverse. The catch is, however, that these scramblers spin after each letter has been encoded (hence the name rotors), and thus have 26 starting positions. Not only does this allow two of the same letter to be different in the ciphertext (e.g. AA -> HS), but also creates a multitude (26^3) of starting positions. In order to decrypt a message, you need to put the machine back on the same rotor settings.

Second is the plugboard. This is an added source of complexity making the machine even harder to decrypt. You are allowed to make up to 10 connections on the plugboard, connecting one letter to another. What this does is when a key is pressed on the keyboard (or in this case entered in the text box), if it is connected to another letter it will swap it out for the letter it's connected to. Additionally, it also swaps out the outputted letter if it is connected to another letter. If a letter is unconnected on the plugboard it'll just stay the same.

*The reflector is a component that has all 26 letters in pairs, and swaps out the inputted letter for its paired letter, and sends it back through the rotors. It is key for having reciprocal encryption (i.e. if you input the ciphertext on the same machine on the same settings, it'll output the message you originally entered).
