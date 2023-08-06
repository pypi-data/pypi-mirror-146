
# -*- coding: utf-8 -*-
###########################################################################
# Bioconvert is a project to facilitate the interconversion               #
# of life science data from one format to another.                        #
#                                                                         #
# Authors: see CONTRIBUTORS.rst                                           #
# Copyright © 2018-2019  Institut Pasteur, Paris and CNRS.                #
# See the COPYRIGHT file for details                                      #
#                                                                         #
# bioconvert is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# bioconvert is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program (COPYING file).                                 #
# If not, see <http://www.gnu.org/licenses/>.                             #
###########################################################################
""" description """

from bioconvert import ConvBase
from bioconvert import requires
from bioconvert.io.gff3 import Gff3


__all__ = ["GFF2GENBANK"]


class GFF32GENBANK(ConvBase):
    """Convert :term:`GFF` file to :term:`GENBANK` file

    Some description to be added by the developer


    AL844502.2  EMBL    region  1   1067971 .   +   . ID=AL844502.2:1..1067971;Dbxref=taxon:36329;Name=3;chromosome=3;gbkey=Src;isolate=3D7;mol_type=genomic DNA


    to 

    FEATURES             Location/Qualifiers
     source          1..1067971
                     /organism="Plasmodium falciparum 3D7"
                     /mol_type="genomic DNA"
                     /isolate="3D7"
                     /db_xref="taxon:36329"
                     /chromosome="3"
     gene            36965..44482
                     /locus_tag="PF3D7_0300100"
     CDS             join(36965..42283,43172..44482)
                     /locus_tag="PF3D7_0300100"
                     /codon_start=1
                     /product="erythrocyte membrane protein 1, PfEMP1"
                     /protein_id="CAB39115.2"
                     /db_xref="GOA:O97324"
                     /db_xref="InterPro:IPR004258"
                     /db_xref="InterPro:IPR008602"
                     /db_xref="InterPro:IPR029210"
                     /db_xref="InterPro:IPR029211"
                     /db_xref="UniProtKB/TrEMBL:O97324"

    """
    _default_method = "python"

    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str infile: input GFF file
        :param str outfile: output GENBANK filename

        """
        super(GFF32GENBANK, self).__init__(infile, outfile, *args, **kargs)

    def _method_python(self, *args, **kwargs):
        gff = Gff3(self.infile)
        with open(self.outfile, "w") as fout:
            for annotation in gff.read():


                # sometimes, we have the word complement. How to get this
                # information from gff annotation ?
                # gene complement(start..end)
                if annotation['type'] == "pseudogene":
                    annotation['type'] = "gene"
                print("\t{type}\t\ŧ{start}..{end}".format(**annotation))


                #v = annotation['attributes']['ID']
                #print('\t\t\t\t/="{}"'.format(v.split(":")[-1])

                # One issue with records is that some gene

                for k,v in annotation['attributes'].items():
                    if k in  ["ID", "Name", "gbkey", "pseudo", "gene_biotype"]:
                        continue

                    if k.lower() == "db_xref":
                        for this in v.split(":"):
                            print('\t\t\t\t/{}="{}"'.format(k.lower(), this))
                    else:
                        print('\t\t\t\t/{}="{}"'.format(k.lower(), v))
