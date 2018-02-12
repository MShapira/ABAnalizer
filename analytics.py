from classes.analytics import PositionDistribution, AADistribution


# get distributions of aminoacid positions
def calculate_position_distribution(antibodies: list)->AADistribution:
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
        pd = PositionDistribution(position=key, aa_array=aminoacids)
        pd.aa_part_counter()
        aad.positions[key] = pd

    return aad