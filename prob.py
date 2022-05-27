from bokeh.plotting import figure, output_file, show

output_file("line.html")

p = figure(width=400, height=400)

# add a steps renderer
p.step([-1, 0, 1, 2, 3], [0, 0.25, 0.75, 1, 1], line_width=2, mode="after")

show(p)
