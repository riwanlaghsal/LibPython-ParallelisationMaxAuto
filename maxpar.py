def interfere(t1, t2):

    r1 = set(t1.reads)
    w1 = set(t1.writes)

    r2 = set(t2.reads)
    w2 = set(t2.reads)

    cond_1 = bool(r1 & w2)
    cond_2 = bool(r2 & w1)
    cond_3 = bool(w1 & w2)

    return cond_1 or cond_2 or cond_3