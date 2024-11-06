from django import template

register = template.Library()


@register.filter(name='separator')
def thousand_separator(value):
    try:
        val = "{:,}".format(value).replace(',', '.')
    except:
        val = value
    return val

@register.filter(name='estado_funcionario')
def estado_funcionario(value):
    d = {
            0: 'Rechazada',
            1: 'Aceptada',
            2: 'Requerimientos pendientes',
            3: 'Presupuesto pendiente',
            4: 'Firma pendiente',
            5: 'Orden de compra pendiente'
            }

    return d[value]
