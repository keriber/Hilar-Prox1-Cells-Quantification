Hilar-Prox1-Cells-Quantification
================================

These are a series of scripts in Javascript  for Photoshop, Python scripts and macros in ImageJ to estimate the number of immuno-reactive Prox1 cells in the hilus of the dentate gyrus of the hippocampus in mice

================================
The scripts can be used individually . But these are the steps to quantify Prox1 cells in the hilus
 
The first step is to perform Immunohistochemistry for Prox1 in free floating brain sections as explained in Myers et al 2013. 
Then sections need to be  dehydrated an coverslipped in permount and photographed with a brightfield microscope and digital camera.
Photographs need to be taken at a 20X magnification.

For each studied animal you need to create a folder for each section an label each Folder as "Section1","Section2", etc. 
Take the pictures of each section and save them on the corresponding folder.

For each of the fallowing steps there is a folder with macros and scripts.

1) Photomerge the images by using  the Javascript script from Step1 in Photoshop.

2) After photomerging all the images. Draw the regions of interests(ROI)s as indicated in Step1.5

3) Then proceed to create ROI binary images  from the alpha channels using the Javascript in Step2 called "Fill_All.jsx". 
In the scripts change the name of the ROIs that you wish to create binary images.To create an ROI that corresposnds to two ROIs uncomment the line that extends the selection.

 These steps need to be completed for each animal.

5) After creating the binary images run the ImageJ macro in Step3 and Step4.

6) Then create the thresholded images using an ImageJ macro in Step5.

7) Then create txt files with the number of cells in each section by using the macro in Step6.

8) Orgnaize the count txt data into a csv file using the Python script in Step8.

9) Orgnaize the area txt data into a csv file using the Python script in Step7.

10) Finally orgnize and plot the data of all the animals by using the Python script in Step9.

Note: All the scripts are a work in progress and were written for my use. There might be more than one script in each folder. This may correspond to different ROIs or different groups of animals.
Example, in these scripts I had the group "P16_P30_P60" and "Cre Bax", and  for ROIs I had "H","Hilus", and "SGZ".



