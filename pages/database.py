import os
import pickle
from typing import Dict
import yaml 
import pandas as pd
import streamlit as st
from sample_utils import perform_cleanup


cfg = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)
PKL_PATH = cfg['PATH']["PKL_PATH"]
DATASET_DIR = cfg['PATH']["DATASET_DIR"]
st.set_page_config(layout="wide")




if 'initialized' not in st.session_state:
    st.session_state.initialized = False

if not st.session_state.initialized:
    perform_cleanup(PKL_PATH)
    st.session_state.initialized = True






def load_database() -> Dict[int, Dict[str, str]]:
    """
    Load the database from the pickle file.

    Returns:
        Dict[int, Dict[str, str]]: A dictionary containing person information,
            where the keys are indices and the values are dictionaries with
            'id', 'name', and 'image' keys.
    """
    try:
        with open(PKL_PATH, "rb") as file:
            database = pickle.load(file)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(DATASET_DIR), exist_ok=True)
        open(PKL_PATH, "wb").close()
        database = {}
    except Exception as e:
        # st.error(f"Error loading database: {e}")
        database = {}

    return database


def render_database(database: Dict[int, Dict[str, str]]):
    """
    Render the database in a tabular format using Streamlit.

    Args:
        database (Dict[int, Dict[str, str]]): A dictionary containing person
            information, where the keys are indices and the values are
            dictionaries with 'id', 'name', and 'image' keys.
    """
    index, id_col, name_col, image_col = st.columns([0.5, 0.5, 3, 3])
    if database:
        for idx, person in database.items():
            with index:
                st.write(idx+1)
            with id_col:
                st.write(person["id"])
            with name_col:
                st.write(person["name"])
            with image_col:
                st.image(person["image"], width=200)
    else:
        st.error("Soory,No Data Found!")



def main():
    database = load_database()
    render_database(database)


if __name__ == "__main__":
    main()
