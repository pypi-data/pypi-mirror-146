.. raw:: html

    <style> .purple {color:purple} </style>
	
.. role:: purple

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

.. _SMAPwindowcrispr:

######
CRISPR
######

A specific extension of the **SMAP haplotype-window** workflow for CRISPR data can be invoked using the optional command ``--guides``.

If CRISPR-mediated genome editing was performed by stable transformation with a CRISPR/gRNA delivery vector, then the presence of the gRNA cassette in the delivery vector may be detected in the transformed genome.
Primers can be designed on the vector sequence to amplify the gRNA sequence in the gRNA expression cassette, and Border regions can be positioned directly flanking the 20 bp gRNA sequence. The haplotype of that 'locus' that is then detected is effectively a copy of the gRNA sequence incorporated into the transformed genome. 
These primers can be included in the HiPlex primer set used to screen for the genomic target loci.
SMAP **haplotype-window** can assign gRNA vector-derived reads to the respective target loci, if the user provides a FASTA file with the target loci names as identifiers and the 20 bp gRNA as sequence.
In this way, genome-edited haplotypes at genomic target loci can be detected in parallel to the gRNAs that cause them, for any number of loci and any number of samples.

  .. image:: ../images/window/smap_window_sgrna_extraction_crispr.png

Example of gRNA sequences FASTA:

========================= =
>AT1G07650_1_gRNA_001
TGAAGTCGCAGAACTTAACG
>AT1G07650_1_gRNA_002
CTGAAGTCGCAGAACTTAAC
========================= =

Example of output file with diverse genome-edited haplotypes at genomic target loci and corresponding gRNA.
By sorting on the fourth column (**Target**) in any output .tsv file, it is possible to arrange all the target loci with their corresponding gRNAs.
Note that the **Edit** column is not listed in the standard output of **SMAP haplotype-window**, it has been added here to indicate haplotypes resulting from CRISPR genome editing. "ref" indicates that the detected haploype is identical to the corresponding reference sequence. Numbers indicate length difference with the reference (positive values are insertions, negative values are deletions, 0-values are SNPs).

.. tabs::

   .. tab:: Unsorted output file
   
     .. csv-table::
	     :file: ../tables/window/crispr_example_unsorted.csv
	     :header-rows: 1
	  
   .. tab:: Sorted output file
   
	  .. csv-table::
	     :file: ../tables/window/crispr_example_sorted.csv
	     :header-rows: 1
		
