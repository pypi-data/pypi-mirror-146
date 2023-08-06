import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.subplot(1, 1, 1)
ax = plt.gca()
ax.invert_yaxis()

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
print(ax.yaxis_inverted())

# Create a Rectangle patch
rect = patches.Rectangle((2, 4), 2, 2, linewidth=1, edgecolor='r', facecolor='none')

# Add the patch to the Axes
ax.add_patch(rect)

plt.show(block=True)