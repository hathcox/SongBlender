import Blender, wave, struct, random, sys


blender = Blender.Blender()
goodSong = 'goodSongs/glitch.wav'
badSong = 'badSongs/glitchmob.wav'
newSong ='babySongs/new3.wav'

def pickPattern(patternList, blankTolerance):
    randomPattern = random.randint(0, len(patternList) +blankTolerance)
    if(randomPattern > len(patternList) -1):
        return [0 for item in patternList[random.randint(0,len(patternList)-1)]]
    else:
        return patternList[randomPattern]

if __name__ == '__main__':
    #blender.blendTwoSongsWithoutChange(goodSong, badSong, newSong)
    
    #blender.loadPatternsFromSong(badSong, 'rawPatterns/test.p')
    
    print blender.loadPatternsFromDisk('rawPatterns/test.p')
       
#    print "Starting Song Generation"
#        
#    newSong = wave.open('babySongs/new5.wav', 'w')
#    newSong.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
#    print "Loaded output Song"
#    
#    print "Making some shit"
#    
#    maxSize = len(goodLeftChannels)
#    
#    del goodLeftChannels
#    
#    counter = 0
#    bufferSize = 100000
#    buffer = []
#    inner = 0 
#    while( counter < maxSize/ bufferSize):
#        inner = 0
#        while(inner < bufferSize):
#            pattern = pickPattern(livingList , 1)
#            for number in pattern:
#                number = int(number)
#                value = struct.pack('h', number)
#                buffer.append(value)
#                buffer.append(value)
#                    
#            inner+=len(pattern)
#        valueString = ''.join(buffer)
#        newSong.writeframes(valueString)
#        del valueString
#        del buffer
#        buffer = []
#        print 'Progress:',counter, '/', (maxSize / bufferSize)
#        counter += 1
#        
#    print "Done!"
#    newSong.close()
    