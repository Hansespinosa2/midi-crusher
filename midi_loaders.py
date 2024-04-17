import os
import pretty_midi as pm
from instrument_mappings import program_map_all_midis, program_map_default, class_to_program_mapping, read_custom_class_to_program_mapping, read_custom_program_map
import instrument_analyzers as ia
import musical_features_cleaner as mc



def load_midi_files(root_directory:str, company:str = None, console:str = None, max_files = None):
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





    loaded_midis = {}
    for i, file_path in enumerate(file_list):
        if  i >= max_files:
            break
        try:
            loaded_midis[file_path] = pm.PrettyMIDI(file_path)
        except:
            print(f'Failed to load file {i}, {file_path}')
    return loaded_midis
    


    
def get_program_to_class_hash():
    hash_table = {number: cls for number, cls, _ in program_map_all_midis}
    return hash_table

def get_program_to_compressed_hash():
    hash_table = {number: cls for number, cls, _ in program_map_default}
    return hash_table


def merge_instruments(instruments:list, the_program_map, max_instruments = None, bypass_default = False,class_to_program_map = None):
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


    
    #If user wants to bypass the default of merging the instruments with max 4 strings, 1 guitar, 1 lead, infinite drums, 1 bass, and 2 pianos
    if bypass_default == True and max_instruments !=None: 
        instruments = ia.get_dominant_instruments(instruments, k=max_instruments)
        

    merged = []

    for instrument in instruments:
        merged.extend(instrument.notes)
    
    merged.sort(key=lambda x: x.start)

    name = the_program_map[instruments[0].program] if not instruments[0].is_drum else 'Drums'
    if name != 'Drop':
        the_program = class_to_program_map[name]
        the_instrument = pm.Instrument(the_program, instruments[0].is_drum, name)
    else:
        return None
    

    the_instrument.notes.extend(merged)
    return the_instrument
        
def merge_to_six(a_midi_file,max_instruments = None, bypass_default = False,the_program_map_path=None, the_class_to_program_path=None):
    if the_program_map_path is None and the_class_to_program_path is None:
        the_program_map = get_program_to_compressed_hash()
        the_class_to_program_map = class_to_program_mapping
    else:
        the_program_map = read_custom_program_map(the_program_map_path)
        the_class_to_program_map = read_custom_class_to_program_mapping(the_class_to_program_path)
    the_dict = ia.separate_instruments_to_class(a_midi_file,the_program_map=the_program_map)
    instrument_list = []

    for keys, _ in the_dict.items():
        for keys1, _ in the_dict[keys].items():
            an_instrument = merge_instruments(the_dict[keys][keys1], the_program_map=the_program_map, max_instruments=max_instruments, bypass_default=bypass_default, class_to_program_map=the_class_to_program_map)
            if an_instrument is not None:
                instrument_list.append(an_instrument)
            
    
    return instrument_list

def get_file_paths(root_directory):
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