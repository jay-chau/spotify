import matplotlib.pyplot as plt

colrs = {
    'green': (0.39,0.73,0.42,0.5), 
    'grey': (1, 1, 1, 0.6),
    'grey_trans': (1, 1, 1, 0.25),
    'grey_super_trans': (1,1,1, 0.05),
    'dark': "#121212"
}

assumption = {
    'max_value_x' : 1000, ## Hours of music
    'text_size': 8
}

def gen_plot(x=10.24,y=5.76, dpi=200):
    fig, ax = plt.figure(figsize=(x,y), dpi=dpi, facecolor="black"), plt.axes()
    ax.grid(True, axis='both',linestyle="--", linewidth=0.25, color=colrs['grey_trans'])
    ax.set_axisbelow(True)
    ax.set_facecolor(colrs['dark'])

    ## X axis
    ax.spines['bottom'].set_color(colrs['grey'])
    ax.xaxis.label.set_color(colrs['grey'])
    ax.tick_params(colors=colrs['grey'], axis='x')

    ## Y Axis
    ax.yaxis.label.set_color(colrs['grey'])
    ax.tick_params(colors=colrs['grey'], axis='y')

    return fig, ax

def set_label(x, y, title):
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)

def set_axis(x,y):
    if x != None:
        plt.xlim(x[0],x[1])
    if y != None:
        plt.ylim(y[0],y[1])

def show_save(save, savelocation, savefile):
    if save == False:
        plt.show()
    else:
        plt.savefig(savelocation+savefile)