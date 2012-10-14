'''
Created on Nov 21, 2011

@author: haddaway
'''
import struct, wave

class Blender():

    def __init__(self):
        self.goodSongs = []
        self.badSongs = []
        self.highestValue = 32767
        self.lowestValue = -32768
        
    def pcm_channels(self, wave_file):
        """Given a file-like object or file path representing a wave file,
        decompose it into its constituent PCM data streams.
    
        Input: A file like object or file path
        Output: A list of lists of integers representing the PCM coded data stream channels
            and the sample rate of the channels (mixed rate channels not supported)
        """
        stream = wave.open(wave_file,"rb")
    
        num_channels = stream.getnchannels()
        sample_rate = stream.getframerate()
        sample_width = stream.getsampwidth()
        num_frames = stream.getnframes()
        
        #num_frames = 3000000
    
        raw_data = stream.readframes( num_frames ) # Returns byte data
        stream.close()
    
        total_samples = num_frames * num_channels
    
        if sample_width == 1: 
            fmt = "%iB" % total_samples # read unsigned chars
        elif sample_width == 2:
            fmt = "%ih" % total_samples # read signed 2 byte shorts
        else:
            raise ValueError("Only supports 8 and 16 bit audio formats.")
    
        integer_data = struct.unpack(fmt, raw_data)
        del raw_data # Keep memory tidy (who knows how big it might be)
    
        channels = [ [] for time in range(num_channels) ]
    
        for index, value in enumerate(integer_data):
            bucket = index % num_channels
            channels[bucket].append(value)
        
        del integer_data
        
        return channels, sample_rate
