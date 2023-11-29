import subprocess
import pandas as pd
import os
from itertools import combinations


from tempfile import NamedTemporaryFile
from .utils import seqs_to_fasta, fasta_to_csv

def number_seqs_as_df(seqs, scheme="imgt"):
    """Number a collection of sequences or (description, sqeuence) pairs with ANARCI,
    returning the numbered Abs as a dataframe. Returns a tuple of dataframes, the first
    corresponding to heavy chain annotations, and the second for light chain annotations. """

    with NamedTemporaryFile(delete=False) as tempf_i:
        seqs_to_fasta(seqs, tempf_i.name)
    with NamedTemporaryFile(delete=False) as tempf_o:
        subprocess.run(["ANARCI", "-i", tempf_i.name, "-o", tempf_o.name, "--csv"])

    if os.path.isfile(tempf_o.name + "_H.csv"):
        df_result_H = pd.read_csv(tempf_o.name + "_H.csv")
        os.remove(tempf_o.name + "_H.csv")
    else:
        df_result_H = None
    if os.path.isfile(tempf_o.name + "_KL.csv"):
        df_result_KL = pd.read_csv(tempf_o.name + "_KL.csv")
        os.remove(tempf_o.name + "_KL.csv")
    else:
        df_result_KL = None

    os.remove(tempf_o.name)
    os.remove(tempf_i.name)

    return df_result_H, df_result_KL

def percent_identity(seq1, seq2):
    """ Compute the percent identity of two strings of equal length. """
    if len(seq1) != len(seq2):
        raise ValueError('Sequences must be the same length.')
    i = 0
    for r1, r2 in zip(seq1, seq2):
        i += int(r1 == r2)
    return i * 100 / len(seq1)

def full_seq_identity(df_anarci_H, df_anarci_KL):
    df_anarci_H = df_anarci_H.copy().set_index('Id')
    df_anarci_KL = df_anarci_KL.copy().set_index('Id')
    df_anarci_H['full_seq_H'] = df_anarci_H.loc[:, '1':].apply(lambda x: ''.join(x), axis=1)
    df_anarci_KL['full_seq_KL'] = df_anarci_KL.loc[:, '1':].apply(lambda x: ''.join(x), axis=1)
    df_anarci = df_anarci_H.merge(df_anarci_KL, left_index=True, right_index=True)
    seqs = [x['full_seq_H'] + x['full_seq_KL'] for _, x in df_anarci.iterrows()]

    identity_dist = [percent_identity(s[0], s[1]) for s in combinations(seqs, 2)]
    return sum(identity_dist) / len(identity_dist)

def cdr3_seq_identity(df_anarci_H):
    df_seqs = df_anarci_H.loc[:, '105':'117']
    seqs = [''.join(x) for _, x in df_seqs.iterrows()]
    identity_dist = [percent_identity(s[0], s[1]) for s in combinations(seqs, 2)]
    return sum(identity_dist) / len(identity_dist)