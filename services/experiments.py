import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt


def accuracy():
    labels = ["Tip Toe", "Toe Clenches", "Toe lift", "Rest"]
    # array = [[49,1,0,0],
    #          [0, 45, 2, 3],   
    #          [0, 0, 49, 1],
    #          [0, 0, 0, 50]]

    array = [[19, 1, 0, 0],
             [0, 19, 1, 0],
             [0, 0, 20, 0],
             [0, 0, 0, 20]]

    # array = [[20,0,0,0],
    #          [2, 15, 3, 0],   
    #          [0, 2, 17, 1],
    #          [0, 0, 0, 20]]
    df_cm = pd.DataFrame(array, range(4), range(4))
    # plt.figure(figsize=(10,7))
    sn.set(font_scale=1.4)  # for label size
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}, xticklabels=labels, yticklabels=labels,
               cmap='Blues')  # font size
    plt.yticks(rotation=0)
    plt.xticks(rotation=0)
    plt.show()


def main():
    accuracy()
    pass


if __name__ == '__main__':
    main()
