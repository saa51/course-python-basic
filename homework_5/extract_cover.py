import os
import argparse
from PyPDF4 import PdfFileReader, PdfFileWriter


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str, default='./homework_5/mypdfs', help='path to source file')
    parser.add_argument('--dest', type=str, default='./homework_5/new.pdf', help='path to destination file')
    args = parser.parse_args()

    if not os.path.exists(args.src):
        raise FileNotFoundError(args.src)
    files = [f for f in os.listdir(args.src) if '.pdf' in f]
    
    writer = PdfFileWriter()
    handles = []
    for f in files:
        handle = open(os.path.join(args.src, f), "rb")
        pdf = PdfFileReader(handle)
        handles.append(handle)
        page = pdf.getPage(0)
        writer.addPage(page)

    with open(args.dest, 'wb+') as output:
        writer.write(output)

    for handle in handles:
        handle.close()