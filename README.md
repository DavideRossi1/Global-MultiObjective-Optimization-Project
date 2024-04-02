# Global-MultiObjective-Optimization-Project
This repository contains the results obtained during the development of the final project for the Global and MultiObjective Optimization course of University of Trieste. The project consists of the implementation of a driver controller for a car in a simple 2D racing game. Tree-based genetic programming has been used to evolve the controller. 

## Requirements
The project has been run using `Python 3.10.13` but is expected to run with any version of Python 3. The following packages are required to run the project:

- `operator` and `random` from the standard library;
- `numpy` to correctly pass the states space and save/load it to/from file;
- `matplotlib` to plot the animations
- `DEAP` library, which can be installed using `pip install deap`: this is the main package used to build and learn trees for GP;
- `pygraphviz` package, which can be installed using `pip install pygraphviz`, used to save readable trees in pdf files;
- (optional) `PyGame`, which can be installed using `pip install pygame`, if you want to play the game with a Graphical User Interface
  
## How to run
Clone the repository and move inside it:
```shell
git clone git@github.com:DavideRossi1/Global-MultiObjective-Optimization-Project.git
cd Global-MultiObjective-Optimization-Project
```
The repository contains two main modules:

- [the GUI game](GUIGame/), a single file which can be run using
  
    ```shell
    python GUIGame/main.py 
    ```
    
    The game will continue running: a new game is started 3 seconds after the previous game is over. To stop the application, just close the window.

- [the main game](source_files/), which contains all the files needed to learn and run an agent to play the game. Before running the game, have a look at the [Constants file](source_files/Constants.py) and set them as you prefer. Then, run the game with
```shell
    python source_files/main.py
```
If no agent has been imported a new agent will be learnt using the parameters set, and some information will be printed to monitor the learning phase.
After the learning phase has ended, the game will start (printed in the terminal, plotted or both, according to the parameters set).

Some learned agents are already available in the [agents folder](agents/).

### Further notes
if you are using a computer with a Rayzen CPU and an integrated AMD Radeon Graphics GPU, you may encounter a warning message like this when trying to plot the animation:
```shell
MESA-LOADER: failed to open radeonsi: /usr/lib/dri/radeonsi_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib/x86_64-linux-gnu/dri:\$${ORIGIN}/dri:/usr/lib/dri, suffix _dri)
failed to load driver: radeonsi
MESA-LOADER: failed to open swrast: /usr/lib/dri/swrast_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib/x86_64-linux-gnu/dri:\$${ORIGIN}/dri:/usr/lib/dri, suffix _dri)
failed to load driver: swrast
```
This probably happens since Matplotlib is trying to use the GPU to plot the animation but fails to load the correct drivers.
In order to fix it, it is enough to set the following environment variable:
```shell
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
```
