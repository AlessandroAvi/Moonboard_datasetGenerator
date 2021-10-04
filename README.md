# Moonboard_Dataset

This repo contains the code that I developed for creating a dataset that contains all the problems from the moonobard app.

I developed this code because the original dataset is private and I couldn't use properly my moonboard led kit that I developed in [this](https://github.com/AlessandroAvi/Moonboard_LED_DIY) project. 

**IDEA**: using an Android emulator on the computer and using openCV I make a screenshot of the app. Then I mask out all the circles (red, green and blue) and perform a circle detection on these maks. By doing this I am able to find the center of the circles that reppresent the positions of the holds. I then associate to each single circle the closest real hold. All the important informations (hold name, identification start/top/middle hold, problem ID) are then stored inside a JSON file. This procedure is done automatically on all the available problems (by exploiting win32api for moving automatically the mouse and select new problems) on the app that I filtered at the time of running the code. Additionally each problem is assigned with a unique ID, this is used for switching on the correct LEDs on the moonboard panel.



## TO DO

- refine the JSON file that gets created
- add the recognition of name and grade (text recognition with openCV)
- make available all datasets (2016 - 2018 -2019)
