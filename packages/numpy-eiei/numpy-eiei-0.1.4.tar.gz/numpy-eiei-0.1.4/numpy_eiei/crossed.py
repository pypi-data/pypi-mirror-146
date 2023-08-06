from typing import List
from .onehot import (
    assign_two_ctx, assign_one_ctx_and_trgt, assign_missing_ctx,
    assign_random_to_unused)
import numpy as np


def eiei_crossed(encoded: List[int],
                 tokenlist_size: int,
                 embed_dim: int = 300,
                 max_context_size: int = 10,
                 sigma: float = None,
                 dtype=np.float16,
                 random_state: int = None,
                 shuffle: str = None,
                 fill: bool = False,
                 max_attempts: int = None,
                 max_patience: int = 20
                 ) -> np.ndarray:
    """Extreme Input Embedding Initialization (EIEI) for Multi-Label Inputs

    Parameters:
    -----------
    encoded: List[int]
        A list of token IDs, e.g. for a whole document or corpus. If you
          created a list of sequences (List[List[int]]) then flatten the
          array, e.g. `encoded=list(itertools.chain(*listofseqs))`

    tokenlist_size : int
        The number of unique tokens or resp. token IDs

    embed_dim : int (Default: 300)
        The desired size of the embedding vector for each token

    max_context_size : int (Default: 10)
        The maximum number of context tokens. The `eiei_crossed` algorithm
          increments the context size by factor 2 up to `max_context_size`.

    sigma : float (default: 1/embed_dim)
        The standard deviation of the normal distributed PRNG. The std. dev.
          is `1.0 / embed_dim` by default.

    dtype : np.dtype (Default: np.float16)
        The floating point precision.

    random_state : int (Default: None)
        Seed of the numpy PRNG

    shuffle : str (Default: 'equal')
        Every time the context size is incremented, a new training set is
          generated. The new training examples can be shuffled according
          the following goals:
            - 'equal' - Shuffle randomly
            - 'frequent' - Prefer examples with high frequency while shuffling
            - 'rare' - Prefer examples with low frequency while shuffling
            - None - Don't shuffle

    fill : bool (default: True)
        Assign random weights for uninitialized IDs in unused columns.

    max_attempts : int (Default: None)
        Maximum number of assignment attempts.

    max_patience: int (Default: 20)
        Maximum number of iterations while the number of zero-elements
          doesn't decrease. If violated the algorithm decreases the
          context size.

    Examples:
    ---------
        from numpy_eiei import eiei_crossed
        encoded = np.arange(10).reshape(2, 5).T
        emb = eiei_crossed(
            encoded, tokenlist_size=np.unique(encoded).shape[0],
            embed_dim=5, max_context_size=2, shuffle='frequent', fill=False)
    """
    # Initialize embedding weight matrix with 0s
    emb = np.zeros(shape=(tokenlist_size, embed_dim), dtype=dtype)

    stop = False
    num_attempts = 0
    if max_attempts is None:
        max_attempts = int(tokenlist_size * embed_dim)

    # scale the std. dev. of the random number depending on the embedding size
    if sigma is None:
        sigma = 0.1 / embed_dim

    # set random seed
    if random_state is not None:
        np.random.seed(random_state)

    # ensure that `max_context_size` is multiple of two
    max_context_size = 2 * (max_context_size // 2)

    # Number of columns available for each context size
    # The number of columns are fixed in `eiei_crossed`
    max_columns = embed_dim // (max_context_size // 2)
    n_block = 0

    # read dimensions
    n_seqlen, k = encoded.shape

    # (1) The outer For-loop to increment `context_size`
    # for context_size in range(2, max_context_size + 1, 2):
    for context_size in range(max_context_size, 1, -2):
        # (1b) Position Indicies of the Target ID and Context IDs
        ctx_pos = list(range(context_size + 1))
        trgt_pos = ctx_pos.pop(context_size // 2)

        # (1c.1) Create new training examples (multi-label)
        num = context_size + 1
        examples = [encoded[i:(i + num), :] for i in range(n_seqlen - num)]
        examples, freq = np.unique(examples, axis=0, return_counts=True)

        # (1d) Context Vector Weights
        t = np.arange(context_size) - context_size // 2 + .5
        t = np.exp(-np.abs(t) * 1. / 3.)
        v = t / t.sum()

        # (1/2) Reset offset
        offset = 0

        # (2d) shuffle indicies
        idx = np.arange(len(examples))
        if shuffle in (True, 'equal'):
            idx = np.random.permutation(idx)
        elif shuffle in ('frequent', 'most_common'):
            idx = np.random.choice(
                idx, size=len(idx), replace=False,
                p=freq[idx] / freq[idx].sum())
        elif shuffle in ('rare', 'edge_cases'):
            idx = np.random.choice(
                idx, size=len(idx), replace=False,
                p=(1. / freq[idx]) / (1. / freq[idx]).sum())

        # (2) Loop over training examples
        lowest_pct_zeros = (emb == 0).mean()
        patience_decrease = 0
        offset = offset % max_columns
        for exidx in idx:
            exbase = examples[exidx]
            for shift in range(k):
                # create new combinations by replacing the target ID
                ex = exbase.copy()
                colidx = np.roll(np.arange(k), shift)
                ex[trgt_pos, :] = exbase[trgt_pos, colidx]

                # Assign embedding weights in the next column
                e = (shift + offset) % max_columns + n_block * max_columns

                # (3) loop over each dimension
                for m in range(k):
                    # (3a) read target ID `i` and context IDs `j`
                    i = ex[trgt_pos, m]
                    j = ex[ctx_pos, m]

                    # (3b) initialize the first example always randomly
                    if (emb[:, e] == 0).all():
                        emb[j, e] = np.random.normal(
                            0.0, sigma, (context_size,))
                        emb[i, e] = np.dot(v, emb[j, e])
                        num_attempts += 1
                        continue  # next example

                    # (3c) Example consists of just 1 type of input
                    if (j == i).all():
                        emb[i, e] = np.random.normal(0.0, sigma, (1, ))
                        num_attempts += 1
                        continue  # next example

                    # (3d) Solve for missing target/context vectors/weights
                    num_ctx_missing = (emb[j, e] == 0).sum()  # `m`
                    flag_trgt_exist = emb[i, e] != 0

                    if flag_trgt_exist and (num_ctx_missing == 2):
                        try:
                            emb = assign_two_ctx(emb, e, i, j, v, sigma)
                            num_attempts += 1
                        except Exception:
                            print(f"ERROR: e:{e} i:{i} j:{j}")

                    elif (not flag_trgt_exist) and (num_ctx_missing == 1):
                        emb = assign_one_ctx_and_trgt(
                            emb, e, i, j, v, sigma)
                        num_attempts += 1

                    elif flag_trgt_exist and (num_ctx_missing == 1):
                        emb = assign_missing_ctx(emb, e, i, j, v)
                        num_attempts += 1

                    # DON'T. NEVER use `assign_missing_target` here.

                    # assign random weights
                    # (the algorithm wouldn't work without this!)
                    elif (not flag_trgt_exist) and (num_ctx_missing > 1):
                        mask = emb[j, e] == 0
                        idx = np.unique(j[mask])
                        if len(idx) > 0:
                            emb[idx[:-1], e] = np.random.normal(
                                0.0, sigma, (len(idx) - 1, ))
                            emb[i, e] = np.dot(v, emb[j, e])
                            num_attempts += 1

            # (2x) start in the next column for the next example
            offset += 1

            # (2) termination
            if num_attempts > max_attempts:
                stop = True
                print("Terminated: Max. num of assignement attempts reached")
                break

            # (2) abort and go to next context size
            pct_zeros = (emb == 0).mean()
            if pct_zeros < lowest_pct_zeros:
                patience_decrease = 0
                lowest_pct_zeros = pct_zeros
            else:
                patience_decrease += 1
            if patience_decrease > max_patience:
                break

        # (1z) Move to next block
        n_block += 1
        if stop:
            break

    # Assign random numbers to uninitialized IDs in the remaining columns
    if fill:
        emb = assign_random_to_unused(emb, sigma)

    # done
    return emb
