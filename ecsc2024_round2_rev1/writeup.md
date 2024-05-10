# Summary
The binary takes a string in input and parse it as commands to move from a starting point inside a maze in which you can bounce on walls. At the end, it checks if the current position is (0, 0) and, if so, it gives the flag. 
For each 4 characters, it parses the first 2 as angle and the last 2 as length. 

The solve script is able to create the input string by playing the maze in an interactive way: by clicking inside the circle, you can move the current position. When you close the plot, you can se the generated string appearing on the console.
Because of roundings, I was not able to place the position correctly in (0, 0), so I created a bruteforce script to guess the len with the given right angle.

![Maze](images/maze.png)