# Code for anonymizing utorid data

# Libraries
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os
import pandas as pd
import hashlib

@click.command()
@click.argument('in_filepath', type=click.Path(exists=True))
@click.argument('out_filepath', type=click.Path(), default="data/interim/anonymized.csv")
@click.option('-c', "--column", type=click.STRING, default="utorid")
@click.option('-d', "--drop_nrows", type=click.INT, default=0)
def anonymize(in_filepath: str, out_filepath: str, column: str, drop_nrows: int) -> None:
    # Open CSV
    stud_csv = pd.read_csv(in_filepath, dtype=str)
    stud_csv = stud_csv.iloc[drop_nrows:]

    # Number of students
    n_stud = stud_csv.shape[0]

    stud_csv[column] = stud_csv[column].apply(lambda x: hashlib.sha512(str(x).encode()).hexdigest())

    # Keep certain columns 
    stud_csv.to_csv(out_filepath, index=False)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    anonymize()



    


    
