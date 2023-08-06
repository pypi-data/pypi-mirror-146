import numpy as np
from numpy_eiei.crossed import eiei_crossed


def test00():
    encoded = np.arange(10).reshape(2, 5).T
    emb = eiei_crossed(
        encoded,
        tokenlist_size=np.unique(encoded).shape[0],
        embed_dim=5,
        max_context_size=2,
        shuffle='frequent',
        fill=False)
    assert not (emb == 0).all()
