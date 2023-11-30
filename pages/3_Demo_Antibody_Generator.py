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


logo = Image.open('logo.png')

st.set_page_config(
    page_title='AntibodyGPT: Demo Antibody Protein Generation', 
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


if submit:
    if target_sequence_input == "":
        st.error('Please enter a target protein sequence.')
        st.stop()
    else:
        st.session_state.submitted = True

else:
    st.session_state.submitted = False

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



            folded_sequence = f"{heavy_chain}GGGGGSGGGGSGGGGS{light_chain}"

            folded_sequences.append(folded_sequence)


        st.write('Processing Done')

    if status == 'COMPLETED':
        delayTime = response_json['delayTime']
        executionTime = response_json['executionTime']
        Estimated_Cost = executionTime / 60 * 0.00048

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

                # heavy_chain = []
                # for key in df_result_H_dict[i].keys():
                #     try:
                #         int_key = int(key)
                #         if df_result_H_dict[i][key] != '-':
                #             heavy_chain.append(df_result_H_dict[i][key])
                #     except ValueError:
                #         # This means the key is not a string representation of a number
                #         continue

                # light_chain = []
                # for key in df_result_KL_dict[i].keys():
                #     try:
                #         int_key = int(key)
                #         if df_result_KL_dict[i][key] != '-':
                #             light_chain.append(df_result_KL_dict[i][key])
                #     except ValueError:
                #         # This means the key is not a string representation of a number
                #         continue

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
                    
                payload = f"{folded_sequences[i]}"


                st.markdown(f'''
                            #### Antibody Sequence
                            {folded_sequences[i]}
                            ''')

                with st.spinner('Folding Sequence'):

                    response = requests.post("https://api.esmatlas.com/foldSequence/v1/pdb/", data=payload, verify=False)

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

                
                




