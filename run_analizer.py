from classes.sequence import ProteinSequence
from classes.antiboby import Antibody
from analytics import calculate_position_distribution, construct_aa_prop_list
from utility import create_session_folder, show_progress, print_to_log


def sequences_parser(filename: str)->list:

    antibodies = []
    str = ''

    with open(filename) as file:
        lines = file.readlines()

        # smart bar for getting the time remaining
        progress_label = 'Parsing the input data'
        show_progress(progress_label, 0.0)
        index = 0

        for line in lines:

            # for appropriate work of smart bar
            index += 1
            show_progress(progress_label, float(index) / float(len(lines)))

            line = line.rstrip()
            # the way to find new seq and initiate new object
            if line[0] == '>':

                # add the sequence to its antibody object as to a previous object in antibodies list
                if len(antibodies) != 0 and str != '':
                    protein_sequence = ProteinSequence(seq=str)
                    antibodies[-1].protein_sequence = protein_sequence
                    str=''

                # generate hot points in class initiating
                laa = line.split('|')
                name = laa[0][1:]
                host = laa[2]
                res = laa[3]
                # initiate an object of class Antibody
                # todo: write a filter to rid out of the sequence duplicates
                antibody = Antibody(name=name, host=host, resource_of_origin=res)

                # define what kind of seq do we have
                if laa[5] == 'protein':
                    antibody.protein_sequence = True
                    antibody.nucleotide_sequence = False
                elif laa[5] == 'nucleotide':
                    antibody.protein_sequence = False
                    antibody.nucleotide_sequence = True
                antibodies.append(antibody)

            else:
                str += line
                # to fill the last line
                if line == lines[-1].rstrip():
                    protein_sequence = ProteinSequence(seq=str)
                    antibodies[-1].protein_sequence = protein_sequence

    return antibodies

create_session_folder()
construct_aa_prop_list()
antibodies = sequences_parser('VHH_al.fa')

# smart bar for getting the time remaining
progress_label = 'Processing the cdr and frameworks filling'
show_progress(progress_label, 0.0)
index = 0

for ab in antibodies[1:20]:

    # for appropriate work of smart bar
    index += 1
    show_progress(progress_label, float(index) / float(len(antibodies[1:20])))

    ab.protein_sequence.construct_seq_dict()
    ab.protein_sequence.identify_cdrs_and_frameworks()
    print_to_log('Name: {0}'.format(ab.name))
    print_to_log('Host organism: {0}'.format(ab.host))
    print_to_log('Resource: {0}'.format(ab.resource_of_origin))
    print_to_log('Sequence: {0}'.format(ab.protein_sequence))
    print_to_log('-' * 30)
print_to_log("#" * 30)
aad = calculate_position_distribution(antibodies[1:20])