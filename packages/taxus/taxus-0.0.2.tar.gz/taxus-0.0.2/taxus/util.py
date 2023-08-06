import numpy as np
import pandas as pd


def deseq_normalization(df: pd.DataFrame) -> pd.DataFrame:
    # Vanilla deseq2 size factors
    pseudo_reference = np.expm1(np.log1p(df).mean(axis=1))
    pseudo_ref_diff = df.div(pseudo_reference, axis=0).fillna(0)
    size_factors = pseudo_ref_diff.median()

    # custom sizefactors taking into account samples with very high counts
    # size_factors = dev_est_df.sum(axis=0) / dev_est_df.sum(axis=0).median()

    norm_df = df.div(size_factors, axis=1)
    return norm_df
