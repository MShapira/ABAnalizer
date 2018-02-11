import subprocess


class ProteinSequence:
    def __init__(self, seq):
        self.whole_seq = seq
        self.chain = 'Heavy'
        self.seq_dict = {}
        self.frameworks = {}
        self.CDRs = {}

    # construct dictionary of aminoacids via its numbering
    def construct_seq_dict(self, scheme='c'):
        # get ANARCI results
        # todo: add an opportunity to chose method (chotia is default)
        anarci_result = subprocess.Popen(['ANARCI -i' + self.whole_seq + ' -s {0}'.format(scheme)],
                                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # todo: write an additional utility for detection the nearest species
        for line in anarci_result.stdout.readlines():
            line = line.decode('utf-8')
            # get rid of param strings in ANARCI output
            if list(line)[0] != '#':
                # leave only aa number and name
                key_value = [arg for arg in line.rstrip().split(' ')[1:] if (arg != '')]
                # construct the dictionary
                if len(key_value) == 2:
                    self.seq_dict[key_value[0]] = key_value[1]
                elif len(key_value) == 3:
                    self.seq_dict[key_value[0] + key_value[1]] = key_value[2]
            else:
                if list(line)[0] == "|" and line.split('|')[0] != 'species':
                    if line.split('|')[1] == "L":
                        self.chain = "Light"

    # create a dict with CDRs sequences and frameworks sequences
    def identify_cdrs_and_frameworks(self):
        if self.chain == 'Heavy':




    def __str__(self):
        return 'Whole Sequence: {0}\n'.format(self.whole_seq) + \
               'Sequence Dictionary: {0}\n'.format(self.seq_dict) + \
               'Chain: {0}\n'.format(self.chain) + \
               '\n'