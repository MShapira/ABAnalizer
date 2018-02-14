from classes.analytics import PositionDistribution, AADistribution
from utility import show_progress


# get distributions of aminoacid positions
def calculate_position_distribution(antibodies: list)->AADistribution:
    # todo: refactor for normal bar working
    show_progress('processing the analysis', percentage=0.05)
    aad = AADistribution()

    # we need to collect all keys in our proteins
    longest_dict_keys = []
    for ab in antibodies:
        for key in ab.protein_sequence.seq_dict.keys():
            if key not in longest_dict_keys:
                longest_dict_keys.append(key)

    # collect the information about the aminoacid positions
    for key in longest_dict_keys:
        aminoacids = []
        for ab in antibodies:
            try:
                aminoacids.append(ab.protein_sequence.seq_dict[key])
            except KeyError:
                continue
        pd = PositionDistribution(position=key, aa_array=aminoacids, maxlen=len(antibodies))
        pd.aa_part_counter()
        pd.generate_pict()
        aad.positions[key] = pd

    return aad