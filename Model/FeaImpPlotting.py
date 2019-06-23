import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_ft_imp(df,fea_imp):
    x_tick_label=list(df.columns)
    hist_val=fea_imp
    fig, ax = plt.subplots(figsize=(16,6))
    index=np.arange(len(fea_imp))
    ax.bar(index,hist_val, .3, color='r')
    ax.set_xticks(range(0, len(fea_imp), 1))
    ax.set_xticklabels(x_tick_label, rotation='vertical')
    plt.show()