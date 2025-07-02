from PyPDF2 import PdfMerger

merger = PdfMerger()
merger.append("file1.pdf")
merger.append("file2.pdf")
merger.append("file3.pdf")
merger.append("file4.pdf")
merger.write("merged-file .pdf")
merger.close()
