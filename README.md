# voice_separation
really basic voice separation algorythm using pyannote speaker diarization

you need to create, inside your folder with the python algorythm, a folder name "speaker segments", this folder is where the algorithm will put the voice he extract, he will create a lot of short wav file with a number corresponding to the voice id he decide to assign and the timing when the voide is speaking in the video, i advise to run the clear short wav file, which delete all the voice .wav file that last less than 1 sec. After that listen to the Wav file created and choose the voice you want to extract, identify his id and merge it with the merge wav segment function. 
I advise you run again on the voice wav file you created with the voice you target, the algorithm to eliminate the noise, but this time use the clean voice separation and ask it to run 5 time, most of the time after 3 turn the algorithm will have eliminate all the noise he can. 

The python file can be a little bit hard to install cause you need to put the way to access your folder, file for the algorythm to use them 
