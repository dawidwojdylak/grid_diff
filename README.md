# Image difference tool

This application allows you to visualize the difference between two images using a grid.

## Installing venv

The virtual environment is recomended.

If venv is not installed:
```
python3 -m pip install --user virtualenv
```

Create the environment:
```
python3 -m venv .venv
```

Activate environment:
```
source .venv/bin/activate
```

Install the required packages:
```
python -m pip install -r ./requirements.txt
```

## Usage

```
usage: main.py [-h] [-g rows cols] [-o OUTPUT] img1 img2
```
### Positional Arguments
```
img1                  1st image path
img2                  2nd image path
```

### Optional Arguments
```
  -h, --help            show this help message and exit
  -g rows cols, --grid rows cols
                        Grid size (rows x cols)
  -o OUTPUT, --output OUTPUT
                        Output image path
```

## Examples of usage

Compare two images:
```
python ./main.py examples/01_bird_norm.png examples/01_bird_edit.png
```

Compare two images using a 4x5 grid:
```
python ./main.py examples/01_bird_norm.png examples/01_bird_edit.png -g 4 5
```

Compare two images using a 5x5 grid and save the result in the output image:
```
python ./main.py examples/01_bird_norm.png examples/01_bird_edit.png -g 5 5 -o compared_image.png
```