import pandas as pd
from scipy.stats import shapiro, mannwhitneyu, ttest_ind
from statsmodels.graphics.gofplots import qqplot_2samples
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm

from typing import List

def make_qqplot(x: List, y: List) -> None:
    #x, y = sorted(x), sorted(y)
    plt_x = sm.ProbPlot(x)
    plt_y = sm.ProbPlot(y)
    qqplot_2samples(plt_x, plt_y)
    plt.savefig("testing")

if __name__ == "__main__":
    df_grades = pd.read_csv("data/interim/cleaned_grades.csv")
    df_mskills1 = pd.read_csv("data/interim/cleaned_metaskills_1.csv")
    df = pd.merge(df_mskills1, df_grades, left_on="Q62_2", right_on="SIS Login ID")

    stress_yes = df.loc[df["show_stress"] == "yes"]
    stress_no = df.loc[df["show_stress"] == "no"]

    exam_plan_yes = df.loc[df["showexamplan"] == "yes"]
    exam_plan_no = df.loc[df["showexamplan"] == "no"]

    growth_mindset_yes = df.loc[df["showgrowthmindset"] == "yes"]
    growth_mindset_no = df.loc[df["showgrowthmindset"] == "no"]

    daily_yes = df.loc[df["showdailyplan"] == "yes"]
    daily_no = df.loc[df["showdailyplan"] == "no"]

    grades_received_stress = stress_yes["Midterm Current Score"]
    grades_received_stress = grades_received_stress.dropna()
    grades_not_stress = stress_no["Midterm Current Score"]
    grades_not_stress = grades_not_stress.dropna()

    grades_received_examplan = exam_plan_yes["Midterm Current Score"]
    grades_received_examplan = grades_received_examplan.dropna()
    grades_not_examplan = exam_plan_no["Midterm Current Score"]
    grades_not_examplan = grades_not_examplan .dropna()

    grades_received_growth = growth_mindset_yes["Midterm Current Score"]
    grades_received_growth = grades_received_growth.dropna()
    grades_not_growth = growth_mindset_no["Midterm Current Score"]
    grades_not_growth = grades_not_growth.dropna()

    grades_daily_yes = daily_yes["Midterm Current Score"]
    grades_daily_yes = grades_daily_yes.dropna()
    grades_daily_no = daily_no["Midterm Current Score"]
    grades_daily_no = grades_daily_no.dropna()



    #make_qqplot(grades_received_stress, grades_not_stress)
    #print(ttest_ind(grades_received_stress, grades_not_stress))
    print(mannwhitneyu(grades_received_stress, grades_not_stress))
    print(mannwhitneyu(grades_received_examplan, grades_not_examplan))
    print(mannwhitneyu(grades_received_growth, grades_not_growth))
    print(mannwhitneyu(grades_daily_yes, grades_daily_no))

    # print(grades_received_stress)
    # print(grades_not_stress)
    plt.hist(x=grades_daily_yes, density=True, label="Received daily planning intervention", alpha=0.3)
    plt.hist(x=grades_daily_no, density=True, label="No daily planning intervention", alpha=0.3)
    plt.legend()
    plt.savefig("hist.png")

    #print(shapiro(grades_daily_yes))
    #print(shapiro(grades_daily_no))


