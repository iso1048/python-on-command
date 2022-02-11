
import os
import fitz
import datetime

def set_outfile_path(to_append=''):
    current_date_and_time = datetime.datetime.now().strftime('%H%M%S_%d%m%Y')
    out_pdf_path = os.path.join(os.getcwd(), current_date_and_time+to_append+'.pdf')
    return out_pdf_path


def merge(arguments):
    """
    Merges pdf files into a single pdf file in the order they are given in
    at the command line. Output pdf file is saved to the current working 
    directory. 

    @param  arguments : arparse.Namespace
        Command line arguments parsed by ArgumentParser.parse_args().
        Will have the following attributes: pdfs
    
    @return out_pdf_path : str
        Path to output pdf file.

    """
    # args: pdfs
    pdfs = arguments.pdfs

    # append pdfs
    src_pdf = fitz.open(pdfs[0])
    for pdf_path in pdfs[1:]:
        with fitz.open(pdf_path) as f:
            src_pdf.insert_pdf(f)

    # save and close file
    out_pdf_path = set_outfile_path() # set the output file
    src_pdf.save(out_pdf_path)
    src_pdf.close()

    return out_pdf_path


def remove(arguments):
    """
    Removes pages from the given pdf file. Output pdf file is saved to 
    the current working directory. 

    @param  arguments : arparse.Namespace
        Command line arguments parsed by ArgumentParser.parse_args().
        Will have the following attributes: src_pdf, pages
    
    @return out_pdf_path : str
        Path to output pdf file.
    
    """
    # args: src_pdf, pages
    src_pdf_path = arguments.src_pdf
    pages_to_rm = arguments.pages
 
    # convert page ranges to list of page numbers, and convert all page
    # inputs to indices
    pages_to_rm_corrected = set()
    for p in pages_to_rm:
        # page range
        if '-' in p:
            s, e = (int(i) for i in p.split('-'))
            for i in range(s-1,e):
                pages_to_rm_corrected.add(i)

        # single page number
        else:
            pages_to_rm_corrected.add(int(p)-1)
    
    pages_to_rm_corrected = sorted(list(pages_to_rm_corrected))

    # open pdf
    src_pdf = fitz.open(src_pdf_path)

    # check that page index does not exceed number of pages in the pdf
    src_pdf_page_count = src_pdf.page_count
    if not all(num <= src_pdf_page_count for num in pages_to_rm_corrected):
        raise ValueError('Page numbers must be less than or equal to the \
            total number of pages ({}) in the pdf.'.format(src_pdf_page_count))

    # remove the pages
    src_pdf.delete_pages(pages_to_rm_corrected)

    # save and close  
    out_pdf_path = set_outfile_path() # set the output file
    src_pdf.save(out_pdf_path)
    src_pdf.close()

    return out_pdf_path

def insert(arguments):
    """
    Inserts a pdf document into the source pdf document after the given
    page number. The output pdf file is saved to the current working
    directory. 

    @param  arguments : arparse.Namespace
        Command line arguments parsed by ArgumentParser.parse_args().
        Will have the following attributes: src_pdf, ins_pdf, page
    
    @return out_pdf_path : str
        Path to output pdf file. 
    """

    # args: src_pdf, ins_pdf, page
    src_pdf_path = arguments.src_pdf
    ins_pdf_path = arguments.ins_pdf
    after_page = arguments.page

    # open pdfs
    src_pdf = fitz.open(src_pdf_path)
    ins_pdf = fitz.open(ins_pdf_path)

    # check that after_page does not exceed number of pages in src_pdf
    if after_page > src_pdf.page_count :
        raise ValueError('argument <page> exceeds the length of <src_pdf> ({} pages)'.format(src_pdf.page_count))

    # insert ins_pdf into src_pdf
    src_pdf.insert_pdf(ins_pdf, start_at=after_page)

    # save and close  
    out_pdf_path = set_outfile_path() # set the output file
    src_pdf.save(out_pdf_path)
    src_pdf.close()

    return out_pdf_path


def split(arguments):
    """
    Splits the source pdf into separate pdf files for each given page/page
    range. Outputs are saved to the current woring directory.

    @param  arguments : arparse.Namespace
        Command line arguments parsed by ArgumentParser.parse_args().
        Will have the following attributes: src_pdf, pages
    
    @return out_pdf_paths : tuple
        Tuple containing the paths to the output pdf files.
    
    """

    # args: src_pdf, pages
    src_pdf_path = arguments.src_pdf
    pages = arguments.pages
    output_pdf_paths = []

    # open source pdf
    src_pdf = fitz.open(src_pdf_path)

    for page_input in pages:

        # open a new, empty pdf file
        new_pdf = fitz.open()

        # page range
        if '-' in page_input:
            start = int(page_input.split('-')[0])
            end = int(page_input.split('-')[1])
            new_pdf.insert_pdf(src_pdf, from_page=start-1, to_page=end-1)

        # single page number
        else:
            new_pdf.insert_pdf(src_pdf, from_page=int(page_input)-1, to_page=int(page_input)-1)
        
        # save and close new pdf
        out_pdf_path = set_outfile_path('_page_'+page_input) # set the output file
        output_pdf_paths.append(out_pdf_path)
        new_pdf.save(out_pdf_path)
        new_pdf.close()

    # close source pdf
    src_pdf.close()

    return tuple(output_pdf_paths)




