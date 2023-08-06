from G_Sketch import *

sketch = Sketch("G_Sketch/flower.png")

# Produces formatted coordinates (with breaks)
# (Uncomment to run)

# print(sketch.get_coords())

# Produces raw coordinates (no breaks)
# (Uncomment to run)

# print(sketch.get_raw_coords())

# Returned list is often quite large, so pixels can be
# diminished using a parameter to set the minimum
# distance 2 given pixels must be from each other

print(len(sketch.get_coords()))
sketch.set_min_distance(5)
print(len(sketch.get_coords()))

