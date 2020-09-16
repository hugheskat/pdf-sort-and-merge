# pdf-sort-and-merge
## Summary

This script will:

1. create a list of the PDFs in a user-specified folder;
2. open that list in a pop-up window so the user can sort the PDFs in merging order; and
3. merge the PDFs.

## Step-by-step instructions

* The PDFs to be merged must be copied to a dedicated folder.
* A user runs the script and enters the path to the folder.
* Processing at this stage depends on whether there is already a list of PDFs in the folder (ie a file 
called **_pdflist.txt**)
  * If there is, the user will be asked to confirm whether they want to use that file.
    * If they enter 'y' for yes, the existing list will be checked against the set of PDFs in the folder. If there are 
    new files — ie files not already on the list — the user will be asked to confirm whether they want to add those 
    files.
      * If they enter 'y', the new files will be appended to the end of the list, which will be opened for sorting.
      * If they enter anything else, the list will be used as-is.
    * If they enter 'n' for no, a new list be will be created and the user will be asked to sort the files.
  * If there isn't, a new list will be created.
* If a new list has been created or an existing one updated, the user will be prompted to sort the files in order. 
A window will pop up showing the list of files. There are options to move a file up or down, or to delete a file. 
Any duplicate files will be highlighted yellow so the user can delete these directly from the pop-up window. 
When sorting is complete, the user should press the **Quit and save** button. The pop-up window will close and a new or 
updated **_pdflist.txt** file will be saved in the input folder.
* The user returns to the command window and enters either 'y' to continue or any other key to exit.
* The script checks for any read errors in the PDFs and lists any such files in the console. These 
PDFs will not be added to the final merged pdf file.
* The PDF merge will start.
* If a **complete-pdf.pdf** file exists in the folder, the user will be prompted if they want to overwrite it.
  * If they enter 'y', the merged pdf will be saved in the user-specified input folder.
  * If they enter 'n', the script will exit.

## Input required

* Path to the folder in which the PDFs to be merged are saved.

## Output

* A PDF **complete-pdf.pdf** will be output in the user-specified input folder.
