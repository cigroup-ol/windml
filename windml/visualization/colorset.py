from pylab import *

colorset = ["#6698cc","#c4d8eb","#cccccc","#69bb3e","#b8e1a5"]

cdict = {'red': ((0.0, 0.4, 0.4),
                 (0.5, 0.72, 0.72),
                 (1.0, 0.41, 0.41)),
         'green': ((0.0, 0.6, 0.6),
                   (0.5, 0.88, 0.88),
                   (1.0, 0.73, 0.73)),
         'blue': ((0.0, 0.8, 0.8),
                  (0.5, 0.65, 0.65),
                  (1.0, 0.01, 0.01))}

0.412, 0.733, 0.012

cmap = matplotlib.colors.LinearSegmentedColormap(\
                'windml_colormap',cdict,256)
