from typing import List
import numpy as np
import random
import warnings


def assign_missing_target(emb: np.ndarray,
                          e: int,
                          i: int,
                          j: List[int],
                          v: List[float]
                          ) -> np.ndarray:
    """The target vector/weight is missing

    Parameters:
    -----------
    emb: np.ndarray
        The embedding matrix
    e: int
        The current column index `e` to which weights are assigned.
    i: int
        The row index of the target token
    j: List[int]
        A lis of row indicies of the context tokens
    v: List[float]
        The context tokens' weighting scheme

    Returns:
    --------
    emb: np.ndarray
        The manipulated embedding matrix

    Example:
    --------
        import numpy as np
        from numpy_eiei.onehot import assign_missing_target
        tokenlist_size = 10
        embed_size = 20
        emb = np.zeros((tokenlist_size, embed_size))
        i = 2
        j = np.array([0, 1, 3, 4])
        v = np.array([.2, .3, .3, .2])
        e = 0
        emb[j, e] = [10, 20,  30, 40]
        emb = assign_missing_target(emb, e, i, j, v)
        emb[i, e]   # 25.
    """
    emb[i, e] = np.dot(v, emb[j, e])
    return emb


def assign_one_ctx_and_trgt(emb: np.ndarray,
                            e: int,
                            i: int,
                            j: List[int],
                            v: List[float],
                            sigma: float = 0.25
                            ) -> np.ndarray:
    """Find next example with 1 unitialized context vector and target vector

    Parameters:
    -----------
    emb: np.ndarray
        The embedding matrix
    e: int
        The current column index `e` to which weights are assigned.
    i: int
        The row index of the target token
    j: List[int]
        A lis of row indicies of the context tokens
    v: List[float]
        The context tokens' weighting scheme
    sigma: float (default: 0.25)
        Standard deviation of N(0, sigma) to generate normal distributed
          random numbers.
    Returns:
    --------
    emb: np.ndarray
        The manipulated embedding matrix

    Example:
    --------
        import numpy as np
        from numpy_eiei.onehot import assign_missing_target
        tokenlist_size = 10
        embed_size = 20
        emb = np.zeros((tokenlist_size, embed_size))
        i = 2
        j = np.array([0, 1, 3, 4])
        v = np.array([.2, .3, .3, .2])
        e = 0
        sigma = 0.25
        emb[j[:-1], e] = [10, 20,  30]
        np.random.seed(42)
        emb = assign_one_ctx_and_trgt(emb, e, i, j, v, sigma)
        emb[i, e]   # == np.dot(v, emb[j, e])
    """
    exists = emb[j, e] != 0
    r = j[np.logical_not(exists)]
    if i == r:
        r_pos = np.argwhere(j == r)[0][0]
        emb[i, e] = np.dot(v[exists], emb[j[exists], e]) / (1. - v[r_pos])
        return emb
    else:
        emb[r, e] = np.random.normal(0.0, sigma, (1,))
        return assign_missing_target(emb, e, i, j, v)


def assign_missing_ctx(emb: np.ndarray,
                       e: int,
                       i: int,
                       j: List[int],
                       v: List[float]
                       ) -> np.ndarray:
    """One context vector/weight is missing

    Parameters:
    -----------
    emb: np.ndarray
        The embedding matrix
    e: int
        The current column index `e` to which weights are assigned.
    i: int
        The row index of the target token
    j: List[int]
        A lis of row indicies of the context tokens
    v: List[float]
        The context tokens' weighting scheme

    Returns:
    --------
    emb: np.ndarray
        The manipulated embedding matrix

    Example:
    --------
        import numpy as np
        from numpy_eiei.onehot import assign_missing_target
        tokenlist_size = 10
        embed_size = 20
        emb = np.zeros((tokenlist_size, embed_size))
        i = 2
        j = np.array([0, 1, 3, 4])
        v = np.array([.2, .3, .3, .2])
        e = 0
        emb[j[:-1], e] = [10, 20,  30]
        emb[i, e] = 40
        emb = assign_missing_ctx(emb, e, i, j, v)
        emb[j[-1], e]   # 115.
    """
    exists = emb[j, e] != 0
    q = j[np.logical_not(exists)]
    q_pos = np.argwhere(j == q)[0][0]
    emb[q, e] = (emb[i, e] - np.dot(v[exists], emb[j[exists], e])) / v[q_pos]
    return emb


def assign_two_ctx(emb: np.ndarray,
                   e: int,
                   i: int,
                   j: List[int],
                   v: List[float],
                   sigma: float = 0.25
                   ) -> np.array:
    """Find next example with exactly 2 uninitialized context vectors

    Parameters:
    -----------
    emb: np.ndarray
        The embedding matrix
    e: int
        The current column index `e` to which weights are assigned.
    i: int
        The row index of the target token
    j: List[int]
        A lis of row indicies of the context tokens
    v: List[float]
        The context tokens' weighting scheme
    sigma: float (default: 0.25)
        Standard deviation of N(0, sigma) to generate normal distributed
          random numbers.
    Returns:
    --------
    emb: np.ndarray
        The manipulated embedding matrix

    Example:
    --------
        import numpy as np
        from numpy_eiei.onehot import assign_missing_target
        tokenlist_size = 10
        embed_size = 20
        emb = np.zeros((tokenlist_size, embed_size))
        i = 2
        j = np.array([0, 1, 3, 4])
        v = np.array([.2, .3, .3, .2])
        e = 0
        sigma = 0.25
        emb[j[:-2], e] = [10, 20]
        emb[i, e] = 30
        np.random.seed(42)
        emb = assign_two_ctx(emb, e, i, j, v, sigma)
        emb[i, e]   # == np.dot(v, emb[j, e])
    """
    exists = emb[j, e] != 0
    q, r = j[np.logical_not(exists)]

    if q == r:
        tmp = np.argwhere(j == q)
        q_pos, r_pos = tmp[0][0], tmp[1][0]
        emb[q, e] = (
            emb[i, e] - np.dot(v[exists], emb[j[exists], e])) \
            / (v[q_pos] + v[r_pos])
        return emb
    else:
        emb[r, e] = np.random.normal(0.0, sigma, (1,))
        return assign_missing_ctx(emb, e, i, j, v)


def assign_random_to_unused(emb: np.ndarray,
                            sigma: float = 0.25
                            ) -> np.array:
    """Assign random numbers to uninitialized IDs in the remaining columns
    """
    ycols = (emb == 0).all(axis=0)
    xcols = (emb == 0).all(axis=1)
    emb[np.outer(xcols, ycols)] = np.random.normal(
        0.0, sigma, (sum(xcols) * sum(ycols), ))
    return emb


def eiei(encoded: List[int],
         tokenlist_size: int,
         embed_dim: int = 300,
         max_context_size: int = 10,
         pct_add: float = 0.0,
         sigma: float = None,
         dtype: np.dtype = np.float16,
         random_state: int = None,
         shuffle: str = 'equal',
         max_columns: int = None,
         max_examples: int = None,
         fill: bool = True,
         tol_zeros: float = 0.01,
         tol_decrease: float = 1e-8,
         max_patience_decrease: int = 20
         ) -> np.ndarray:
    """Extreme Input Embedding Initialization (EIEI) for One-Hot Inputs

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
        The maximum number of context tokens. The `eiei` (onehot) algorithm
          increments the context size by factor 2 up to `max_context_size`.

    max_patience : int (Default: 4)
        The number of loops over the whole training set where the termination
          criteron is NOT checked.

    pct_add : float (Default: 0.0)
        The probability of assigning weights to the next column too.

    sigma : float (default: 1/embed_dim)
        The standard deviation of the normal distributed PRNG. The std. dev.
          is `1.0 / embed_dim` by default.

    dtype : np.dtype (Default: np.float16)
        The floating point precision.

    random_state : int (Default: None)
        Seed of the numpy PRNG

    shuffle : str (Default: 'equal')
        Every time the column index `e` is incremented, a new training set is
          generated. The new training examples can be shuffled according
          the following goals:
            - 'equal' - Shuffle randomly
            - 'frequent' - Prefer examples with high frequency while shuffling
            - 'rare' - Prefer examples with low frequency while shuffling
            - None - Don't shuffle

    max_columns : int (default: None)
        The maximum number of embedding matrix columns used per context size.

    max_examples : int (default: None)
        Limit the number of examples used to initialize missing embedding
          weights. The limit is imposed after the shuffling step.

    fill : bool (default: True)
        Assign random weights for uninitialized IDs in unused columns.

    tol_zeros : float (Default: 0.01)
        The percentage of zeros in the embedding matrix below which
          the EIEI algorithm stops.

    tol_decrease : float (Default: 1e-8)
        The required decrease in percentage of zeros in the embedding matrix.

    max_patience_decrease : int (Default: 20)
        The number of times to violate tol_decrease before EIEI algorithm stops

    Examples:
    ---------
        from numpy_eiei import eiei
        encoded = list(range(10))
        emb = eiei(
            encoded, tokenlist_size=len(set(encoded)), embed_dim=2,
            max_context_size=2, pct_add=0.0, fill=False)
    """
    # Initialize embedding weight matrix with 0s
    emb = np.zeros(shape=(tokenlist_size, embed_dim), dtype=dtype)
    n_weights = np.prod(emb.shape)
    lowest_pct_zeros = (emb == 0).sum() / n_weights
    patience_decrease = 0
    stop = False

    # scale the std. dev. of the random number depending on the embedding size
    if sigma is None:
        sigma = 0.1 / embed_dim

    # set random seed
    if random_state is not None:
        np.random.seed(random_state)

    # ensure that `max_context_size` is multiple of two
    max_context_size = 2 * (max_context_size // 2)

    # maximal num of rounds for each context size
    if max_columns is None:
        max_columns = embed_dim // (max_context_size // 2)

    # There are three loops
    # - The outer while loop increments `context_size` from 2,4,6,...
    # - The inner while loop increments to the e-th column of `emb[:, e]`
    # - The For loop iterates over the available examples to assign weights
    context_size = 0  # `c`
    e = 0

    # (1) The outer While-loop to increment `context_size`
    while (context_size + 2) <= max_context_size:
        # abort if inner loop reach its end
        if e >= embed_dim:
            break

        # (1a) Increment context_size by 2
        context_size += 2
        cur_round = 0

        # (1b) Create new training examples
        num = context_size + 1
        examples = [encoded[i:(i + num)] for i in range(len(encoded) - num)]
        examples = np.array(examples)
        examples, freq = np.unique(examples, axis=0, return_counts=True)

        # (1c) Position Indicies of the Target ID and Context IDs
        ctx_pos = list(range(context_size + 1))
        trgt_pos = ctx_pos.pop(context_size // 2)

        # (1d) Context Vector Weights
        t = np.arange(context_size) - context_size // 2 + .5
        t = np.exp(-np.abs(t) * 1. / 3.)
        v = t / t.sum()

        # (1e) Reset counter
        cnt = np.zeros((len(examples),), dtype=int)
        prev_cnt = cnt.sum()

        # (2) loop over all embedding columns
        while e < embed_dim:
            # (2a) loop over all examples
            flag_first = True

            # (2b) only select unused examples (use each example only once!)
            idx = np.where(cnt == 0)[0]

            # (2c) abort inner while loop
            if (idx.size == 0) or (cur_round > max_columns):
                break  # => increase context_size!

            # (2d) shuffle indicies
            if shuffle in (True, 'equal'):
                available = np.random.permutation(idx)
            elif shuffle in ('frequent', 'most_common'):
                available = np.random.choice(
                    idx, size=len(idx), replace=False,
                    p=freq[idx] / freq[idx].sum())
            elif shuffle in ('rare', 'edge_cases'):
                available = np.random.choice(
                    idx, size=len(idx), replace=False,
                    p=(1. / freq[idx]) / (1. / freq[idx]).sum())
            else:
                available = idx

            # (2e) Limit the number of examples used
            if max_examples is not None:
                available = available[:max_examples]

            # (3) loop over available/unused training examples
            for a in available:

                # (3a) read target ID `i` and context IDs `j`
                ids = examples[a, :]
                i = ids[trgt_pos]
                j = ids[ctx_pos]

                # (3b) initialize the first example always randomly
                if flag_first:
                    cnt[a] += 1
                    emb[j, e] = np.random.normal(0.0, sigma, (context_size,))
                    emb[i, e] = np.dot(v, emb[j, e])
                    flag_first = False  # run it only once
                    continue  # next example

                # (3c) Example consists of just 1 type of input
                if (j == i).all():
                    if emb[i, e] == 0:
                        emb[i, e] = np.random.normal(0.0, sigma, (1, ))
                        continue  # next example

                # (3d) Solve for missing target/context vectors/weights
                num_ctx_missing = (emb[j, e] == 0).sum()  # `m`
                flag_trgt_exist = emb[i, e] != 0
                prev_a = cnt[a]  # to check if there was a match

                if flag_trgt_exist and (num_ctx_missing == 2):
                    cnt[a] += 1
                    emb = assign_two_ctx(emb, e, i, j, v, sigma)

                elif (not flag_trgt_exist) and (num_ctx_missing == 1):
                    cnt[a] += 1
                    emb = assign_one_ctx_and_trgt(emb, e, i, j, v, sigma)

                elif flag_trgt_exist and (num_ctx_missing == 1):
                    cnt[a] += 1
                    emb = assign_missing_ctx(emb, e, i, j, v)

                elif (not flag_trgt_exist) and (num_ctx_missing == 0):
                    cnt[a] += 1
                    emb = assign_missing_target(emb, e, i, j, v)

                # (3e) assign weights in the next column too?
                # - don't run if it's last column
                # - run only if the training example was added in column e
                # - only if no weight exists for all context vec and trgt
                # - run only until `pct_add` percent of elements are assigned
                if ((e + 1) < embed_dim) and (prev_a != cnt[a]):
                    if (emb[j, e + 1] == 0).all():
                        if (emb[:, e + 1] != 0).mean() < pct_add:
                            cnt[a] += 1
                            emb[j, e + 1] = np.random.normal(
                                0.0, sigma, (context_size,))
                            emb[i, e + 1] = np.dot(v, emb[j, e + 1])

            # (2f) termination
            pct_zeros = (emb == 0).sum() / n_weights
            if pct_zeros < tol_zeros:
                stop = True
                break

            if (pct_zeros + tol_decrease) < lowest_pct_zeros:
                patience_decrease = 0
                lowest_pct_zeros = pct_zeros
            else:
                patience_decrease += 1

            if patience_decrease > max_patience_decrease:
                stop = True
                break

            # (2g) set counter
            if prev_cnt < cnt.sum():
                e += 1
                cur_round += 1
                prev_cnt = cnt.sum()
            else:
                warnings.warn((
                    "No change to the embedding happenend. Please add more "
                    "data or change the EIEI settings."))
                break

        # terminate
        if stop:
            break

    # Assign random numbers to uninitialized IDs in the remaining columns
    if fill:
        emb = assign_random_to_unused(emb, sigma)

    # done
    return emb
