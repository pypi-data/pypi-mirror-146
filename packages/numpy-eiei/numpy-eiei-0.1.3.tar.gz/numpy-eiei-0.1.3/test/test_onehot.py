import numpy as np
from numpy_eiei.onehot import (
    assign_missing_target, assign_one_ctx_and_trgt,
    assign_missing_ctx, assign_two_ctx, eiei)


# def test00():
#     encoded = list(range(10))
#     emb = eiei(
#         encoded,
#         tokenlist_size=len(set(encoded)),
#         embed_dim=2,
#         max_context_size=2,
#         pct_add=0.0,
#         fill=False)
#     assert (emb[:, 0] == 0).sum() == 1
#     assert (emb[:, 1] == 0).all()


def test01():
    encoded = list(range(10))
    emb = eiei(
        encoded,
        tokenlist_size=len(set(encoded)),
        embed_dim=3,
        max_context_size=2,
        pct_add=0.5,  # add some weights to next column
        fill=False)
    # assert (emb[:, 0] == 0).sum() == 1
    assert not (emb[:, 1] == 0).all()
    # assert (emb[:, 2] == 0).all()


def test10():
    tokenlist_size = 10
    embed_size = 20
    emb = np.zeros((tokenlist_size, embed_size))
    i = 2
    j = np.array([0, 1, 3, 4])
    v = np.array([.2, .3, .3, .2])
    e = 0
    emb[j, e] = [10, 20, 30, 40]
    emb = assign_missing_target(emb, e, i, j, v)
    assert emb[i, e] == 25.


def test20():
    tokenlist_size = 10
    embed_size = 20
    emb = np.zeros((tokenlist_size, embed_size))
    i = 2
    j = np.array([0, 1, 3, 4])
    v = np.array([.2, .3, .3, .2])
    e = 0
    sigma = 0.25
    emb[j[:-1], e] = [10, 20, 30]
    np.random.seed(42)
    emb = assign_one_ctx_and_trgt(emb, e, i, j, v, sigma)
    assert emb[i, e] == np.dot(v, emb[j, e])


def test30():
    tokenlist_size = 10
    embed_size = 20
    emb = np.zeros((tokenlist_size, embed_size))
    i = 2
    j = np.array([0, 1, 3, 4])
    v = np.array([.2, .3, .3, .2])
    e = 0
    emb[j[:-1], e] = [10, 20, 30]
    emb[i, e] = 40
    emb = assign_missing_ctx(emb, e, i, j, v)
    assert emb[j[-1], e] == 115.


def test40():
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
    assert emb[i, e] == np.dot(v, emb[j, e])
