The game is known as a sliding puzzle.
Gameplay link:
https://youtu.be/4zHPDZ5pwa8

The player will be able to choose a image and the image will be sliced up and put into different tiles.

The tiles will then be shuffled.

In order to win the game, the player has to reorganise the tiles by clicking them and rearranging them such that the final tile positions will form the original image selected.

A link on strategies to solve the puzzle: 
https://www.youtube.com/watch?v=NXRIrP1k4dE&

*Describe your code*
In the code, there are three different screens:

The first screen will load a file selection tool, where the player will be able to choose an image they want. The image at the side will load whichever picture the player chooses.
It uses a BoxLayout horizontally to display the file selection tool, the chosen image and the button to bring the player to the next screen.

The second screen will display the chosen image from the first screen. A 'back' button is available if the player wants to choose another picture.
The purpose of this screen is to call the function to upon clicking and releasing the "Scramble" button. It will also bring the player over to the game screen.

The third screen is the game screen and will be for the player to rearrange the puzzle. Once done, click the 'solve' button and the game will tell if you have won as well as the score.
Tiles are initialised but the background_normal has not, thus the player will need to click show scrambled image to view the puzzle. The buttons are programmed with behavior such that they will only move towards the direction of a blank tile. If a blank tile is not present or if the tile is at the edge, it will not move towards outside the game zone. The coordinates of the tile is constantly tracked and each instance of button-pressing will increase the score for the player. The lower the score, the better. The player can always click the 'original image' button to refer to the previous screen for the chosen image. A 'close and delete' button is at the top right-hand-corner to let the player close the game after deleting the images slices created in the 'scramble' button. This clears up disk space and does not clutter the root directory. *remember to click 'close and delete' if not the sliced images will remain and you will have to delete them yourself*

First Screen:
'Go!' --> Brings you to the next screen to confirm your selection of image

Second Screen:
'Choose another picture' --> Sends you back to the previous screen for you to choose another image
'Scramble' --> initialises the resizing and slicing of images; resized and sliced images will be stored in the same directory as main.py

Third Screen:
'Original Image' --> Brings you back to the previous for you to refer to original image chosen
'Solve' --> Displays whether you have solved the puzzle or not, and returns you your score if you have.
'Show scrambled image' --> Initialises the tiles with the scrambled images
'Close and Delete' --> Deletes the resized and sliced images within the directory and closes the kivy window.

This game uses a coordinate guide to determine if the tiles are in their correct positions. Window size is also not changeable to allow player to click quickly and more efficiently. 

Three sample images are given in the root file directory. 


Have fun solving!

