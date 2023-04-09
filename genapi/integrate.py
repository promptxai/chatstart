from googleapiclient.discovery import build
import pandas as pd
import json
import io
import streamlit as st

# Molecule Generator
from stmol import showmol
import py3Dmol
from rdkit import Chem
from rdkit.Chem import AllChem

def makeblock(smi):
    mol = Chem.MolFromSmiles(smi)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    mblock = Chem.MolToMolBlock(mol)
    return mblock

def is_valid_smiles(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        return mol is not None
    except:
        return False

def render_mol(xyz):
    xyzview = py3Dmol.view(height=400, width=650)
    xyzview.addModel(xyz,'mol')
    # xyzview.setStyle({'stick':{}})
    xyzview.setStyle({'stick':{}, 'sphere':{'radius':0.5}})
    xyzview.setBackgroundColor('white')
    xyzview.zoomTo()
    showmol(xyzview, height=500, width=750)

def molecule(conversation):
    num_quotes = conversation.count('"')
    prompt = conversation.split('"')[num_quotes - 1]
    if not is_valid_smiles(prompt):
        st.write('Invalid SMILES')
    else:
        blk=makeblock(prompt)
        render_mol(blk)
    return prompt

def stability(conversation, model, size=512):
    num_quotes = conversation.count('"')
    prompt = conversation.split('"')[num_quotes - 1]
    return model.generate_art_sd(prompt, size)

def dalle(conversation, model, size='1024x1024', separator='"'):
    num_separators = conversation.count(separator)
    prompt = conversation.split(separator)[num_separators - 1]
    response = model.image(prompt, size)      
    return response['data'][0]['url']

def google_image(conversation, key, cx, num):
    num_quotes = conversation.count('"')
    search_query = conversation.split('"')[num_quotes - 1]
    service = build("customsearch", "v1", developerKey=key)
    return (service.cse().list(q=search_query, cx=cx, num=num,
                                searchType="image", filter="1", safe="active",).execute())

def dataframe(conversation):
    num_csv = conversation.count('```')
    dataset_csv = conversation.split('```')[num_csv - 1]
    csv_source = io.StringIO(dataset_csv)
    return pd.read_table(csv_source, sep=",", index_col=1, skipinitialspace=True)

def vegalite(conversation):            
    num_jsons = conversation.count('```')
    chart_json = conversation.split('```')[num_jsons - 1]
    return json.loads(chart_json.replace('vega-lite {', '{').replace('json', ''))

def youtube(conversation):
    youtube_links = [link for link in conversation.split() if 'youtube.com' in link]
    return youtube_links[-1]
