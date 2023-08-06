# -*- coding: utf-8 -*-
"""
GRN Motif Binding Site Inference
--------------------------------

This module allows to infer Gene Regulatory Networks based on Transcription
Factor binding sites motifs. This module relies on the `iRegulon`_ dataset,
which has also been used for `i-cistarget`_.

Example:
    Test the example by running this file::

        $ python motifsearch.py

.. _iRegulon:
   http://iregulon.aertslab.org/collections.html#motifcolldownload

.. _i-cistarget:
    https://github.com/aertslab/pySCENIC 
"""

from Bio import SeqIO
from Bio import motifs
from os.path import join
from os import listdir
import pandas as pd
import numpy as np
from tqdm import tqdm
from Bio.Alphabet import IUPAC
import multiprocessing as mp

__author__ = "Sergio Peignier"
__copyright__ = "Copyright 2019, The GReNaDIne Project"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Sergio Peignier"
__email__ = "sergio.peignier@insa-lyon.fr"
__status__ = "pre-alpha"

def load_motifs(folder):
    """
    Load 10K motifs (position weight matrices PWM) from iRegulon
    Args:
        folder: path to the motif files

    Returns:
        list: [Bio.motifs.jaspar.Motif] list of motifs
    """
    pwds_total = []
    for f in tqdm(listdir(folder)):
        if f[0] != ".":
            f_path = join(folder,f)
            pwd = motifs.parse(open(f_path,"r"), "jaspar")[0]
            pwds_total.append(pwd)
            #print(pwd.name)
    return(pwds_total)

def motif2pssm(motif, alphabet):
    """
    convert motif to PSSM (position-specific scoring matrix) distribution
    Args:
        motif (Bio.motifs.jaspar.Motif): biopython motif (PWM)
        alphabet (dict): letter to frequency in the genome

    Returns:
        dict: {<original motif>, <pssm>, <distribution>}
    """
    # Add pseudocounts to prevent zero probabilities
    ppm = motif.counts.normalize(pseudocounts=alphabet)
    # Set the background (species biases)
    pssm = ppm.log_odds(background=alphabet)
    # Compute the distribution of PWM scores
    distribution = pssm.distribution(background=alphabet, precision=10**3)
    return(motif.name, {"motif":motif,"pssm":pssm,"distribution":distribution})

def motifs2pssms(motifs, alphabet):
    """
    Converts each motif in pssm
    Args:
        motif list : list of biopython motif (PWM)
        alphabet (dict): letter to frequency in the genome

    Returns:
        dict: dictionnary motifID -> {<original motif>, <pssm>, <distribution>}
    """
    pssms = {}
    for motif in tqdm(motifs):
        motif_name, pssm = motif2pssm(motif, alphabet)
        pssms[motif_name] = pssm
    return(pssms)

def max_aggregation(scores):
    """
    Computes the maximal score for a list of scores, NaN are set to 0

    Args:
        scores (list): list of scores

    Returns
        float : maximal score in sequence

    Examples:
        >>> max_aggregation([1,2,np.nan])
        2
    """
    return(np.nan_to_num(scores).max())

def score_sequence_with_pssm(sequence, pssm, f_aggregation=None):
    """
    Score the sequence positions w.r.t. a PSSM and aggregates the resulting
    vector to output a single score

    Args:
        sequence (Bio.Seq.Seq): Biopython sequence
        pssm (Bio.motifs.matrix.PositionSpecificScoringMatrix): PSSM
        f_aggregation (func): Aggregation function

    Returns:
        float or numpy.array: if f_aggregation is not None, a single float score
        is returned, otherwise a numpy.array with the score for each location
        of the sequence is returned
    """
    sequence.alphabet = pssm.alphabet
    score = pssm.calculate(sequence)
    if f_aggregation is not None:
        score = f_aggregation(score)
    return(score)


def score_sequence_pssms_dict(sequence,
                              pssm_dic,
                              f_aggregation=None):
    """
    Score a sequence w.r.t. a dictionnary of PSSM

    Args:
        sequence (Bio.Seq.Seq): Biopython sequence
        pssm (dict): dict of Bio.motifs.matrix.PositionSpecificScoringMatrix
        f_aggregation (func): Aggregation function

    Returns:
        dict: PSSM key -> sequence score for the given PSSM
    """
    scores = {}
    for k in pssm_dic:
        scores[k] = score_sequence_with_pssm(sequence,
                                             pssm_dic[k],
                                             f_aggregation)
    return(scores)

def _score_sequence_pssms_dict(sequence_id,
                               sequence,
                               pssm_dict,
                               f_aggregation=None):
    """
    Applies score_sequence_pssms_dict, but also returns the sequence id

    Args:
        sequence_id (str): sequence id
        sequence (Bio.Seq.Seq): Biopython sequence
        pssm (dict): dict of Bio.motifs.matrix.PositionSpecificScoringMatrix
        f_aggregation (func): Aggregation function

    Returns:
        str: sequence id
        dict: PSSM key -> sequence score for the given PSSM
    """
    scores = score_sequence_pssms_dict(sequence,pssm_dict,f_aggregation)
    return(sequence_id,scores)

def score_sequences(genes_sequences,
                    pssm_distrib_dict,
                    f_aggregation=None,
                    n_jobs=1):
    """
    Scores sequences w.r.t. PSSM motifs

    Args:
        genes_sequences (dict): geneID -> contextual sequence
        pssm_distrib_dic (dict):
            motifID -> {<original motif>, <pssm>, <distribution>}
        f_aggregation (func): Aggregates the score along the sequence
        n_jobs (int): number of jobs to run in parallel

    Returns:
        dict: gene -> motif -> scores along sequence and context
    """

    def chunk_gene_sequences(genes_sequences, n=100):
        l = genes_sequences.items()
        l = list(l)
        for i in range(0, len(l), n):
            yield dict(l[i:i + n])
    # create a dictionnary of pssms only
    pssm_dict = {k:pssm_distrib_dict[k]["pssm"] for k in pssm_distrib_dict}
    # chunk the gene sequences dict
    sub_gene_sequences = list(chunk_gene_sequences(genes_sequences))
    # Set the number of jobs
    if n_jobs > mp.cpu_count():
        n_jobs = mp.cpu_count()
    pool = mp.Pool(n_jobs)
    # generate multiprocess tasks
    scores_mp = []
    for sub_sequences in tqdm(sub_gene_sequences):
        scores_mp +=  [pool.apply_async(_score_sequence_pssms_dict,
                                        args=(seq_id,seq,pssm_dict,f_aggregation))
                                        for seq_id,seq in sub_sequences.items()]
    pool.close()
    # Run multiprocess computations
    scores = []
    for p in tqdm(scores_mp):
        scores.append(p.get())
    scores = pd.DataFrame(dict(scores))
    return(scores)


def get_max_score(scores):
    """
    Get highest score in sequence
    Args:
        dict: gene -> motif -> scores along sequence and context

    Returns:
        dict: gene -> motif -> best score

    TODO:
        let the selection function be a parameter
    """
    max_score = {}
    for gene in tqdm(scores):
        max_score[gene] = {}
        for tf in scores[gene]:
            max_score[gene][tf] = np.nan_to_num(scores[gene][tf]).max()
    return(max_score)

def compute_threshold(pssm_distrib_dic, fpr=0.001):
    """
    Compute a likelihood threshold based on the distribution of the motif
    the false positive rate is set as a parameter
    Args:
        pssm_distrib_dic (dict):
            motifID -> {<original motif>, <pssm>, <distribution>}
        fpr (float): False Positive Rate

    Returns:
        dict: motif -> threshold
    """
    thresholds = {}
    for motif in pssm_distrib_dic:
        distribution =  pssm_distrib_dic[motif]["distribution"]
        thresholds[motif] = distribution.threshold_fpr(fpr)
        #.threshold_balanced(100)
        #threshold_fpr(0.0001)
        #.threshold_patser()
        #.threshold_fnr(0.5)
    return(thresholds)


if __name__ == '__main__':
    from aphids.genome import alphabet_acypi
    motifs = load_motifs()
    # for m in motifs:
    #     print(m)
    pssms = motifs2pssms(motifs, alphabet_acypi)
    # import pickle
    # pssms = pickle.load(open('/Users/sergiopeignier/Documents/libraries/grn/models/motifs/pssms_10k.pickle',"rb"))
    for pssm in pssms:
        print(pssm)
    from aphids.genome import load_aphidbase_gene_sequences
    genes_sequences = load_aphidbase_gene_sequences(delta_pre=3000,
                                                    delta_post=8000)
    scores_full = score_sequences(genes_sequences,pssms)
    scores_best = get_max_score(scores_full)
    scores_df = pd.DataFrame(scores_best)
    import matplotlib.pyplot as plt
    plt.imshow(scores_df.T,aspect="auto")
    plt.show()
    thresholds = compute_threshold(pssms)
    plt.imshow(scores_df.T > pd.Series(thresholds),aspect="auto")
    plt.show()
