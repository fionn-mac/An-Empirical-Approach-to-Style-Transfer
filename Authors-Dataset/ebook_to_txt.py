from os import system
from os import path
from os import getcwd
from os import listdir
from sys import exit

class Converter(object):
    def __init__(self):
        self.mobi_files = []
        self.epub_files = []
        self.pdf_files = []

    def reset(self):
        self.epub_files = []
        self.mobi_files = []
        self.pdf_files = []

    def combine_txt_files(self, author_name, base_dir, dest_dir):
        txt_files = [path.join(base_dir, file) for file in listdir(base_dir) if file.endswith(".txt")]
        lines = []

        for file in txt_files:
            with open(file) as f:
                lines = f.readlines()

            system('rm "%s"' % file)

            with open(path.join(dest_dir, author_name + ".txt"), "a") as w:
                for line in lines:
                    w.write(line)

    def convert_epub_to_txt(self, dest_dir):
        for i, file in enumerate(self.epub_files):
            system('ebook-convert "%s" "%s"' % (file, path.join(dest_dir, str(i) + ".txt")))

    def convert_mobi_to_txt(self, dest_dir):
        for i, file in enumerate(self.mobi_files):
            system('ebook-convert "%s" "%s"' % (file, path.join(dest_dir, str(i) + ".txt")))

    def convert_pdf_to_txt(self, dest_dir):
        for i, file in enumerate(self.pdf_files):
            system('pdftotext "%s" "%s"' % (file, path.join(dest_dir, str(i) + ".txt")))

    def get_epub_files(self, directory):
        self.epub_files += [path.join(directory, file) for file in listdir(directory) if file.endswith(".epub")]

    def get_mobi_files(self, directory):
        self.mobi_files += [path.join(directory, file) for file in listdir(directory) if file.endswith(".mobi")]

    def get_pdf_files(self, directory):
        self.pdf_files += [path.join(directory, file) for file in listdir(directory) if file.endswith(".pdf")]

    def recurse_over_dir(self, dir):
        self.get_epub_files(dir)
        self.get_mobi_files(dir)
        self.get_pdf_files(dir)

        dirs = [path.join(dir, result) for result in listdir(dir) if path.isdir(path.join(dir, result))]

        for sub_dir in dirs:
            self.recurse_over_dir(sub_dir)

    def convert_and_combine(self, author_name, base_dir, dest_dir):
        self.recurse_over_dir(base_dir)

        self.convert_epub_to_txt(base_dir)
        self.convert_mobi_to_txt(base_dir)
        self.convert_pdf_to_txt(base_dir)

        self.combine_txt_files(author_name, base_dir, dest_dir)

if __name__ == "__main__":

    cwd = getcwd()
    contents = listdir(cwd)
    authors = [content for content in contents if path.isdir(content)]

    converter = Converter()

    for author in authors:
        converter.convert_and_combine(author, path.join(cwd, author), cwd)
        converter.reset()
