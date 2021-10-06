# Imports
import cv2
import numpy as np

import tkinter as tk
import tkinter.filedialog as fd

import re


class Table:

    def __init__(self, root, data):
        total_rows = len(data.keys())

        self.e = tk.Entry(root, width=20, fg='red', font=('Arial', 16, 'bold'))
        self.e.grid(row=0, column=0)
        self.e.insert(tk.END, 'FILE NAME')

        self.e = tk.Entry(root, width=20, fg='red', font=('Arial', 16, 'bold'))
        self.e.grid(row=0, column=1)
        self.e.insert(tk.END, 'CONFLUENCE')

        count = 1
        for key in data:
            self.e = tk.Entry(root, width=20, fg='black', font=('Arial', 16))
            self.e.grid(row=count, column=0)
            self.e.insert(tk.END, key)

            self.e = tk.Entry(root, width=20, fg='black', font=('Arial', 16))
            self.e.grid(row=count, column=1)
            self.e.insert(tk.END, data[key])

            count = count + 1


if __name__ == '__main__':
    # Initial settings
    debug = True

    # Browse images
    root = tk.Tk()
    files = fd.askopenfilenames(parent=root, title='Choose a file')

    data = dict()

    for filename in files:
        # Loading color image
        img = cv2.imread(filename, 1)

        # Grayscale, binarization, and dilation
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((5, 5), np.uint8)
        th_dilation = cv2.dilate(thresh, kernel, iterations=1)

        # Contour extraction
        contours, hierarchy = cv2.findContours(th_dilation, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        contour_img = np.copy(img)
        img_contour = cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 3)

        # Compute confluence
        whole_area = th_dilation.size
        cells_area = cv2.countNonZero(th_dilation)
        empty_area = whole_area - cells_area

        # Show estimate and print (Linux/PyCharm)

        """
        name_search = re.search('.*/(.*)$', filename, re.IGNORECASE)
        name = name_search.group(1)
        print('\033[93m' + name + '\033[0m' + ' Confluence = ' + str(cells_area / whole_area * 100) + ' %')
        print('\033[93m' + name + '\033[0m' + ' Empty Area = ' + str(empty_area / whole_area * 100) + ' %\n')
        """

        # Show estimate and print (Windows)
        name_search = re.search('.*/(.*)$', filename, re.IGNORECASE)
        name = name_search.group(1)
        confluence = cells_area / whole_area * 100
        data[name] = confluence

    t = Table(root, data)

    # If debug is True --> Image display
    if debug:
        for key in data:
            cv2.namedWindow(key , cv2.WINDOW_NORMAL)
            grey_3_channel = cv2.cvtColor(th_dilation, cv2.COLOR_GRAY2BGR)
            panel = np.concatenate((img, contour_img, grey_3_channel), axis=1)
            cv2.moveWindow(key , 20, 20)
            cv2.resizeWindow(key, 1600, 768)
            cv2.imshow(key, panel)

    tk.mainloop()

    """cv2.waitKey(0)
    cv2.destroyAllWindows()"""



