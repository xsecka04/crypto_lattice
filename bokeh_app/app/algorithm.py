from bokeh.models import ColumnDataSource, Div, Slider, TextInput, Range1d, Arrow, OpenHead, NormalHead, TapTool, Button
from bokeh.layouts import row, column
from bokeh.plotting import figure
from bokeh.events import Tap

import random
import numpy as np
from sympy import *



def alg_app(doc):

    
    def pmatrix(a):
        if len(a.shape) > 2:
            raise ValueError('bmatrix can at most display two dimensions')
        lines = str(a).replace('[', '').replace(']', '').splitlines()
        rv = [r'\begin{pmatrix}']
        rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
        rv +=  [r'\end{pmatrix}']
        return '\n'.join(rv)

    n = 3
    #m = 4
    q = 17
    message = 0

    def calculate_lwe(n,q,message):
        m = int(np.ceil(1.1 * np.log(q) * n))
        A = np.random.randint(low=-q,high=q,size=(m,n))
        s = np.random.randint(low=-q,high=q,size=n)
        e = np.random.randint(-1,1,size=m)

        s = np.transpose(s)
        e = np.transpose(e)

        B = np.mod(np.add(np.dot(A,s), e), q)
        ap = np.mod(A.sum(axis=0),q)
        pp = (B.sum() + message * q//2) % q

        ep = (pp - np.dot(ap, s)) % q

        #print(f'Range ({(q//2-q//4)}, {(q//2+(q//4))})')
        decrypted = 1 if (q//2-(q//4)) < ep < (q//2+(q//4)) else 0

        return A,s,e,B,decrypted,ep, ap, pp, m
    
    A,s,e,B,decrypted,ep, ap, pp, m = calculate_lwe(n,q,message)


    source = ColumnDataSource(data=dict(n=[n], m=[m], q=[q], msg=[message], dec=[decrypted], ciph=[ep], pp=[pp]))
    bsource = ColumnDataSource(data=dict(A=A, B=B))
    csource = ColumnDataSource(data=dict(s=s, ap=ap))
    dsource = ColumnDataSource(data=dict(e=e))

    def lwe_callback(event):
        try:
            message = int(message_input.value)
        except ValueError:
            message = 0
        try:
            n = int(n_input.value)
        except ValueError:
            n = 3
        #try:
        #    m = int(m_input.value)
        #except ValueError:
        #    m = 4
        try:
            q = int(q_input.value)
        except ValueError:
            q = 17


        A,s,e,B,decrypted,ep, ap, pp, m = calculate_lwe(n,q,message)
        source.data = dict(n=[n], m=[m], q=[q], msg=[message], dec=[decrypted],ciph=[ep], pp=[pp])
        bsource.data = dict(A=A, B=B)
        csource.data = dict(s=s, ap=ap)
        dsource.data = dict(e=e)
        out.text = f"""Plaintext: {source.data['msg'][0]}, Ciphertext: {source.data['dec'][0]} ({source.data['ciph'][0]})"""
        private.text = f"Private key: $$s={pmatrix(csource.data['s'])}$$, $$e={pmatrix(dsource.data['e'])}$$"
        public.text = f"Public key: $$A={pmatrix(bsource.data['A'])}$$, $$p={pmatrix(bsource.data['B'])}$$"
        equation.text = f"""$${pmatrix(bsource.data['A'])} {pmatrix(csource.data['s'])}^\\top + $$ <br> $$+ {pmatrix(dsource.data['e'])}^\\top  = {pmatrix(bsource.data['B'])}^\\top (\\bmod {source.data['q'][0]})$$"""
        enc_pair.text=r"$$a' = \sum_I " + f"{pmatrix(bsource.data['A'])} = {pmatrix(csource.data['ap'])}$$"
        enc_pair2.text=r"$$p' = " + r"\sum_I " + f"{pmatrix(bsource.data['B'])} + {source.data['msg'][0]} " + r"*\lfloor \frac{" + f"{source.data['q'][0]}" +r"}{2} \rfloor = " + f"{source.data['pp'][0]}$$"
        dec_pair.text=f"$$ {source.data['pp'][0]} - {pmatrix(csource.data['ap'])} \\times {pmatrix(csource.data['s'])}^\\top = {source.data['ciph'][0]} $$"
        dec_pair2.text=f"$$ Dec({source.data['ciph'][0]})=" + r"\begin{cases} 0, & \text{if } x \sim 0 \\ 1, & \text{if } x \sim " + f"{source.data['q'][0]}/2" + r"\end{cases}" + f" = {source.data['dec'][0]}$$"





    private = Div(text=f"""Private key: $$s={pmatrix(csource.data['s'])}$$, $$e={pmatrix(dsource.data['e'])}$$""", width=200, height=200)
    public = Div(text=f"""Public key: $$A={pmatrix(bsource.data['A'])}$$, $$p={pmatrix(bsource.data['B'])}$$""", width=200, height=200)

    out = Div(text=f"""Plaintext: {source.data['msg'][0]}, Ciphertext: {source.data['dec'][0]} ({source.data['ciph'][0]})""", width=200, height=200)

    equation = Div(text=f"""$${pmatrix(bsource.data['A'])} {pmatrix(csource.data['s'])}^\\top + $$ <br> $$+ {pmatrix(dsource.data['e'])}^\\top = {pmatrix(bsource.data['B'])}^\\top (\\bmod {source.data['q'][0]})$$""", 
    width=300, height=200, style={'font-size': '100%'})


    button = Button(label="Recalculate keys", button_type="default")
    button.on_click(lwe_callback)

    message_input = TextInput(value="0", title="Plaintext:")
    n_input = TextInput(value="4", title="Dimension n:")
    m_input = TextInput(value="3", title="Dimension m:")
    q_input = TextInput(value="17", title="Prime number:")

   # message_input.on_change('value', lwe_callback)


    prelimA = Div(text=f"Alice", width=300, height=50)
    prelimB = Div(text=f"Bob", width=300, height=50)
    prelimC = Div(text=f"Network", width=300, height=50)
    send = Div(text=f"Alice sends (pub)", width=300, height=200)
    send2 = Div(text=f"Bob sends (ap, pp)", width=300, height=200)
    space = Div(text=f"", width=300, height=200)

    #enc_pair = Div(text=f"""$$({pmatrix(csource.data['ap'])}, {source.data['pp']})$$""", width=300, height=200)
    enc_pair = Div(text=r"$$a' = \sum_I " + f"{pmatrix(bsource.data['A'])} = {pmatrix(csource.data['ap'])}$$", width=300, height=150)
    enc_pair2 = Div(text=r"$$p' = " + r"\sum_I " + f"{pmatrix(bsource.data['B'])} + {source.data['msg'][0]} " + r"*\lfloor \frac{" + f"{source.data['q'][0]}" +r"}{2} \rfloor = " + f"{source.data['pp'][0]}$$", width=300, height=50)

    dec_pair = Div(text=f"$$ {source.data['pp'][0]} - {pmatrix(csource.data['ap'])} \\times {pmatrix(csource.data['s'])}^\\top = {source.data['ciph'][0]} $$", width=300, height=50)
    dec_pair2 = Div(text=f"$$ Dec({source.data['ciph'][0]})=" + r"\begin{cases} 0, & \text{if } x \sim 0 \\ 1, & \text{if } x \sim " + f"{source.data['q'][0]}/2" + r"\end{cases}" + f" = {source.data['dec'][0]}$$", width=300, height=50)

    #f"$$ Dec({source.data['ciph']})" + r"\begin{cases} 0, & \text{if } x ~ 0 \\ 1, & \text{if } x ~ q/2 \end{cases}" + f" = {source.data['dec']}$$"


    prelim = row(prelimA, prelimC, prelimB)
    keygen = row(equation, send, space)
    encryption = row(space, send2, column(enc_pair,enc_pair2))
    decryption = row(column(dec_pair, dec_pair2))


    #alice = column(prelimA, equation)
    #btw = column(prelimC, send, space)
    #bob = column(prelimB, decryption)

    protocol = column(prelim, keygen, encryption, decryption)


    #buttons = column(button, width=250)
    #inputs = column(n_input, m_input, q_input, message_input, button)
    inputs = column(n_input, q_input, message_input, button)

    outputs = column(private,public, out, equation)
    #doc.add_root(row(inputs, outputs))
    doc.add_root(row(inputs, protocol))

    doc.title = "LWE algorithm"
