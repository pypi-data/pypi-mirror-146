#!/usr/bin/env python3
#
# GlobalChemExtensions - Master Object
#
# -----------------------------------

class ExtensionsError(Exception):

    __version_error_parser__ = "0.0.1"
    __allow_update__ = False

    '''
    
    Raise an Extension Error if something is wrong. 
    
    '''
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

class GlobalChemExtensions(object):

    __version__ = '0.0.1'

    def __init__(self):

        pass

    @staticmethod
    def sunburst_chemical_list(smiles_list, save_file=False):

        '''


        Sunburst a chemical list

        Arguments:
            smiles_list (String): list of smiles strings to analyze
            save_file (Boolean): whether the user would like it as a file

        '''

        from global_chem_extensions.analysis_tools.sunburster.sunburster import Sunburster

        Sunburster(smiles_list, save_file)


    @staticmethod
    def node_pca_analysis(
            smiles_list,
            morgan_radius = 1,
            bit_representation = 512,
            number_of_clusters = 5,
            number_of_components = 0.95,
            random_state = 0,
            file_name = 'pca_analysis.html',
            save_file = False,
            return_mol_ids = False,
    ):

        '''

        Perform a pca analysis on a node within globalchem, can be extended to lists outside of the dedicated SMILES.

        Arguments:
            smiles_list (List): list of SMILES that the user wants to cluster
            morgan_radius (Int): Morgan Radius of the chemical environment
            bit_representation (Int): Length of the bit representation
            number_of_clusters (Int): Number of clusters the user would like to do
            number_of_components (Int): How many PCA vectors to analyze
            random_state (Int):
            file_name (String): file name the user would like to input
            save_file (Bool): Whether the user wants to display the plot or save it.
            return_mol_ids (Bool): Return the molecule IDS for the user to mine.

        '''

        from global_chem_extensions.analysis_tools.node_pca_analysis.node_pca_analysis import PCAAnalysis

        pca_analysis = PCAAnalysis(
            smiles_list,
            morgan_radius,
            bit_representation,
            number_of_clusters,
            number_of_components,
            random_state,
            file_name,
            save_file=save_file,
            return_mol_ids = False
        )

        return_mol_ids = pca_analysis.conduct_analysis()

        if return_mol_ids:
            return return_mol_ids

    @staticmethod
    def smiles_to_amino_acids(
            smiles_list
    ):

        '''

        Arguments:
            smiles_list (List): List of the SMILES

        Returns:
            converted_list (List): Converted list of the SMILES to the amino acid converters

        '''

        from global_chem_extensions.language_adapters.amino_acid_converter.amino_acid_converter import AminoAcidConverter

        converter = AminoAcidConverter()
        converted_list = []

        for smiles in smiles_list:

            converted_list.append(
                converted_list.append(converter.convert_smiles_to_amino_acid_sequence(smiles))
            )

        return converted_list

    @staticmethod
    def amino_acids_to_smiles(
            amino_acid_list
    ):

        '''

        Arguments:
            amino_acid_list (List): List of the Amino Acids

        Returns:
            converted_list (List): Converted list of the SMILES to the amino acid converters

        '''

        converter = AminoAcidConverter()

        converted_list = []

        for amino_acid in amino_acid_list:

            converted_list.append(
                converter.convert_amino_acid_sequence_to_smiles(amino_acid)
            )

        return converted_list

    @staticmethod
    def check_status_on_open_source_databases():

        '''

        Check the Status on Databases

        '''

        from global_chem_extensions.monitoring_services.database_monitor.database_monitor import DatabaseMonitor

        database_monitor = DatabaseMonitor()
        database_monitor.heartbeat()


    @staticmethod
    def filter_smiles_by_criteria(
            smiles_list,
            lipinski_rule_of_5=False,
            ghose=False,
            veber=False,
            rule_of_3=False,
            reos=False,
            drug_like=False,
            pass_all_filters=False
    ):

        '''

        Arguments:
            lipinski_rule_of_5 (Bool): Lipinski Rule of 5 Criteria
            ghose (Bool): Ghose Filter,
            veber (Bool): Veber Filter,
            rule_of_3 (Bool): Rule of 3 Filter
            reos (Bool): Reos Filter
            drug_like (Bool): Drug Like Filter
            pass_all_filters (Bool): whether the user would like to pass all the filters

        Returns:

            the filtered data set
        '''

        from global_chem_extensions.analysis_tools.drug_design_filters.drug_design_filters import DrugDesignFilters

        drug_design_filters = DrugDesignFilters(
            smiles_list,
            lipinski_rule_of_5=lipinski_rule_of_5,
            ghose=ghose,
            veber=veber,
            rule_of_3=rule_of_3,
            reos=reos,
            drug_like=drug_like,
            pass_all_filters=pass_all_filters
        )

        return drug_design_filters.filter()

    @staticmethod
    def convert_to_networkx(network):

        '''

        Arguments:
            network (Dict): Convert to a networkx object for interoperability

        Returns:
            converted_network (Graph Object): Networkx Graph object

        '''

        from global_chem_extensions.software_adapters.networkx_adapter.networkx_adapter import NetworkxAdapter

        network_adapter = NetworkxAdapter()
        converted_network = network_adapter.convert(network)

        return converted_network

    @staticmethod
    def scatter_deep_layer_network(deep_layer_network, height=800, width=1700, save_file=False):

        '''

        Arguments:
            deep_layer_network (Object): DGN coming from GlobalChem

        '''

        from global_chem_extensions.analysis_tools.deep_layer_scatter.deep_layer_scatter import DeepLayerScatter

        deep_layer_scatter = DeepLayerScatter(deep_layer_network, save_file=save_file)
        deep_layer_scatter.scatter(height=height, width=None)

    @staticmethod
    def smarts_pattern_identifier(host='0.0.0.0', port=5000, debugger=True):

        '''

        Launch a Flask App for the SMARTS Pattern Identifier

        '''

        from global_chem_extensions.analysis_tools.smarts_pattern_identifier.smarts_pattern_identifier import SmartsPatternIdentifier

        spi = SmartsPatternIdentifier()
        spi.launch_app(host=host, port=port, debug=debugger)

    @staticmethod
    def find_protonation_states(
            smiles_list,
            min_ph=6.4,
            max_ph=8.4,
            pka_precision=1.0,
            max_variants=128,
            label_states=False
    ):

        '''

        Find the protonation states of a SMILES string

        Returns:
            states (Dict): States of the SMILES input.

        '''

        from global_chem_extensions.software_adapters.dimorphite_dl_adapter.dimorphite_dl import DimorphiteAdapter

        dimorphite_adapter = DimorphiteAdapter(
            smiles_list,
            min_ph,
            max_ph,
            pka_precision,
            max_variants,
            label_states
        )

        states = dimorphite_adapter.run()

        return states

    @staticmethod
    def verify_smiles(
            smiles_list,
            partial_smiles=True,
            rdkit=False,
            pysmiles=False,
            molvs=False,
            deepsmiles=False,
            partial=False,
            selfies=False,
            return_failures=False
    ):

        '''

        Arguments:
            smiles_list (List): List of smiles
            rdkit (Bool): Whether the RDKit flag is true
            partial_smiles (Bool): Whether to pass the partial smiles validation
            pysmiles (Bool): Whether to pass the validation through pysmiles
            molvs (Bool): Whether to pass the validation through MolVS
            deepsmiles (Bool): deepSMILES validation for machine learning
            partial (Bool): whether the user would like to have partial fragments
            selfies (Bool): whether the user would like to pass in the selfies for machine learning
            return_failures (Bool): whether the user would like to have failures returned.

        '''

        from global_chem_extensions.validation.partial_smiles import PartialSmilesValidation

        psv = PartialSmilesValidation(
            partial=partial
        )

        successes, failures = psv.validate(
            smiles_list,
            rdkit=rdkit,
            partial_smiles=partial_smiles,
            pysmiles=pysmiles,
            molvs=molvs,
            deepsmiles=deepsmiles,
            selfies=selfies
        )

        if return_failures:
            return successes, failures
        else:
            return successes

    @staticmethod
    def smiles_to_pdf(
        smiles = [],
        labels = [],
        file_name = 'molecules.pdf',
        include_failed_smiles = True,
        title = 'CHEMICAL LIST BY MOLPDF',
    ):

        '''


        Arguments:
            smiles (List): List of smiles you want to parse
            labels (List): List of labels you want to parse
            file_name (String): File name you want the output to be
            include_failed_smiles (Bool): Whether to include SMILES that didn't render.
            title (String): Title of the PDF
        '''

        from global_chem_extensions.software_adapters.pdf_adapter.molpdf_parser import MolPDFAdapter

        molpdf_adapter = MolPDFAdapter(
            smiles = smiles,
            labels = labels,
            file_name = file_name,
            include_failed_smiles = include_failed_smiles,
            title = title
        )

        molpdf_adapter.generate_document()

    @staticmethod
    def pdf_to_smiles(
        file_name
    ):

        '''

        Arguments:
             file_name (String): File name for the pdf to be parsed

        Returns:
            molecules (List): List of molecules

        '''

        from global_chem_extensions.software_adapters.pdf_adapter.molpdf_parser import MolPDFAdapter

        molpdf_adapter = MolPDFAdapter(
            file_name = file_name
        )

        molecules = molpdf_adapter.parse_document()

        return molecules

    @staticmethod
    def encode_smiles(
            smiles_list,
            max_length = 120
    ):

        '''

        Arguments:

            smiles_list (List): List of SMILES
            max_length (Int): List of the encoded SMILES

        Returns:
            encoded_list (List): List of the encoded SMILES

        '''

        from global_chem_extensions.machine_learning.one_hot_encoding import SmilesOneHotEncoder

        encoder = SmilesOneHotEncoder(
            smiles_list = smiles_list,
            max_length = max_length
        )

        encoded_list = encoder.encode()

        return encoded_list

    @staticmethod
    def decode_smiles(
            smiles_list
    ):

        '''

        Arguments:

            smiles_list (List): List of SMILES

        Returns:
            decoded_list (List): List of the decoded SMILES

        '''

        from global_chem_extensions.machine_learning.one_hot_encoding import SmilesOneHotEncoder

        encoder = SmilesOneHotEncoder(
            smiles_list = smiles_list,
        )

        decoded_list = encoder.decode()

        return decoded_list

    @staticmethod
    def initialize_globalchem_molecule(
            smiles,
            stream_file = None,
            frcmod_file = None,
    ):

        '''

        Arguments:
            smiles (String): A smiles string
            stream_file (String): stream file for CGenFF
            frcmod_file (String): FRCMOD file for GAFF2

        '''

        from global_chem_extensions.entities.molecule.molecule import GlobalChemMolecule
        from global_chem_extensions.forcefields.cgenff.cgenff_molecule import CGenFFMolecule
        from global_chem_extensions.forcefields.gaff2.gaff2_molecule import GaFF2Molecule


        cgenff_molecule = None
        gaff2_molecule = None

        if stream_file:

            cgenff_molecule = CGenFFMolecule(stream_file=stream_file)

        if frcmod_file:

            gaff2_molecule = GaFF2Molecule(frcmod_file=frcmod_file)

        global_chem_molecule = GlobalChemMolecule(
            smiles=smiles,
            cgenff_molecule = cgenff_molecule,
            gaff2_molecule = gaff2_molecule
        )

        return global_chem_molecule

    @staticmethod
    def initialize_globalchem_protein(
            pdb_id = None,
            pdb_path = None,
            peptide_sequence = None
    ):
        '''

        Arguments:
            pdb_id (String): pdb id unique 4 letter code
            pdb_path (String): path to the pdb file
            peptide_sequence (String): Peptide sequence
        '''

        from global_chem_extensions.entities.protein.protein import GlobalChemProtein

        global_chem_protein = GlobalChemProtein(
            pdb_file = pdb_id,
            fetch_pdb = pdb_path,
            peptide_sequence = peptide_sequence,
        )

        return global_chem_protein

    @staticmethod
    def initialize_globalchem_dna(
            dna_sequence,
            name = None,
    ):

        '''

        Arguments:
            dna_sequence (String): DNA sequence string
            name (String): Name of the DNA instance
        '''

        from global_chem_extensions.entities.dna.dna import GlobalChemDNA

        global_chem_dna = GlobalChemDNA(
            dna_sequence = dna_sequence,
            name = name
        )

        return global_chem_dna

    @staticmethod
    def initialize_globalchem_rna(
            rna_sequence,
            name = None,
    ):

        '''

        Arguments:
            rna_sequence (String): DNA sequence string
            name (String): Name of the DNA instance
        '''

        from global_chem_extensions.entities.rna.rna import GlobalChemRNA

        global_chem_rna = GlobalChemRNA(
            rna_sequence = rna_sequence,
            name = name
        )

        return global_chem_rna

    @staticmethod
    def initialize_cgenff_molecule(stream_file):

        '''

        Arguments:

            stream_file (String): stream file from CGenFF

        '''

        from global_chem_extensions.forcefields.cgenff.cgenff_molecule import CGenFFMolecule

        cgenff_molecule = CGenFFMolecule(
            stream_file=stream_file
        )

        return cgenff_molecule

    @staticmethod
    def initialize_gaff2_molecule(frcmod_file):

        '''

        Arguments:

            frcmod_file (String): frcmod file for GaFF2

        '''

        from global_chem_extensions.forcefields.gaff2.gaff2_molecule import GaFF2Molecule

        gaff2_molecule = GaFF2Molecule(
            frcmod_file=frcmod_file
        )

        return gaff2_molecule

    @staticmethod
    def visualize_smarts(smarts):

        '''

        Arguments:
            smarts (String): Viusalize the SMARTS string

        '''

        from global_chem_extensions.software_adapters.smarts_visualizer.smarts_visualizer import SmartsVisualizer

        visualizer = SmartsVisualizer(
            smarts
        )

        return visualizer.get_image()

    @staticmethod
    def compute_cgenff_dissimilar_score(stream_file_1, stream_file_2, verbose=False):


        '''

        Arguments:
            stream_file_1 (String): file path of the first molecule
            stream_file_2 (String): file path of the second molecule
            verbose (Bool): If you want the full parameter output

        Returns:
            score (Float): similarity score

        '''

        from global_chem_extensions.forcefields.cgenff.cgenff_molecule import CGenFFMolecule
        from global_chem_extensions.forcefields.cgenff.dissimilarity_score import CGenFFDissimilarityScore

        molecule_1 = CGenFFMolecule(stream_file_1)
        molecule_2 = CGenFFMolecule(stream_file_2)

        dissimilar = CGenFFDissimilarityScore(
            molecule_1,
            molecule_2,
            verbose=verbose
        )

        score = dissimilar.compute_dissimilar_score_two_compounds()

        return score

    @staticmethod
    def apply_plotly_template(
            figure,
            x_title='X-Axis',
            y_title = 'Y-Axis',
            height = 500,
            width = 1000
    ):
        '''

        Arguments:
            figure (Plotly Figure Object): plotly object you want beautified
            x_title (String): title of the x-axis
            y_title (String): title of the y-axis
            height (Int): height of the graph
            width (Int): width of the graph

        '''

        from global_chem_extensions.graphing_templates.plotly_template import PlotlyTemplate

        PlotlyTemplate(
            figure,
            x_title=x_title,
            y_title = y_title,
            height = height,
            width = width
        )