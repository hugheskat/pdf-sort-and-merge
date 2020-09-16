# from tkinter import filedialog
from tkinter import *
import os
import time
from PyPDF2 import PdfFileMerger, PdfFileReader, utils

start_time = time.time()

def listbox_widget(pdf_txt_file=True):
    """
    Outputs a Tkinter Listbox widget displaying all the PDFs to merge.The user can sort the list into the correct order
    and save the list to a .txt file.
    Args:
        pdf_txt_file: Whether the Listbox should be based on the list of of files in a .txt file or the order of the
        files in the directory.
    """

    def file_list_to_list():
        """
        Returns: a list of the PDFs contained in the _pdflist.txt file.
        """
        data = []
        file = open(os.path.join(folder_selected, "_pdflist.txt"), "r", encoding="utf-8")
        for f in file.readlines():
            data.append(f.strip())

        return data


    def quit():
        """Action performed when you click the button quit and save. It saves the entries in the Listbox to
        a _pdflist.txt file and exits the Listbox."""

        file = open(os.path.join(folder_selected, "_pdflist.txt"), "w", encoding="utf-8")
        # loop through entries in Listbox widget and add to text file
        for d in listbox.get(0, END):
            file.write(d + "\n")
        file.close()
        # exit the Listbox widget
        root.destroy()
        root.quit()

    def duplicates():
        """To highlight duplicate entries in the Listbox."""

        all_entries = [] # list of entries in Listbox minus duplicates
        duplicates = [] # list of duplicate entries in Listbox
        # loop through entries in Listbox
        for i, entry in enumerate(listbox.get(0, END)):
            # find duplicates
            if entry in all_entries:
                duplicates.append(entry)
                # highlight yellow
                listbox.itemconfig(i, bg='yellow')
            else:
                all_entries.append(entry)
        # print a list of any duplicate entries
        if duplicates:
            print('\nThe following files are duplicate entries in the file list. They will be highlighted in yellow in '
                  'the pop-up window. Please delete as necessary from the pop-up window.')
            for dup in duplicates:
                print('  * ' + dup)

    def move_up():
        """To move an item in the Listbox up a notch."""

        try:
            selections = listbox.curselection()
            if not selections:
                return
            for pos in selections:
                if pos == 0:
                    continue
                text = listbox.get(pos)
                listbox.delete(pos)
                listbox.insert(pos - 1, text)
                listbox.selection_set(pos - 1)  # ensure the selection stays in place
        except:
            pass

    def move_down():
        """To move an item in the Listbox down a notch."""

        try:
            selections = listbox.curselection()
            if not selections:
                return
            for pos in selections:
                if pos == len(selections):
                    continue
                text = listbox.get(pos)
                listbox.delete(pos)
                listbox.insert(pos + 1, text)
                listbox.selection_set(pos + 1)  # ensure the selection stays in place
        except:
            pass

    def delete():
        """To delete an item in the Listbox."""

        listbox.delete(ANCHOR)

    # the Tkinter window which will contain the Listbox
    global root
    root = Tk()
    # add a PDF icon to the Tkinter window
    root.iconbitmap(r'\\voyager\templates\Python\Kepler\python-3\icons\pdf.icon.ico')
    root.title("PDFs list")
    label_ = Label(root,
              text="Sort the list of PDFs into the correct order. Click 'Quit and save' when done.")
    label_.pack()
    # the scrollbar
    y_scrollbar = Scrollbar(root, orient="vertical")
    y_scrollbar.pack(side=RIGHT, fill=Y)
    # the button to move up a selected item
    moveUpButton = Button(root, text="Move Selected Item Up", command=move_up)
    moveUpButton.pack(pady=5)
    # the button to move down a selected item
    moveDownButton = Button(root, text="Move Selected Item Down", command=move_down)
    moveDownButton.pack(pady=5)
    # the button to delete only selected items
    deleteButton = Button(root, text='Delete Selected Item', command=delete)
    deleteButton.pack(pady=5)
    # the listbox
    global listbox
    listbox = Listbox(root, selectmode=BROWSE, yscrollcommand=y_scrollbar.set)
    listbox.pack(fill="both", expand=False, pady=5)
    listbox.config(width=60, height=15, relief='sunken', borderwidth=2)
    # the button to save the data in the Listbox to a '_pdflist.txt' file and exit the Tkinter window
    quitButton = Button(root, text="Quit and save", command=quit)
    quitButton.pack(pady=5)

    # if the user wants to use the data in the existing file list text file
    if pdf_txt_file == True:
        # convert the PDFs in the text file to a list object
        list_data = file_list_to_list()
        # get any PDFs that are in the folder but not listed in the text file
        pdfs_not_in_text_file = []
        for file in os.listdir(folder_selected):
            if file not in list_data:
                if file.endswith('.pdf') and file != 'complete-pdf.pdf':
                    pdfs_not_in_text_file.append(file)
        # if there are PDFs in the folder not listed in the text file, prompt if the user would like them added
        if pdfs_not_in_text_file:
            print('\nWe found one or more PDFs in the folder that aren\'t on the list:')
            for pdf in pdfs_not_in_text_file:
                print('* ' + str(pdf))
            append_text_file = input('Would you like these to be added to the text file? '
                                     'Please type \'y\' or \'n\' followed by ENTER.')

            if append_text_file.lower() == 'y':
                # add the PDFs in the folder but not in the text file to the Listbox widget
                list_data = list_data + pdfs_not_in_text_file
                for pdf in list_data:
                    if pdf.endswith('.pdf') and pdf != 'complete-pdf.pdf':
                        listbox.insert(END, pdf)
                # prompt user to reorder the files in the Listbox widget and click 'Quit and save'
                print('\nPlease check the order of the files in the pop-up window and click \'Quit and save\' '
                      'when you are ready.')
                time.sleep(1)
                # call the function to highlight any duplicate entries in the Listbox
                duplicates()
                # bring the Tkinter window to the front
                root.lift()
                root.attributes('-topmost', True)
        # if there are no PDFs in the folder that are not in the text file, add all the PDF file names in the folder to
        # the Listbox widget
        else:
            for pdf in list_data:
                if pdf.endswith('.pdf') and pdf != 'complete-pdf.pdf':
                    listbox.insert(END, pdf)
            # call the function to highlight any duplicate entries in the Listbox
            duplicates()
            # bring the Tkinter window to the front
            root.lift()
            root.attributes('-topmost', True)
    # if the user wants a new file list text file to be generated
    elif pdf_txt_file == False:
        list_data = os.listdir(folder_selected)
        # add the files to the listbox
        for file in list_data:
            if file.endswith('.pdf') and file != 'complete-pdf.pdf':
                listbox.insert(END, file)
        # call the function to highlight any duplicate entries in the Listbox
        duplicates()
        # bring the Tkinter window to the front
        root.lift()
        root.attributes('-topmost', True)

    root.mainloop()


def validate_pdfs():
    """To check for any PDFs that bring up a read error"""

    file = open(os.path.join(folder_selected, "_pdflist.txt"), "r", encoding="utf-8")
    # list of invalid files
    invalid_pdfs = []
    # look through the PDFs that are in the file list
    for line in file.readlines():
        line = line.strip()
        for pdf_ in os.listdir(folder_selected):
            if pdf_.lower().endswith('.pdf'):
                if line == pdf_:
                    try:
                        # read the pdf
                        PdfFileReader(open(os.path.join(folder_selected, pdf_), 'rb'))
                    except utils.PdfReadError:
                        invalid_pdfs.append(pdf_)
    # if there are invalid PDFs, print out the list of files in the console
    if invalid_pdfs:
        print('\nThe following PDFs are invalid:')
        for pdf1 in invalid_pdfs:
            print('  * ' + str(pdf1))
        print('These will not be added to the merged PDF.')
    else:
        pass


def merge_pdfs():
    """To merge the PDFs into a single file"""

    # confirmation that the PDFs are about to be merged
    print('\nMerging the PDFs into a single file...')
    time.sleep(1)
    # set the file counter to 0
    file_count = 0
    # create a PDF merger object
    merger = PdfFileMerger()
    # get path to _pdflist text file
    file = open(os.path.join(folder_selected, "_pdflist.txt"), "r", encoding="utf-8")
    # loop through the PDFs in the same order as the file names in the _pdflist.txt file
    for line in file.readlines():
        line = line.strip()
        for pdf_ in os.listdir(folder_selected):
            if pdf_.lower().endswith('.pdf'):
                if line == pdf_:
                    file_count +=1
                    try:
                        # confirmation that the pdf is being added to the merged file
                        print('Adding...' + str(pdf_))
                        merger.append(PdfFileReader(open(os.path.join(folder_selected, pdf_), 'rb')))
                    # flag up any PDF read errors
                    except utils.PdfReadError:
                        print('* '+ str(pdf_) + " is an invalid PDF file and won't be added to the merged PDF.")
                        pass

    # if there is a 'complete-pdf' file in the folder, prompt the user if they want to overwrite it
    if 'complete-pdf.pdf' in os.listdir(folder_selected):
        overwrite_pdf = input('\n\'complete-pdf.pdf\' already exists. Do you want to overwrite this? Please '
                              'enter \'y\' or \'n\' followed by ENTER: ')
        # if the user wants to overwrite, write the merged file to the input folder
        if overwrite_pdf.lower() == 'y':
            merger.write(os.path.join(folder_selected, 'complete-pdf.pdf'))
            merger.close()
            # confirmation of end of script
            print('\n' + str(file_count) + ' PDFs have been merged in '+
                  str(time.time() - start_time) + ' seconds.\nThe file \'complete-pdf.pdf\' is saved here: '
                  + str(folder_selected) +'.')
            input('Press any key to exit...')
        # if the user doesn't want to overwrite, exit the script
        else:
            exit()
    # if there is no 'complete-pdf' file, write the merged file to the input folder
    else:
        merger.write(os.path.join(folder_selected, 'complete-pdf.pdf'))
        merger.close()
        print('\n' + str(file_count) + ' PDFs have been merged in ' + str(time.time() - start_time)
              + ' seconds.\nThe file \'complete-pdf.pdf\' is saved here: ' + str(folder_selected))
        input('Press any key to exit...')


def main():
    """The main function."""

    # summary of script to display in console
    print("""This script will:
1. create a list of the PDFs in a user-specified folder;
2. open that list in a pop-up window so the user can sort the PDFs in merging order; and
3. merge the PDFs.""")

    ## Uncomment the below if you want a file dialogue to get the folder path instead of user input
    ## bring up file dialogue to select directory containing the PDFs
    # root = Tk()
    # root.withdraw()  # shut down the pop-up window
    # print('A browser window will open shortly. Please browse to the directory of the folder containing the PDFs.')
    # time.sleep(1)
    # global folder_selected
    # folder_selected = filedialog.askdirectory()
    ## confirmation of the directory containing the PDFs
    #print('\nSearching for PDFs in: ' + str(folder_selected) + '...')

    global folder_selected
    folder_selected = input('\nTo start please enter the path to the folder containing the PDFs: ')

    # bring up the Listbox widget, so the user can sort the PDF files if necessary
    if '_pdflist.txt' in os.listdir(folder_selected):
        text_file = input('\nThere\'s a file list in this folder already. Do you want to use this? '
                          'Please type \'y\' or \'n\' followed by ENTER: ')
        # retrieve the list of PDF files from '_pdflist.txt'
        if text_file.lower() == 'y':
            print('\nPlease sort the list of PDFs into the correct order in the pop-up window. Press \'Quit and save\' '
                  'when you\'re done.')
            time.sleep(1)
            listbox_widget(pdf_txt_file=True)
        # retrieve the list of PDF files from the folder
        else:
            print('\nPlease sort the list of PDFs into the correct order in the pop-up window. Press \'Quit and save\' '
                  'when you\'re done.')
            time.sleep(1)
            listbox_widget(pdf_txt_file=False)
    # retrieve the list of PDF files from the folder
    else:
        continue_ = input('\nThere is no file list in this folder. Do you want '
                          'to continue? Please type \'y\' or \'n\' '
                          'followed by ENTER: ')
        if continue_.lower() == 'y':
            print('\nPlease sort the list into the correct order in the pop-up window. Press \'Quit and save\' '
                  'when you are done.')
            time.sleep(1)
            listbox_widget(pdf_txt_file=False)
    # confirmation that the file list has been saved
    print('\nThe list of PDFs has been saved here: ' + str(folder_selected) + '/_pdflist.txt.')
    # ask if the user wants to proceed with merging the PDFs
    continue__ = input('\nWould you like to proceed with merging the PDFs into a single file? Please press \'y\''
                       ' or any other key to exit.')
    if continue__ == 'y':
        # check for any PDFs that bring up a read error
        validate_pdfs()
        # merge the PDFs into a single file
        merge_pdfs()
    else:
        exit()


# call the main function
if __name__ == '__main__':
    main()
