# grouponefunctions

A package containing the necessary functions to smoothly run the analysis in DSCI-310-Group-1.

## Installation

Note: The installation is not likely to proceed for Python version lower than 3.9.10. Please check your Python version the code below.

```bash
python --version
```

Then you can install the package by the command below.

```bash
pip install grouponefunctions
```

## Usage

`grouponefunctions` is primarily used for analysis of [Predicting students’ grades using multi-variable regression](https://github.com/DSCI-310/DSCI-310-Group-1), but contains three general use functions. To implement the functions, `import` our package `grouponefunctions` as a module. The package has three functions: `splitxy`, `listfun`, and `plotsquaredata`. 

### `split_xy`

 `split_xy` can be used to split data into predictor feature and target variables as follows:

```python
from grouponefunctions.grouponefunctions import split_xy

X_train, y_train = split_xy(train_df, ["feature1", "feature2", "feature3"], target)
X_test, y_test = split_xy(test_df, ["feature1", "feature2", "feature3"], target) 
```

### `plot_square_data`

This function is capable at creating plots to display in a grid configuration.

```python
from grouponefunctions.grouponefunction import plot_square_data

plot_square_data(X_train, y_train, ["feature1", "feature2", "feature3"], ["title1", "title2", "title3], "This is Plot 1")
plot_square_data(dependent, independednts, ["income"], ["retirement_age"], "Income and Retirement Age Relation")
```

### `list_abs`

This function is the abstract function for list, used in Results part in the analysis. 

```python
from grouponefunctions.grouponefunction import list_abs

list_abs(preprocessor, "pipeline-2", "onehotencoder", categorical_features)
```



## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`grouponefunctions` was created by Andres Zepeda Perez, Daniel Hou, Zizhen Guo, Timothy Zhou. It is licensed under the terms of the MIT license.

## Credits

`grouponefunctions` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
