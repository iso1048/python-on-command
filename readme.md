
# PDF On Command (POC)

PDF On Command (POC) is a command line application for performing simple operations on PDF files, namely merging, removing, inserting, and splitting (at present). 

**This is a personal project for me to practice programming**


## Requirements

- PyMuPDF
- pytest

## Usage

After navigating to the project directory (`POC`)...

```
python poc [-h] [command] [args ...]
```

Running the application from the `POC` directory with the `-h` option will show the available commands:

```
...\POC>python poc -h
usage: poc [-h] {merge,remove,insert,split} ...

positional arguments:
  {merge,remove,insert,split}
                        command help
    merge               merges two or more pdf files into a single pdf file
    remove              remove pages from a pdf file
    insert              insert one pdf file into another pdf file, after the given page number
    split               split a pdf file into separate pdf files

options:
  -h, --help            show this help message and exit
```

Each command can also be run with the `-h` option to show the arguments that it accepts - see below.

Unless otherwise stated, all outputs are saved to the current working directory.

## Commands

### ```merge```

Multiple pdf files are appended together in the order that they are passed in. 

Help:
```
...\POC>python poc merge -h
usage: poc merge [-h] pdfs [pdfs ...]

positional arguments:
  pdfs        paths to two or more pdf files

options:
  -h, --help  show this help message and exit
```

The following are valid calls to the `merge` command:
```
python poc merge C:\Users\...\one.pdf C:\Users\...\two.pdf
python poc merge C:\Users\...\one.pdf C:\Users\...\two.pdf C:\Users\...\three.pdf
```

### ```remove```

Help:

```
...\POC>python poc remove -h
usage: poc remove [-h] src_pdf pages [pages ...]

positional arguments:
  src_pdf     path to the pdf file to remove pages from
  pages       pages to remove from the source pdf, given as page number/s and/or page range/s in the format X-Y (inclusive) where X and Y are non-zero and X < Y  
              e.g. '2-3 5-7 9' would remove pages 2, 3, 5, 6, 7, and 9 from the source pdf.

options:
  -h, --help  show this help message and exit
```

The following are valid calls to the `remove` command:
```
python poc merge C:\Users\...\one.pdf 2 
python poc merge C:\Users\...\one.pdf 2
python poc merge C:\Users\...\one.pdf 2 9 22
python poc merge C:\Users\...\one.pdf 2-5 25 10-14 23
```
If any page number or page range passed to `pages` is larger than the number of pages in `src_pdf`, no pages are removed and a `ValueError` is raised. 


### ```insert```

Help:
```
...\POC>python poc insert -h
usage: poc insert [-h] src_pdf ins_pdf page

positional arguments:
  src_pdf     path to the source pdf file into which <ins_pdf> will be inserted
  ins_pdf     path to the pdf file to insert into <src_pdf>
  page        page number in <src_pdf> which <ins_pdf> will be inserted after e.g. if <page> is 5, then <ins_pdf> will be inserted after   
              page 5 of <src_pdf>, such that the first page of <ins_pdf> will be page 6 in the output pdf file

options:
  -h, --help  show this help message and exit
```

### ```split```

Help:
```
...\POC>python poc split -h
usage: poc split [-h] src_pdf pages [pages ...]

positional arguments:
  src_pdf     path to the source pdf file which is to be split
  pages       pages to save as separate pdf files, given as single page numbers or a range of pages in  the format X-Y (inclusive) where X
              and Y are non-zero and X < Y e.g. '2-3 5-7 9' would save pages 2-3, 5-7, and 9 in the source pdf as three separate pdf
              files.

options:
  -h, --help  show this help message and exit
```





