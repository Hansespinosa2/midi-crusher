import pretty_midi as pm
import midi_loaders as ml

def get_highest_note(an_instr:pm.Instrument):
    return max([note.pitch for note in an_instr.notes])

def get_lowest_note(an_instr:pm.Instrument):
    return min([note.pitch for note in an_instr.notes])

def separate_instruments_to_class(midi_file:pm.PrettyMIDI,the_program_map = None):
    if the_program_map is None:
        the_program_map = ml.get_program_to_class_hash()
    separated = {}
    for instrument in midi_file.instruments:
        if the_program_map[instrument.program] not in separated:
            separated[the_program_map[instrument.program]] = {}
        if instrument.is_drum not in separated[the_program_map[instrument.program]]:
            separated[the_program_map[instrument.program]][instrument.is_drum] = []
        separated[the_program_map[instrument.program]][instrument.is_drum].append(instrument)
    return separated

def get_program_list(midi_files, package = 'pretty_midi'):

    if package == 'pretty_midi':
        program_list = []
        for midi in midi_files:
            programs = [instrument.program for instrument in midi.instruments]
            program_list.append(programs)
        return program_list
    else:
        return None
    
#Create a function that will input a list of instruments, a parameter k and will return an output of the k most dominent instruments
#Dominance is defined as a combination of the number of notes and their duration

def get_dominant_instruments(instruments, k):
    """
    Get the k most dominant instruments from a list of instruments.
    
    Parameters:
    instruments (list): A list of instruments.
    k (int): The number of dominant instruments to return.
    
    Returns:
    list: The k most dominant instruments.
    """
    return sorted(instruments, key=lambda instrument: len(instrument.notes) * sum([note.end - note.start for note in instrument.notes]), reverse=True)[:k]

def total_notes(midi_file):
    """
    Get the total number of notes in a midi file.
    
    Parameters:
    midi_file (pm.PrettyMIDI): The midi file to check.
    
    Returns:
    int: The total number of notes in the midi file.
    """
    return sum([len(instrument.notes) for instrument in midi_file.instruments])