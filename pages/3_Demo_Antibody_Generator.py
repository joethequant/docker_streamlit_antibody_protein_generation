# pip freeze > requirements.txt
# https://blog.runpod.io/serverless-create-a-basic-api/
# https://rascore.streamlit.app/
# folding https://esmatlas.com/about
# https://resources.wolframcloud.com/FunctionRepository/resources/ESMFoldProteinSequence/
# https://www.nature.com/articles/s41592-022-01488-1
# https://github.com/facebookresearch/esm#esmfold
# https://alphafold.ebi.ac.uk/api-docs
# https://towardsdatascience.com/how-to-deploy-and-interpret-alphafold2-with-minimal-compute-9bf75942c6d7

# igfold - > https://github.com/Graylab/IgFold

import time
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import helpers.sidebar as sidebar
from helpers.seq import ab_number, full_seq_identity, cdr3_seq_identity
import requests
import os
import requests
from dotenv import load_dotenv
load_dotenv()

run_runpod_rest_api = True
runpod_id = os.getenv('runpod_id')
runpod_secret = os.getenv('runpod_secret')
linker = "GGGGGSGGGGSGGGGS"

@st.cache_data(ttl=60*5) # 5 minutes cache
def send_sequence_to_api(model_name ,number_of_sequences, target_sequence_input, start_antibody_sequence=None):

    if run_runpod_rest_api:
        if (start_antibody_sequence != "") and (start_antibody_sequence != None):
            target_sequence_input = target_sequence_input + linker + start_antibody_sequence
        else:
            target_sequence_input = target_sequence_input + linker

        url = f'https://api.runpod.ai/v2/{runpod_id}/run'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {runpod_secret}'
        }

        # The JSON data payload
        data = {
            'input': {
                "model_name": model_name,
                "target_sequence": target_sequence_input,
                "number_of_sequences": number_of_sequences
            },
            "policy":{
                "executionTimeout": 600000 # 10 minutes in miliseconds
            }
        }

        # Make the POST request
        response = requests.post(url, json=data, headers=headers)

        print(response.text)

        job_id = response.json()['id']

    else:
        job_id = 'xxxxx' # fake job id
    return job_id


def get_response_from_api(job_id):

    if run_runpod_rest_api:

        url = f'https://api.runpod.ai/v2/{runpod_id}/status/{job_id}'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {runpod_secret}'
        }

        response = requests.get(url, headers=headers)
        response = response.json()
    else:

        response = {
                "delayTime": 5558,
                "executionTime": 89414,
                "id": "f91d0c20-e9bd-4a68-b48c-d17b0bfe51ea-u1",
                "output": [
                    "MQIPQAPWPVVWAVLQLGWRPGWFLDSPDRPWNPPTFSPALLVVTEGDNATFTCSFSNTSESFVLNWYRMSPSNQTDKLAAFPEDRSQPGQDCRFRVTQLPNGRDFHMSVVRARRNDSGTYLCGAISLAPKAQIKESLRAELRVTERRAEVPTAHPSPSPRPAGQFQTLVVGVVGGLLGSLVLLVWVLAVICSRAARGTIGARRTGQPLKEDPSAVPVFSVDYGELDFQWREKTPEPPVPCVPEQTEYATIVFPSGMGTSSPARRGSADGPRSAQPLRPEDGHCSWPLGGGGGSGGGGSGGGGSDVQLVESGGDLVKPGGGKLLVPCLASENAKPESLYGKFFKGFVMAGTPAELTLRFENANRYITLFCALQANRAPVARLFRGARVEEGVFRLTALKTDREIPIVYWLAGCPFSGGAIPFLRAQDSLA",
                    "MQIPQAPWPVVWAVLQLGWRPGWFLDSPDRPWNPPTFSPALLVVTEGDNATFTCSFSNTSESFVLNWYRMSPSNQTDKLAAFPEDRSQPGQDCRFRVTQLPNGRDFHMSVVRARRNDSGTYLCGAISLAPKAQIKESLRAELRVTERRAEVPTAHPSPSPRPAGQFQTLVVGVVGGLLGSLVLLVWVLAVICSRAARGTIGARRTGQPLKEDPSAVPVFSVDYGELDFQWREKTPEPPVPCVPEQTEYATIVFPSGMGTSSPARRGSADGPRSAQPLRPEDGHCSWPLGGGGGSGGGGSGGGGSDVQLVESGGDLVKPGGGETGLLQTHLKVQFARPSQQSVMEYRTDVVMMPFAEVRLRNEHGEATTWSRQEAGGWVQRWTQRASQRPRLDATGTVEIAFRIYRSGQPCQVKAEKCDCQVKFRVLEGGLMLVLGCTWQPQQNATAADREETKAFLKGATYWPGAQDSGALPEGAKVDFKLAPGVDVGLSWEYLPGSAKLPNLRASYRGXXXXXEKVSASPLVTEVTNGGLVAPVYKVTSLPKGEGCERSERRIYIAYKQSHFEVCVLTNGTATGPVEGSYH",
                    "MQIPQAPWPVVWAVLQLGWRPGWFLDSPDRPWNPPTFSPALLVVTEGDNATFTCSFSNTSESFVLNWYRMSPSNQTDKLAAFPEDRSQPGQDCRFRVTQLPNGRDFHMSVVRARRNDSGTYLCGAISLAPKAQIKESLRAELRVTERRAEVPTAHPSPSPRPAGQFQTLVVGVVGGLLGSLVLLVWVLAVICSRAARGTIGARRTGQPLKEDPSAVPVFSVDYGELDFQWREKTPEPPVPCVPEQTEYATIVFPSGMGTSSPARRGSADGPRSAQPLRPEDGHCSWPLGGGGGSGGGGSGGGGSDVQLVESGGDLVKPGGGETLRSRELVALSCRVSEDIIGTAGHHYLYWHFLHRVQHASLESHERVPWIPESRDCHINLNSDTVGFPERTGSQILCTVKALDVFDADLAYSPDPLNDLPRAHADSNSNKFLGLLFGGGGSGGGGSGGGGSDVQLVESGGDLVKPGGGETLRSRELVALSCRVSEDIISYAYGANLTTPALSVNGQSTMAPEQLITGLEHEKHQVTISSKPESRTALCSIGLEEGMLISYILTHMECWFCCLEDRVQITREIHNRVVRSKECTVAIVDTNEARNLTLREGLTLNTVLSRGHLICSVLGNSMCHDASILKLGETGHHIAQKFTSGVEVLELELAKYRIVACDNSISRPSKREVETTKMQVLFQAGFQVHAGIKLTPGSSKAKAPVAI",
                    "MQIPQAPWPVVWAVLQLGWRPGWFLDSPDRPWNPPTFSPALLVVTEGDNATFTCSFSNTSESFVLNWYRMSPSNQTDKLAAFPEDRSQPGQDCRFRVTQLPNGRDFHMSVVRARRNDSGTYLCGAISLAPKAQIKESLRAELRVTERRAEVPTAHPSPSPRPAGQFQTLVVGVVGGLLGSLVLLVWVLAVICSRAARGTIGARRTGQPLKEDPSAVPVFSVDYGELDFQWREKTPEPPVPCVPEQTEYATIVFPSGMGTSSPARRGSADGPRSAQPLRPEDGHCSWPLGGGGGSGGGGSGGGGSDVQLVESGGDLVKPGGGPAVQLTVTLHASRSVSLAVLIYRSLTTPLAQPMYSTTVMRECGTSAYTVPEGKSGSPAGPSAEGVYWACTLLFRLRPGSVALQQRLSTSLSLYRTVPSFCVGFHLPPPIISCVSDKEIFSAATTFTNEVTATHLLGRREVDLGTLETDXXAPREVKEPTLEAFKGIRTVSMFRNEVAPFDLCILVLCPQNSAGGGGSGGGGSGGGGSDVQLVQSGAEVKKPGESLKISCKGSGYSFTTYWIGWVRQMPGKGLEWMGIIYPGDSYTKYSPSFQGQVTISADKSISTAYLQWSSLKASDTAMYYCARLSLRVWSGYYYYYYGMDVWGQGTTVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKRVEPKSCDKTHHHHHHGGGGSGGGGSGGGGSDIQMTQSPSSLSAAVGDKVTITCRASQSFPRYYNYINWYQQQPGKAPKLLIYRASNLWSGVPSRFSGSRSGTEFTLTISSLQPEDFATYYCQQSHEDPYTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC",
                    "MQIPQAPWPVVWAVLQLGWRPGWFLDSPDRPWNPPTFSPALLVVTEGDNATFTCSFSNTSESFVLNWYRMSPSNQTDKLAAFPEDRSQPGQDCRFRVTQLPNGRDFHMSVVRARRNDSGTYLCGAISLAPKAQIKESLRAELRVTERRAEVPTAHPSPSPRPAGQFQTLVVGVVGGLLGSLVLLVWVLAVICSRAARGTIGARRTGQPLKEDPSAVPVFSVDYGELDFQWREKTPEPPVPCVPEQTEYATIVFPSGMGTSSPARRGSADGPRSAQPLRPEDGHCSWPLGGGGGSGGGGSGGGGSEVQLVESGGDVVKPGGSLRLSCAASGFTFSSYGMSWVRQAPGTGLEWVSVIYGGGRTDYRDDVKGRFTISRDNSKNTLYLQMSSLRAEDTAVYYCAREPPGGDMDYWGQGTLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCGGGGSGGGGSGGGGSYELTQPPSVSVSPGQTARITCSGDALPKQYAYWYQQKPGQAPVLVIYKDSERPSGIPERFSGSSSGTTVTLTISGVQAEDEADYYCQSADSDDINYVFGTGTKVTVLGQPKAAPSVTLFPPSSEELQANKATLVCLISDFYPGAVTVAWKADSSPVKAGVETTTPSKQSNNKYAASSYLSLTPEQWKSHRSYSCQVTHEGSTVEKTVAPTECS"
                ],
                "status": "COMPLETED"
                }

    return response


@st.cache_data
def fold_sequence(sequence):
    return requests.post("https://api.esmatlas.com/foldSequence/v1/pdb/", data=sequence, verify=False)


logo = Image.open('logo.png')

st.set_page_config(
    page_title='AntibodyGPT: Demo Antibody Protein Generation', 
    page_icon=logo
    )

sidebar.get_sidebar()

# Define the example sequences
example_sequences = {
    'PD1': "MQIPQAPWPVVWAVLQLGWRPGWFLDSPDRPWNPPTFSPALLVVTEGDNATFTCSFSNTSESFVLNWYRMSPSNQTDKLAAFPEDRSQPGQDCRFRVTQLPNGRDFHMSVVRARRNDSGTYLCGAISLAPKAQIKESLRAELRVTERRAEVPTAHPSPSPRPAGQFQTLVVGVVGGLLGSLVLLVWVLAVICSRAARGTIGARRTGQPLKEDPSAVPVFSVDYGELDFQWREKTPEPPVPCVPEQTEYATIVFPSGMGTSSPARRGSADGPRSAQPLRPEDGHCSWPL",
    'SARS-CoV2': "RVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNF",
    'vWF': "DLVFLLDGSSRLSEAEFEVLKAFVVDMMERLRISQKWVRVAVVEYHDGSHAYIGLKDRKRPSELRRIASQVKYAGSQVASTSEVLKYTLFQIFSKIDRPEASRITLLLMASQEPQRMSRNFVRYVQGLKKKKVIVIPVGIGPHANLKQIRLIEKQAPENKAFVLSSVDELEQQRDEI"
}


st.header('Demo Antibody Protein Generator', divider='green')

st.markdown('''
    This is a demo of our Antibody Protein Generation API leveraging the fine-tuned Progen2 models. 
    The fine-tuned models models were trained on the SAbDab dataset, which is a large dataset of antibody sequences.
    
    The below is running as an example. If you would like to run additional sequences at scale or help getting started, please use our open sourced models or reach out to the research team.

    ### Model Cards:
    - Small Model: [https://huggingface.co/AntibodyGeneration/fine-tuned-progen2-small](https://huggingface.co/AntibodyGeneration/fine-tuned-progen2-small)
    - Medium Model: [https://huggingface.co/AntibodyGeneration/fine-tuned-progen2-medium](https://huggingface.co/AntibodyGeneration/fine-tuned-progen2-medium)
    - Large Model: [https://huggingface.co/AntibodyGeneration/fine-tuned-progen2-large](https://huggingface.co/AntibodyGeneration/fine-tuned-progen2-large)

    ### Example Target Sequences:
            
    #### PD1: Programmed Cell Death Protein 1 (PD-1)

    - **Function**: PD-1 is a cell surface receptor crucial for downregulating the immune system. It prevents the overactivation of T-cells, which are essential components of the immune response.
    - **Role in Immune Regulation**: By interacting with its ligands, PD-L1 and PD-L2, PD-1 helps maintain the balance in the immune system, ensuring that it doesn't mistakenly attack the body's own tissues. This mechanism is vital for preventing autoimmune diseases.
    - **Clinical Relevance**: However, this same mechanism can be problematic in cancer, as it allows cancer cells to evade the immune system by expressing PD-L1, effectively 'turning off' T-cell responses against them.
    - **Therapeutic Target**: PD-1 has become a significant target in cancer immunotherapy. Drugs that inhibit PD-1 or its interactions can reactivate the immune system against cancer cells, offering a promising approach for treatment.
    - **Our Goal**: Generate antibody candidates that bind to PD-1, which can be used to **activate the immune system against cancer cells**.
                    
    #### SARS-CoV-2 Protein Sequence for Antibody Development

    - **Overview**: This sequence is derived from the SARS-CoV-2 virus, the causative agent of the COVID-19 pandemic. It represents a specific portion of the virus's protein structure.
    - **Importance in Virus Functionality**: The sequence is crucial for understanding how the virus interacts with human cells, replicates, and evades the immune system. It includes key areas that are essential for the virus's life cycle.
    - **Our Goal**: Our aim is to use this sequence to design antibodies that can specifically recognize and bind to SARS-CoV-2. These antibodies would ideally trigger a robust immune response, neutralizing the virus and providing therapeutic benefits.

    #### Von Willebrand Factor (vWF) Protein Sequence for Therapeutic Development

    - **Overview**: This sequence represents a portion of the von Willebrand Factor (vWF), a key protein in blood coagulation and platelet adhesion. vWF plays a critical role in the formation of blood clots and wound healing.
    - **Importance in Blood Coagulation**: The vWF sequence is essential for understanding how the protein interacts with other blood components, particularly in initiating the adhesion of platelets to damaged blood vessels. It is crucial in the early stages of blood clot formation.
    - **Clinical Relevance**: Variations or deficiencies in the vWF sequence can lead to bleeding disorders, such as von Willebrand Disease, which is the **most common hereditary coagulation abnormality in humans**. Understanding this sequence aids in diagnosing and treating such conditions.
    - **Our Goal**: Our objective is to utilize this sequence to develop therapeutic antibodies that can either mimic or modulate the function of vWF. This could be instrumental in treating bleeding disorders and improving wound healing processes.

            
    ### Running the below models:
    - The larger the model, the longer it will take to run.
    - The larger the number of sequences requested, the longer it will take to run.
    ''')


st.header('', divider='green')

# st.subheader('Run Model and Get Sequences', divider='green')


# ### Clear the App Cache

def clear_cache():
    submit = False
    if 'submitted' in st.session_state:
        del st.session_state['submitted']

    send_sequence_to_api.clear()
    st.success('Cache Cleared')

st.write('We cache api requests for 5 minutes, delete cache to get new results:')
if st.button('Clear Cache'):
    clear_cache()

#  Create a container for the buttons and the label
col1, col2, col3, col4 = st.columns([.4,.2,.2,.2], gap="small")

# Place a label in the first column
col1.write("Use Example Target Sequence:")


# Callback function to set the text input
def set_target_sequence_input(example_key):
    st.session_state.target_sequence_input = example_sequences[example_key]

# Check if 'text_input' key exists in the session state
if 'target_sequence_input' not in st.session_state:
    st.session_state.target_sequence_input = ''

# Buttons to set the example sequences
if col2.button('PD1'):
    set_target_sequence_input('PD1')

if col3.button('SARS-CoV2'):
    set_target_sequence_input('SARS-CoV2')

if col4.button('vWF'):
    set_target_sequence_input('vWF')

sequence_form = st.form("generate_sequences_form")
with sequence_form:

    model_selection = st.radio(
    "Select Model",
    [
        "Fine-tuned Progen2-small", 
        "Fine-tuned Progen2-medium", 
        "Fine-tuned Progen2-large",

        ],
    
    captions = [
        "Fine-tuned model trained from the Progen2 small foundational model",
        "Fine-tuned model trained from the Progen2 medium foundational model", 
        "Fine-tuned model trained from the Progen2 large foundational model"]
    )

    number_of_sequences = st.slider('Number of Sequences', 1, 5, 1)

    target_sequence_input = st.text_area("Target Protein Sequence", value=st.session_state.target_sequence_input, height=200)
    
    start_antibody_sequence = st.text_area("Optional: Start of Antibody Sequence", height=50)

    submit = st.form_submit_button('Generate Sequences!', type='primary')

    
if submit:
    if target_sequence_input == "":
        st.error('Please enter a target protein sequence.')
        send_sequence_to_api.clear()
        st.stop()
    else: 
        st.session_state.submitted = True


if 'submitted' in st.session_state:
    
    st.write("Model Requested: ", model_selection)

    st.write("Number of Sequences Requested: ", number_of_sequences)
    
    st.write(f"Target Sequence: {target_sequence_input}")

    if start_antibody_sequence != "":
        target_sequence_input = target_sequence_input + start_antibody_sequence 
        st.write(f"Start of Antibody Sequence: {start_antibody_sequence}")

    if model_selection == "Fine-tuned Progen2-small":
        model_name = "simple_fine_tuned_progen2-small"
    elif model_selection == "Fine-tuned Progen2-medium":
        model_name = "simple_fine_tuned_progen2-medium"
    elif model_selection == "Fine-tuned Progen2-large":
        model_name = "simple_fine_tuned_progen2-large"


    status = 'IN_QUEUE'

    job_start_time = time.time()
    with st.status("Generating Sequences...", expanded=False):
        st.write("Sending request to model.")
        
        job_id = send_sequence_to_api(model_name, number_of_sequences, target_sequence_input, start_antibody_sequence)

        st.write(f"Job Status: {status}")

        while (status != 'COMPLETED') and (status != 'FAILED'):
            
            # Make the POST request
            api_response_json = get_response_from_api(job_id)

            status = api_response_json['status']

            if (status != 'COMPLETED') and (status != 'FAILED'):

                sleep_amount = 20 #* number_of_sequences
                st.write(f"Job Status: {status}, waiting {sleep_amount} seconds...")
                time.sleep(sleep_amount)
    
        if status == 'FAILED':
            st.write("Job failed. Please try again.")
            send_sequence_to_api.clear()
            st.stop()
        else:
            st.write("Job completed. Downloading sequences...")

        st.write('Processing Sequences.')
        sequences = api_response_json['output']
        df_result_H, df_result_KL = ab_number.number_seqs_as_df(sequences)

        # df_result_H.to_csv('testing.csv')

        # did we get any valid sequences?
        valid_sequences = (df_result_H is not None) and (len(df_result_H) > 0) and (df_result_KL is not None) and (len(df_result_KL) > 0)
        
        if valid_sequences:

            df_result_H_dict = df_result_H.to_dict('records')
            df_result_KL_dict = df_result_KL.to_dict('records')

            heavy_and_light_sequences = df_result_H.add_prefix('H_').merge(df_result_KL.add_prefix('KL_'), left_index=True, right_index=True)

            heavy_chain_strings = []
            light_chain_strings = []
            folded_sequences = []

            for i in range(len(df_result_H)):
                heavy_chain = []
                for key in df_result_H_dict[i].keys():
                    try:
                        int_key = int(key)
                        if df_result_H_dict[i][key] != '-':
                            heavy_chain.append(df_result_H_dict[i][key])
                    except ValueError:
                        # This means the key is not a string representation of a number
                        continue

                heavy_chain = ''.join(heavy_chain)
                heavy_chain_strings.append(heavy_chain)

                light_chain = []
                for key in df_result_KL_dict[i].keys():
                    try:
                        int_key = int(key)
                        if df_result_KL_dict[i][key] != '-':
                            light_chain.append(df_result_KL_dict[i][key])
                    except ValueError:
                        # This means the key is not a string representation of a number
                        continue


                light_chain = ''.join(light_chain)
                light_chain_strings.append(light_chain)

                folded_sequence = f"{heavy_chain}{linker}{light_chain}"

                folded_sequences.append(folded_sequence)

        st.write('Processing Done')


    if status == 'COMPLETED':
        delayTime = api_response_json['delayTime']
        executionTime = api_response_json['executionTime']
        Estimated_Cost = executionTime / 60 * 0.00048

        if valid_sequences is False:
            st.header('Job Summary', divider='green')

            st.markdown(f'''
                **GPU:** 'A6000'
            
                **Delay Time:** {round(delayTime / 1000, 1)} seconds

                **Execution Time:** {round(executionTime / 1000, 1)} seconds

                **Estimated Cost:** ${round(Estimated_Cost, 2)} USD    

                **Cost Per Sequence Requested:** ${round(Estimated_Cost / number_of_sequences, 2)} USD

            ''')

            st.divider()

            st.error('No valid Human sequences generated. Add additional sequences to request and try again.')
            st.cache_data.clear()
            st.stop()            

        else:   


            st.header('Job Summary', divider='green')

            col1, col2 = st.columns([.5,.5], gap="small")
            

            st.markdown(f'''
                **GPU:** 'A6000'
            
                **Delay Time:** {round(delayTime / 1000, 1)} seconds

                **Execution Time:** {round(executionTime / 1000, 1)} seconds

                **Estimated Cost:** ${round(Estimated_Cost, 2)} USD    

                **Cost Per Sequence Requested:** ${round(Estimated_Cost / number_of_sequences, 2)} USD

                **Cost Per Valid Sequence Returned:** ${round(Estimated_Cost / len(df_result_H), 2)} USD
                ''')


            st.header('Model Results', divider='green')


            csv = heavy_and_light_sequences.to_csv(index=False)

            # Step 2: Use st.download_button to create a download button
            st.download_button(
                label="Download generated sequences",
                data=csv,
                file_name='data.csv',
                mime='text/csv',
            )


            if len(df_result_H) > 1:

                
                st.markdown(f'''
                    **Sequences Requested:** {number_of_sequences}       

                    **Valid Sequences Returned:** {len(df_result_H)}

                    **Percent Success Rate:** {round(len(df_result_H) / number_of_sequences * 100, 0)}%

                    **Average Sequence Identity HL:** {round(full_seq_identity(df_result_H, df_result_KL), 1)}

                    **Average Sequence Identity HCDR3:** {round(cdr3_seq_identity(df_result_KL), 1)}

                ''')

            else:
                st.markdown(f'''
                    **Sequences Requested:** {number_of_sequences}       

                    **Valid Sequences Returned:** {len(df_result_H)}

                    **Percent Success Rate:** {round(len(df_result_H) / number_of_sequences * 100, 0)}%

                    **Average Sequence Identity HL:** {0}

                    **Average Sequence Identity HCDR3:** {0}

                ''')            


            st.header('Antibody Protein Sequences Generated', divider='green')

            # Create tabs dynamically
            tabs = st.tabs([f'Sequence {i+1}' for i in range(len(df_result_H))])
            # tabs = st.tabs([f'Sequence {i+1}' for i in range(1)])
            for i, tab in enumerate(tabs):
                with tab:


                    col1, col2 = st.columns([.5,.5], gap="small")

                    with col1:
                        st.markdown(f'''
                                    
                                    #### Heavy Chain

                                    {heavy_chain_strings[i]}

                                    '''
                                    )

                    with col2:
                        st.markdown(f'''
                                        
                                        #### Light Chain
                                    
                                        {light_chain_strings[i]} 

                                        '''
                                        )
                        
                    col1, col2 = st.columns([.5,.5], gap="small")
                        
                    with col1:
                        st.markdown(f'''
                                    

                                    ##### ANARCI Results
                                    
                                    **Species:** {df_result_H_dict[i]['hmm_species']}

                                    **Chain Type:** {df_result_H_dict[i]['chain_type']}

                                    **E-Value:** {round(df_result_H_dict[i]['e-value'], 6)}

                                    **Score:** {df_result_H_dict[i]['score']}
                                    '''
                                    )

                    with col2:
                        st.markdown(f'''
                                        

                                        ##### ANARCI Results
        
                                        **Species:** {df_result_KL_dict[i]['hmm_species']}
        
                                        **Chain Type:** {df_result_KL_dict[i]['chain_type']}
        
                                        **E-Value:** {round(df_result_KL_dict[i]['e-value'], 6)}
        
                                        **Score:** {df_result_KL_dict[i]['score']}
                                        '''
                                        )
                    
                    st.markdown(f'''
                                #### Antibody Sequence
                                {folded_sequences[i]}
                                ''')

                    with st.spinner('Folding Sequence: Running ESM Fold...'):

                        response = fold_sequence(folded_sequences[i])

                    # Check the status of the request
                    if response.status_code == 200:
                        pdb_data = response.text

                        # Step 1: Convert the PDB data to a binary format
                        pdb_data_binary = pdb_data.encode()

                        # Step 2: Use the st.download_button function to create a download button
                        st.download_button(
                            label="Download PDB file",
                            data=pdb_data_binary,
                            file_name=f'sequence_{i+1}.pdb',
                            mime='application/octet-stream'
                        )
                        
                        html_template = f"""
                        <div id="mol-container" style="width: 100%; height: 600px;"></div>
                        <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
                        <script>
                        let viewer = new $3Dmol.createViewer('mol-container');
                        viewer.addModel(`{pdb_data}`, "pdb");
                        viewer.setStyle({{'cartoon': {{color:'spectrum'}}}});  // Note the extra quotes and braces
                        viewer.zoomTo();
                        viewer.render();
                        </script>
                        """

                        components.html(html_template, height=600)

                    else:
                        # If the request was not successful, print an error message
                        st.write(f"Error: Could not fold sequence. {response.text}")