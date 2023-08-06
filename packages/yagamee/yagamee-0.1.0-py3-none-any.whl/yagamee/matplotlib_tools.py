def init_rcparams():
    import json
    import matplotlib
    yagamee_rcparams = json.load(open('yagamee_rcparams.json'))
    matplotlib.rcParams.update(yagamee_rcparams)


def init_matplotlib():
    init_rcparams()
    import japanize_matplotlib
