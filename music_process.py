#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, division, print_function

import argparse
import sys

from madmom.audio import SignalProcessor
from madmom.features import (ActivationsProcessor, DBNBeatTrackingProcessor,
                             RNNBeatProcessor)
from madmom.io import write_beats
from madmom.ml.nn import NeuralNetworkEnsemble
from madmom.processors import IOProcessor, io_arguments_single

def main():
    """ music_process """

    # define parser
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=
        '''
        python music_process.py ./data/Jian_chrous.wav -o ./data/jian_beat.txt
        ''')
    # version
    p.add_argument('--version', action='version',
                   version='FDGame-music-process-0.1')
    # input/output options
    # p.add_argument('single')
    # p.add_argument('./data/Jian_chrous.wav')
    io_arguments_single(p)
    ActivationsProcessor.add_arguments(p)
 
    # signal processing arguments
    SignalProcessor.add_arguments(p, norm=False, gain=0)
 
    # peak picking arguments
    DBNBeatTrackingProcessor.add_arguments(p)
    NeuralNetworkEnsemble.add_arguments(p, nn_files=None)

    # parse arguments
    args = p.parse_args()

    # set immutable arguments
    args.fps = 100

    # print arguments
    if args.verbose:
        print(args)

    # input processor
    if args.load:
        # load the activations from file
        in_processor = ActivationsProcessor(mode='r', **vars(args))
    else:
        # use a RNN to predict the beats
        in_processor = RNNBeatProcessor(**vars(args))

    # output processor
    if args.save:
        # save the RNN beat activations to file
        out_processor = ActivationsProcessor(mode='w', **vars(args))
    else:
        # track the beats with a DBN and output them
        beat_processor = DBNBeatTrackingProcessor(**vars(args))
        out_processor = [beat_processor, write_beats]

    # create an IOProcessor
    processor = IOProcessor(in_processor, out_processor)

    # and call the processing function
    args.func(processor, **vars(args))


if __name__ == '__main__':
    main()
