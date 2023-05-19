Assignment 2:

Setup assumes that you are using a UNIX-based OS with python3 and python3-venv installed.

To build the virtual environment and install necessary packages:

```
> make
```

Note: The requirements.txt file contains all necessary packages.

To activate the virtual environment:

```
> source ./venv/bin/activate
```

To run the code:

```
> python ./src/main.py
```

Program controls:

- The two lights are initially set in position, these can be made to orbit by pressing 'o'. They can be stopped at any time by pressing 'o' again. This can be done at any time.
- The colours of the lights can be set to cycle by pressing 'v'. These can be stopped at any time be pressing 'v' again. This can be done at any time.
- The camera can be orbitted around the model by pressing 'c' and then incremented using '-' and '+' on the keyboard. Once you are done, press the 'enter' key on the keyboard to clear the controls.
- We can apply a transformation to the model:
    Press 'r' for rotate or 's' for scale.
    - Then select the axis: 
        Press 'x' for x-axis, 'y' for y-axis or 'z' for z-axis. These can be changed without having to select a transformation type again.
    - The transformations can be controled with minus '-' and plus '+' on the keyboard.
    - Once you are done with a setting, press the 'enter' key on the keyboard to clear the controls. You may then select a transformation again.
- The model and lights can be reset by pressing 'l' on the keyboard. This can be clicked at any time and clears all controls.
- To quit the program, press 'q'. This can be done at any time.

For extra marks I added a model for each light source to visualise their orbits, as well as implementing animated textures. I did this by converting a gif into a sprite-sheet (this is an image that contains all the frames of an animation) and then used it as my texture. I got inspiration for this from https://sudonull.com/post/77686-Animated-Textures-in-OpenGL. I appended each frame to a list and then I bind a new frame to the model every 100ms in the render function.
