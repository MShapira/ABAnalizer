from classes.analytics import PositionDistribution, AADistribution
from utility import show_progress


# get distributions of aminoacid positions
def calculate_position_distribution(antibodies: list)->AADistribution:
    aad = AADistribution()

    # we need to collect all keys in our proteins
    longest_dict_keys = []
    for ab in antibodies:
        for key in ab.protein_sequence.seq_dict.keys():
            if key not in longest_dict_keys:
                longest_dict_keys.append(key)

    # smart bar for getting the time remaining
    progress_label = 'Generating pictures'
    show_progress(progress_label, 0.0)
    index = 0

    # collect the information about the aminoacid positions
    for key in longest_dict_keys:

        # for smart bar
        index += 1
        show_progress(progress_label, float(index) / float(len(longest_dict_keys)))

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