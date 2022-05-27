from bokeh.models import ColumnDataSource, Div, Slider, TextInput, Range1d, Arrow, OpenHead, NormalHead, TapTool, Button, RadioButtonGroup
from bokeh.layouts import row, column
from bokeh.plotting import figure

import numpy as np


def lwe_basis_app(doc):


    def pmatrix(a):
        if len(a.shape) > 2:
            raise ValueError('bmatrix can at most display two dimensions')
        lines = str(a).replace('[', '').replace(']', '').splitlines()
        rv = [r'\begin{pmatrix}']
        rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
        rv +=  [r'\end{pmatrix}']
        return '\n'.join(rv)


    def generate_lattice(basis):
        xval = []
        yval = []
        xval.append(0)
        yval.append(0)
        for a in range(-50, 50):
            for b in range(-50, 50):
                xnew = a * basis[0][0] + b * basis[0][1]
                xval.append(xnew)
                ynew = a * basis[1][0] + b * basis[1][1]
                yval.append(ynew)
        return xval, yval

    def calculate_lwe(n,m,q,message):
        A = np.random.randint(low=-q,high=q,size=(m,n))
        s = np.random.randint(low=-q,high=q,size=n)
        e = np.random.randint(-1,1,size=m)

        s = np.transpose(s)
        e = np.transpose(e)

        B = np.mod(np.add(np.dot(A,s), e), q)
        ap = np.mod(A.sum(axis=0),q)
        
        pp, ep = enc_dec(B, message, q, ap, s)

        #print(f'Range ({(q//2-q//4)}, {(q//2+(q//4))})')
        decrypted = 1 if (q//2-(q//4)) < ep < (q//2+(q//4)) else 0

        return A,s,e,B,decrypted,ep

    def enc_dec(B, message, q, ap, s):

        pp = (B.sum() + message * q//2) % q
        ep = (pp - np.dot(ap, s)) % q

        return pp, ep
    
    message = 0

    A,s,e,B,decrypted,ep = calculate_lwe(2,2,17,message)


    basis = A
    x,y = generate_lattice(basis)
    secx=s[0]*basis[0][0] + s[1]*basis[0][1]
    secy=s[0]*basis[1][0] + s[1]*basis[1][1]

    pubx=s[0]*basis[0][0] + s[1]*basis[0][1] + e[0]
    puby=s[0]*basis[1][0] + s[1]*basis[1][1] + e[1]

    epx=np.sin((2*np.pi/17)*ep)
    epy=np.cos((2*np.pi/17)*ep)

    source = ColumnDataSource(data=dict(x=x, y=y))
    bsource = ColumnDataSource(data=dict(x=basis[0], y=basis[1]))
    csource = ColumnDataSource(data=dict(pubx=[pubx], puby=[puby], secx=[secx], secy=[secy], epx=[epx], epy=[epy]))

    dsource = ColumnDataSource(data=dict(A=A, B=B))
    esource = ColumnDataSource(data=dict(s=s))
    fsource = ColumnDataSource(data=dict(e=e))



    p = figure(
        title="LWE on lattice",
        width=400,
        height=400,
        tools="pan, wheel_zoom, reset, save"
    )

    p.x_range = Range1d(-20, 20)
    p.y_range = Range1d(-20, 20)


    p.circle('x', 'y', source=source, size=10, color="navy", alpha=0.5)
    p.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
                    x_start=0, y_start=0, x_end='x', y_end='y', source=bsource))

    secret = Arrow(end=NormalHead(line_color="orange", line_width=4),
                    x_start=0, y_start=0, x_end='secx', y_end='secy', source=csource)

    public = Arrow(end=NormalHead(line_color="blue", line_width=4),
                    x_start=0, y_start=0, x_end='pubx', y_end='puby', source=csource)

    p.add_layout(secret)
    p.add_layout(public)



    p2 = figure(plot_width=400, plot_height=400, match_aspect=True, tools="pan, wheel_zoom, reset, save") 


    p2.x_range = Range1d(-1.3, 1.3)
    p2.y_range = Range1d(-1.3, 1.3)


    p2.circle(0,0,radius=1,fill_color=None,line_color='OliveDrab')
    p2.circle('epx', 'epy', source=csource,size=10,color="navy")


    def lwe_callback(event):
        A,s,e,B,decrypted,ep = calculate_lwe(2,2,17,message)

        basis = np.transpose(A)
        x,y = generate_lattice(basis)

        secx=s[0]*basis[0][0] + s[1]*basis[0][1]
        secy=s[0]*basis[1][0] + s[1]*basis[1][1]

        epx=np.sin((2*np.pi/17)*ep)
        epy=np.cos((2*np.pi/17)*ep)

        pubx=s[0]*basis[0][0] + s[1]*basis[0][1] + e[0]
        puby=s[0]*basis[1][0] + s[1]*basis[1][1] + e[1]


        dsource.data = dict(A=A, B=B)
        esource.data = dict(s=s)
        fsource.data = dict(e=e)

        equation.text= f"""$${pmatrix(dsource.data['A'])} {pmatrix(esource.data['s'])}^\\top + {pmatrix(fsource.data['e'])}^\\top = {pmatrix(dsource.data['B'])}^\\top (\\bmod 17)$$"""

        source.data = dict(x=x, y=y)
        bsource.data = dict(x=basis[0], y=basis[1])
        csource.data = dict(pubx=[pubx], puby=[puby], secx=[secx], secy=[secy], epx=[epx], epy=[epy])

        private.text = f"Private key: $$s={pmatrix(s)}$$, $$e={pmatrix(e)}$$"
        public.text = f"Public key: $$A={pmatrix(A)}$$, $$B={pmatrix(B)}$$"


    button = Button(label="Recalculate keys", button_type="default")
    button.on_click(lwe_callback)


    private = Div(text=f"Private key: $$s={pmatrix(s)}$$, $$e={pmatrix(e)}$$", width=200, height=100)
    public = Div(text=f"Public key: $$A={pmatrix(A)}$$, $$B={pmatrix(B)}$$", width=200, height=100)

    equation = Div(text=f"""$${pmatrix(dsource.data['A'])} {pmatrix(esource.data['s'])}^\\top + {pmatrix(fsource.data['e'])}^\\top = {pmatrix(dsource.data['B'])}^\\top (\\bmod 17)$$""", 
    width=300, height=200, style={'font-size': '100%', 'margin-top': '170px'})



    controls = column(button, private, public)

    doc.add_root(row(controls, p, equation))
    doc.title = "LWE on Lattices"
