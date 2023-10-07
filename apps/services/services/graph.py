import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO


def get_graph(float_list):
    plt.style.use('_mpl-gallery')

    chart_len = len(float_list)
    chart_max_value = max(float_list)
    float_names = ['1st', '2nd']

    fig, ax = plt.subplots()

    bar_container = ax.bar(float_names, float_list)
    ax.set(ylabel='Earning', title='Earning by action', ylim=(0, 2 * chart_max_value))
    ax.bar_label(bar_container, fmt='{:,.0f}')

    ax.set_title('Earning by action')
    ax.legend()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return string.decode('utf-8')
