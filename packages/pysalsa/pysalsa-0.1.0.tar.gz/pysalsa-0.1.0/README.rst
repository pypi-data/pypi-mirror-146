SALSA
======

Set of scripts related to biomics projects and provided by the SALSA group 



.. image:: https://badge.fury.io/py/salsa.svg
    :target: https://pypi.python.org/pypi/salsa

.. image:: https://github.com/biomics-pasteur-fr/salsa/actions/workflows/main.yml/badge.svg?branch=main
    :target: https://github.com/biomics-pasteur-fr/salsa/actions/workflows/main.yml

.. image:: https://coveralls.io/repos/github/biomics-pasteur-fr/salsa/badge.svg?branch=main
    :target: https://coveralls.io/github/biomics-pasteur-fr/salsa?branch=main




:Python version: 3.7, 3.8, 3.9
:Issues: `On github <https://github.com/biomics-pasteur-fr/salsa/issues>`_

Tutorial
=========

comute-test sub command
-----------------------

Compute ttest of a input file that contains two groups of genes with their log2 fold change and pvalues. Input file has this header::

    gene, Group1_sample1_L2FC, Group1_sample2_L2FC, Group1_sample3_L2FC, Group1_sample4_L2FC, 
          Group1_sample5_padj, Group1_sample6_padj, Group1_sample7_padj, Group1_sample8_padj, 

where Group1 and Group2 are tag to defined the two groups, and log2FoldChange and padj two patterns to set the log Fold change and adjuster pvalues columns. This names can be set to whatever string since options can be used to specify them. 

See an example in test/data/test_compute_ttest.csv

:: 

   salsa compute-ttest --infile test.csv --outpfile out.csv --name-group1  Group1 --name-group2 Group2  \
       --name-log2-foldchange L2FC --name-log2-foldchange L2FC


