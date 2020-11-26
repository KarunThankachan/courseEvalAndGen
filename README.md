# Course Content Evaluation and Generation
Automatic Evaluation and Generation of Course Content

- AL-CPL/ : Downloaded from (https://github.com/dayouzi/CMEB)
    - Textbook/ : Contains the textbooks the AL-CPL dataset is built upon
    - features/
        - *_retation_v2.csv: Contains the manually identified prerequisites in tab-separated form.
            0 Indicates the A, B pair does not have a pre-requisite
            1 Indicates that A is prerequiste of B
            -1 Indicates that B is a prerequisit of A
        - proc_*_relation_v2.csv: Contains the data processed from respecitve *_relation_v2.csv file in CSV form
            0 Indicates the A, B pair does not have a pre-requisite
            1 Indicates that A is prerequiste of B
- data/ : Contains open-soruce textbooks identified for domain of investigation i.e. Cloud Computing and Data Science
- db/ : Contains python code to create an in-memory db, to speed up performance
- error_analysis/: Script and python notebooks for performing error analysis on model results
- models/: [CORE] Code model code that will be made available for distribution
- notebooks/: python notebooks for prototyping
- pkgs/: external third-party packages
- results/: [CORE] processed data/final resultant data will be located here
- utils/: [CORE] Code for support functionalities, made available for distribution
- references/: papers/studies used to support research

## Code Quality
All [CORE] pacakges will be made public. Tested/Documented code must be pushed here
Atleast 60% Code coverage is required. unittest will be used for testing
Coding Conventaions
- Docstring for all function/classes
- PEP-8 standrad will be followed for naming/indentation and all styling conflicts

## Code Control
Please make chekins to DEV branch
Post code-review code will move into MASTER branch
Push code from master [CORE] folders into DIST branch


