[GitHub Pages](https://jameskabbes.github.io/ml_pipeline)

# ml_pipeline
A centralized pattern for creating Machine Learning pipelines

# Description
Contains a host of tools for standardizing the format of machine learning pipelines. Provides methods for querying databases, cleaning data, preprocessing data, model operations, exporting results, and more. Each machine learning project is a "child" of this template, with the ability to overwrite any of the default class attributes/methods.

# Code Overview
Read this high-level overview is necessary to understand how the package operates.

**Code Hierarchy**
Models &rarr; Model &rarr; Input_Files &rarr; Input_File &rarr; Features &rarr; Feature

Each point in the hierarchy has certain methods and attributes associated with it. These methods give you the functionality for operating the pipeline.


# First Time Setup
If you have not installed the garden, follow the instructions here: [the_garden](https://www.github.com/jameskabbes/the_garden)

# Usage
High-level overviews for common operations. For more detailed instructions, checkout the Pages.


## Initializing a Repo for ml_pipeline

1. Navigate to a directory in command prompt

```
cd C:/Path/to/Repo
```

2. Call the package's main script

```
python -m ml_pipeline
```

## Navigating the Menu

1. Run `python main_XXX.py` This opens the Models options screen, along with the options for the "Models" class instance.
2. To navigate one level down to a Model, select the option "Open Model"
3. Select a Model from the list.
4. Now in the Model options screen, press enter to navigate back up to Models.
5. You can navigate from Models->Model->Input_Files->Input_File->Features->Feature and all the way back up.
6. Option 1 shows "Open XXXXX" to navigate to the next level down in the tree. 
7. Press enter to exit back up to the previous level. 

## Query new Raw Data

1. `python main_XXX.py`
2. At the Models options screen, select "Open Model".
3. Select any Model from the list (this selection does not matter)
4. In the Model options screen, select "Open Input Files".
5. Select the first option.
6. In the Input Files options screen, select "Open Input File"
7. Select the Input File for which you would like to query new data.
8. In the Input File options screen, select "Query from Source Database"

## Move Query Staged data to Raw Data

1. Follow steps (1-7) from "Query new Raw Data" to get to the Input File of interest.
2. In the Input File options screen, select "Move from Query Staging"

## Clean a Raw Dataset

1. Follow steps (1-7) from "Query new Raw Data" to get to the Input File of interest.
2. In the Input File options screen, select "Clean Raw Dataset"

## Running one Model

1. `python main_XXX.py`
2. At the Models options screen, select the option for "Open Model"
3. Select the Model you would like to run
4. In the Model options screen, select the option for "Run Pipeline"

## Running all Models

1. `python main_XXX.py`
2. At the Models options screen, select the option for "Run Models"



# Author(s)
James Kabbes