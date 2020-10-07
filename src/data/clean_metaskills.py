# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('survey_number', type=click.INT, default=1)
@click.option('-o', '--output_filepath', type=click.Path())
def clean(survey_number: int, output_filepath: str) -> None:
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"cleaning metaskills #{survey_number}...")
    
    metaskills_path = f"data/raw/Metaskills_{survey_number}.csv"
    df = pd.read_csv(metaskills_path)
    num_to_text_map = extract_q_text(df)
    df = df.drop(df.index[[0, 1]])
    click.echo(df.head())

def extract_q_text(df: pd.DataFrame) -> pd.DataFrame:
    question_num_to_text = dict(zip(df.columns, df.loc[0, :]))
    return question_num_to_text

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    clean()
