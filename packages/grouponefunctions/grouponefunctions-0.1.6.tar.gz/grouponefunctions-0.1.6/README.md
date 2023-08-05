# grouponefunctions

A package containing the necessary functions to smoothly run the analysis in DSCI-310-Group-1

## Installation

```bash
$ pip install grouponefunctions
```

## Usage

grouponefunctions is primarily used for analysis of (Predicting students’ grades using multi-variable regression)[https://github.com/DSCI-310/DSCI-310-Group-1], but contains three general use functions.

The first function `split_xy` can be used to split data into predictors and target variables as follows:

```
from grouponefunctions import grouponefunctions

X_train, y_train = grouponefunctions.split_xy(train_df, predictors, target)
X_test, y_test = grouponefunctions.split_xy(test_df, predictors, target) 
```

The second function `plot_square_data` can be used to create plots to display in a square manner.

The third function `list_abs` can be used to create a list for the result of our notebook.


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`grouponefunctions` was created by Andres Zepeda Perez, Daniel Hou, Zizhen Guo, Timothy Zhou. It is licensed under the terms of the MIT license.

## Credits

`grouponefunctions` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
