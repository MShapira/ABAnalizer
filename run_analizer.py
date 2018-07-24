from analytics import calculate_position_distribution, construct_aa_prop_list, construct_property_profile
from utility import create_session_folder, show_progress, print_to_log, sequences_parser
import sys

create_session_folder()
kidera = construct_aa_prop_list()
print_to_log(kidera)
print_to_log('#' * 30)

# get filename and throw the warning if it is empty
filename = sys.argv[-1]
if filename == sys.argv[0]:
    filename = input('Please, enter the data filename: ')
antibodies = sequences_parser(filename)

# smart bar for getting the time remaining
progress_label = 'Processing the cdr and frameworks filling'
show_progress(progress_label, 0.0)
index = 0

for ab in antibodies:

    # for appropriate work of smart bar
    index += 1
    show_progress(progress_label, float(index) / float(len(antibodies)))

    ab.protein_sequence.identify_cdrs_and_frameworks()
    print_to_log('Name: {0}'.format(ab.name))
    print_to_log('Host organism: {0}'.format(ab.host))
    print_to_log('Resource: {0}'.format(ab.resource_of_origin))
    print_to_log('Sequence: {0}'.format(ab.protein_sequence))
    print_to_log('-' * 30)
print_to_log("#" * 30)
aad = calculate_position_distribution(antibodies)

prop_list = [x for x in kidera['ALA'] if isinstance(kidera['ALA'][x], (float, int))]
construct_property_profile(aad, prop_list, kidera)