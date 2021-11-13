# MOONBOARD DATASET

This repo contains the code that I developed for creating a dataset that contains all the problems from the moonobard app.

I developed this code because the original dataset is private and I couldn't use properly my moonboard LED controller that I developed withan STM32. Other related project to this are:

- [STM32 project](https://github.com/AlessandroAvi/Moonboard_LED_DIY) for controlling LED lights through manual keypad or bluetooth connection to the my custom Moonboard app (FishBoard)
- [Android app](https://github.com/AlessandroAvi/Moonboard_Android_App) that can be used to filter the moonboard problems (dataset created from this repo), visualize them on the screen and later send the most relevant information via bluetooth to the STM32 microcontroller

## IDEA 

The code is based on application of basic computer vision concept on screenshots of the moonboard app. The idea is to take a screenshot for every single moonboard problem and then use OpenCV for the extraction of the main informations of the problem. 

In order to detect the holds used from the boulder three masks are created, where each mask is just the original image but where only the red/green/blue pixels are maintained (red=top hold, blue=middle hold, green=start hold). This creates three black and white images where the circles are well distincted from the background. Once these image are obtained is immediate to apply a circle detector which is able to find the x,y coordinates of the centers of the circle. These coordinates are then associated to the closest real hold.

After that also some text recognition is applied in order to store also the name and grade of the boulder problem.

Everything is then stored in a JSON file (holds used, type of hold, problem name, problem grade, benckmark, problem ID->just a number reppresenting the n-th boulder).

The procedure has to be performed on a computer, where an Android simulator with the monnboard app is visible on the screen. The script will catch a portion of the screen (to be defined manually), take a screenshot, detect the holds, detect name and grade, store the informations inside the JSON, automatically move the mouse to move to the next problem.

Currently the JSON file on thsi repo only contains the problemswith black holds (because my moonboard panel only has those holds).

 ![name-of-you-image](https://github.com/AlessandroAvi/Moonboard_Dataset/blob/main/Img/How_to.jpg) 



## HOW  TO USE

- download an andoid simualtor (I used bluestack)
- open the moonboard app in the simulator and move the window as big as possible in a visible part of the screen
- change the parameters inside the script (screen size, total number of holds to be detected, JSON file path, coordinates of the capture region -> for this I suggest to take a screenshot of the entire screen and then use paint to see where exactly the cature region in the script should be)
- run the script

## TO DO

- refine the JSON file that gets created
- make available all datasets (2016 - 2018 -2019)





