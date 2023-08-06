def init_rcparams():
    import matplotlib
    from yagamee.yagamee_rcparams import yagamee_rcparams
    matplotlib.rcParams.update(yagamee_rcparams)


def init_matplotlib():
    init_rcparams()
    import japanize_matplotlib
