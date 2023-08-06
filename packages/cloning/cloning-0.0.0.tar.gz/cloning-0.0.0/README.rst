*******
Cloning
*******

.. image:: https://img.shields.io/pypi/v/cloning.svg
   :alt: Last release
   :target: https://pypi.python.org/pypi/cloning

.. image:: https://img.shields.io/pypi/pyversions/cloning.svg
   :alt: Python version
   :target: https://pypi.python.org/pypi/cloning

.. image:: https://img.shields.io/readthedocs/cloning.svg
   :alt: Documentation
   :target: https://cloning.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/github/workflow/status/kalekundert/cloning/Test%20and%20release/master
   :alt: Test status
   :target: https://github.com/kalekundert/cloning/actions

.. image:: https://img.shields.io/coveralls/kalekundert/cloning.svg
   :alt: Test coverage
   :target: https://coveralls.io/github/kalekundert/cloning?branch=master

.. image:: https://img.shields.io/github/last-commit/kalekundert/cloning?logo=github
   :alt: Last commit
   :target: https://github.com/kalekundert/cloning

The purpose of this project is to provide the ability to simulate any step 
involved in cloning DNA constructs, e.g. PCR, restriction digests, Gibson 
assemblies, Golden Gate assemblies, etc.  Some implementation details:

- DNA is represented with a very high level of detail and generality, so that 
  things like sticky ends, phosphorylated ends, modified nucleotides etc. can 
  be accounted for.  For example, something like this:

  .. code-block:: python

    class Duplex:
        watson: Strand
        crick: Strand
        
    class Strand:
        # Generally the graph will be a simple linked list, but it is possible 
        # for nucleotides to branch.
        polymer: nx.Graph

    class Nucleotide:
        # There's a library called `pysmiles` than can construct graphs of 
        # atoms from SMILES strings.
        atoms: nx.Graph

        # Node indices in the above graph.
        attachment_points: int

        # e.g. ATCG
        symbol: str

    class DegenerateNucleotide:
        mix: Dict[Nucleotide, float]

    def dsdna_from_str(str, *, phos_5, phos_3, sticky_5, sticky_3):
        # I'll want a lot of keyword argument to control how the duplex is 
        # constructed.  I've listed a few here, but I haven't really thought 
        # about the format they'd take.
        pass

    def ssdna_from_str(...):
        pass

    def dsrna_from_str(...):
        pass

    def ssrna_from_str(...):
        pass

  At the same time, every effort is made to accept simple strings wherever a 
  sequence is required, for convenience.

- Cloning steps would be implemented as simple functions, for the most part.  
  Maybe in some cases it'd be better to use functors, just to make it easier to 
  pass lots of parameters, but I don't want to lean into that.  Some examples:

  .. code-block:: python

    def pcr(template, primer1, primer_2):
        # Check that primers face each other (accounting for circular 
        # templates) and that product is unambiguous.
        return Duplex(...)

    def gibson(fragments):
        # - Build graph using ends of each fragment
        # - Make sure that the graph is circular, and uses each fragment 
        #   exactly once.
        return Duplex(..., circular=True)

    def golden_gate(fragments):
        # Similar to Gibson.
        return Duplex(..., circular=True)

    def digest(duplex, enzymes):
        return Duplex(...)

    def phosphorylate(strand):
        # If duplex provided, phosphorylate both strands.
        return Strand(...)
        
    def ligate(fragments):
        # - Require phosphorylated ends.
        # - Require a single unique product, by default.
        return Duplex(..., circular=True)

    def anneal(oligo_1, oligo_2):
        return Duplex(...)

    def transcribe(template):
        # Check for promoter.  Maybe optionally require GGG for T7.
        return Strand(..., rna=True)

    def express(template, start_codon=0):
        # - Require RNA template
        # - Third party functions should be used to predict start codon from 
        #   transcript, if the user needs that necessary.
        return Strand()

- Some general-purpose tools that I'd like to include:

  - Reverse complement.
  - Translation.
  - Melting temperature calculation (via Biopython).
  - Sequence alignment, especially for circular sequences.
  - Support for parsing IDT sequence strings.

- Some general purpose tools I'm hesitant to include:

  - Reverse translation: Doing this for any real application is a pretty 
    intense optimization problem, e.g. finding a sequence that uses common 
    codons, avoids restriction sites, minimizes internal 
    RBSs/promoters/terminators, isn't too complex, etc.  I think this should be 
    the domain of a devoted tool.

Some ideas about names:

- `cloning`: Shocking that this is available.
- `biopolymers`: Might be a better fit for the actual function, since it makes 
  sense to include `transcribe()` and `express()` functions.
- `biopol`/`biopols`: Abbreviations of above.



