from classes.analytics import PositionDistribution, AADistributionfrom utility import show_progress, read_from_csv, generate_linear_chartfrom natsort import natsorted# get distributions of amino acid positionsdef calculate_position_distribution(antibodies: list)->AADistribution:    aad = AADistribution()    # we need to collect all keys in our proteins    longest_dict_keys = []    for ab in antibodies:        for key in ab.protein_sequence.seq_dict.keys():            if key not in longest_dict_keys:                longest_dict_keys.append(key)    # smart bar for getting the time remaining    progress_label = 'Generating bar chars'    show_progress(progress_label, 0.0)    index = 0    # collect the information about the amino acid positions    for key in longest_dict_keys:        # for smart bar        index += 1        show_progress(progress_label, float(index) / float(len(longest_dict_keys)))        amino_acids = []        for ab in antibodies:            try:                amino_acids.append(ab.protein_sequence.seq_dict[key])            except KeyError:                continue        pd = PositionDistribution(position=key, aa_array=amino_acids, maxlen=len(antibodies))        pd.aa_part_counter()        pd.generate_aa_distribution_pict()        aad.positions[key] = pd    return aad# construct the amino acids properties listdef construct_aa_prop_list()-> dict:    # get data from files    kidera = read_from_csv('ref_mat/Kidera_factors.csv', '3-Letter')    phy_chem = read_from_csv('ref_mat/AA_params_table.csv', '3-Letter')    # combine the data    for factor in kidera.keys():        for parameter in phy_chem.keys():            if factor.upper() == parameter.upper():                kidera[factor].update(phy_chem[parameter])    # print 1-letter code to folder_name.txt    with open('sessions/folder_name.txt', 'a') as file:        amino_acids = []        line = ''        for key in kidera:            amino_acids.append(kidera[key]['1-Letter'])        for aa in sorted(amino_acids):            line += aa        file.write(line + '\n')        file.close()    return kidera# generate the profile of property per residuesdef construct_property_profile(aad: AADistribution, prop_list: list, kidera: dict):    # smart bar for getting the time remaining    progress_label = 'Generating linear chars with kidera faactors'    show_progress(progress_label, 0.0)    index = 0    # for each property in the defined list calculate the weighted sum for each position    for property in prop_list:        # for smart bar        index += 1        show_progress(progress_label, float(index) / float(len(prop_list)))        positions = {}        for position in aad.positions.keys():            value = 0            for aa in aad.positions[position].parts_dict.keys():                for k in kidera:                    # find appropriate amino acid in the kidera list                    if kidera[k]['1-Letter'] == aa:                        value += aad.positions[position].parts_dict[aa] * kidera[k][property]            positions[position] = value        amino_acids = natsorted(positions.keys())        values = [positions[x] for x in amino_acids]        generate_linear_chart(x=amino_acids, y=values, xlabel='amino acid position', ylabel=property, fld_name='kidera_factors')