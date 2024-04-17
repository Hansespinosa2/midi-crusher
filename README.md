# midi-crusher
This is a tool designed to allow people to take a midi file and intelligently compress it into a set number of instruments

Currently this tool can be used by cloning the repository and running the run.py file in python environment that has the numpy, pandas, and pretty_midi packages.
*It has not been test on MacOS or Linux yet*

Create a folder inside of the repository with the midi files that you would like to process, and then run the run.py file with the desired arguments.

Here is an example of usage:

`python3 run.py input_dir output_dir --HARSH --FOUR_FOUR`

This would run through all the midi files in the input_dir, and standardize them via the default six instrument mapping (guitar, piano, bass, drums, synth, and strings) and cut out all but the most important instruments and all non standard time songs.
