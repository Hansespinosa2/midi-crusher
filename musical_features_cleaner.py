import pretty_midi as pm
import instrument_analyzers as ia

def is_extreme_pitched(an_instr:pm.Instrument):
    """
    Check if an instrument has extreme pitch range.
    
    Args:
        an_instr (pm.Instrument): The instrument to check.
    
    Returns:
        bool: True if the instrument has extreme pitch range, False otherwise.
    """
    if ia.get_highest_note(an_instr) > 108 or ia.get_lowest_note(an_instr) < 21:
        return False
    

def is_four_four(a_midi_file:pm.PrettyMIDI):
    """
    Check if a midi file is in 4/4 time signature. 
    Currently not used because the pretty midi time signatures are not reliable.
    
    Args:
        a_midi_file (pm.PrettyMIDI): The midi file to check.
    
    Returns:
        bool: True if the midi file is in 4/4 time signature, False otherwise.
    """
    the_list = [True if time_signature.denominator == time_signature.numerator else False for time_signature in a_midi_file.time_signature_changes]
    
    return any(the_list)