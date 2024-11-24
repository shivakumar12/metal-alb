"""
All the utility method that are required to perform git operations
"""
import argparse

def str2bool(v):
    """
    Return boolean value
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def split_strip_list(input_parameters, delimiter):
    """
    Split the input with given delimiter and return list.
    """
    input_list = input_parameters.split(delimiter)
    input_list = [x.strip(" ") for x in input_list]
    return input_list
