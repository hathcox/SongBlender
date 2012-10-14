'''
Created on Nov 21, 2011

@author: haddaway
'''
import struct, wave
from difflib import SequenceMatcher
from itertools import imap
import cPickle as pickle

class Blender():

    def __init__(self):
        self.goodSongs = []
        self.badSongs = []
        self.highestValue = 32767
        self.lowestValue = -32768
        
    def findPatterns(self, leftSide, rightSide, numberOfIterations, riskFactor):
        '''
        Old outdated method, possibly useful in the future
        '''
        patterns = []
        sequenceMatcher = SequenceMatcher()
        sequenceMatcher.set_seqs(leftSide, rightSide)
        ratio = sequenceMatcher.ratio()
        print ratio
        if(True):
            matchingBlocks = sequenceMatcher.get_matching_blocks()
            print matchingBlocks
            for block in matchingBlocks:
                if(leftSide[block[0]:block[0] + block[2]] != '' and leftSide[block[0]:block[0] + block[2]] != ' ' ):
                    print "Found a pattern!"
                    print "Added:",leftSide[block[0]:block[0] + block[2]], "To the pattern list!"
                    patterns.append(leftSide[block[0]:block[0] + block[2]])
        
        return patterns
                
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
    
    def loadPatternsFromSong(self, song, patternListName):
        print "Loading Song..."
        goodChannels, goodSampleRate = self.pcm_channels(song)
        goodLeftChannels = goodChannels[0]
        
        tolerance = 100
        print "Builing Raw String..."
                
        rawString = '|'.join(imap(str, goodLeftChannels))
        print "Building String list"
        stringList = rawString.split('|0|')
        livingList = []
        
        print "Finding Initial patterns"
        for index, item in enumerate(stringList):
            if(len(item) > tolerance):
                livingList.append(stringList[index])
            
            
        print "Found [",len(livingList), "] initial Patterns"
        
        print "Returning patterns to ints"
        
        for index, pattern in enumerate(livingList):
            patternList = pattern.split('|')        
            livingList[index] = patternList
                
        print "Cleaning some of this shit up"
        
        print len(livingList[1])
             
        del goodChannels, patternList, goodSampleRate, goodLeftChannels,  rawString, stringList, 
     
        print "Writing this pattern set to disk....this might take a while since we have to buffer it...."
       
        fileHandle = open(patternListName, 'wb')
       
        counter = 0
        maxSize = len(livingList)
        while(counter < maxSize ):
            pickle.dump(livingList[counter], fileHandle)
            counter += 1
        
        print "Finished! "
        
    def loadPatternsFromDisk(self, patternListName):
        print "Starting!"
        fileHandle = open(patternListName, 'rb')
        print "Loading all patterns, this is going to be a while!"
        patternList = []
        notFinished = True
        while(notFinished):
            currentPattern = pickle.load(fileHandle)
            if(currentPattern != -1):   
                patternList.append(currentPattern)
            else:
                notFinished = False
            
        print "Finished loading Patterns!"
        
        return patternList

    def blendTwoSongsWithoutChange(self, goodSong, badSong, outputSong):
        '''
        When passed the string location of two wav songs, this will combine the two songs into a single song of the smallest length. 
        
        No values of the songs are changed, instead all of the data is just combined into a single stereo track
        
        '''
        
        newSong = wave.open(outputSong, 'w')
        newSong.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
        print "Loaded output Song"
        
        good_channels, good_sample_rate = self.pcm_channels(goodSong)
        good_left_channels = good_channels[0]
        good_right_channels = good_channels[1]
        print "Loaded good song"
        
        bad_channels, bad_sample_rate = self.pcm_channels(badSong)
        bad_left_channels = bad_channels[0]
        bad_right_channels = bad_channels[1]
        maxSize = len(good_left_channels)
        print "Loaded bad song"
            
        print "Making some shit"
        
        bufferSize = 100000
        buffer = []
        counter = 0
        inner = 0    
        while(counter < maxSize / bufferSize):
            inner = 0
            while(inner < bufferSize):
                average_left = int((good_left_channels[((counter * bufferSize )+inner) % maxSize -1] + bad_left_channels[((counter * bufferSize )+inner) % maxSize-1]) / 2)
                average_right = int((good_right_channels[((counter * bufferSize )+inner) % maxSize-1] + bad_right_channels[((counter * bufferSize )+inner) % maxSize-1]) / 2)
                average_value_packed = struct.pack('h', (average_left + average_right) /2)
                buffer.append(average_value_packed)
                buffer.append(average_value_packed)
                inner += 1
                del average_left, average_right, average_value_packed
                
            valueString = ''.join(buffer)
            newSong.writeframes(valueString)
            del valueString
            del buffer
            buffer = []
            print 'Progress:',counter, '/', (maxSize / bufferSize)
            counter += 1
        
        newSong.close()
        
        print "were done!"
        
        
        
        
        
        ##Extra scrap code
        
        
    '''
    counter = 0
    while counter < 3000000:
        pv = ''
        if(counter < 1000000):
            pv = struct.pack('h', counter % 20000)
        elif(counter < 2000000):
            pv = struct.pack('h', counter % 15000)
        else:
            pv = struct.pack('h', counter % -50) 
        finalValues.append(pv)
        counter +=1
        
   
       
    good_channels, good_sample_rate = blender.pcm_channels('babySongs/new3.wav')
    print len(good_channels)
      '''
        
        # More old Code
    '''
         print "Loading Song..."
    goodChannels, goodSampleRate = blender.pcm_channels(goodSong)
    goodLeftChannels = goodChannels[0]
    totalItems = goodLeftChannels[1000000:1000100]
    
    
    print "Removing negatives"
    for index, item in enumerate(totalItems):
        item += 100000
        totalItems[index] = item
        
    print "Loading Channels"
    goodLeftString = ''.join(imap(str, totalItems))
    
    print goodLeftString[:len(goodLeftString)/2]
    print goodLeftString[len(goodLeftString)/2:]
    
    print blender.findPatterns(goodLeftString[:len(goodLeftString)/2], goodLeftString[len(goodLeftString)/2:], 100, .3)
    '''
        
