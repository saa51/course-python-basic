import xlwt
import xlrd
import webbrowser
import re
import argparse
import webbrowser

def extract_url(sheet, link_col):
    texts = []
    for row in range(1, sheet.nrows):
        texts.append(sheet.cell_value(row, args.link_col))
    
    for pos, link in sheet.hyperlink_map.items():
        if pos[1] == args.link_col:
            texts[pos[0] - 1] += ' '
            texts[pos[0] - 1] += link.url_or_path
    
    urls = []
    pattern = '(https|http|ftp)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(:[0-9]{1,5})?(\/[\S]*)?'
    pattern = re.compile(pattern)
    for text in texts:
        matches = pattern.finditer(text)
        url_list = [match.group() for match in matches]
        url_set = set(url_list)
        if len(url_set) == 0:
            print(f"There is no url in {text}")
            urls.append(None)
            continue
        if len(url_set) != 1:
            print(f"There is no unique url in {text}: get {url_set}")
        urls.append(url_set.pop())
    return urls
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str, default='./homework_4/H1.xls', help='path to source file')
    parser.add_argument('--dest', type=str, default='./homework_4/New_H1.xls', help='path to destination file')
    parser.add_argument('--web', action='store_true', help='whether open all links in the web browser')
    parser.add_argument('--link_col', type=int, default=2, help='the index of column containing the link')
    args = parser.parse_args()

    data = xlrd.open_workbook(args.src)
    sheet = data.sheet_by_index(0)
    
    urls = extract_url(sheet, args.link_col)

    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('NewSheet')
    worksheet.write(0, 0, label = 'Row 0, Column 0 Value')
    for idx in range(len(urls)):
        worksheet.write(idx + 1, 0, label = urls[idx])
    workbook.save(args.dest)

    if args.web:
        for url in urls:
            if url:
                webbrowser.open_new(url)
    