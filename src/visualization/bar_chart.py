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
from src.data.subset import *

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

    ax.set_ylabel("Average Stress Level")
    ax.set_xlabel("Condition")
    ax.set_title(title)
    ax.set_xticks(x_loc)
    ax.set_xticklabels(labels)

    fig.tight_layout()
    plt.savefig(filename)

def cohens_d(first_group, second_group) -> float:
    return (first_group.mean() - second_group.mean()) / (sqrt((first_group.std() ** 2 + second_group.std() ** 2) / 2))


def label_on_bar(ax: matplotlib.axes.Axes, rects: matplotlib.container.BarContainer, sample_sizes: List, means: List, sems: List) -> None:
    for i, rect in enumerate(rects):
        height = rect.patches[0].get_height()
        N_sample, mean, sem = sample_sizes[i], "{:.3f}".format(means[i]), "{:.3f}".format(sems[i])
        info_str = f"N={N_sample}\nMean={mean}\nSEM={sem}"
        ax.annotate(info_str, xy=(rect.patches[0].get_x() + rect.patches[0].get_width() / 10, height / 2))

if __name__ == "__main__":
    grades_stress_yes_male, grades_stress_no_male, grades_stress_yes_female, grades_stress_no_female = stress_intervention_and_midterm_grade_by_gender()
    total_students = len(grades_stress_yes_female) +  len(grades_stress_no_female) 
    _, p_val = mannwhitneyu(grades_stress_yes_female, grades_stress_no_female)
    bar_chart(f"Average Midterm grade\n based on stress intervention for female students\n(N={total_students}, p={p_val})","stress_female.png", **{"Received stress intervention female": grades_stress_yes_female, 
    #"Received stress intervention female": grades_stress_yes_female, 
    "Did not receive \nstress intervention female": grades_stress_no_female, })
    print(cohens_d(grades_stress_yes_female, grades_stress_no_female))
    #"Did not receive \nstress intervention female": grades_stress_no_female})
    assert False
    grades_fpath = "data/interim/cleaned_grades.csv"
    metaskills_fpath = "data/interim/cleaned_metaskills_1.csv"
    metaskills_2_fpath = "data/interim/cleaned_metaskills_2.csv"
    midterm_survey_fpath = "data/interim/cleaned_midterm_survey.csv"

    df = join_w_grades(grades_fpath, metaskills_fpath)
    df = drop_unfinished(df, "Finished")
    df_2 = pd.read_csv(metaskills_2_fpath)
    df_2 = drop_unfinished(df_2, "Finished")
    df_midterm_survey = pd.read_csv(midterm_survey_fpath)
    df = pd.merge(df, df_midterm_survey, how="inner", left_on="Q62_2", right_on="Q2_2_TEXT")
    #df = pd.merge(df, df_2, how="inner", left_on="Q62_2", right_on="Q10_2")
    stress_A = df.loc[df["stress_F"] == "yes"]["Midterm Current Score"].dropna()
    stress_not_A = df.loc[df["stress_F"] == "no"]["Midterm Current Score"].dropna()

    total_students = len(stress_A) + len(stress_not_A)
    _, p_val_stress = mannwhitneyu(stress_A, stress_not_A)

    bar_chart(f"Average Midterm Grade\n based on stress intervention\n(N={total_students}, p={p_val_stress})", "stress_F_vs_not.png", **{"Received stress intervention F": stress_A, "Did not receive \nstress intervention F": stress_not_A})

    assert False



    #df = drop_unfinished(df, "Finished_x")

    # look at overall stress intervention
    #Q216 - year of study
    grades_stress_yes = df.loc[df["show_stress"] == "yes"]
    grades_stress_no = df.loc[df["show_stress"] == "no"]

    grades_stress_yes = grades_stress_yes.dropna(subset=["Q51_y"])
    grades_stress_yes["Q51_y"] = grades_stress_yes["Q51_y"].apply(lambda x: '0' if 'not troubled' in x else x)
    grades_stress_yes["Q51_y"] = grades_stress_yes["Q51_y"].apply(lambda x: '10' if 'very troubled' in x else x)  
    grades_stress_yes_first_year = grades_stress_yes.loc[grades_stress_yes["Q216"] == "1"]
    grades_stress_yes_upper_year = grades_stress_yes.loc[grades_stress_yes["Q216"] != "1"]

    grades_stress_no = grades_stress_no.dropna(subset=["Q51_y"])
    grades_stress_no["Q51_y"] = grades_stress_no["Q51_y"].apply(lambda x: '0' if 'not troubled' in x else x)
    grades_stress_no["Q51_y"] = grades_stress_no["Q51_y"].apply(lambda x: '10' if 'very troubled' in x else x) 
    grades_stress_no_first_year = grades_stress_no.loc[grades_stress_no["Q216"] == "1"]
    grades_stress_no_upper_year = grades_stress_no.loc[grades_stress_no["Q216"] != "1"] 

    stress_answers_yes_first_year = grades_stress_yes_first_year["Q51_y"].astype(int)
    stress_answers_no_first_year = grades_stress_no_first_year["Q51_y"].astype(int)
    stress_answers_yes_upper_year = grades_stress_yes_upper_year["Q51_y"].astype(int)
    stress_answers_no_upper_year = grades_stress_no_upper_year["Q51_y"].astype(int)

    total_students = len(stress_answers_yes_first_year) + len(stress_answers_no_first_year)
    _, p_val_stress = mannwhitneyu(stress_answers_yes_first_year, stress_answers_no_first_year)

    bar_chart(f"Average Stress Level (0-10)\n based on stress intervention for first-year students\n(N={total_students}, p={p_val_stress})", "stress_q51_first_year.png", **{"Received stress intervention": stress_answers_yes_first_year, "Did not receive \nstress intervention": stress_answers_no_first_year})

    assert False
    
    grades_stress_yes, grades_stress_no = grades_stress_yes.dropna(subset=["Q216", "Midterm Current Score"]), grades_stress_no.dropna(subset=["Q216", "Midterm Current Score"])

    stress_first_year = grades_stress_yes.loc[grades_stress_yes["Q216"] == "1"]["Midterm Current Score"]
    stress_other = grades_stress_yes.loc[grades_stress_yes["Q216"] != "1"]["Midterm Current Score"]

    no_stress_first_year = grades_stress_no.loc[grades_stress_no["Q216"] == "1"]["Midterm Current Score"]
    no_stress_other = grades_stress_no.loc[grades_stress_no["Q216"] != "1"]["Midterm Current Score"]

    #total_students = len(stress_first_year) + len(stress_other) + len(no_stress_first_year) + len(no_stress_other)
    total_students = len(stress_other) + len(no_stress_other) 
    #_, p_val_grades = kruskal(stress_first_year, stress_other, no_stress_first_year, no_stress_other)
    _, p_val_grades = mannwhitneyu(stress_other, no_stress_other)
    
    cohens_d = (stress_first_year.mean() - no_stress_first_year.mean()) / (sqrt((stress_first_year.std() ** 2 + no_stress_first_year.std() ** 2) / 2))
    print(cohens_d)
    bar_chart(f"Average Midterm Grade for upper-year students\n based on stress intervention\n(N={total_students}, p={p_val_grades})", "upper_year_stress.png", **{"Received stress intervention": stress_other, "Did not receive\nstress intervention": no_stress_other})

    assert False

    

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




