# -*- coding: utf-8 -*-
"""
Creating and saving feather files
---------------------------------

This module allows to write the feather files (scores and ranks) 
obtained with the motifsearch module.

Example:
    Test the example by running this file::

        $ python create_feather.py

Todo:
    * compare with pyscenic creat_cisTarget_database: https://github.com/aertslab/create_cisTarget_databases

"""

import os,sys
import pickle
import pandas as pd
import pyarrow.feather as feather
from feather_creator.motifsearch import score_sequences, max_aggregation, motifs2pssms, load_motifs

__author__ = "Timothée Frouté and Sergio Peignier"
__copyright__ = "Copyright 2019, The GReNaDIne Project"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Sergio Peignier"
__email__ = "sergio.peignier@insa-lyon.fr"
__status__ = "pre-alpha"

def test_feather_read_write():
    """
    Tests the writing and the reading of a .feather file using pyarrow 0.16.0 functions.
    """
    data = {'product_name': ['laptop', 'printer', 'tablet', 'desk', 'chair'],
    'price': [1200, 150, 300, 450, 200]
    }

    df = pd.DataFrame(data)

    writer = feather.FeatherWriter("./test.feather") 
    writer.write(df)

    test = feather.read_feather("test.feather")
    print(test)

def save_scores_feather(scores_df,scores_feather_file):
    """
    Feather file writer, allows writting a feather file, used to write the motifs scores dataframe.

    Args:
        scores_df (pandas.DataFrame): scores matrix obtained with the score_sequences function,
            where each row is a motif name and each column is a gene sequence name
        feather_file (str): name of the .feather file to write

    Examples:
        >>> from motifsearch import score_sequences
        >>> from motifsearch import max_aggregation
        >>> scores_best = score_sequences(genes_sequences,pssms,max_aggregation,n_jobs=8)
        >>> save_scores_feather(scores_best,"./scores_full_acypi_background.feather")
    """
    writer = feather.FeatherWriter(scores_feather_file) 
    scores_df.reset_index(level=0, inplace=True)
    writer.write(scores_df)

def load_scores_feather(scores_feather_file):
    """
    Feather file loader, loads a feather file, used to load the motifs scores dataframe.

    Args:
        scores_df (pandas.DataFrame): scores matrix obtained with the score_sequences function,
            where each row is a motif name and each column is a gene sequence name
        scores_feather_file (str): name of the .feather file to load

    Examples:
        >>> save_scores_feather(scores_best,"./scores_full_acypi_background.feather")
        >>> scores_df = load_scores_feather("scores_full_acypi_background.feather")
        >>> scores_df
                               ACYPI084998  ACYPI44835  ACYPI010106  ACYPI26530  ACYPI089001  ...  ACYPI085136  ACYPI000318  ACYPI30960  ACYPI24141  ACYPI006702
        elemento-AAAATGGCG     1.784074    0.000000     0.000000    0.000000     1.784074  ...     0.000000     0.000000    0.000000    0.000000     0.000000
    """
    scores_df = feather.read_feather(scores_feather_file)
    scores_df = scores_df.set_index("index")
    return scores_df

def save_ranks_feather(scores_df,ranks_feather_file): 
    """
    Feather file writer, allows the ranking and writting of a feather file, used to write the motifs ranks dataframe.

    Args:
        scores_df (pandas.DataFrame): scores matrix obtained with the score_sequences function,
            where each row is a motif name and each column is a gene sequence name
        ranks_feather_file (str): name of the .feather file to write

    Examples:
        >>> from motifsearch import score_sequences
        >>> from motifsearch import max_aggregation
        >>> scores_best = score_sequences(genes_sequences,pssms,max_aggregation,n_jobs=8)
        >>> save_ranks_feather(scores_df,"./ranks_full_acypi_background.feather")
        >>> rank_df = feather.read_feather("ranks_full_acypi_background.feather")
        >>> rank_df
                    features  ACYPI084998  ACYPI44835  ACYPI010106  ACYPI26530  ACYPI089001  ...  ACYPI065189  ACYPI085136  ACYPI000318  ACYPI30960  ACYPI24141  ACYPI006702
            0          0         3210       10749        10750       10751         3211  ...        36933        36934        36935       36936       36937        36938
            1          1         3360        3361        17718       15937        17719  ...        36935        36936        15936       36937       36938         2180
 
    """
    ranks_df = (-scores_df).rank(axis=1,method="first")
    ranks_df = ranks_df - 1
    ranks_df = ranks_df.astype(int)
    ranks_df.reset_index(level=0, inplace=True)
    cols = [c for c in ranks_df.columns]
    cols[0] = "features"
    ranks_df.columns = cols
    writer = feather.FeatherWriter(ranks_feather_file) 
    writer.write(ranks_df)

def full_process(genes_sequences, pssms, scores_feather_file, ranks_feather_file,output_dir = "../output", alphabet=False):
    """
    Scores sequences w.r.t. PSSM motifs, writes scores and ranks feather files.

    Args:
        genes_sequences (dict): geneID -> contextual sequence 
        pssms (str or dict):
            motif dir path, pickle path or 
            motifID -> {<original motif>, <pssm>, <distribution>}
        scores_feather_file (str): name of the scores .feather file to write
        ranks_feather_file (str): name of the ranks .feather file to write
        output_dir (str): name of the output directory
        alphabet (dict): letter to frequency in the genome

    Examples:
        >>> motifs = load_motifs("motifs")
        >>> pssms = motifs2pssms(motifs, alphabet_acypi)
        >>> genes_sequences = load_aphidbase_gene_sequences(delta_pre=2000,
                                                    delta_post=2000)
        >>> genes_sequences = {k:genes_sequences[k] for k in list(genes_sequences.keys())}                                            
        >>> full_process(genes_sequences, pssms,"./scores_full_acypi_background.feather", "./ranks_full_acypi_background.feather")
    """
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    if type(pssms) is str:
        if pssms.endswith(".pickle") and os.path.isfile(pssms):
            pssms = pickle.load(open(pssms,"rb"))
        
        elif os.path.isdir(pssms) and len(os.listdir(pssms)) != 0 and alphabet:
            pssms = motifs2pssms(pssms, alphabet)
    if type(pssms) is not dict:
        print("Please use motif dir, .pickle file or correct pssms dict format")
        return 0
    scores_best = score_sequences(genes_sequences,pssms,max_aggregation,n_jobs=8)
    save_scores_feather(scores_best,os.path.join(output_dir,scores_feather_file))
    scores_df = load_scores_feather(os.path.join(output_dir,scores_feather_file))
    save_ranks_feather(scores_df,os.path.join(output_dir,ranks_feather_file))

if __name__ == "__main__":

    from aphids.genome import load_aphidbase_gene_sequences
    from aphids.genome import alphabet_acypi
    motifs = load_motifs("../motifs")
    pssms = motifs2pssms(motifs, alphabet_acypi)

    genes_sequences = load_aphidbase_gene_sequences(delta_pre=2000,
                                                    delta_post=2000)
                                    
    genes_sequences = {k:genes_sequences[k] for k in list(genes_sequences.keys())}

    full_process(genes_sequences, pssms,"./scores_full_acypi_background.feather", "./ranks_full_acypi_background.feather")

