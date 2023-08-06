#  This file is part of SALSA software
#
#  Copyright (c) 2022 - SALSA Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/biomics-pasteur-fr/salsa
#
##############################################################################
import pandas as pd
from pylab import *
import click
import statsmodels.api
import statsmodels.formula
import statsmodels.stats.multitest
from tqdm import tqdm


@click.command()
@click.option("--infile", type=click.STRING, required=True)
@click.option("--outfile", type=click.STRING, required=True)
@click.option("--multiple-correction", type=click.Choice(["fdr_bh", "bonferroni"]), default="fdr_bh")
@click.option("--separator", default=";")
@click.option("--name-group1", required=True)
@click.option("--name-group2", required=True)
@click.option("--name-log2-foldchange", default="_log2FoldChange")
@click.option("--name-pvalue-adjusted", default="_padj")
@click.option("--image", default="scatter.png")
def compute_ttest(**kwargs):
    """Compute ttest for each line using two groups of genes

    ttest is computed using the log2Foldchange; The pvalues is used to weight the values.
    Output is a set of pvalues (and weighted pvalues) for which multiple testing is also perfomed

        python compute_ttest.py compute-ttest --name-group1 Group1 --name-group2 Group2 \
            --name-log2-foldchange L2FC --name-log2-foldchange L2FC \
            --infile 220414_ES_Transcriptomics_Grouped_Gt3_Vs_NonGt3.csv \
            --outfile 220414_ES_Transcriptomics_Grouped_Gt3_Vs_NonGt3_ttest.csv



    """
    df = pd.read_csv(kwargs["infile"], sep=kwargs["separator"])

    df = df.set_index("Unnamed: 0")
    df = df.dropna()

    GA = [x for x in df.columns if kwargs["name_group1"] in x and kwargs["name_log2_foldchange"] in x]
    GAp = [x for x in df.columns if kwargs["name_group1"] in x and kwargs["name_pvalue_adjusted"] in x]

    GB = [x for x in df.columns if kwargs["name_group2"] in x and kwargs["name_log2_foldchange"] in x]
    GBp = [x for x in df.columns if kwargs["name_group2"] in x and kwargs["name_pvalue_adjusted"] in x]

    # store pvalues, weigted pvalues
    pvalues = []
    pvaluesW = []
    dfGA = df[GA]
    dfGB = df[GB]

    print(f"Found {len(GA)} columns in group1 and {len(GB)} columns in group2 (log2 fold change)")
    print(f"Found {len(GAp)} columns in group1  and {len(GBp)} columns in group2 (pvalue adjusted)")
    if not len(GA) or not len(GB) or not len(GAp) or not len(GBp):  # pragma: no cover
        print("Something wrong with your group name. Could not find any match")
        print(df.columns)
        return

    for i in tqdm(range(len(df))):

        wA = -log10(df[GAp].iloc[i].values)
        wA = wA / sum(wA) * len(wA)

        wB = -log10(df[GBp].iloc[i].values)
        wB = wB / sum(wB) * len(wB)

        compW = statsmodels.stats.weightstats.CompareMeans.from_data(
            dfGA.iloc[i].values, dfGB.iloc[i].values, weights1=wA, weights2=wB
        )
        (T_statsW, P_valueW, degrees_f) = compW.ttest_ind()

        comp = statsmodels.stats.weightstats.CompareMeans.from_data(dfGA.iloc[i].values, dfGB.iloc[i].values)
        (T_stats, P_value, degrees_f) = comp.ttest_ind()

        pvalues.append(P_value)
        pvaluesW.append(P_valueW)

    res = pd.DataFrame(
        {"pvalue": pvalues, "weighted_pvalue": pvaluesW, "muA": df[GA].mean(axis=1), "muB": df[GB].mean(axis=1)}
    )

    (
        _,
        correctedPvalues,
        _,
        _,
    ) = statsmodels.stats.multitest.multipletests(res["pvalue"].values, alpha=0.05, method="fdr_bh")
    (
        _,
        correctedPvaluesW,
        _,
        _,
    ) = statsmodels.stats.multitest.multipletests(res["weighted_pvalue"].values, alpha=0.05, method="fdr_bh")

    res["corrected_pvalue"] = correctedPvalues
    res["corrected_weighted_pvalue"] = correctedPvaluesW

    query = "abs(muA)>1 and abs(muB)>1 and corrected_pvalue<0.05"
    N = len(res.query(query))
    print(f"Found {len(res.query('pvalue<0.05'))} genes with pvalues below 0.05")
    print(f"Found {len(res.query('weighted_pvalue<0.05'))} genes with weighted pvalues below 0.05")
    print(f"Found {len(res.query('corrected_pvalue<0.05'))} genes with corrected pvalues below 0.05")
    print(f"Found {len(res.query('corrected_weighted_pvalue<0.05'))} genes with corrected weighted pvalues below 0.05")
    print(f"Found {N} genes with corrected pvalues below 0.05 and absolute average fold change > 1 in both groups")
    scatter(
        -log10(res.query(query)["pvalue"]),
        -log10(res.query(query)["weighted_pvalue"]),
        c=res.query(query)["muB"],
        s=12,
        cmap="jet",
    )
    colorbar()
    xlabel("-log10 pvalue")
    xlabel("-log10 weighted pvalue")
    # plot([0,6], [0,6], alpha=0.5, c='grey')

    savefig(kwargs["image"])

    res.to_csv(kwargs["outfile"])
