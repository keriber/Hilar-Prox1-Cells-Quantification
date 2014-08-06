
var animal = "SW_21"

var sampleFolderDir = "F:/Backup Seagate Hardrive/Quantification_C57_SW/Quantification_Default_GCL_H/Copy of Images/"+animal
var workFolderDir = "F:/Backup Seagate Hardrive/Quantification_C57_SW/Quantification_Default_GCL_H/H_Area/" +animal

var samplesFolder = Folder(sampleFolderDir);
var workFolder = Folder(workFolderDir);
workFolder.create();

//~ if (workFolder.exists= false){
//~     var workFolder= new Folder(workFolderDir);
//~     workFolder.create();
//~     }

tiffOpts = new TiffSaveOptions();

var fList = samplesFolder.getFiles('*.tif' )
for( var i = 0; i < fList.length; i++ ) 
{ 
    if (fList[i] instanceof File)
    {
    open(fList[i])
    if (app.activeDocument.layers.length > 1){
    app.activeDocument.mergeVisibleLayers();
    }
    var selRef = app.activeDocument.selection
    selRef.load (app.activeDocument.channels["H"])
    //selRef.load (app.activeDocument.channels["GCL"],SelectionType.EXTEND)
    //selRef.load (app.activeDocument.channels["ML"],SelectionType.EXTEND)
    var fillColor = new SolidColor()
    fillColor.rgb.red = 0
    fillColor.rgb.green = 0
    fillColor.rgb.blue =0
    selRef.fill( fillColor, ColorBlendMode.NORMAL,100, false)
    selRef.invert()
    selRef.clear()
    app.activeDocument.changeMode(ChangeMode.GRAYSCALE)
    app.activeDocument.channels.removeAll()
    var doc_name = fList[i].name;
    app.activeDocument.saveAs( new File(workFolder+'/'+doc_name) , tiffOpts, true, Extension.LOWERCASE); 
    app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
    }
  }
alert ("The Files are done")