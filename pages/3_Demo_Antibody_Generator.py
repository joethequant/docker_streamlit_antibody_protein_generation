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
from PIL import Image
import helpers.sidebar as sidebar
from helpers.seq import ab_number, full_seq_identity, cdr3_seq_identity
import requests
import os
from dotenv import load_dotenv
load_dotenv()

run_runpod_rest_api = True
runpod_id = os.getenv('runpod_id')
runpod_secret = os.getenv('runpod_secret')

# st.sidebar.markdown("## Main Menu")

logo = Image.open('logo.png')

st.set_page_config(
    page_title='Antigen.ai: Demo Antibody Protein Generation', 
    page_icon=logo
    )

sidebar.get_sidebar()

# Define the example sequences
example_sequences = {
    'PD1': "MQIPQAPWPVVWAVLQLGWRPGWFLDSPDRPWNPPTFSPALLVVTEGDNATFTCSFSNTSESFVLNWYRMSPSNQTDKLAAFPEDRSQPGQDCRFRVTQLPNGRDFHMSVVRARRNDSGTYLCGAISLAPKAQIKESLRAELRVTERRAEVPTAHPSPSPRPAGQFQTLVVGVVGGLLGSLVLLVWVLAVICSRAARGTIGARRTGQPLKEDPSAVPVFSVDYGELDFQWREKTPEPPVPCVPEQTEYATIVFPSGMGTSSPARRGSADGPRSAQPLRPEDGHCSWPLGGGGGSGGGGSGGGGS",
    'SARS-CoV2': "RVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNFGGGGGSGGGGSGGGGS",
    'vWF': "DLVFLLDGSSRLSEAEFEVLKAFVVDMMERLRISQKWVRVAVVEYHDGSHAYIGLKDRKRPSELRRIASQVKYAGSQVASTSEVLKYTLFQIFSKIDRPEASRITLLLMASQEPQRMSRNFVRYVQGLKKKKVIVIPVGIGPHANLKQIRLIEKQAPENKAFVLSSVDELEQQRDEIGGGGGSGGGGSGGGGS"
}


st.header('Demo Antibody Protein Generator', divider='green')

st.markdown('''
    This is a demo of our Antibody Protein Generation API leveraging the fine-tuned Progen2 models. 
    The fine-tuned models models were trained on the SAbDab dataset, which is a large dataset of antibody sequences.
    
    The below is running as an example. If you would like to run additional sequences at scale or help getting started, please reach out to the research team.

    Notes about running the below models:
    - The larger the model, the longer it will take to run.
    - The larger the number of sequences requested, the longer it will take to run.
    
    ''')


st.header('', divider='green')

# st.subheader('Run Model and Get Sequences', divider='green')

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

with st.form("generate_sequences_form"):

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

    submit = st.form_submit_button('Generate Sequences!')

# if st.button('Generate Sequences!'):
if submit:

    if target_sequence_input == "":
        st.error('Please enter a target protein sequence.')
        st.stop()

    
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

    with st.status("Generating Sequences...", expanded=True):
        st.write("Sending request to model.")
        
        if run_runpod_rest_api:

            url = f'https://api.runpod.ai/v2/{runpod_id}/run'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {runpod_secret}'
            }

            # The JSON data payload
            data = {
                'input': {
                    "model_name": "simple_fine_tuned_progen2-small",
                    "target_sequence": target_sequence_input,
                    "number_of_sequences": number_of_sequences
                }
            }

            # Make the POST request
            response = requests.post(url, json=data, headers=headers)

            print(response.text)
            job_id = response.json()['id']

            # st.write(response.json())

            st.write("Received job id.")

            status = 'IN_QUEUE'
            url = f'https://api.runpod.ai/v2/{runpod_id}/status/{job_id}'

            while (status != 'COMPLETED') and (status != 'FAILED'):
                st.write("Checking status of job...")
                # Make the POST request
                response = requests.get(url, headers=headers)

                status = response.json()['status']
                # st.write(status)
                time.sleep(20)
        
            if status == 'FAILED':
                st.write("Job failed. Please try again.")
                # st.stop()
            else:
                st.write("Job completed. Downloading sequences...")

            response_json = response.json()

        else:
            status = 'COMPLETED'
            response_json = {
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
            
        st.write('Processing Sequences.')
        sequences = response_json['output']
        df_result_H, df_result_KL = ab_number.number_seqs_as_df(sequences)

        df_result_H_dict = df_result_H.to_dict('records')
        df_result_KL_dict = df_result_KL.to_dict('records')

        st.write('Processing Done')

    if status == 'COMPLETED':
        delayTime = response_json['delayTime']
        executionTime = response_json['executionTime']
        Estimated_Cost = executionTime / 60 * 0.00048

        st.header('Generation Job Summary', divider='green')


        col1, col2 = st.columns([.5,.5], gap="small")
        
        with col1:
            st.markdown(f'''
                **GPU:** 'A6000'
            
                **Estimated Cost:** ${round(Estimated_Cost, 2)} USD        

                **Cost Per Sequence Requested:** ${round(Estimated_Cost / number_of_sequences, 2)} USD

                **Cost Per Valid Sequence Returned:** ${round(Estimated_Cost / len(df_result_H), 2)} USD

                **Delay Time:** {round(delayTime / 1000, 1)} seconds

                **Execution Time:** {round(executionTime / 1000, 1)} seconds
            ''')

        with col2: 
            st.markdown(f'''   

                **Sequences Requested:** {number_of_sequences}       

                **Valid Sequences Returned:** {len(df_result_H)}

                **Percent Success Rate:** {round(len(df_result_H) / number_of_sequences * 100, 0)}%

                **Average Sequence Identity HL:** {full_seq_identity(df_result_H, df_result_KL)}

                **Average Sequence Identity HCDR3:** {cdr3_seq_identity(df_result_KL)}


            ''')

        st.header('Antibody Protein Sequences Generated', divider='green')

        # Create tabs dynamically
        tabs = st.tabs([f'Sequence {i+1}' for i in range(len(df_result_H))])

        for i, tab in enumerate(tabs):
            with tab:

                heavy_chain = []
                for key in df_result_H_dict[i].keys():
                    try:
                        int_key = int(key)
                        heavy_chain.append(df_result_H_dict[i][key])
                    except ValueError:
                        # This means the key is not a string representation of a number
                        continue

                light_chain = []
                for key in df_result_KL_dict[i].keys():
                    try:
                        int_key = int(key)
                        light_chain.append(df_result_KL_dict[i][key])
                    except ValueError:
                        # This means the key is not a string representation of a number
                        continue

                st.markdown(f''' 

                        #### Heavy Chain:
                        {''.join(heavy_chain)}

                        #### Light Chain:
                        {''.join(light_chain)} 


                        #### ANARCI Results


                            ''')
                

                col1, col2 = st.columns([.5,.5], gap="small")

                with col1:
                    st.markdown(f'''
                                
                                ##### Heavy Chain

                                **Species:** {df_result_H_dict[i]['hmm_species']}

                                **Chain Type:** {df_result_H_dict[i]['chain_type']}

                                **E-Value:** {df_result_H_dict[i]['e-value']}

                                **Score:** {df_result_H_dict[i]['score']}
                                '''
                                )

                with col2:
                    st.markdown(f'''
                                    
                                    ##### Light Chain
    
                                    **Species:** {df_result_KL_dict[i]['hmm_species']}
    
                                    **Chain Type:** {df_result_KL_dict[i]['chain_type']}
    
                                    **E-Value:** {df_result_KL_dict[i]['e-value']}
    
                                    **Score:** {df_result_KL_dict[i]['score']}
                                    '''
                                    )




