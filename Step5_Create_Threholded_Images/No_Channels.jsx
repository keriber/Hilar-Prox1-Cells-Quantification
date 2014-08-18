var samplesFolder = Folder("F:/Backup Seagate Hardrive/Quantification_C57_SW/Quantification_Default_GCL_H/Copy of Images/C57_25_p16");
var workFolder = Folder("F:/Backup Seagate Hardrive/Quantification_C57_SW/Quantification_Default_GCL_H/Default/C57_25_p16");
tiffOpts = new TiffSaveOptions();

var fList = samplesFolder.getFiles('*.tif' )
for( var i = 0; i < fList.length; i++ ) 
{ 
    if (fList[i] instanceof File)
    {
    open(fList[i])
    app.activeDocument.flatten()
    app.activeDocument.channels.removeAll()
    var doc_name = fList[i].name;
    app.activeDocument.saveAs( new File(workFolder+'/'+doc_name) , tiffOpts, true, Extension.LOWERCASE); 
    //app.activeDocument.close()
    }
  }