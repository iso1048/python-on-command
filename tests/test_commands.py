import os
import sys 
sys.path.insert(0, os.path.dirname(sys.path[0]))
import fitz
import pytest
import argparse
from poc.helpers import set_args
import poc.commands as commands

# note that the commands are being tested with valid inputs since before 
# the arguments are passed to the command functions, they will have been
# checked by the appropiate checking functions

#-----------------------------------
# merge
#-----------------------------------

def test_merge_01_two_pdfs():
    parser = set_args()
    args = parser.parse_args(['merge', 'tests/test_files/pdf_1.pdf', 'tests/test_files/pdf_2.pdf'])
    outfile = commands.merge(args)
    with fitz.open(outfile) as f:
        assert len(f) == 6
        assert 'PDF file 1' and 'page 1' in f.get_page_text(0) #load_page(0).get_text() 
        assert 'PDF file 2' and 'page 2' in f.get_page_text(4) #load_page(4).get_text()
    os.remove(outfile)
    return

def test_merge_02_four_pdfs():
    parser = set_args()
    args = parser.parse_args(['merge', 'tests/test_files/pdf_1.pdf', 'tests/test_files/pdf_2.pdf', 
                            'tests/test_files/pdf_3.pdf', 'tests/test_files/pdf_4.pdf'])
    outfile = commands.merge(args)
    with fitz.open(outfile) as f:
        assert len(f) == 12
        assert 'PDF file 1' and 'page 1' in f.get_page_text(0) #load_page(0).get_text() 
        assert 'PDF file 2' and 'page 2' in f.get_page_text(4) #load_page(4).get_text()
        assert 'PDF file 4' and 'page 3' in f.get_page_text(11) #load_page(11).get_text() 
    os.remove(outfile)
    return

#-----------------------------------
# remove
#-----------------------------------

def test_remove_01():
    parser = set_args()
    args = parser.parse_args(['remove', 'tests/test_files/pdf_5_bigboy.pdf', '13', '18-20', '2', '4-7'])
    outfile = commands.remove(args)
    with fitz.open(outfile) as f:
        assert len(f) == 11
        assert 'PDF file 5' and 'page 1' in f.get_page_text(0) #load_page(0).get_text() 
        assert 'PDF file 5' and 'page 2' not in f.get_page_text(1) #load_page(1).get_text()
        assert 'PDF file 5' and 'page 3' in f.get_page_text(1) #load_page(1).get_text()
        assert 'PDF file 5' and 'page 17' in f.get_page_text(-1) #load_page(-1).get_text()
    os.remove(outfile)
    return

def test_remove_02():
    # 21-23 exceeds the number of pages in the pdf, so should raise a ValueError
    parser = set_args()
    args = parser.parse_args(['remove', 'tests/test_files/pdf_5_bigboy.pdf', '2', '4-7', '13', '21-23'])
    with pytest.raises(ValueError):
        commands.remove(args)
    return

#-----------------------------------
# insert 
#-----------------------------------

def test_insert_01():
    # 
    parser = set_args()
    args = parser.parse_args(['insert', 'tests/test_files/pdf_1.pdf', 'tests/test_files/pdf_2.pdf', '2'])
    outfile = commands.insert(args)
    with fitz.open(outfile) as f:
        assert len(f) == 6
        assert 'PDF file 1' and 'page 1' in f.get_page_text(0) #load_page(0).get_text()
        assert 'PDF file 2' and 'page 2' in f.get_page_text(3) #load_page(3).get_text()
        assert 'PDF file 1' and 'page 3' in f.get_page_text(-1) #load_page(-1).get_text()
    os.remove(outfile)
    return

def test_insert_02():
    # 
    parser = set_args()
    args = parser.parse_args(['insert', 'tests/test_files/pdf_5_bigboy.pdf', 'tests/test_files/pdf_4.pdf', '14'])
    outfile = commands.insert(args)
    with fitz.open(outfile) as f:
        assert len(f) == 23
        assert 'PDF file 5' and 'page 1' in f.get_page_text(0) #load_page(0).get_text()
        assert 'PDF file 4' and 'page 3' in f.get_page_text(16) #load_page(16).get_text()
        assert 'PDF file 5' and 'page 20' in f.get_page_text(-1) #load_page(-1).get_text()
    os.remove(outfile)
    return

def test_insert_03():
    # given page exceeds the number of pages in the source pdf
    parser = set_args()
    args = parser.parse_args(['insert', 'tests/test_files/pdf_3.pdf', 'tests/test_files/pdf_2.pdf', '7'])
    with pytest.raises(ValueError):
        commands.insert(args)
    return

#-----------------------------------
# split 
#-----------------------------------

def test_split_01():
    # expect one output file
    parser = set_args()
    args = parser.parse_args(['split', 'tests/test_files/pdf_3.pdf', '3'])
    output_paths = commands.split(args)

    assert len(output_paths) == 1

    with fitz.open(output_paths[0]) as f:
        assert len(f) == 1
        assert 'PDF file 3' and 'page 3' in f.get_page_text(0)
    for outfile in output_paths:
        os.remove(outfile)
    return

def test_split_02():
    # expect 4 output pdf files
    parser = set_args()
    args = parser.parse_args(['split', 'tests/test_files/pdf_5_bigboy.pdf', '2', '5-8', '13-17', '20'])
    output_paths = commands.split(args)

    assert len(output_paths) == 4
    
    with fitz.open(output_paths[0]) as f:
        assert len(f) == 1
        assert 'PDF file 5' and 'page 2' in f.get_page_text(0)
    
    with fitz.open(output_paths[1]) as f:
        assert len(f) == 4
        assert 'PDF file 5' and 'page 6' in f.get_page_text(1)
        assert 'PDF file 5' and 'page 8' in f.get_page_text(-1)
    
    with fitz.open(output_paths[2]) as f:
        assert len(f) == 5
        assert 'PDF file 5' and 'page 13' in f.get_page_text(0)
        assert 'PDF file 5' and 'page 15' in f.get_page_text(2)
        assert 'PDF file 5' and 'page 17' in f.get_page_text(-1)

    with fitz.open(output_paths[3]) as f:
        assert len(f) == 1
        assert 'PDF file 5' and 'page 20' in f.get_page_text(0)

    for outfile in output_paths:
        os.remove(outfile)
    return


