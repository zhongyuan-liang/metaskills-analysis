import pandas as pd
import pdb

from src.analysis.analyze_intervention import join_w_grades, compare_treatment, drop_unfinished, drop_after_midterm, drop_low_time

grades_fpath = "D:/metaskills-analysis-main/metaskills-analysis-main/src/data/interim/cleaned_grades.csv"
metaskills_fpath = "D:/metaskills-analysis-main/metaskills-analysis-main/src/data/interim/cleaned_metaskills_1.csv"
metaskills_2_fpath = "D:/metaskills-analysis-main/metaskills-analysis-main/src/data/interim/cleaned_metaskills_2.csv"
midterm_survey_fpath = "D:/metaskills-analysis-main/metaskills-analysis-main/src/data/interim/cleaned_midterm_survey.csv"

df = join_w_grades(grades_fpath, metaskills_fpath)
df = drop_unfinished(df, "Finished")
df = drop_after_midterm(df, "survey_taken")

META_1 = df.copy()

df = drop_low_time(df, "stress_int_minutes")

META_1_ENGAGED = df.copy()

df_midterm_survey = pd.read_csv(midterm_survey_fpath)
df = pd.merge(META_1, df_midterm_survey, how="inner", left_on="Q62_2", right_on="Q2_2_TEXT")

META_1_AND_MIDTERM = df.copy()

META_1_AND_MIDTERM_ENGAGED = pd.merge(META_1_ENGAGED, df_midterm_survey, how="inner", left_on="Q62_2", right_on="Q2_2_TEXT")

df_2 = pd.read_csv(metaskills_2_fpath)
df_2 = drop_unfinished(df_2, "Finished")
META_2 = df_2.copy()
META_1_AND_META_2 = pd.merge(META_1, df_2, how="inner", left_on="Q62_2", right_on="Q10_2")
META_1_AND_META_2_ENGAGED = pd.merge(META_1_ENGAGED, df_2, how="inner", left_on="Q62_2", right_on="Q10_2")

META_1_2_AND_MIDTERM = pd.merge(META_1_AND_MIDTERM, META_2, how="inner", left_on="Q62_2", right_on="Q10_2")
META_1_2_AND_MIDTERM_ENGAGED = pd.merge(META_1_AND_MIDTERM_ENGAGED, META_2, how="inner", left_on="Q62_2", right_on="Q10_2")

def stress_specific_intervention_and_grades(intervention_letter: str, engaged: bool = False) -> tuple:
    intervention_letter = intervention_letter.upper()
    if intervention_letter not in ["A", "B", "C", "D", "E", "F"]:
        raise ValueError("Intervention letter must be in range A...F")
    if engaged:
        df = META_1_AND_MIDTERM_ENGAGED
    else:
        df = META_1_AND_MIDTERM
    stress_yes = df.loc[df[f"stress_{intervention_letter}"] == "yes"]["Midterm Current Score"].dropna()
    stress_no = df.loc[df[f"stress_{intervention_letter}"] == "no"]["Midterm Current Score"].dropna()

    return stress_yes, stress_no

def stress_intervention_and_grades(by_year: bool = False, engaged: bool = False) -> tuple:
    if engaged:
        df_engaged = META_1_2_AND_MIDTERM_ENGAGED
        df = META_1_2_AND_MIDTERM
    else:
        df_engaged = META_1_2_AND_MIDTERM
        df = META_1_2_AND_MIDTERM

    grades_stress_yes = df_engaged.loc[df_engaged["show_stress"] == "yes"]
    grades_stress_no = df.loc[df["show_stress"] == "no"]

    grades_stress_yes, grades_stress_no = grades_stress_yes.dropna(subset=["Q216", "Midterm Current Score"]), grades_stress_no.dropna(subset=["Q216", "Midterm Current Score"])

    stress_first_year = grades_stress_yes.loc[grades_stress_yes["Q216"] == "1"]["Midterm Current Score"]
    stress_other = grades_stress_yes.loc[grades_stress_yes["Q216"] != "1"]["Midterm Current Score"]

    no_stress_first_year = grades_stress_no.loc[grades_stress_no["Q216"] == "1"]["Midterm Current Score"]
    no_stress_other = grades_stress_no.loc[grades_stress_no["Q216"] != "1"]["Midterm Current Score"]

    if by_year:
        return stress_first_year, no_stress_first_year, stress_other, no_stress_other

    return grades_stress_yes["Midterm Current Score"], grades_stress_no["Midterm Current Score"]

def stress_intervention_and_stress_question(divide_by_year: bool = False, engaged: bool = False) -> tuple:
    if engaged:
        df_engaged = META_1_2_AND_MIDTERM_ENGAGED
        df = META_1_2_AND_MIDTERM
    else:
        df = META_1_2_AND_MIDTERM
        df_engaged = df

    grades_stress_yes = df_engaged.loc[df_engaged["show_stress"] == "yes"]
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

    stress_answers_yes = grades_stress_yes["Q51_y"].astype(int)
    stress_answers_no = grades_stress_no["Q51_y"].astype(int)

    if divide_by_year:
        return stress_answers_yes_first_year, stress_answers_no_first_year, stress_answers_yes_upper_year, stress_answers_no_upper_year

    return stress_answers_yes, stress_answers_no

def enjoyment_and_midterm_grade(divide_by_year: bool = False) -> tuple:
    raise NotImplementedError

def student_year_and_enjoyment():
    raise NotImplementedError

def stress_intervention_and_midterm_grade_by_language_ability():
    raise NotImplementedError

def stress_intervention_and_midterm_grade_by_gender(engaged: bool = False):
    if engaged:
        df_engaged = META_1_AND_MIDTERM_ENGAGED
        df = META_1_AND_MIDTERM
    else:
        df = META_1_AND_MIDTERM
        df_engaged = df

    grades_stress_yes = df_engaged.loc[df_engaged["show_stress"] == "yes"]
    grades_stress_no = df.loc[df["show_stress"] == "no"]

    grades_stress_yes_male = grades_stress_yes.loc[grades_stress_yes["gender"] == "Male"]
    grades_stress_no_male = grades_stress_no.loc[grades_stress_no["gender"] == "Male"]

    grades_stress_yes_female = grades_stress_yes.loc[grades_stress_yes["gender"] == "Female"]
    grades_stress_no_female = grades_stress_no.loc[grades_stress_no["gender"] == "Female"]

    grades_stress_yes_male = grades_stress_yes_male["Midterm Current Score"].dropna().astype(int)
    grades_stress_yes_female = grades_stress_yes_female["Midterm Current Score"].dropna().astype(int)

    grades_stress_no_male = grades_stress_no_male["Midterm Current Score"].dropna().astype(int)
    grades_stress_no_female = grades_stress_no_female["Midterm Current Score"].dropna().astype(int)

    return grades_stress_yes_male, grades_stress_no_male, grades_stress_yes_female, grades_stress_no_female


def stress_intervention_and_midterm_grade_by_growth_mindset():
    raise NotImplementedError

if __name__ == "__main__":
    stress_intervention_and_grades("A")



