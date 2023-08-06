.. raw:: html

    <style> .purple {color:purple} </style>
	
.. role:: purple

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

######################
Scope & Quick Start
######################

Scope
-----

| **SMAP haplotype-window** extracts haplotypes from reads aligned to a predefined set of Windows in a reference sequence, wherein each Window is enclosed by a pair of Border regions.
| **SMAP haplotype-window** can be used for highly multiplex amplicon sequencing (HiPlex) or Shotgun sequencing data.
| **SMAP haplotype-window** extracts an entire DNA sequence between two Borders as a haplotype allele, without prior knowledge of polymorphisms within that sequence, and considers any unique DNA sequence as a haplotype. This is different from :external+haplotype-sites:ref:`SMAP haplotype-sites  <SMAPhaploquickstart>`, which performs read-backed haplotyping using prior positional information of read alignments and creates multi-allelic haplotypes from a concatenated short string of polymorphic sites (ShortHaps).

  .. image:: ../images/window/SMAP_haplotype_window_SQS_short.png

:purple:`SMAP haplotype-window requires this input:`
	
	1. a FASTA file with the reference sequence.
	2. a GFF file with the coordinates of pairs of Borders that enclose a Window. Any number of Windows may be given and will be processed in parallel.
	3. a set of FASTQ files with reads that need to be haplotyped. Any number of samples may be given and will be processed in parallel.
	4. a set of BAM files made with `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_ using the respective reference sequence and FASTQ files.
	5. optional: a FASTA file containing the gRNA sequences in case CRISPR was performed by stable transformation with a CRISPR/gRNA delivery vector, see also :ref:`CRISPR <SMAPwindowcrispr>`.


| In the **SMAP haplotype-window** workflow, the user first selects Windows (loci to be haplotyped) enclosed by pairs of Border regions. Then, for each BAM file and each Window, **SMAP haplotype-window** extracts the ID's of reads that overlap with the respective Windows with at least one nucleotide. Using the list of read-IDs, a new temporary FASTQ file is created for each sample-Window combination. Then, for each sample-Window FASTQ file, the corresponding Border sequences are used for pattern-match read trimming with `Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_. The remaining read sequences per Window are considered haplotypes, which are counted and listed in an integrated haplotype table per sample and per Window.  
|
| **SMAP haplotype-window** considers the entire read sequence spanning the region between the Borders as haplotype.
| **SMAP haplotype-window** filters out genotype calls of Windows with low read depth and low frequency haplotypes to control for noise in the data.
| **SMAP haplotype-window** creates a multi-allelic haplotype matrix listing haplotype counts and frequencies per Window, per sample, across the sample set.
| **SMAP haplotype-window** plots the haplotype frequency distribution across all Windows per sample, and the distribution of haplotype diversity (number of distinct haplotypes per locus) across the sample set.
| **SMAP haplotype-window** can transform the haplotype frequency table into multi-allelic discrete genotype calls.

----
 
.. _SMAPwindowquickstart:
 
Quick Start
-----------

.. tabs::

   .. tab:: procedure

	  | **Step 1**
	  | 
	  | **SMAP haplotype-window** extracts haplotypes from reads aligned to a predefined set of loci, here called Windows, in a reference sequence. Each Window is enclosed by a pair of Border regions.
	  | Border regions can be defined at primer binding sites, either $with$ (Window 1) or *without* (Window 2) an off-set. Borders can be of variable length, defined by the user (typically 5-10 bp). Pairs of Borders can also be defined so that they enclose Sliding frames, for instance to process Shotgun data.
	  | 
	  | **Step 2**
	  | 
	  | Read mapping is used to assign reads to their corresponding locus on the reference genome. 
	  | Consider a sequenced fragment derived from a given genomic locus with a large deletion, or highly polymorphic region with multiple flanking SNPs, in the middle of the fragment. 
	  | Two flanking primers can bind the genome sequence of the sample and can amplify the fragment. Also, the two regions flanking the central polymorphism in the same read contain (near-)exact sequence similarity to the reference sequence of the genomic locus.
	  | Mapping reads with `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_, defines which genomic locus is the origin of the sequenced fragment (the maximal exact match that seeds the alignment), and extends the alignment outwards untill a maximum number of read-reference mismatches is reached.
	  | If read-reference alignments are truncated before the end of the read, BWA-MEM removes the unmapped region of the sequence read in the resulting BAM file (called soft-clipping).
	  | Consequently, the sequence of a given read in the FASTQ file (before read mapping) may have a different length compared to the corresponding read in the BAM file (after mapping). 
	  | Also, the polymorphisms that caused the truncation of the read alignment are no longer present in the BAM file (not as alignment, not as FASTQ sequence data), and can not be used to detect polymorphisms by direct read-reference alignment comparison.
	  | 
	  | **Step 3**
	  | 
	  | For each Window, **SMAP haplotype-window** will define the Window region in the reference genome by pairing Border regions defined in a GFF file. 
	  | For each BAM file and for each Window, **SMAP haplotype-window** will identify the IDs of reads that overlap with at least one nucleotide for a given Window, retrieve their original complete read sequence from the corresponding sample's FASTQ file and create a separate FASTQ file for each sample-Window combination. 
	  | These steps make sure that reads that are soft-clipped during read alignment by BWA-MEM but that initially do contain the Border sequences at their respective ends, can still be evaluated in their entirety. Soft-clipping results in partial read alignment and removal of the unmapped part of the sequence read from the BAM file.
	  | **SMAP haplotype-window** then retrieves the respective sequences for the upstream Border and downstream Border regions using the GFF coordinates and the reference genome FASTA sequence for each Window. 
	  |
	  | **Step 4**
	  | 
	  | All separate FASTQ files (one for each sample-Window combination) are then passed to `Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_ using the Window-specific pair of Border sequences for pattern trimming. 
	  | Because the Window is defined as the region *inbetween* the Borders (*i.e.* read regions retained after removal of the Borders), the entire read sequence spanning the Window is considered as a unique haplotype. 
	  | 
	  | 
	  | **Step 5**
	  | 
	  | These haplotypes are then counted per Window per sample, optionally filtered for (min/max) total read count per Window per sample.
	  | All individual sample specific haplotype count tables are integrated into a large haplotype count matrix.
	  | This procedure detects unique haplotypes in Windows enclosed by two known Border sequences consisting of any (*a priori* unknown) combination of InDels and/or SNPs, *without* using the BAM alignment itself for the detection of InDels and/or SNPs. The `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_ alignment is merely used for efficiently sorting reads across the reference genome and grouping by locus. 
	  | Haplotype counts are converted into relative frequencies, which can then be filtered to remove low-frequency noise.
	  | The final step of **SMAP haplotype-window** is only applicable on individuals and converts haplotype frequencies into discrete calls. 
	  | Using customizable frequency intervals, haplotype frequencies can either be transformed into dominant calls (0/1) or dosage calls (0/1/2/..).

   .. tab:: overview
	  
	  | The scheme below shows an overview of the entire **SMAP haplotype-window** workflow.
	  
	  .. image:: ../images/window/haplotype_window_scheme_short_TR_all.png
	  
   .. tab:: required input

	  .. tabs::

		 .. tab:: reference sequence
		 
			The FASTA file containing the reference sequence.

		 .. tab:: GFF
         
			| The `GFF <https://en.wikipedia.org/wiki/General_feature_format#:~:text=In%20bioinformatics%2C%20the%20general%20feature,DNA%2C%20RNA%20and%20protein%20sequences.>`_ file describes the position of the Border regions on the reference sequence in 9 columns. **SMAP haplotype-window** expects two Borders that together enclose a Window, which are paired based on the \'NAME=\' field in the 9th column. The file does not need to contain a header. These fields need to be specified:

				| 1. Name of the sequence in the reference that contains the Window.
				| 2. Source of the feature. [SMAP haplotype-window]. 
				| 3. Feature type. Because in SMAP haplotype-window pairs of Borders define Windows, two feature types are used: Border_upstream and Border_downstream. Each line in the GFF is one of those borders. Borders always come in pairs.
				| 4. The start coordinate of the Border region [in the 1-based GFF coordinate system].
				| 5. The end coordinate of the Border region [in the 1-based GFF coordinate system, value must always be higher than column 4].
				| 8. Score. Irrelevant for SMAP haplotype-window [.].
				| 7. Orientation of the Border [always +].
				| 8. Phase. Irrelevant for SMAP haplotype-window [.].
				| 9. Attributes of the Border, the field \'NAME=\' is required. This field is used to pair Borders (by exact \'NAME=\' matching), and define the corresponding Window regions. The field Name must be unique for each Window and will be used to name loci in the haplotype frequency tables.

			| Depending on the type of data (HiPlex or Shotgun Seq), a specific GFF file must be created to define pairs of Borders enclosing Windows.

				.. tabs::

					.. tab:: HiPlex / primer binding sites
					
						| For HiPlex data it is advised to use the 5-10 nucleotides on the 3' of the primer binding site, where they flank the Window (to extract the sequence read region *inbetween* the primers). 

						 .. csv-table::
						    :file: ../tables/window/example_HiPlex_gff.csv
						    :header-rows: 0

					.. tab:: Shotgun Sequencing / Sliding Windows
					
						| Shotgun Sequencing data may be analysed with a set of sliding Windows, with a customisable Window size (here 50), step size (here 20), and Border length (here 10). See also :ref:`Scripts <SMAPwindowgffscripts>` for template scripts for creating sliding windows.

						 .. csv-table:: 	  
						    :file: ../tables/window/example_Shotgun_gff.csv
						    :header-rows: 0

		 .. tab:: FASTQ
		 
			A set of FASTQ files with reads that need to be haplotyped.

		 .. tab:: BAM
			
			 A set of BAM files made with `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_ using the respective reference sequence and FASTQ files.
		 
	  
	  
   .. tab:: commands
      
	  The complete list of commands, and some examples, can be found at :ref:`Summary of Commands <SMAPwindowcommands>`.


----
	  
Output
------ 

**Tabular output**

.. tabs::

   .. tab:: General output

      By default, **SMAP haplotype-window** will return two .tsv files.  
 
      :purple:`haplotype counts`
      
      **counts_cx_fx_mx.tsv** (with x the value per option used in the analysis) contains the read counts (``-c``) and haplotype frequency (``-f``) filtered and/or masked (``-m``) read counts per haplotype per locus as defined in the BED file from **SMAP delineate**.  
      This is the file structure:
	  
		  ========= ========= ========== ======= ======= ========
		  Reference Locus     Haplotypes Sample1 Sample2 Sample..
		  ========= ========= ========== ======= ======= ========
		  Chr1      Window_1  ACGTCGTCGC 60      13      34
		  Chr1      Window_1  ACGTCGTCAC 19      90      51
		  Chr1      Window_2  GCTCATCG   70      63      87
		  Chr1      Window_2  GCTCTCG    108     22      134
		  ========= ========= ========== ======= ======= ======== 

      :purple:`relative haplotype frequency`
      
      **haplotypes_cx_fx_mx.tsv** contains the relative frequency per haplotype per locus in sample (based on the corresponding count table: counts_cx_fx_mx.tsv). The transformation to relative frequency per locus-sample combination inherently normalizes for differences in total number of mapped reads across samples, and differences in amplification efficiency across loci.  
      This is the file structure:

		  ========= ========= ========== ======= ======= ========
		  Reference Locus     Haplotypes Sample1 Sample2 Sample..
		  ========= ========= ========== ======= ======= ========
		  Chr1      Window_1  ACGTCGTCGC 0.76    0.13    0.40
		  Chr1      Window_1  ACGTCGTCAC 0.24    0.87    0.60
		  Chr1      Window_2  GCTCATCG   0.39    0.74    0.39
		  Chr1      Window_2  GCTCTCG    0.61    0.26    0.61
		  ========= ========= ========== ======= ======= ========

	  | Additionally **freqs_unfiltered.tsv** can be further filtered using the options ``-j`` (minimum distinct haplotypes) and ``-k`` (maximum distinct haplotypes), resulting in the file **freqs_distinct_haplotypes_filter.tsv**

   .. tab:: Additional output for individuals
   
	  | For individuals, if the option ``--discrete_calls`` is used, the program will return three additional .tsv files. Their order of creation and content is shown in the scheme :ref:`above <SMAPhaplostep4>`.
	  | The first file is called **haplotypes_cx_fx_mx_total_discrete_calls.tsv** and this file contains the total sum of discrete calls, obtained after transforming haplotype frequencies into discrete calls, using the defined ``--frequency_interval_bounds``. The total sum of discrete dosage calls is expected to be 2 in diploids and 4 in tetraploids.
	  | The second file is **haplotypes_cx_fx_mx_call.tsv**, which incorporates the filter ``--dosage_filter`` to remove loci per sample with an unexpected number of haplotype calls in **haplotypes_cx_fx_mx_total_discrete_calls.tsv**. The expected number of calls is set with option ``-z`` [use 2 for diploids, 4 for tetraploids].
	  | The third file, **haplotypes_cx_fx_mx_AF.tsv**, lists the population haplotype frequencies (over all individual samples) based on the total number of discrete haplotype calls relative to the total number of calls per Window.

**Graphical output**

