import os
import pretty_midi as pm
from globals_and_longs import data, my_data, class_to_program_mapping
import instrument_analyzers as ia
import musical_features_cleaner as mc



def load_midi_files(root_directory:str = 'vg_music_database', company:str = None, console:str = None,package:str= 'pretty_midi', max_files = None):
    file_list = []
    for root, _, files in os.walk(root_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    if max_files == None:
        max_files = len(file_list)
    file_path_split = [file.split('\\') for file in file_list]

    if console != None:
        file_list = [file for i, file in enumerate(file_list) if file_path_split[i][-3] == console]
    if company != None:
        file_list = [file for i, file in enumerate(file_list) if file_path_split[-4] == company]




    
    if package == 'pretty_midi':
        loaded_midis = {}
        for i, file_path in enumerate(file_list):
            if  i >= max_files:
                break
            try:
                loaded_midis[file_path] = pm.PrettyMIDI(file_path)
            except:
                print(f'Failed to load file {i}, {file_path}')
        return loaded_midis
    elif package == 'miditoolkit':
        import miditoolkit as mt

        loaded_midis = [mt.MidiFile(file_path) for file_path in file_list]
        return loaded_midis
    elif package == 'music21':
        import music21 as m21

        loaded_midis = [m21.converter.parse(file_path) for file_path in file_list]
        return loaded_midis
    else:
        return None
    


    
def get_program_to_class_hash():
    hash_table = {number: cls for number, cls, _ in data}
    return hash_table

def get_program_to_compressed_hash():
    hash_table = {number: cls for number, cls, _ in my_data}
    return hash_table


def merge_instruments(instruments:list, the_program_map = None, max_instruments = None, bypass_default = False):
    """
    Merge multiple same programmed instruments into a single instrument.
    
    Parameters:
    instruments (list): A list of instruments to be merged.
    
    Returns:
    pm.Instrument: The merged instrument.
    
    Raises:
    ValueError: If the instruments have different programs or drum status.
    """
    instruments = [instrument for instrument in instruments if len(instrument.notes) > 0 and not mc.is_extreme_pitched(instrument)]

    if the_program_map == None:
        the_program_map = get_program_to_class_hash()
    
    #If user wants to bypass the default of merging the instruments with max 4 strings, 1 guitar, 1 lead, infinite drums, 1 bass, and 2 pianos
    if bypass_default == True: 
        if max_instruments != None:
            instruments = ia.get_dominant_instruments(instruments, k=max_instruments)
    else:
        if instruments[0].is_drum:
            pass #Drums are always merged
        elif the_program_map[instruments[0].program] == 'Piano':
            instruments = ia.get_dominant_instruments(instruments, k=4)
        elif the_program_map[instruments[0].program] == 'Guitar':
            instruments = ia.get_dominant_instruments(instruments, k=2)
        elif the_program_map[instruments[0].program] == 'Bass':
            instruments = ia.get_dominant_instruments(instruments, k=2)
        elif the_program_map[instruments[0].program] == 'Lead':
            instruments = ia.get_dominant_instruments(instruments, k=3)
        elif the_program_map[instruments[0].program] == 'Strings':
            instruments = ia.get_dominant_instruments(instruments, k=4)
        

    merged = []

    for instrument in instruments:
        merged.extend(instrument.notes)
    
    merged.sort(key=lambda x: x.start)

    name = the_program_map[instruments[0].program] if not instruments[0].is_drum else 'Drums'
    if name != 'Drop':
        the_program = class_to_program_mapping[name]
        the_instrument = pm.Instrument(the_program, instruments[0].is_drum, name)
    else:
        return None
    

    the_instrument.notes.extend(merged)
    return the_instrument
        
def merge_to_six(a_midi_file,max_instruments = None, bypass_default = False):
    the_dict = ia.separate_instruments_to_class(a_midi_file,the_program_map=get_program_to_compressed_hash())
    instrument_list = []

    for keys, _ in the_dict.items():
        for keys1, _ in the_dict[keys].items():
            an_instrument = merge_instruments(the_dict[keys][keys1], the_program_map=get_program_to_compressed_hash(), max_instruments=max_instruments, bypass_default=bypass_default)
            if an_instrument is not None:
                instrument_list.append(an_instrument)
            
    
    return instrument_list

def get_file_paths(root_directory:str = 'vg_music_database'):
    file_list = []
    for root, _, files in os.walk(root_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list

def get_midi_file(file_path:str):
    try:
        the_file =  pm.PrettyMIDI(file_path)
    except:
        print(f'Failed to load file {file_path}')
        the_file = None
    return the_file