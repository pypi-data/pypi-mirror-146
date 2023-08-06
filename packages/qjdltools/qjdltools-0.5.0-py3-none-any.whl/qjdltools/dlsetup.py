# -*- coding:utf-8 -*-
'''
Setup and log.

Version 1.0  2022-04-15 20:35:22 by QiJi.
'''
import time
import os
import sys
from functools import wraps


def time_str():
    return time.strftime("%H:%M:%S", time.localtime())


def rank_zero_only(fn):
    """Function that can be used as a decorator to enable a function/method being called only on rank 0."""

    @wraps(fn)
    def wrapped_fn(*args, **kwargs):
        if rank_zero_only.rank == 0:
            return fn(*args, **kwargs)
        return None

    return wrapped_fn

def _get_rank() -> int:
    # SLURM_PROCID can be set even if SLURM is not managing the multiprocessing,
    # therefore LOCAL_RANK needs to be checked first
    rank_keys = ("RANK", "LOCAL_RANK", "SLURM_PROCID", "JSM_NAMESPACE_RANK")
    for key in rank_keys:
        rank = os.environ.get(key)
        if rank is not None:
            return int(rank)
    return 0


# add the attribute to the function but don't overwrite in case Trainer has already set it
rank_zero_only.rank = getattr(rank_zero_only, "rank", _get_rank())


class __redirection__:
    def __init__(self, mode='console', file_path=None):
        assert mode in ['console', 'file', 'both']

        self.mode = mode
        self.buff = ''
        self.__console__ = sys.stdout

        self.file = None
        if file_path is not None and mode != 'console':
            try:
                self.file = open(file_path, "w", buffering=1)
            except OSError:
                print('Fail to open log_file: {}'.format(
                    file_path))

    @rank_zero_only
    def write(self, output_stream):
        self.buff += output_stream
        if self.mode == 'console':
            self.to_console(output_stream)
        elif self.mode == 'file':
            self.to_file(output_stream)
        elif self.mode == 'both':
            self.to_console(output_stream)
            self.to_file(output_stream)

    @rank_zero_only
    def to_console(self, content):
        sys.stdout = self.__console__
        print(content, end='')
        sys.stdout = self

    @rank_zero_only
    def to_file(self, content):
        if self.file is not None:
            sys.stdout = self.file
            print(content, end='')
            sys.stdout = self

    @rank_zero_only
    def all_to_console(self, flush=False):
        sys.stdout = self.__console__
        print(self.buff, end='')
        sys.stdout = self

    @rank_zero_only
    def all_to_file(self, file_path=None, flush=True):
        if file_path is not None:
            self.open(file_path)
        if self.file is not None:
            sys.stdout = self.file
            print(self.buff, end='')
            sys.stdout = self
            # self.file.close()

    @rank_zero_only
    def open(self, file_path):
        try:
            self.file = open(file_path, "w", buffering=1)
        except OSError:
            print('Fail to open log_file: {}'.format(
                file_path))

    @rank_zero_only
    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    @rank_zero_only
    def flush(self):
        self.buff = ''

    @rank_zero_only
    def reset(self):
        sys.stdout = self.__console__


def unify_type(param, ptype=list, repeat=1):
    ''' Unify the type of param.

    Args:
        ptype: support list or tuple
        repeat: The times of repeating param in a list or tuple type.
    '''
    if repeat == 1:
        if type(param) is not ptype:
            if ptype == list:
                param = [param]
            elif ptype == tuple:
                param = (param)
    elif repeat > 1:
        if type(param) is ptype and len(param) == repeat:
            return param
        elif type(param) is list:
            param = param * repeat
        else:
            param = [param] * repeat
            param = ptype(param)

    return param


def args_list2dict(params):
    if type(params) is dict:
        return params
    elif type(params) is list:
        assert len(params) % 2 == 0, 'Must be paired args'
        options = {}
        for i in range(0, len(params), 2):
            options[params[i]] = params[i+1]

        return options
