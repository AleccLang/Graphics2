Assignment 1:

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

- First select the transformation type:
    Press 't' for transform, 'r' for rotate, 's' for scale or 'c' for colour change.
- Then select the axis: 
    Press 'x' for x-axis, 'y' for y-axis or 'z' for z-axis. These can be changed without having to select a transformation type again.(Note: scale and colour have no set axis, hence this step can be skipped for them)
- The transformations can be controled with minus '-' and plus '+' on the keyboard. (Colour changes only with '+')
- Once you are done with a setting, press the 'enter' key on the keyboard to clear the controls. You may then select a transformation again.
- To load in a second model, press 'n'. This can be done at any time and will also reset the models to the origin. Transformations will apply to both models. The second model can be removed by pressing 'n' again.
- The model/s can be reset by pressing 'l' on the keyboard. This can be clicked at any time and clears all controls.
- To quit the program, press 'q'. This can be done at any time.