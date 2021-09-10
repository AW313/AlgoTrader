# clean code
# - read the pdf (google: clean code pdf) for casual reading
# - functions
# - typing / typehinting
# - useful variable names
# - if reusing numbers, assign to a CONSTANT

# others:
# args, kwargs
# index against asx200
# catch specific errors (IndexError, etc) instead of blanket try/except
# extra reading: how to split code into separate files
# - e.g. asx program - one code file to crawl + save from yahoo, one code file to process, one code file to save to pdf
# - can ctrl-click on function name to hop to function definition
# - also right click to see where your function is used (Go To References)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages


pd.options.display.float_format = "{:,.2f}".format


# functions to create and merge pdf pages


def df_to_table(df: pd.DataFrame) -> matplotlib.figure.Figure:
    # https://stackoverflow.com/questions/32137396/how-do-i-plot-only-a-table-in-matplotlib
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis("tight")
    ax.axis("off")
    ax.table(cellText=df.values, colLabels=df.columns, loc="center")
    return fig


def append_dataframe_to_pdf(pdf: PdfPages, df: pd.DataFrame):
    fig = df_to_table(df)
    pdf.savefig(fig, bbox_inches="tight")


"""
def append_dataframe_to_pdf(*args, **kwargs):
    print(type(args))
    print(type(kwargs))
    print("args", args)
    print("kwargs", kwargs)
"""


def append_dfplot_to_pdf(pdf: PdfPages, df: pd.DataFrame, **kwargs):
    # https://stackoverflow.com/questions/35484458/how-to-export-to-pdf-a-graph-based-on-a-pandas-dataframe/35484726
    df.plot(**kwargs)
    pdf.savefig()


# _____________________________________________________________________

pp = PdfPages("foo.pdf")

# for num_rows in range(6, 11):
#     df = pd.DataFrame(np.random.random((num_rows, 2)), columns=("col 1", "col 2"))
#     append_dataframe_to_pdf(pp, df)
# append_dfplot_to_pdf(pp, df, x="col 1", y="col 2", kind="line")

# pp.close()

df = pd.read_csv("/home/ajw/Documents/VSstudio/ASX Scaper/Stockscrappy2/tsety22.csv")
append_dataframe_to_pdf(pp, df)
# append_dfplot_to_pdf(pp, df, x='buypice', y='3month$', kind='line')
pp.close()



#----------------------------------------------------

df = pd.read_csv('testdf.csv')