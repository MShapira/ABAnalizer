from analytics import calculate_position_distribution, construct_aa_prop_list, construct_property_profile
from utility import create_session_folder, show_progress, print_to_log, sequences_parser, get_longest_cdrs_and_frameworks
from pprint import pprint


create_session_folder()
kidera = construct_aa_prop_list()
pprint(kidera)
antibodies = sequences_parser('test.fa')

# smart bar for getting the time remaining
progress_label = 'Processing the cdr and frameworks filling'
show_progress(progress_label, 0.0)
index = 0

for ab in antibodies[1:20]:

    # for appropriate work of smart bar
    index += 1
    show_progress(progress_label, float(index) / float(len(antibodies[1:20])))
    ab.protein_sequence.identify_cdrs_and_frameworks()
    print_to_log('Name: {0}'.format(ab.name))
    print_to_log('Host organism: {0}'.format(ab.host))
    print_to_log('Resource: {0}'.format(ab.resource_of_origin))
    print_to_log('Sequence: {0}'.format(ab.protein_sequence))
    print_to_log('-' * 30)
print_to_log("#" * 30)
aad = calculate_position_distribution(antibodies[1:20])
get_longest_cdrs_and_frameworks(antibodies[1:20])

prop_list = [x for x in kidera['ALA'] if isinstance(kidera['ALA'][x], (float, int))]
construct_property_profile(aad, prop_list, kidera)