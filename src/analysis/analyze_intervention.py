import pandas as pd
from scipy.stats import shapiro, mannwhitneyu, ttest_ind
from statsmodels.graphics.gofplots import qqplot_2samples
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pdb

from typing import List

experience_likert = {"1 = no experience": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9 = a lot of experience": 9}
year_likert = {"1": 1, "2": 2, "3": 3, "4": 4, "5 or above": 5}
agree = ["Slightly Agree", "Somewhat Agree", "Mostly Agree", "Strongly Agree"]
disagree = ["Strongly Disagree", "Mostly Disagree", "Somewhat Disagree", "Slightly Disagree"]

def make_qqplot(x: List, y: List) -> None:
    plt_x = sm.ProbPlot(x)
    plt_y = sm.ProbPlot(y)
    qqplot_2samples(plt_x, plt_y)
    plt.savefig("testing")

def join_w_grades(grades_filepath: str, metaskills_resp_filepath: str, left_col: str = "Q62_2", right_col: str = "SIS Login ID") -> pd.DataFrame:
    df_grades = pd.read_csv(grades_filepath)
    df_mskills1 = pd.read_csv(metaskills_resp_filepath)
    df = pd.merge(df_mskills1, df_grades, left_on=left_col, right_on=right_col)
    return df

def compare_treatment(df: pd.DataFrame, treatment_name: str, outcome_name: str) -> tuple:
    treatment_yes = df.loc[df[treatment_name] == "yes"]
    treatment_no = df.loc[df[treatment_name] == "no"]

    outcome_yes = treatment_yes[outcome_name]
    outcome_no = treatment_no[outcome_name]

    return outcome_yes, outcome_no

def drop_unfinished(df: pd.DataFrame, completion_col: str) -> pd.DataFrame:
    return df.loc[df[completion_col] == True]

def drop_after_midterm(df: pd.DataFrame, midterm_date_col: str) -> pd.DataFrame:
    return df.loc[df[midterm_date_col] == "before test"]

def drop_low_time(df: pd.DataFrame, time_col: str, min_time: int = 0.1) -> pd.DataFrame:
    return df.loc[df[time_col] >= min_time]

if __name__ == "__main__":
    grades_fpath = "D:/metaskills-analysis-main/metaskills-analysis-main/src/data/interim/cleaned_grades.csv"
    metaskills_fpath = "D:/metaskills-analysis-main/metaskills-analysis-main/src/data/interim/cleaned_metaskills_1.csv"
    midterm_survey_fpath = "D:/metaskills-analysis-main/metaskills-analysis-main/src/data/interim/cleaned_midterm_survey.csv"

    df = join_w_grades(grades_fpath, metaskills_fpath)
    #df_midterm_survey = pd.read_csv(midterm_survey_fpath)
    #df = pd.merge(df, df_midterm_survey, how="inner", left_on="Q62_2", right_on="Q2_2_TEXT")
    #df = drop_unfinished(df, "Finished_x")

    #experience_daily_yes, experience_daily_no = compare_treatment(df, "showdailyplan", "prior_experience")
    #experience_daily_yes, experience_daily_no = experience_daily_yes.dropna(), experience_daily_no.dropna()
    #experience_daily_yes, experience_daily_no = experience_daily_yes.replace(experience_likert), experience_daily_no.replace(experience_likert)
    #print(mannwhitneyu(list(experience_daily_yes), list(experience_daily_no)))

    #year_daily_yes, year_daily_no = compare_treatment(df, "showdailyplan", "Q216")
    #year_daily_yes, year_daily_no = year_daily_yes.dropna(), year_daily_no.dropna()
    #year_daily_yes, year_daily_no = year_daily_yes.replace(year_likert), year_daily_no.replace(year_likert)
    #print(mannwhitneyu(list(year_daily_yes), list(year_daily_no)))
    #assert False
    grades_stress_yes, grades_stress_no = compare_treatment(df, "show_stress", "Midterm Current Score")
    grades_stress_yes, grades_stress_no = grades_stress_yes.dropna(), grades_stress_no.dropna()

    grades_stress_A, _ = compare_treatment(df, "stress_A", "Midterm Current Score")
    grades_stress_A = grades_stress_A.dropna()

    grades_stress_C, _ = compare_treatment(df, "stress_C", "Midterm Current Score")
    grades_stress_C = grades_stress_C.dropna()

    grades_examplan_yes, grades_examplan_no = compare_treatment(df, "showexamplan", "Midterm Current Score")
    grades_examplan_yes, grades_examplan_no = grades_examplan_yes.dropna(), grades_examplan_no.dropna()

    grades_growth_yes, grades_growth_no = compare_treatment(df, "showgrowthmindset", "Midterm Current Score")
    grades_growth_yes, grades_growth_no = grades_growth_yes.dropna(), grades_growth_no.dropna()

    grades_daily_yes, grades_daily_no = compare_treatment(df, "showdailyplan", "Midterm Current Score")
    grades_daily_yes, grades_daily_no = grades_daily_yes.dropna(), grades_daily_no.dropna()

    grades_enjoyed = df.loc[df["Q124"].isin(agree)]["Midterm Current Score"]
    grades_not_enjoyed = df.loc[df["Q124"].isin(disagree)]["Midterm Current Score"]

    print(mannwhitneyu(grades_stress_yes, grades_stress_no))
    print(mannwhitneyu(grades_examplan_yes, grades_examplan_no))
    print(mannwhitneyu(grades_growth_yes, grades_growth_no))
    print(mannwhitneyu(grades_daily_yes, grades_daily_no))
    print(mannwhitneyu(grades_enjoyed, grades_not_enjoyed))
    assert False


    print(grades_stress_A.mean())
    print(grades_stress_A.std())
    print(grades_stress_C.mean())
    print(grades_stress_C.std())

    print(len(grades_stress_A))
    print(len(grades_stress_C))
    plt.hist(x=grades_daily_yes, density=True, label="Stress intervention A (text)", alpha=0.3)
    plt.hist(x=grades_daily_no, density=True, label="Stress intervention C (vid)", alpha=0.3)
    plt.xlabel("Midterm grade")
    plt.ylabel("Density")
    plt.legend()
    plt.savefig("hist_a_c.png")

    #print(shapiro(grades_daily_yes))
    #print(shapiro(grades_daily_no))


