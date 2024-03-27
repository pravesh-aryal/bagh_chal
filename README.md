# Bagh Chal (Tiger-Goat) game
**Bagh chal game made using python3 and pygame**

### Activate the virtual environment
```pipenv shell```
### Install pygame 2.4.0
```pip install -r requirements.txt```
### Run the game
```python3 main.py```

# **BaghChal Blog**

!https://cdn-images-1.medium.com/max/1000/1*7vhObuXIJCG2SdSivt_WLw.jpeg

### **Creating Bagh-Chal (Tiger-Goat) Board Game in Python.**

In this article, we are creating a popular board game originating from Nepal. We won't code along in this article, but it will guide you on implementing this game on your chosen tech stack. 

Let's create the game by dividing it into chunks.

### **Generating the Board**

The first step is creating the board's tiny circles in each row. We need to generate coordinates/points as the center for each circle. The code may look like this:

```
# For simplicity, assume the upper-left circle's center is (0,0).
# Coordinates for circles in the first row will be (0,0), (1,0), ..., (4,0).
function generate_coordinates():
  coordinates = empty_array()  # this will store 5 rows
  for y in [0, 1, 2, 3, 4]:  # y coordinate 0 through 4
    row = empty_array()  # row will store coordinates in each row
    for x in [0, 1, 2, 4]:  # x coordinate 0 through 4
       row.add(x, y)
    coordinates.add(row)

  return coordinates  # 5 * 5 matrix

```

Now we need to draw those tiny circles at each point from coordinates. Suppose we have a  function for that.

```
pythonCopy code
# Since coordinates is an array of arrays, we have to loop over it twice to get points.
for each_row in coordinates:
  for each_point in each_row:
    circle.draw(each_point)  # this draws a circle filled with gray color with each point as its center

```

Now draw the lines. 

```
pythonCopy code
# Suppose we have a  function that draws a square connecting four points.
draw_square((0,0), (4,0), (4, 4), (0, 4))

# Vertical lines
draw_line((0,0), (0,4))
draw_line((1,0), (1,4))
draw_line((2,0), (2,4))
draw_line((3,0), (3,4))

# Horizontal lines
draw_line((0,0), (4,0))
draw_line((0,1), (4,1))
draw_line((0,2), (4,2))
draw_line((0,3), (4,3))
draw_line((0,4), (4,4))

# Two diagonals across the board
draw_line((0,0), (4,4))
draw_line((4,0), (0,4))

# Square inside the board
draw_square((2,0), (4,2), (2,4), (0,2))

```

!https://cdn-images-1.medium.com/max/1000/1*3ZZsYbLNgkORqBDNjt7wEQ.png

Now our board is set up; we need to display the tigers in their default position using our  functions:

```python
pythonCopy code
tiger1.draw(0,0)
tiger2.draw(0, 4)
tiger3.draw(4, 4)
tiger4.draw(4, 0)

```

Our board is initialized with all required pieces and setup. Now it's time to place the goats. The goat's player must place 20 goats before moving any. For each circle, we add an event handler in JavaScript that will render a goat image when clicked. We would also group these goats because later in the game, we may need to delete them.

