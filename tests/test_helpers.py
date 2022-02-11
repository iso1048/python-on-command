
# run from POC directory

import os
import sys 
import pytest
sys.path.insert(0, os.path.dirname(sys.path[0]))
# from poc.helpers import check_filepath
import poc.helpers as poc_helpers

#-----------------------------------
# check_filepath
#-----------------------------------

test_files_dir = 'tests/test_files/'

def test_check_filepath_01_true():
    true_filepaths = [test_files_dir+fpath for fpath in os.listdir(test_files_dir)]
    for true_path in true_filepaths:
        assert poc_helpers.check_filepath(true_path) == True
    return

def test_check_filepath_02_false():
    false_filepaths = [test_files_dir+fpath for fpath in ['pdf_5.pdf', 'pdf_6.pdf', 'does_not_exist.txt']]
    for false_path in false_filepaths:
        with pytest.raises(FileNotFoundError):
            poc_helpers.check_filepath(false_path)
    return

def test_check_filepath_03_pdf():
    fpaths = [test_files_dir+fpath for fpath in ['pdf_1.pdf', 'pdf_2.pdf', 'pdf_3.pdf', 'pdf_4.pdf']]
    for true_path in fpaths:
         assert poc_helpers.check_filepath(true_path, 'pdf') == True
    return

def test_check_filepath_04_not_pdf():
    fpaths = [test_files_dir+fpath for fpath in ['pdf_1.docx', 'random.txt']] 
    for path in fpaths:
        with pytest.raises(Exception):
            poc_helpers.check_filepath(path, 'pdf')
    return

#-----------------------------------
# check_page_format
#-----------------------------------

def test_check_page_format_01_true():
    page_inputs = ['2', '3', '4', '12', '3-5', '2-12', '23-45', '02', '03-13']
    for p in page_inputs:
        assert poc_helpers.check_page_format(p) 
    return

def test_check_page_format_02_raise():
    page_inputs = ['0', '12-12', '10-2', '4-4']
    for p in page_inputs:
        with pytest.raises(ValueError):
            poc_helpers.check_page_format(p)
    return

def test_check_page_format_03_raise():
    page_inputs = ['asd', '20ds', 'ad--2', '', '12-14-16']
    for p in page_inputs:
        with pytest.raises(ValueError):
            poc_helpers.check_page_format(p)
    return

#-----------------------------------
# 
#-----------------------------------

