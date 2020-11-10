# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from typing import List

PERSONAL_INFO_COLS = {
    1: [
        "Q62_1",
        "Q62_3",
        "Q14_Browser",
        "Q14_Version",
        "Q14_Operating System",
        "Q14_Resolution",
        "Q120",
        "IPAddress",
        "RecipientLastName",
        "RecipientFirstName",
        "RecipientEmail",
        "LocationLatitude",
        "LocationLongitude"
    ],
    2: [
        "Q10_1",
        "Q10_3",
        "Q12_Browser",
        "Q12_Version",
        "Q12_Operating System",
        "Q12_Resolution",
        "Q108_1",
        "Q168",
        "IPAddress",
        "RecipientLastName",
        "RecipientFirstName",
        "RecipientEmail",
        "LocationLatitude",
        "LocationLongitude"
    ],
    3: [
        "Q10_1",
        "Q10_3",
        "Q168",
        "Q523_Browser",
        "Q523_Version",
        "Q523_Operating System",
        "Q523_Resolution",
        "IPAddress",
        "RecipientLastName",
        "RecipientFirstName",
        "RecipientEmail",
        "LocationLatitude",
        "LocationLongitude"
    ],
    4: [
        "Q10_1",
        "Q10_3",
        "Q523_Browser",
        "Q523_Version",
        "Q523_Operating System",
        "Q523_Resolution",
        "Q168",
        "IPAddress",
        "RecipientLastName",
        "RecipientFirstName",
        "RecipientEmail",
        "LocationLatitude",
        "LocationLongitude"
    ], 
    5: [
        "Q10_1",
        "Q10_3",
        "Q523_Browser",
        "Q523_Version",
        "Q523_Operating System",
        "Q523_Resolution",
        "Q168",
        "IPAddress",
        "RecipientLastName",
        "RecipientFirstName",
        "RecipientEmail",
        "LocationLatitude",
        "LocationLongitude"
    ], 
    6: [
        "Q10_1",
        "Q10_3",
        "Q523_Browser",
        "Q523_Version",
        "Q523_Operating System",
        "Q523_Resolution",
        "Q168",
        "IPAddress",
        "RecipientLastName",
        "RecipientFirstName",
        "RecipientEmail",
        "LocationLatitude",
        "LocationLongitude"
    ],
    7: [ #There is no metaskills 7 - this is the grades sheet
        "Student",
        "ID"
    ]
}

@click.command()
@click.argument('survey_number', type=click.INT, default=1)
@click.option('-o', '--output_filepath', type=click.Path(), default="data/interim/cleaned_metaskills.csv")
@click.option('-c', '--consent_filepath', type=click.Path(), default="data/raw/classlist_consent/consenters_any.csv")
@click.option('-i', '--id_col', type=click.STRING, default="Q62_2")
def clean(survey_number: int, output_filepath: str, consent_filepath: str, id_col: str) -> None:
    logger = logging.getLogger(__name__)
    logger.info(f"cleaning metaskills #{survey_number}...")
    
    metaskills_path = f"data/interim/Metaskills_{survey_number}.csv"
    if survey_number == 7:
        metaskills_path = "data/interim/grades.csv"
    df = pd.read_csv(metaskills_path) 
    consenters = list(pd.read_csv(consent_filepath)["student_id"])
    num_to_text_map = extract_q_text(df)

    click.echo(df)
    click.echo(df.columns)

    df = remove_non_consenters(df, consenters, id_col)
    df = remove_personal_info_cols(df, survey_number)
    click.echo(df)
    click.echo(df.columns)

    df.to_csv(output_filepath, index=False)

def extract_q_text(df: pd.DataFrame) -> dict:
    question_num_to_text = dict(zip(df.columns, df.loc[0, :]))
    return question_num_to_text

def remove_non_consenters(df: pd.DataFrame, consenter_list: List, id_col: str) -> pd.DataFrame:
    return df[df[id_col].isin(consenter_list)]

def remove_personal_info_cols(df: pd.DataFrame, survey_number: int) -> pd.DataFrame:
    return df.drop(axis=1, labels=PERSONAL_INFO_COLS[survey_number])


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    clean()
