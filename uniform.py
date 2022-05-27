import numpy as np
import scipy.special

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show


def make_plot(title, hist, edges, x, pdf, cdf):
    p = figure()
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)
    p.line(x, pdf, line_color="firebrick", line_width=4, alpha=0.7)
    #p.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend_label="CDF")

    p.y_range.start = 0
    #p.legend.location = "center_right"
    #p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'P(x)'
    p.grid.grid_line_color="white"
    return p

# Normal Distribution

mu, sigma = 0, 0.5

measured = np.random.normal(mu, sigma, 1000)
hist, edges = np.histogram(measured, density=True, bins=50)

x = np.linspace(-2, 2, 1000)
pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
cdf = (1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2


measured = np.random.uniform(1, 2, 1000)
hist, edges = np.histogram(measured, density=True, bins=50)

p2 = figure()

x = np.linspace(1, 2, 1000)

p2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="navy", line_color="white", alpha=0.5)
p2.line(x, 1, line_color="firebrick", line_width=4, alpha=0.7)
p2.xaxis.axis_label = 'x'
p2.yaxis.axis_label = 'P(x)'


p = make_plot("Normal Distribution (μ=0, σ=0.5)", hist, edges, x, pdf, cdf)

show(p2)
