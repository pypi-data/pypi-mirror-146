.. raw:: html

    <style> .purple {color:purple} </style>
	
.. role:: purple

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

###########################
HiPlex amplicon sequencing
###########################

.. _SMAPwindowHiPlexHIW:

Setting the stage
-----------------

.. admonition:: Core

	**Windows are defined as any region enclosed by a pair of Borders**. **SMAP haplotype-window** considers the entire read sequence spanning the region between the Borders as haplotypes. Any pair of Borders can be chosen and searched for in a given set of reads. Because the primer sequence itself becomes incorporated into the amplicon molecule, (parts of) primers can naturally function as Border sequences delineating the enclosed amplified region.

HiPlex library preparation and preprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The schemes below show how HiPlex libraries are prepared, sequenced, and trimmed to remove sample-specific barcodes and adapter sequences. The reads obtained by HiPlex amplicon sequencing can be mapped directly onto a reference sequence.
Optionally, gRNAs can be designed together with amplicons, so that HiPlex targetted resequencing can be used to characterize CRISPR/Cas induced mutations.

.. tabs::

   .. tab:: Primer and (optional) gRNA design
   
      .. image:: ../../images/window/SMAP_window_design_1.png
	  
   .. tab:: Multiplex PCR per sample
   
      .. image:: ../../images/window/SMAP_window_crispr_2.png
	  
   .. tab:: Multiplex amplicon pooling across all samples
   
      .. image:: ../../images/window/SMAP_window_crispr_3.png
	  
   .. tab:: Illumina adapter ligation
   
      .. image:: ../../images/window/SMAP_window_crispr_4.png
	  
   .. tab:: Paired-end sequencing
   
      .. image:: ../../images/window/SMAP_window_crispr_5.png
	  
   .. tab:: Forward and Reverse read merging

      .. image:: ../../images/window/SMAP_window_crispr_6.png

   .. tab:: Sample demultiplexing

      .. image:: ../../images/window/SMAP_window_crispr_7.png

   .. tab:: Sample index and universal tail trimming  
   
      .. image:: ../../images/window/SMAP_window_crispr_8.png 

Recognizing haplotypes
~~~~~~~~~~~~~~~~~~~~~~

| In HiPlex data **primer sequences** are **preferably retained** during trimming in preprocessing in order to create more positive matches during mapping. Because these sequences are invariable and technical, they are not taken into consideration by **SMAP haplotype-window**, instead they are preferably used to recognize the start and stop positions of the enclosed amplified region, i.e. the Window to be haplotyped.
| Border sequences are recommended to have a length between **5** and **10** bp and require an **exact** match between the reads and the reference genome sequence.
| This sequence delineation by two border sequences in HiPlex data is identical to the delineation in Shotgun Seq data. However in Shotgun Seq data, border sequences are created using sliding windows, whereas in HiPlex data they can be defined based on primer positions. 

The tabs below show the same locus/amplicon in 3 diploid individuals. A total of 4 SNPs and 2 deletions are found among the individuals; 4 haplotypes can clearly be defined (1 reference allele and 3 alternative alleles). 

.. tabs::

   .. tab:: HiPlex merged reads, Sample 1
	  
	  .. image:: ../../images/window/Sample1_window_bam_AS.png

   .. tab:: HiPlex merged reads, Sample 2
	  
	  .. image:: ../../images/window/Sample2_window_bam_AS.png
	  
   .. tab:: HiPlex merged reads, Sample 3
	  
	  .. image:: ../../images/window/Sample3_window_bam_AS.png

----
	  
Step 1: Extracting window-overlapping reads ID's from BAM files and reads from FASTQ files
-------------------------------------------------------------------------------------------

procedure
~~~~~~~~~	  

In order to run **SMAP haplotype-window** on HiPlex data, the user should create a custom GFF file with the desired Border positions enclosing Windows (see :ref:`instructions here <SMAPwindowquickstart>`). 

.. image:: ../../images/window/SMAP_window_step1_AS.png

| For each locus (here called Window), **SMAP haplotype-window** will extract the Window-sequence from the reference FASTA file. 
| For each BAM file, for every read that overlaps with the Window-region with at least 1 nucleotide, the read-ID is used to retrieve the corresponding read from the original FASTQ file.
| Any loss of sequence length in the reads that are partially mapped in the BAM file (due to hard/soft-clipping), is therefore mitigated by stepping back to the original reads. Large insertions or deletions, or regions with high density SNPs are therefore captured, independent of read mapping artefacts and/or *a-priori* variant calling algorithms, as long as they map specifically, and at least partially, to the Window region in the reference and contain both Border sequences enclosing the Window.

.. image:: ../../images/window/window_bam_to_fastq_AS.png

----

Step 2: Trimming and counting haplotypes
-----------------------------------------

Per FASTQ file (one for each sample-Window combination), reads are passed to `Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_ using the Window-specific pair of Border sequences for pattern trimming. 
Both Borders need to be found and trimmed, otherwise the read is discarded. This approach ensures the identification and removal of partial Window sequences, that would otherwise be mistaken for additional haplotypes. 
Because the Window is defined as the region *inbetween* the Borders (*i.e.* read regions retained after removal of the Borders), the entire read sequence spanning the Window is considered as a unique haplotype. 


.. image:: ../../images/window/SMAP_window_step2_AS_new.png

procedure
~~~~~~~~~

:purple:`The following procedure is performed per sample:`

| For each locus-specific FASTQ file, reads are first trimmed at border sequences using pattern trimming performed by `Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_.
| Then, the remaining fragments of reads that correspond to the Window are sorted into unique haplotypes.
| These haplotypes are then counted per sample and passed through a read depth filter ``-c``, and the resulting haplotypes and counts are stored in tables.
| 
| **Thus the algorithm does not compare the sequences base by base but in their entirety. This procedure allows for the detection of any combination of InDels and/or SNPs, without calling them using the read-reference alignment.** 

.. image:: ../../images/window/SMAP_window_step4b_new.png

filters
~~~~~~~

:purple:`loci with low read count are removed from the dataset with a read count threshold (option` ``-c``:purple:`)`

Accurate haplotype frequency estimation requires a minimum read count which is different between sample type (individuals and Pool-Seq) and ploidy levels.

The user is advised to use the read count threshold to ensure that the reported haplotype frequencies per locus are indeed based on sufficient read data. If a locus has a total haplotype count below the user-defined minimal read count threshold (option ``-c``; default 0, recommended 10 for diploid individuals, 20 for tetraploid individuals, and 30 for pools) then all haplotype observations are removed for that sample. For more information see page :ref:`Recommendations <SMAPwindowrec>`.

:purple:`Only loci with an number of haplotypes between a custom interval across all samples are returned`

``-j``, ``--min_distinct_haplotypes`` :white:`###` *(int)* :white:`###` Filter for the minimum number of distinct haplotypes per locus [0].  

``-k``, ``--max_distinct_haplotypes`` :white:`###` *(int)* :white:`###` Filter for the maximum number of distinct haplotypes per locus [inf].  

:purple:`Only haplotypes with a relative frequency higher than a custom threshold in at least one sample are retained` (see Step 3)

``-f``, ``--min_haplotype_frequency`` :white:`###` *(int)* :white:`###` Set minimal HF (in %) to retain the haplotype in the genotyping matrix. Haplotypes above this threshold in at least one of the FAST files are retained. Haplotypes that never reach this threshold in any of the FASTQ files are removed [0].
	
