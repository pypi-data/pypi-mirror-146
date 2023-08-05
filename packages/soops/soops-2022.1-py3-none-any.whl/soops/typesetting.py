def format_float(val, prec):
    if val == 0.0:
        return '0'

    else:
        fmt = '{{:.{}e}}'.format(prec)
        sval = fmt.format(val)
        iexp = list(map(float, sval.split('e')))
        iexp[1] = int(iexp[1])
        return r'${} \cdot 10^{{{}}}$'.format(*iexp)

def format_float2(val, prec):
    fmt = '{{:.{}e}}'.format(prec)
    aux = fmt.format(val)
    return aux.replace('.', ':') # Make LaTeX happy.
