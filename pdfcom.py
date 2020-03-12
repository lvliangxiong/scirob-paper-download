# this script is used combine the pdfs downloaded from science robotics

import os
import re
import time
from PyPDF2 import PdfFileMerger


def combine(filenames, combined_filename):
    merger = PdfFileMerger()
    for file in filenames:
        try:
            merger.append(open(file, "rb"))
        except:
            return

    with open(combined_filename, "wb") as f:
        merger.write(f)


if __name__ == "__main__":
    # execute only when directly provoked
    # define the path of downloads
    path = "downloads"
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    combined_filename = "Sci Rob Latest Compilation.pdf"
    issue_filenames = []
    os.chdir(path)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("%s [JOEYLYU] Current directory: %s" % (current_time, os.getcwd()))
    # iterate the issues
    issues = [x for x in os.listdir() if os.path.isdir(x)]
    for issue in issues:
        os.chdir(issue)
        # matching the file with filename started with [1], [2], [22] and etc
        filenames = [x for x in os.listdir() if re.match(r"\[(\d*)\]", x)]
        # sort the filenames by index
        filenames.sort(
            # get the index by lambda function
            key=lambda filename: int(
                re.match(r"\[(\d*)\]", filename).group(1)),
            reverse=False,
        )
        issue_filename = "Sci Rob %s.pdf" % issue
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("%s [JOEYLYU] Combined File Number: %s, Combined Filename: %s" %
              (current_time, len(filenames), issue_filename))
        # combine the selected files in the issue
        combine(filenames, issue_filename)
        issue_filenames.append("%s/%s" % (issue, issue_filename))
        os.chdir("..")
    # sort the issue filenames according their issue no
    issue_filenames.sort(
        key=lambda filename: int(re.search(r"Issue (\d*)", filename).group(1)))
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("%s [JOEYLYU] Combining Files ... into %s" %
          (current_time, combined_filename))
    combine(issue_filenames, combined_filename)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("%s [JOEYLYU] DONE!" % current_time)
