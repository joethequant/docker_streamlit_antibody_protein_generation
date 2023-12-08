# pip freeze > requirements.txt
# https://blog.runpod.io/serverless-create-a-basic-api/

import time
import streamlit as st
from PIL import Image
import helpers.sidebar as sidebar
import requests
import os
from dotenv import load_dotenv
load_dotenv()


runpod_id = os.getenv('runpod_id')
runpod_secret = os.getenv('runpod_secret')

# st.sidebar.markdown("## Main Menu")

logo = Image.open('logo.png')

st.set_page_config(
    page_title='AntibodyGPT: Antibody Protein Generation', 
    page_icon=logo)

sidebar.get_sidebar()
    
st.write("# Welcome to AntibodyGPT")


st.markdown(
    """
    ## A Fine-Tuned GPT for De Novo Therapeutic Antibodies

    ### What are antibodies?

    Antibodies are proteins that bind to a target protein (called an antigen) in order to mount an immune response

    They are incredibly **safe** and **effective** therapeutics against infectious diseases, cancer, and autoimmune disorders.

    ### Why aren’t there more antibodies on the market?

    Current antibody discovery methods require a lot of capital, expertise, and luck.

    Generative AI opens up the possibility of moving from a paradigm of antibody discovery to antibody generation.

    However, work is required to translate the advances of LLMs to the realm of drug discovery.

    ### What is AntibodyGPT?

    A fine-tuned GPT language model that researchers can use to rapidly generate functional, diverse antibodies for any given target sequence

    ### Key Features

    - Rapid generation
    - Only requires target sequence
    - Outputs diverse, human-like antibodies

    ### Links: 
        
    - [Huggingface Model Repository](https://huggingface.co/AntibodyGeneration)
    - [Web Demo](https://orca-app-ygzbp.ondigitalocean.app/Demo_Antibody_Generator)
    - [OpenSource RunPod Severless Rest API](https://github.com/joethequant/docker_protein_generator)
    - [The Code for this App](https://github.com/joethequant/docker_streamlit_antibody_protein_generation)

    ### Additional Resources and Links
    - [Progen Foundation Models](https://github.com/salesforce/progen)
    - [ANARCI Github](https://github.com/oxpig/ANARCI)
    - [ANARCI Webserver](http://opig.stats.ox.ac.uk/webapps/anarci/)
    - [TAP: Therapeutic Antibody Profiler](https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/tap)
    - [ESM Fold](https://esmatlas.com/resources?action=fold)

    

    ### Example Code To Use AntibodyGPT

    ```python
    from models.progen.modeling_progen import ProGenForCausalLM
    import torch
    from tokenizers import Tokenizer
    import json

    # Define the model identifier from Hugging Face's model hub
    model_path = 'AntibodyGeneration/fine-tuned-progen2-small'

    # Load the model and tokenizer
    model = ProGenForCausalLM.from_pretrained(model_path)
    tokenizer = Tokenizer.from_file('tokenizer.json')

    # Define your sequence and other parameters
    target_sequence = 'MQIPQAPWPVVWAVLQLGWRPGWFLDSPDRPWNPPTFSPALLVVTEGDNATFTCSFSNTSESFVLNWYRMSPSNQTDKLAAFPEDRSQPGQDCRFRVTQLPNGRDFHMSVVRARRNDSGTYLCGAISLAPKAQIKESLRAELRVTERRAEVPTAHPSPSPRPAGQFQTLVVGVVGGLLGSLVLLVWVLAVICSRAARGTIGARRTGQPLKEDPSAVPVFSVDYGELDFQWREKTPEPPVPCVPEQTEYATIVFPSGMGTSSPARRGSADGPRSAQPLRPEDGHCSWPL'
    number_of_sequences = 2

    # Tokenize the sequence
    tokenized_sequence = tokenizer(target_sequence, return_tensors="pt")

    # Move model and tensors to CUDA if available
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    tokenized_sequence = tokenized_sequence.to(device)

    # Generate sequences
    with torch.no_grad():
        output = model.generate(**tokenized_sequence, max_length=1024, pad_token_id=tokenizer.pad_token_id, do_sample=True, top_p=0.9, temperature=0.8, num_return_sequences=number_of_sequences)

    # Decoding the output to get generated sequences
    generated_sequences = [tokenizer.decode(output_seq, skip_special_tokens=True) for output_seq in output]

    ```
"""
)



