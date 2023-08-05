

def elim_apostrophes(args):
    """ strip apostrphes form items in dict args, allows for user to enslose characters and phrases that cannot naturally
    be parsed, such as spaces, or items beginning in a hyphen like negative numbers"""

    for key in args.keys():
        if isinstance(args[key], list):
            for i in range(0, len(args[key])):
                args[key][i] = args[key][i].replace("'", '')
        elif isinstance(args[key], str):
            args[key] = args[key].replace("'", '')
