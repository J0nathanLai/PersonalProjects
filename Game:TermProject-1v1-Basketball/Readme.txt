Readme File
TP - 1v1 Basketball 
by Jonathan Lai (jklai)


Project Description:
This term project is a 1v1 basketball game involving NBA players with realistic attributes similar to their playstyles. One user will play against the AI in a game of 21 points. And the player can select the player they’re controlling and the opposing AI player. Both players can shoot 3-pointers, midrange 2-pointers, layups, dribble past their opponent, and steal the ball from their opponent. There is also a power indicator for jump shots to assist the user with shooting the ball. The probability of performing a move (e.g. making a shot, stealing, dribbling past) depends on the user’s input and the chosen NBA player’s attribute; so if the user shoots the ball and doesn’t get close to the basket, then it will result in a miss; if the user shoots the ball and gets close to the basket, the probability of making the basket depends on a randomly generated number being smaller than an arbitrary threshold for that shot type. 


How to run the project and other modules and libraries:
In the zip file, there will be a bunch of images for the project and the code in a .py file type. To set up, download cmu_graphics from this website https://academy.cs.cmu.edu/desktop. Make sure you place the images and the cmu_graphics folder from the dowloa in the same location as your code file on your computer (e.g. if you placed the code file on your desktop, make sure you place the images and the cmu_graphics folder on your desktop too). Then, at the beginning of the code file, ensure you have the line “from cmu_graphics import *”. 


To access the images in the zip file and import it into the code, first import the module image from the library PIL by writing “from PIL import image” after the cmu_graphics import line. Then also import the modules os, and pathlib by writing “import os, pathlib”. Then, to open the images, we use the line “Image.open(os.path.join(pathlib.Path(__file__).parent,{filename}))” and put the image’s file name in the curly brackets. Lastly, since we are using cmu_graphics, we have to convert the image into a CMU image by using “CMUImage({image_varaible_name})”. 


Lastly, “import random” for the probabilities used in calculating the probability of success of the players’ moves. 


Shortcuts & Commands:
For instructions on the gameplay, press “i” in the menu/player selection screen. Use the arrow keys to choose your players. Then press “enter” or “return” to start the gameplay. Inside the game, you can press “i” to pause the game. Or you can press “escape” or “esc” to leave the game and will not save your game progress. To start a new game simply press “enter” again at the menu screen.