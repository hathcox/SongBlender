'''
Created on Dec 1, 2011

@author: Hathcox
'''

import cPickle as pickle

class Pattern():
    '''
    This is a small section of raw wav data that will later be combined into a SongPattern
    '''

    def __init__(self):
        self.data = None
        
        