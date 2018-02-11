class Antibody:
    def __init__(self, name, host, resource_of_origin):
        self.name = name
        self.host = host
        self.resource_of_origin = resource_of_origin
        self.protein_sequence = None
        self.nucleotide_sequence = None

        def __str__(self):
            return 'Name: {0}\n'.format(self.name) + \
                   'Host organism: {0}\n'.format(self.host) + \
                   'Resource: {0}\n'.format(self.resource_of_origin) + \
                   'Protein sequence: {0}\n'.format(self.protein_sequence) + \
                   'Nucleotide sequence: {0}\n'.format(self.nucleotide_sequence) + \
                   '\n'