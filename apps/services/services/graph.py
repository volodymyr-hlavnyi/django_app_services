import matplotlib.pyplot as plt
import base64
import logging
from io import BytesIO


def get_graph(float_list, client_list):
    logger = logging.getLogger("django")
    result = None

    try:
        if float_list:

            if len(float_list) > 0:
                chart_max_value = max(float_list)
                float_names = client_list
            else:
                chart_max_value = 0
                float_names = []

            logger.info(f"----- float_names: {float_names}")
            logger.info(f"----- float_list: {float_list}")

            fig, ax = plt.subplots()

            bar_container = ax.bar(float_names, float_list)
            ax.set(ylabel='Earning',
                   title='Earning by action',
                   ylim=(0, 2 * chart_max_value),
                   autoscale_on=True
            )
            ax.bar_label(bar_container, fmt='{:,.0f}')
            ax.set_title('Earning by action')
            ax.legend()

            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())

            result = string.decode('utf-8')
        else:
            result = None

    except Exception as e:
        logger.error(f"Graph error: Error in graph definition! - {e}")

    return result
