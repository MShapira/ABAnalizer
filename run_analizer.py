from classes.sequence import ProteinSequence
from classes.antiboby import Antibody


def sequences_parser(filename: str)->list:

    antibodies = []
    str = ''

    with open(filename) as file:
        for line in file.readlines():
            line= line.rstrip()
            # the way to find new seq and initiate new object
            if list(line)[0] == '>':

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
                str = str + line

    return antibodies

antibodies = sequences_parser('VHH_al.fa')


for ab in antibodies[1:5]:
    ab.protein_sequence.construct_seq_dict()
    ab.protein_sequence.identify_cdrs_and_frameworks()
    print('Name: {0}'.format(ab.name))
    print('Host organism: {0}'.format(ab.host))
    print('Resource: {0}'.format(ab.resource_of_origin))
    print('Sequence: {0}'.format(ab.protein_sequence))
    print('-' * 30)
print(len(antibodies))
print("#" * 30)