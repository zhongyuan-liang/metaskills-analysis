import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb
from scipy.stats import mannwhitneyu, kruskal
from typing import List
from statistics import mean, stdev
from math import sqrt


from src.analysis.analyze_intervention import join_w_grades, compare_treatment, drop_unfinished

agree = ["Slightly Agree", "Somewhat Agree", "Mostly Agree", "Strongly Agree"]
disagree = ["Strongly Disagree", "Mostly Disagree", "Somewhat Disagree", "Slightly Disagree"]
BAR_WIDTH = 0.4

likert_to_score = {"Strongly disagree": 1, "Mostly disagree": 2, "Somewhat disagree": 3, "Slightly disagree": 4, "Neither agree nor disagree": 5,
"Slightly Agree": 6, "Somewhat agree": 7, "Mostly agree": 8, "Strongly agree": 9}

def bar_chart(title: str, filename: str, **group_data: pd.Series) -> None:
    x_loc = np.arange(len(group_data))
    labels = []
    sample_size = []
    means = []
    sems = []
    rects = []

    fig, ax = plt.subplots()

    for i, (group_name, data) in enumerate(group_data.items()):
        labels.append(group_name)
        sample_size.append(len(data))
        mean = data.mean()
        means.append(mean)
        sem = data.sem()
        sems.append(sem)
        rect = ax.bar(x_loc[i], mean, BAR_WIDTH, yerr=sem, capsize=2.0)
        rects.append(rect)
    
    label_on_bar(ax, rects, sample_size, means, sems)

    ax.set_ylabel("Average Midterm Grade")
    ax.set_xlabel("Condition")
    ax.set_title(title)
    ax.set_xticks(x_loc)
    ax.set_xticklabels(labels)

    fig.tight_layout()
    plt.savefig(filename)

def label_on_bar(ax: matplotlib.axes.Axes, rects: matplotlib.container.BarContainer, sample_sizes: List, means: List, sems: List) -> None:
    for i, rect in enumerate(rects):
        height = rect.patches[0].get_height()
        N_sample, mean, sem = sample_sizes[i], "{:.3f}".format(means[i]), "{:.3f}".format(sems[i])
        info_str = f"N={N_sample}\nMean={mean}\nSEM={sem}"
        ax.annotate(info_str, xy=(rect.patches[0].get_x() + rect.patches[0].get_width() / 10, height / 2))

if __name__ == "__main__":
    grades_fpath = "data/interim/cleaned_grades.csv"
    metaskills_fpath = "data/interim/cleaned_metaskills_1.csv"
    midterm_survey_fpath = "data/interim/cleaned_midterm_survey.csv"

    df = join_w_grades(grades_fpath, metaskills_fpath)
    df = drop_unfinished(df, "Finished")

    stress_A = df.loc[(df["stress_A"] == "yes") & (df["stress_E"] == "no")]
    stress_C = df.loc[(df["stress_A"] == "no") & (df["stress_E"] == "yes")]

    A_only = df.loc[
        (((df["stress_A"] == "yes") &
        (df["stress_B"] == "no") ) &
        ((df["stress_C"] == "no") &
        (df["stress_D"] == "no"))) &
        ((df["stress_E"] == "no") &
        (df["stress_F"] == "no")) 
    ] #syntax ew
    B_only = df.loc[
        (((df["stress_A"] == "no") &
        (df["stress_B"] == "yes") ) &
        ((df["stress_C"] == "no") &
        (df["stress_D"] == "no"))) &
        ((df["stress_E"] == "no") &
        (df["stress_F"] == "no")) 
    ] 
    C_only = df.loc[
        (((df["stress_A"] == "no") &
        (df["stress_B"] == "no") ) &
        ((df["stress_C"] == "yes") &
        (df["stress_D"] == "no"))) &
        ((df["stress_E"] == "no") &
        (df["stress_F"] == "no")) 
    ] 
    D_only = df.loc[
        (((df["stress_A"] == "no") &
        (df["stress_B"] == "no") ) &
        ((df["stress_C"] == "no") &
        (df["stress_D"] == "yes"))) &
        ((df["stress_E"] == "no") &
        (df["stress_F"] == "no")) 
    ] 
    E_only = df.loc[
        (((df["stress_A"] == "no") &
        (df["stress_B"] == "no") ) &
        ((df["stress_C"] == "no") &
        (df["stress_D"] == "no"))) &
        ((df["stress_E"] == "yes") &
        (df["stress_F"] == "no")) 
    ] 
    F_only = df.loc[
        (((df["stress_A"] == "no") &
        (df["stress_B"] == "no") ) &
        ((df["stress_C"] == "no") &
        (df["stress_D"] == "no"))) &
        ((df["stress_E"] == "no") &
        (df["stress_F"] == "yes")) 
    ] 

    stress_A_grades = stress_A["Midterm Current Score"].dropna()
    stress_C_grades = stress_C["Midterm Current Score"].dropna()

    stress_A_enjoy = stress_A["Q58"].dropna().replace(likert_to_score)
    stress_C_enjoy = stress_C["Q58"].dropna().replace(likert_to_score)

    A_only_grades = A_only["Midterm Current Score"].dropna()
    B_only_grades = B_only["Midterm Current Score"].dropna()
    C_only_grades = C_only["Midterm Current Score"].dropna()
    D_only_grades = D_only["Midterm Current Score"].dropna()
    E_only_grades = E_only["Midterm Current Score"].dropna()
    F_only_grades = F_only["Midterm Current Score"].dropna()

    A_only_enjoy = A_only["Q58"].dropna()
    B_only_enjoy = B_only["Q58"].dropna()
    C_only_enjoy = C_only["Q58"].dropna()
    D_only_enjoy = D_only["Q58"].dropna()
    E_only_enjoy = E_only["Q58"].dropna()
    F_only_enjoy = F_only["Q58"].dropna()

    grades_enjoyed = df.loc[df["Q124"].isin(agree)]["Midterm Current Score"]
    grades_not_enjoyed = df.loc[df["Q124"].isin(disagree)]["Midterm Current Score"]

    cohens_d = (grades_enjoyed.mean() - grades_not_enjoyed.mean()) / (sqrt((grades_enjoyed.std() ** 2 + grades_not_enjoyed.std() ** 2) / 2))

    print(cohens_d)
    assert False

    #print(kruskal(A_only_grades, B_only_grades, C_only_grades, D_only_grades, E_only_grades, F_only_grades))
    #print(kruskal(A_only_enjoy, B_only_enjoy, C_only_enjoy, D_only_enjoy, E_only_enjoy, F_only_enjoy))

    total_sample_size = len(stress_A_grades) + len(stress_C_grades)
    enjoy_sample_size = len(stress_A_enjoy) + len(stress_C_enjoy)
    test_stat, p_val = mannwhitneyu(stress_A_grades, stress_C_grades)
    test_stat_enjoy, p_val_enjoy = mannwhitneyu(stress_A_enjoy, stress_C_enjoy)
    p_val = "{:.3f}".format(p_val)
    p_val_enjoy = "{:.3f}".format(p_val_enjoy)
    total_enjoy_opinion = len(grades_enjoyed) + len(grades_not_enjoyed)
    test_stat_enjoy_grades, p_val_enjoy_grades = mannwhitneyu(grades_enjoyed, grades_not_enjoyed)
    p_val_enjoy_grades = "{:.4f}".format(p_val_enjoy_grades)

    #bar_chart(f"Average Midterm Grade by Stress Intervention Received\n(N={total_sample_size}, p={p_val})", "bar_a_vs_e.png", **{"Stress Intervention A (text)": stress_A_grades, "Stress Intervention E (prompt)": stress_C_grades})
    #bar_chart(f"Average Enjoyment Score (1-9) by Stress Intervention Received\n(N={enjoy_sample_size}, p={p_val_enjoy})", "bar_a_vs_e_enjoy.png", **{"Stress Intervention A (text)": stress_A_enjoy, "Stress Intervention E (prompt)": stress_C_enjoy})
    bar_chart(f"Average Midterm Grade by Enjoyment of Modules\n(N={total_enjoy_opinion}, p={p_val_enjoy_grades})", "bar_enjoy_vs_grades.png", **{"Enjoyed metaskills modules": grades_enjoyed, "Did not enjoy metaskills modules": grades_not_enjoyed})




