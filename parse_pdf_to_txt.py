import pdftotext
import os
import shutil
import pandas as pd
from pdfrw import PdfReader, PdfWriter

if __name__ == '__main__':
    input_file = "racmyp_articles_1973.csv"
    df = pd.read_csv(input_file, header=0)
    if os.path.exists("articles_txt"):
        shutil.rmtree("articles_txt")

    os.mkdir("articles_txt")

    for id in df.id:
        with open("articles_pdf/" + str(id) + ".pdf", "rb") as f:
            pdf = pdftotext.PDF(f)

        file = open("articles_txt/" + str(id) + ".txt", "w", encoding='utf-8')
        file.write("\n\n".join(pdf))
        file.close()

