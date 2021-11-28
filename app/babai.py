from bokeh.models import ColumnDataSource, Div, Slider, TextInput, Range1d, Arrow, OpenHead, NormalHead, TapTool, Button
from bokeh.layouts import row, column
from bokeh.plotting import figure
from bokeh.events import Tap

import random
import numpy as np
from sympy import *



def babai_app(doc):
    def generate_lattice(basis):
        xval = []
        yval = []
        xval.append(0)
        yval.append(0)
        for a in range(-50, 50):
            for b in range(-50, 50):
    #           if mod is not 0:                
    #               xnew = (a * basis[0][0] + b * basis[0][1]) % mod
    #               xval.append(xnew)
    #              ynew = (a * basis[1][0] + b * basis[1][1]) % mod
    #              yval.append(ynew)
    #           else:
                    xnew = a * basis[0][0] + b * basis[0][1]
                    xval.append(xnew)
                    ynew = a * basis[1][0] + b * basis[1][1]
                    yval.append(ynew)
        return xval, yval


    def hadamard_ratio(basis):
        dimension = basis.ndim
        det = abs(np.linalg.det(basis))
        mult = 1
        for v in basis:
            mult = mult * np.linalg.norm(v)
        hratio = (det / mult) ** (1.0 / dimension)
        return hratio


    def solve_babai(basis, t):
        res = np.array([t[0],t[1]])
        print(f"babai fist step {res}")
        a = np.round(np.linalg.solve(basis, res))
        print(f"babai round step {a}")
        dot = np.dot(basis, a)
        return dot


    def rand_unimod(n):
        random_matrix = [ [np.random.randint(-3,3) for _ in range(n) ] for _ in range(n) ]
        upperTri = np.triu(random_matrix,0)
        lowerTri = [[np.random.randint(-3,3) if x<y else 0 for x in range(n)] for y in range(n)]  

        for r in range(len(upperTri)):
            for c in range(len(upperTri)):
                if(r==c):
                    if bool(random.getrandbits(1)):
                        upperTri[r][c]=1
                        lowerTri[r][c]=1
                    else:
                        upperTri[r][c]=-1
                        lowerTri[r][c]=-1
        uniModular = np.matmul(upperTri,lowerTri)
        return uniModular


    def regenerate_lattice(basis):
        x, y = generate_lattice(basis)
        source.data = dict(x=x, y=y)
        bsource.data = dict(x=basis[0], y=basis[1], xu=bsource.data['xu'], yu=bsource.data['yu'], hadamard=[hadamard_ratio(basis), bsource.data['hadamard'][1]])
        hadamard.text = f"""Hadamard Ratio: {bsource.data['hadamard'][0]}"""

        (lambdas, V) = np.linalg.eig(basis.T)
        i = 1 if basis[lambdas == 0, :].size == 0 else 0
        csource.data = dict(xb=csource.data['xb'], xub=csource.data['xub'], yb=csource.data['yb'], yub=csource.data['yub'], xsource=csource.data['xsource'], ysource=csource.data['ysource'], independence=[i])
        negation = "not" if i == 0 else ""
        independence.text = f"""Basis vectors are {negation} independent."""


    # Define the figure plot
    p = figure(
        title="Lattice with defined basis",
        width=400,
        height=400,
        tools="pan, wheel_zoom, reset, save"
    )

    # Set Ranges for the graph axis
    p.x_range = Range1d(0, 10)
    p.y_range = Range1d(0, 10)

    # Initialize the plot with arbitrary lattice
    basis = np.array([[2, 1], [1, 2]])
    x, y = generate_lattice(basis)

    # Create data sources for lattice and basis
    source = ColumnDataSource(data=dict(x=x, y=y))
    bsource = ColumnDataSource(data=dict(x=basis[0], y=basis[1], xu=np.array([0, 0]), yu=np.array([0, 0]), hadamard=[hadamard_ratio(basis), 0]))
    csource = ColumnDataSource(data=dict(xb=[0], xub=[0], yb=[0], yub=[0], xsource=[0], ysource=[0], independence=[1]))
    # Define lattice plot

    p.circle('x', 'y', source=source, size=10, color="navy", alpha=0.5)
    p2 = figure(width=400,height=400, x_range=p.x_range, y_range=p.y_range, title="Basis with applied uminodular matrix")

    p2.circle('x', 'y', source=source, size=10, color="navy", alpha=0.5)

    # Define basis vector plot
    p.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
                    x_start=0, y_start=0, x_end='x', y_end='y', source=bsource))

    p2.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
                    x_start=0, y_start=0, x_end='xu', y_end='yu', source=bsource))

    p.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
                    x_start=0, y_start=0, x_end='xc', y_end='yc', source=bsource))

    babai_unimod = Arrow(end=NormalHead(line_color="orange", line_width=4),
                    x_start=0, y_start=0, x_end='xub', y_end='yub', source=csource)
    babai_normal = Arrow(end=NormalHead(line_color="orange", line_width=4),
                    x_start=0, y_start=0, x_end='xb', y_end='yb', source=csource)

    p2.add_layout(babai_unimod)

    p.add_layout(babai_normal)

    selection_arrow = Arrow(end=NormalHead(line_color="yellow", line_width=4),
                    x_start=0, y_start=0, x_end='xsource', y_end='ysource', source=csource)

    p2.add_layout(selection_arrow)

    p.add_layout(selection_arrow)




    def babai_callback(event):
        coords=(round(event.x, 3), round(event.y, 3))
        print(coords)
        basis = np.array([bsource.data['x'], bsource.data['y']])
        print(basis)
        ubasis = np.array([bsource.data['xu'], bsource.data['yu']])
        cvp = solve_babai(basis, coords)
        ucvp = solve_babai(ubasis, coords)
        print(cvp)
        csource.data = dict(xb=[cvp[0]], xub=[ucvp[0]], yb=[cvp[1]], yub=[ucvp[1]], xsource=[coords[0]], ysource=[coords[1]], independence=csource.data['independence'])


    def x1_callback(attr, old, new):
        try:
            new = int(new)
        except ValueError:
            new = old

        basis = bsource.data
        basis['x'][0] = new
        newbasis = np.array([basis['x'], basis['y']])
        regenerate_lattice(newbasis)


    def x2_callback(attr, old, new):
        try:
            new = int(new)
        except ValueError:
            new = old

        basis = bsource.data
        basis['x'][1] = new
        newbasis = np.array([basis['x'], basis['y']])
        regenerate_lattice(newbasis)

    def y1_callback(attr, old, new):
        try:
            new = int(new)
        except ValueError:
            new = old

        basis = bsource.data
        basis['y'][0] = new
        newbasis = np.array([basis['x'], basis['y']])
        regenerate_lattice(newbasis)


    def y2_callback(attr, old, new):
        try:
            new = int(new)
        except ValueError:
            new = old

        basis = bsource.data
        basis['y'][1] = new
        newbasis = np.array([basis['x'], basis['y']])
        regenerate_lattice(newbasis)

    #def mod_callback(attr, old, new):
    #    try:
    #        new = int(new)
    #    except ValueError:
    #        new = old

    #    regenerate_lattice(bsource.data)


    def unimod_callback(event):
        basis = bsource.data
        print(basis)
    #   try:
    #       newbasis = np.array([[basis['x'][2], basis['x'][3]], [basis['y'][2], basis['y'][3]]])
    #       print(f"true{newbasis}")
    #   except IndexError:
    #       newbasis = np.array([basis['x'], basis['y']])
    #       print(f"false{newbasis}")

        newbasis = np.matmul(np.array([basis['x'], basis['y']]),rand_unimod(2))
        print(newbasis)
    #  new_data = {
    #  'x' : newbasis[0],
    #   'y' : newbasis[1],
    #    'hadamard': [hadamard_ratio(newbasis), 0]
    #    }
        bsource.data = dict(x=bsource.data['x'], y=bsource.data['y'], xu=newbasis[0], yu=newbasis[1], hadamard=[bsource.data['hadamard'][0], hadamard_ratio(newbasis)])
    #    bsource.stream(new_data)
        hadamard2.text = f"""Hadamard Ratio: {bsource.data['hadamard'][1]}"""



    x1 = Slider(title="X1", value=2, start=-10, end=10, step=1)
    x2 = Slider(title="X2", value=1, start=-10, end=10, step=1)
    y1 = Slider(title="Y1", value=1, start=-10, end=10, step=1)
    y2 = Slider(title="Y2", value=2, start=-10, end=10, step=1)

    x1_input = TextInput(value="2", title="X1:")
    x1_input.on_change('value', x1_callback)
    x2_input = TextInput(value="1", title="X2:")
    x2_input.on_change('value', x1_callback)
    y1_input = TextInput(value="1", title="Y1:")
    y1_input.on_change('value', x1_callback)
    y2_input = TextInput(value="2", title="Y2:")
    y2_input.on_change('value', x1_callback)

    #mod_input = TextInput(value="0", title="Modular group q:")
    #mod_input.on_change('value', mod_callback)

    x1.on_change('value', x1_callback)
    y1.on_change('value', y1_callback)
    x2.on_change('value', x2_callback)
    y2.on_change('value', y2_callback)

    independence = Div(text=f"""Basis vectors are {"not" if csource.data['independence'] == 1 else ""} independent.""", width=200, height=50)
    hadamard = Div(text=f"""Hadamard Ratio: {bsource.data['hadamard'][0]}""", width=200, height=100)
    hadamard2 = Div(text=f"""Hadamard Ratio: {bsource.data['hadamard'][1]}""", width=200, height=100)

    button = Button(label="Apply Unimodular matrix", button_type="default")
    button.on_click(unimod_callback)

    p.add_tools(TapTool())
    p.on_event(Tap, babai_callback)

    buttons = column(x1, x1_input, y1, y1_input, x2, x2_input, y2, y2_input, button, independence)
    baseplot = column(p, hadamard)
    uniplot = column(p2, hadamard2)
    doc.add_root(row(buttons, baseplot, uniplot, width=400))
    doc.title = "Lattice-based Cryptography"


