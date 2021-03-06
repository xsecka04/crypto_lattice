import json
from bokeh.models import ColumnDataSource, Div, TextInput, Range1d, Button, CustomJS, RadioButtonGroup
from bokeh.layouts import row, column
from bokeh.plotting import figure

import numpy as np
from os.path import dirname, join

#JSON Encoder
class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def alg_app(doc):

    #Set print numPy matrices to max 20 elements 
    np.set_printoptions(threshold=20)

    #numPy to JSON parser
    def lwe_to_json(A, s, e, B, ap, pp ,ep ,dec, q):
        ret = {"A": A,
                "s": s,
                "e": e,
                "B": B,
                "ap": ap,
                "pp": int(pp),
                "ep": int(ep),
                "dec": int(dec),
                "q": int(q)}

        enc = json.dumps(ret, cls=NumpyArrayEncoder)
        return enc

    #numPy matrix to LaTeX parser
    def pmatrix(a):
        lines = str(a).replace('[', '').replace(']', '').splitlines()
        rv = [r'\begin{pmatrix}']
        rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
        rv +=  [r'\end{pmatrix}']
        return '\n'.join(rv)
    
    #Parameters calc
    def calculate_lwe_params(n,q):
        m = int(np.ceil(1.1 * np.log(q) * n)) #1.1 works much better in lower dimensions than 2
        A = np.random.randint(low=-q,high=q,size=(m,n))
        s = np.random.randint(low=-q,high=q,size=n)
        e = np.random.randint(-1,1,size=m)

        s = np.transpose(s)
        e = np.transpose(e)

        B = np.mod(np.add(np.dot(A,s), e), q)
        return A,s,e,B,m

    #Encryption
    def calculate_lwe_enc(A,B,q, message):
        ap = np.mod(A.sum(axis=0),q)
        pp = (B.sum() + message * q//2) % q
        return ap, pp

    #Decryption
    def calculate_lwe_dec(s,q,ap,pp):
        ep = (pp - np.dot(ap, s)) % q 
        decrypted = 1 if (q//2-(q//4)) < ep < (q//2+(q//4)) else 0
        return ep, decrypted

    #The whole protocol
    def calculate_lwe(n,q,message):
        A,s,e,B,m = calculate_lwe_params(n,q)
        ap,pp = calculate_lwe_enc(A,B,q, message)
        ep,decrypted = calculate_lwe_dec(s,q,ap,pp)

        #print(f'Range ({(q//2-q//4)}, {(q//2+(q//4))})')

        return A,s,e,B,decrypted,ep, ap, pp, m
    
    #Initial params
    n = 4
    q = 17
    message = 0
    A,s,e,B,decrypted,ep, ap, pp, m = calculate_lwe(n,q,message)

    #Table sources
    source = ColumnDataSource(data=dict(n=[n], m=[m], q=[q], msg=[message], dec=[decrypted], ciph=[ep], pp=[pp]))
    bsource = ColumnDataSource(data=dict(A=A, B=B))
    csource = ColumnDataSource(data=dict(s=s, ap=ap))
    dsource = ColumnDataSource(data=dict(e=e))

    #Unit circle calc
    ep = int(source.data['ciph'][0])
    epx=np.sin((2*np.pi/17)*ep)
    epy=np.cos((2*np.pi/17)*ep)

    esource = ColumnDataSource(data=dict(epx=[epx], epy=[epy]))

    #Figure definition
    p2 = figure(plot_width=250, plot_height=250, match_aspect=True, tools="") 

    p2.x_range = Range1d(-1.3, 1.3)
    p2.y_range = Range1d(-1.3, 1.3)
    p2.circle(0,0,radius=1,fill_color=None,line_color='OliveDrab')
    p2.circle('epx', 'epy', source=esource,size=10,color="navy")


    #Callbacks
    def lwe_callback(event):
        try:
            message = int(message_input.value)
        except ValueError:
            message = 0
        try:
            n = int(n_input.value)
        except ValueError:
            n = 3
        try:
            q = int(q_input.value)
        except ValueError:
            q = 17


        A,s,e,B,decrypted,ep, ap, pp, m = calculate_lwe(n,q,message)
        source.data = dict(n=[n], m=[m], q=[q], msg=[message], dec=[decrypted],ciph=[ep], pp=[pp])
        bsource.data = dict(A=A, B=B)
        csource.data = dict(s=s, ap=ap)
        dsource.data = dict(e=e)

        private.text = f"Private key: $$s={pmatrix(csource.data['s'])}$$, $$e={pmatrix(dsource.data['e'])}$$"
        public.text = f"Public key: $$A={pmatrix(bsource.data['A'])}$$, $$p={pmatrix(bsource.data['B'])}$$"
        enc_pair.text=r"$$a' = \sum_I " + f"{pmatrix(bsource.data['A'])} = {pmatrix(csource.data['ap'])}$$"
        enc_pair2.text=r"$$p' = " + r"\sum_I " + f"{pmatrix(bsource.data['B'])} + {source.data['msg'][0]} " + r"*\lfloor \frac{" + f"{source.data['q'][0]}" +r"}{2} \rfloor = " + f"{source.data['pp'][0]}$$"
        dec_pair.text=f"$$ {source.data['pp'][0]} - {pmatrix(csource.data['ap'])} \\times {pmatrix(csource.data['s'])}^\\top = {source.data['ciph'][0]} $$"
        dec_pair2.text=f"$$ Dec({source.data['ciph'][0]})=" + r"\begin{cases} 0, & \text{if } x \sim 0 \\ 1, & \text{if } x \sim " + f"{source.data['q'][0]}/2" + r"\end{cases}" + f" = {source.data['dec'][0]}$$"


    def lwe_keygen_callback(event):
        #Sanitization and upper input limits
        try:
            n = int(n_input.value)
            if n > 1000:
                raise ValueError
        except ValueError:
            n = 3
        try:
            q = int(q_input.value)
            if q > 100000:
                raise ValueError
        except ValueError:
            q = 17

        A,s,e,B,m = calculate_lwe_params(n,q)

        source.data['n'] = [n]
        source.data['m'] = [m]
        source.data['q'] = [q]
        bsource.data = dict(A=A, B=B)
        csource.data['s'] = s
        dsource.data = dict(e=e)

        private.text = f"Private key: $$s={pmatrix(csource.data['s'])}^\\top$$ $$e={pmatrix(dsource.data['e'])}^\\top$$"
        public.text = f"Public key: $$A={pmatrix(bsource.data['A'])}$$ $$p={pmatrix(bsource.data['B'])}^\\top$$"

    def lwe_enc_callback(event):

        message = int(message_input.active)

        ap,pp = calculate_lwe_enc(bsource.data['A'],bsource.data['B'],int(source.data['q'][0]), message)
        
        source.data['msg'] = [message]
        csource.data['ap'] = ap
        source.data['pp'] = [pp]

        enc_pair.text=r"$$a' = \sum_I " + f"{pmatrix(bsource.data['A'])} = {pmatrix(csource.data['ap'])}$$"
        enc_pair2.text=r"$$p' = " + r"\sum_I " + f"{pmatrix(bsource.data['B'])} + {source.data['msg'][0]} " + r"*\lfloor \frac{" + f"{source.data['q'][0]}" +r"}{2} \rfloor = " + f"{source.data['pp'][0]}$$"

    def lwe_dec_callback(event):

        ep,decrypted = calculate_lwe_dec(csource.data['s'],int(source.data['q'][0]),csource.data['ap'],int(source.data['pp'][0]))

        source.data['ciph'] = [ep]
        source.data['dec'] = [decrypted]

        dec_pair.text=f"$$ e' = {source.data['pp'][0]} - {pmatrix(csource.data['ap'])} $$ <br> $$\\times {pmatrix(csource.data['s'])}^\\top = {source.data['ciph'][0]} $$"
        dec_pair2.text=f"$$ Dec({source.data['ciph'][0]})=" + r"\begin{cases} 0, & \text{if } x \sim 0 \\ 1, & \text{if } x \sim " + f"{source.data['q'][0]}/2" + r"\end{cases}" + f" = {source.data['dec'][0]}$$"

        ep = int(source.data['ciph'][0])
        q = int(source.data['q'][0])
        epx=np.sin((2*np.pi/q)*ep)
        epy=np.cos((2*np.pi/q)*ep)
        esource.data=dict(epx=[epx], epy=[epy])

        ret.text = lwe_to_json(bsource.data['A'], csource.data['s'], dsource.data['e'], bsource.data['B'], csource.data['ap'], source.data['pp'][0] ,source.data['ciph'][0] ,source.data['dec'][0], source.data['q'][0])


    #Invisible Div containing the JSON data
    ret = Div(text=lwe_to_json(bsource.data['A'], csource.data['s'], dsource.data['e'], bsource.data['B'], csource.data['ap'], source.data['pp'][0] ,source.data['ciph'][0] ,source.data['dec'][0], source.data['q'][0]))

    #Divs containing LaTeX data
    private = Div(text=f"""Private key: $$s={pmatrix(csource.data['s'])}^\\top$$ $$e={pmatrix(dsource.data['e'])}^\\top$$""", width=200, height=50)
    public = Div(text=f"""Public key: $$A={pmatrix(bsource.data['A'])}$$ $$p={pmatrix(bsource.data['B'])}^\\top$$""", width=200, height=200)

    button = Button(label="Recalculate keys", button_type="default")
    button.on_click(lwe_callback)

    message_input = RadioButtonGroup(labels=["0", "1"], active=0)

    n_input = TextInput(value="4", title="Dimension n:")
    q_input = TextInput(value="17", title="Prime number:")

    enc_pair = Div(text=r"$$a' = \sum_I " + f"{pmatrix(bsource.data['A'])} = {pmatrix(csource.data['ap'])}$$", width=300, height=150)
    enc_pair2 = Div(text=r"$$p' = " + r"\sum_I " + f"{pmatrix(bsource.data['B'])} + {source.data['msg'][0]} " + r"*\lfloor \frac{" + f"{source.data['q'][0]}" +r"}{2} \rfloor = " + f"{source.data['pp'][0]}$$", width=300, height=50)

    dec_pair = Div(text=f"$$ e' = {source.data['pp'][0]} - {pmatrix(csource.data['ap'])} $$ <br> $$ \\times {pmatrix(csource.data['s'])}^\\top = {source.data['ciph'][0]} $$", width=750, height=50)
    dec_pair2 = Div(text=f"$$ Dec({source.data['ciph'][0]})=" + r"\begin{cases} 0, & \text{if } x \sim 0 \\ 1, & \text{if } x \sim " + f"{source.data['q'][0]}/2" + r"\end{cases}" + f" = {source.data['dec'][0]}$$", width=600, height=50)


    download_button = Button(label="Download", button_type="success")
    download_button.js_on_event("button_click", CustomJS(args=dict(source=ret),
                            code=open(join(dirname(__file__), "download.js")).read()))


    #Protocol structure
    key = Div(text="<h5>Key Generator</h5>", width=300, height=30)
    key_button = Button(label="Generate keys", button_type="success")
    key_button.on_click(lwe_keygen_callback)
    keygen_row = row(column(key, n_input, q_input, key_button), column(public,private))

    enc = Div(text="<h5>Encryption</h5>", width=300, height=30)
    enc_button = Button(label="Encrypt the message", button_type="success")
    enc_button.on_click(lwe_enc_callback)
    enc_row = row(column(enc, message_input, enc_button), column(enc_pair,enc_pair2))

    dec = Div(text="<h5>Decryption</h5>", width=300, height=30)
    dec_button = Button(label="Decrypt the message", button_type="success")
    dec_button.on_click(lwe_dec_callback)
    dec_row = row(column(dec, dec_button, download_button), column(dec_pair,dec_pair2), p2)


    protocol = column(keygen_row, enc_row, dec_row)

    doc.add_root(protocol)

    doc.title = "LWE protocol"
