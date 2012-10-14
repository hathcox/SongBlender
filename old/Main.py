import Blender, wave, struct, random

blender = Blender.Blender()
goodSong = 'goodSongs/popCulture.wav'
badSong = 'badSongs/glitchmob.wav'

newSong = wave.open('babySongs/new3.wav', 'w')
newSong.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
print "Loaded new Song"

if __name__ == '__main__':
    
    good_channels, good_sample_rate = blender.pcm_channels(goodSong)
    good_left_channels = good_channels[0]
    good_right_channels = good_channels[1]
    print len(good_left_channels)
    print "Loaded good song"
    
    bad_channels, bad_sample_rate = blender.pcm_channels(badSong)
    bad_left_channels = bad_channels[0]
    bad_right_channels = bad_channels[1]
    print len(bad_left_channels)
    print "Loaded bad song"
    
    finalValues = []
    
    print "Making some shit"
    
    bufferSize = 200000
    iterations = len(bad_channels[0]) / bufferSize
    
    
    for iteration in range(iterations): 
        for index in range(len(bad_channels[0]) * iteration):
            average_left = int((good_left_channels[index] + bad_left_channels[index]) / 2)
            average_right = int((good_right_channels[index] + bad_right_channels[index]) / 2)
    
            average_value_packed = struct.pack('h', (average_left + average_right) /2)
            finalValues.append(average_value_packed)
            
            del average_left, average_right, average_value_packed
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
    '''    
    print "were done!"
    valueString = ''.join(finalValues)
    newSong.writeframes(valueString)
    newSong.close()
        
        
        
        