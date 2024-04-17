import pretty_midi as pm
from midi_loaders import get_file_paths, get_midi_file
from midi_loaders import merge_to_n
from musical_features_cleaner import is_four_four
from instrument_analyzers import total_notes
import argparse
import os


    
def main(INPUT_DIR, OUTPUT_DIR, FOUR_FOUR:bool = True, HARSH:bool=False,CUSTOM_INSTRUMENTS:str=None, CUSTOM_PROGRAMS:str=None):
    output_path = OUTPUT_DIR
    file_paths = get_file_paths(INPUT_DIR)

    if HARSH is True:
        max_instruments=1
        bypass_default=True
    else:
        max_instruments=None
        bypass_default=False

    if (CUSTOM_INSTRUMENTS is None)^ (CUSTOM_PROGRAMS is None):
        raise ValueError('CUSTOM_INSTRUMENTS and CUSTOM_PROGRAMS must both be specified or neither.')

    for i, file_path in enumerate(file_paths):
        the_mid_name = os.path.basename(file_path)
        midi_file = get_midi_file(file_path)
        if midi_file is not None and (is_four_four(midi_file) or ~FOUR_FOUR) and total_notes(midi_file) > 100:
            print(f"Reading {the_mid_name} with {len([instrument.program for instrument in midi_file.instruments])} instruments -> {i}/{len(file_paths)}")
            midi_out = pm.PrettyMIDI()
            midi_out.instruments.extend(merge_to_n(midi_file,max_instruments,bypass_default,the_program_map_path=CUSTOM_INSTRUMENTS, the_class_to_program_path=CUSTOM_PROGRAMS))
            print(f"Writing {the_mid_name} with {len([instrument.program for instrument in midi_out.instruments])} instruments  -> {i}/{len(file_paths)}")
            midi_out.write(f"{output_path}OUT_{i}_{the_mid_name}")
        else:
            continue
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process MIDI files.')
    parser.add_argument('INPUT_DIR', type=str, help='Directory of input MIDI files.')
    parser.add_argument('OUTPUT_DIR', type=str, help='Directory where processed MIDI files will be saved.')
    parser.add_argument('--FOUR_FOUR', type=bool, default=True, help='Filter MIDI files to process only those in 4/4 time signature.')
    parser.add_argument('--HARSH', type=bool, default=False, help='Apply harsh processing parameters.')
    parser.add_argument('--CUSTOM_INSTRUMENTS', type=str, default=None, help='Path to a custom instrument mapping file for MIDI processing. \n See the custom_instrument_example file for an example of how to structure.')
    parser.add_argument('--CUSTOM_PROGRAMS', type=str, default=None,help='Path to a custom program mapping. \n See the custom_program_example file for an example of how to structure.')


    args = parser.parse_args()

    main(args.INPUT_DIR, args.OUTPUT_DIR, args.FOUR_FOUR, args.HARSH, args.CUSTOM_INSTRUMENTS, args.CUSTOM_PROGRAMS)
