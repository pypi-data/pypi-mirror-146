# -*- coding: utf-8 -*-
"""
Mapping TF list to motif2TF file
--------------------------------

This module allows to write a subcollection of interactions between
transcription factor binding sites (TFBSs) and transcription factors (TFs), based on
a list of TFs. The interactions in the subcollection will involve only the TFs in the list.

Example:
    Test the example by running this file::

        $ python mapping.py
"""

import pandas as pd 

__author__ = "Timothée Frouté and Sergio Peignier"
__copyright__ = "Copyright 2019, The GReNaDIne Project"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Sergio Peignier"
__email__ = "sergio.peignier@insa-lyon.fr"
__status__ = "pre-alpha"

def write_ortho_motifs(motifs_file_path,ortho_gene_list_file_path,outfile="../mapped_motifs.tbl"):
    """
    Gets and writes a subcollection of motifs-TF interactions based on list of transcription factors. 

    Args:
        motifs_file_path (str): motif2tf file path from the cistarget databases 
        ortho_gene_list_file_path (str): name of the scores .feather file to write

    Examples:
        >>> ortho_gene_list_file_path = "../dros_ortho_tf_puc.txt"
        >>> motifs_file_path = "../motifs-v9-nr.flybase-m0.001-o0.0.tbl"
        >>> write_ortho_motifs(motifs_file_path,ortho_gene_list_file_path)
    """
    f = open(ortho_gene_list_file_path)
    ortho_gene_list = []
    for gene in f.readlines():
        ortho_gene_list.append(gene.strip())
    ortho_gene_list = list(dict.fromkeys(ortho_gene_list)) #gets rid of duplicates, if any
    total_motifs = pd.read_csv(motifs_file_path,sep="\t",low_memory=False)
    df = pd.DataFrame(columns=total_motifs.columns)
    for gene_name in ortho_gene_list:
        if gene_name in list(total_motifs["gene_name"]):
            df = df.append(total_motifs.loc[total_motifs["gene_name"] == gene_name],ignore_index=True)
    df.to_csv(outfile, sep="\t", index=0)
    return df

if __name__ == "__main__":
    id_list_file = "../example_list.txt"
    motifs_file = "../motifs-v9-nr.flybase-m0.001-o0.0.tbl"
    motifs = write_ortho_motifs(motifs_file,id_list_file)