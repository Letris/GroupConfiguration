# GroupConfiguration

This repository contains the code and data for the Canvas Recruiter, created for the course Knwowledge Engineering at the Vrije Universiteit Amsterdam.

File setup:
- CanvasRecruiter
  - CSV
    - scenario1
    - scenario2
  - Project
    - classes.py
    - evaluation.py
    - inference_functions.py
    - main.py
    - operationalize.py
    - sort.py
    - util.py 
    - verify_hard.py
  
  The map CSV contains two scenarios that can be used as input for the Canvas Recruiter. To add more scernarios, simply copy paste one of the two scenario directories and adjust to your liking. The project directory contains the python files that make up the Canvas recruiter. To run the code, open main.py and adjust the parameters to your liking and then run main.py. Inference_functions.py contains the inference functions that map directly to our inference layer and are used in main.py. When inference functions within inference_functions.py use subfunctions, then those can be found in the python file with the same name as the inference function. Evaluation.py holds functions that are used to evaluate the performance of the system and generate the output. Finally, util.py holds utility functions.
