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
        # todo: add an opportunity to choose method (chotia is default)
        anarci_result = subprocess.Popen(['ANARCI -i' + self.whole_seq + ' -s {0}'.format(scheme)],
                                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # todo: write an additional utility for detection of the nearest species
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
    def identify_cdrs_and_frameworks(self, scheme='c'):

        # initialize all parts of sequence
        self.frameworks['fr_1'] = ''
        self.frameworks['fr_2'] = ''
        self.frameworks['fr_3'] = ''
        self.frameworks['fr_4'] = ''
        self.CDRs['cdr_1'] = ''
        self.CDRs['cdr_2'] = ''
        self.CDRs['cdr_3'] = ''

        if scheme == 'c':
            if self.chain == 'Heavy':
                # fill the first framework
                self.frameworks['fr_1'] = self.whole_seq[:25]

                # fill the first CDR and second frameworks
                if '35A' in self.seq_dict.keys() and '35B' in self.seq_dict.keys():
                    self.CDRs['cdr_1'] = self.whole_seq[25:34]
                    self.frameworks['fr_2'] = self.whole_seq[34:51]
                elif '35A' in self.seq_dict.keys():
                    self.CDRs['cdr_1'] = self.whole_seq[25:33]
                    self.frameworks['fr_2'] = self.whole_seq[33:51]
                else:
                    self.CDRs['cdr_1'] = self.whole_seq[25:32]
                    self.frameworks['fr_2'] = self.whole_seq[32:51]

                # fill the CDR 2
                self.CDRs['cdr_2'] = self.whole_seq[51:56]

                # calculate the number of 82 aa and define the length of sequence part for fr_3
                count82 = 0
                for key in self.seq_dict.keys():
                    try:
                        key.index('82')
                    except ValueError:
                        continue
                    else:
                        count82 += 1
                self.frameworks['fr_3'] = self.whole_seq[56:93+count82]

                # calculate the number of 100 aa and define the length of sequence part for cdr_3
                count100 = 0
                for key in self.seq_dict.keys():
                    try:
                        key.index('100')
                    except ValueError:
                        continue
                    else:
                        count100 += 1
                self.CDRs['cdr_3'] = self.whole_seq[93+count82:101+count100]

                # fill the framework 4
                self.frameworks['fr_4'] = self.whole_seq[101+count100:]

                # code for development
                print('Framework 1: {0}'.format(self.frameworks['fr_1']))
                print('CDR 1: {0}'.format(self.CDRs['cdr_1']))
                print('Framework 2: {0}'.format(self.frameworks['fr_2']))
                print('CDR 2: {0}'.format(self.CDRs['cdr_2']))
                print('Framework 3: {0}'.format(self.frameworks['fr_3']))
                print('CDR 3: {0}'.format(self.CDRs['cdr_3']))
                print('Framework 4: {0}'.format(self.frameworks['fr_4']))


    def __str__(self):
        return 'Whole Sequence: {0}\n'.format(self.whole_seq) + \
               'Chain: {0}\n'.format(self.chain) + \
               '\n'