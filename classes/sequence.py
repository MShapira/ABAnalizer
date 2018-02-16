import subprocess
from collections import OrderedDict, Counter
from natsort import natsorted


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
        # todo: add an opportunity to choose method ("chotia" is default)
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

        # turn our dict to ordered dict (special class) and ordering by key
        self.seq_dict = OrderedDict(natsorted(self.seq_dict.items(), key=lambda d: d[0]))

    # create a dict with CDRs and frameworks
    def identify_cdrs_and_frameworks(self, scheme='c'):

        # initialize all parts of sequence
        self.frameworks['fr_1'] = []
        self.frameworks['fr_2'] = []
        self.frameworks['fr_3'] = []
        self.frameworks['fr_4'] = []
        self.CDRs['cdr_1'] = []
        self.CDRs['cdr_2'] = []
        self.CDRs['cdr_3'] = []

        # define and count the number of positions with additional letters
        positions_with_additional_letters = []
        additional_aa = []
        for key in self.seq_dict.keys():
            try:
                int(key)
            except ValueError:
                additional_aa.append(key)
                positions_with_additional_letters.append(int(key[:-1]))
                continue
        counter = Counter(positions_with_additional_letters)

        # construct the CDR region due to the last position in it
        def construct_cdr(end: int, cdr_name: str):
            if key not in additional_aa:
                if int(key) < end:
                    self.CDRs[cdr_name].append(key)
            else:
                if int(key[:-1]) < end:
                    self.CDRs[cdr_name].append(key)

        # construct the framework region due to the last position in it
        def construct_fr(end: int, fr_name: str):
            if key not in additional_aa:
                if int(key) < end:
                    self.frameworks[fr_name].append(key)
            else:
                if int(key[:-1]) < end:
                    self.frameworks[fr_name].append(key)

        # working only with chotia numeration
        if scheme == 'c':
            if self.chain == 'Heavy':

                # fill the first framework
                for key in self.seq_dict.keys():
                    construct_fr(end=26, fr_name='fr_1')

                # fill the first CDR
                for key in self.seq_dict.keys():
                    if key not in self.frameworks['fr_1']:
                        # check if the 35 position has additional letters
                        if 35 in positions_with_additional_letters:
                            if counter[35] >= 2:
                                construct_cdr(end=35, cdr_name='cdr_1')
                            elif counter[35] == 1:
                                construct_cdr(end=34, cdr_name='cdr_1')
                        else:
                            construct_cdr(end=33, cdr_name='cdr_1')

                # fill the second framework
                for key in self.seq_dict.keys():
                    if key not in self.frameworks['fr_1'] and key not in self.CDRs['cdr_1']:
                        construct_fr(end=52, fr_name='fr_2')

                # fill the second CDR
                for key in self.seq_dict.keys():
                    if key not in self.frameworks['fr_1'] and key not in self.CDRs['cdr_1'] and \
                                    key not in self.frameworks['fr_2']:
                        construct_cdr(end=57, cdr_name='cdr_2')

                # fill the third framework
                for key in self.seq_dict.keys():
                    if key not in self.frameworks['fr_1'] and key not in self.CDRs['cdr_1'] and \
                                    key not in self.frameworks['fr_2'] and key not in self.CDRs['cdr_2']:
                        construct_fr(end=95, fr_name='fr_3')

                # fill the third CDR
                for key in self.seq_dict.keys():
                    if key not in self.frameworks['fr_1'] and key not in self.CDRs['cdr_1'] and \
                                    key not in self.frameworks['fr_2'] and key not in self.CDRs['cdr_2'] and \
                                    key not in self.frameworks['fr_3']:
                        construct_cdr(end=102, cdr_name='cdr_3')

                # fill the fourth framework
                for key in self.seq_dict.keys():
                    if key not in self.frameworks['fr_1'] and key not in self.CDRs['cdr_1'] and \
                                    key not in self.frameworks['fr_2'] and key not in self.CDRs['cdr_2'] and \
                                    key not in self.frameworks['fr_3'] and key not in self.CDRs['cdr_3']:
                        construct_fr(end=len(self.seq_dict.keys())+1, fr_name='fr_4')

    # generate a str from list of keys to self.seq_dict
    def get_seq_from_keys_list(self, keys_list: list):
        str = ''
        for key in keys_list:
            str += self.seq_dict[key]

        return str

    def __str__(self):
        return 'Whole Sequence: {0}\n'.format(self.whole_seq) + \
               'Chain: {0}\n'.format(self.chain) + \
               'Framework 1: {0}\n'.format(self.get_seq_from_keys_list(self.frameworks['fr_1'])) + \
               'CDR 1: {0}\n'.format(self.get_seq_from_keys_list(self.CDRs['cdr_1'])) + \
               'Framework 2: {0}\n'.format(self.get_seq_from_keys_list(self.frameworks['fr_2'])) + \
               'CDR 2: {0}\n'.format(self.get_seq_from_keys_list(self.CDRs['cdr_2'])) + \
               'Framework 3: {0}\n'.format(self.get_seq_from_keys_list(self.frameworks['fr_3'])) + \
               'CDR 3: {0}\n'.format(self.get_seq_from_keys_list(self.CDRs['cdr_3'])) + \
               'Framework 4: {0}\n'.format(self.get_seq_from_keys_list(self.frameworks['fr_4'])) + \
               '\n'