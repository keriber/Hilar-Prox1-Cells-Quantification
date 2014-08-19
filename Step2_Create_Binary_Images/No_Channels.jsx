var samplesFolder = Folder("F:/Backup Seagate Hardrive/Quantification_C57_SW/Quantification_Default_GCL_H/Copy of Images/C57_31_p30_C_H/To_Quantify");
var workFolder = Folder("F:/Backup Seagate Hardrive/Quantification_C57_SW/Quantification_Default_GCL_H/Default/C57_31_p30_C_H");
tiffOpts = new TiffSaveOptions();

var fList = samplesFolder.getFiles('*.tif' )
for( var i = 0; i < fList.length; i++ ) 
{ 
    if (fList[i] instanceof File)
    {
    open(fList[i])
//~     var selRef = app.activeDocument.selection
//~      selRef.load (app.activeDocument.channels["SGZ"])
    //selRef.load (app.activeDocument.channels["GCL"],SelectionType.EXTEND)
    //selRef.load (app.activeDocument.channels["ML"],SelectionType.EXTEND)
//~     var fillColor = new SolidColor()
//~     fillColor.rgb.red = 0
//~     fillColor.rgb.green = 0xxc
//~     fillColor.rgb.blue =0
//~     selRef.fill( fillColor, ColorBlendMode.NORMAL,100, false)
//~     selRef.invert()
//~     selRef.clear()
//~     app.activeDocument.changeMode(ChangeMode.GRAYSCALE)
    app.activeDocument.flatten()
    app.activeDocument.channels.removeAll()
    var doc_name = fList[i].name;
    app.activeDocument.saveAs( new File(workFolder+'/'+doc_name) , tiffOpts, true, Extension.LOWERCASE); 
    app.activeDocument.close(SaveOptions.DONOTSAVECHANGES)
    
    }
  }
alert ("The Files are done")