//This will be the direcotry of the images
var workFolder = Folder("Z:/Bermudez-Hernandez/Strains Project/Animals/C57_20/Prox1_NeuN/Slide2");
var folders = workFolder.getFiles(); 
runphotomergeFromScript = true;
//runphotomergeFromScript = true;
$.evalFile( "C:/Program Files/Adobe/Adobe Photoshop CC/Presets/Scripts/Photomerge.jsx")
//photomerge.createPanorama(
//fileList, displayDialog );

psdOpts = new PhotoshopSaveOptions(); 
psdOpts.embedColorProfile = true; 
psdOpts.alphaChannels = true; 
psdOpts.layers = false; 

tiffOpts = new TiffSaveOptions();
psdOpts.layers = false;

for( var i = 0; i < folders.length; i++ ) 
{ 	
     if (folders[i] instanceof Folder){
	var folder = folders[i]; 
	var fList = folder.getFiles( '*.tif' );
    
   // override Photomerge.jsx settings. Default is "Auto". Uncomment to override the default. 
   //photomerge.alignmentKey   = "Auto"; 
   //photomerge.alignmentKey   = "Prsp"; 
   //photomerge.alignmentKey   = "cylindrical"; 
   //photomerge.alignmentKey   = "spherical"; 
   //photomerge.alignmentKey   = "sceneCollage"; 
   photomerge.alignmentKey   = "translation" ; // "Reposition" in layout dialog    

   // other setting that may need to be changed. Defaults below 
   photomerge.advancedBlending      = true; // 'Bend Images Together' checkbox in dialog 
   photomerge.lensCorrection      = false; // Geometric Distortion Correction'checkbox in dialog 
   photomerge.removeVignette      = false; // 'Vignette Removal' checkbox in dialog 
    if( fList.length > 1 )
   {
	   photomerge.createPanorama(fList,false); 
   } 
   
    var doc_name = fList[0].name;
    var final_name = doc_name.slice(0,-6);
    //alert(final_name);
    activeDocument.saveAs( new File( fList[0].parent+'/'+final_name+'.psd') , psdOpts, true, Extension.LOWERCASE); 
    activeDocument.saveAs( new File(workFolder.parent+'/'+final_name+'.tif') , tiffOpts, true, Extension.LOWERCASE); 
    activeDocument.close( SaveOptions.DONOTSAVECHANGES ); 
     }
}
 
/*function savePSB(fileNameAndPath)
{
	function cTID(s) { return app.charIDToTypeID(s); };
	function sTID(s) { return app.stringIDToTypeID(s); };

	var desc19 = new ActionDescriptor();
     var desc20 = new ActionDescriptor();
	desc20.putBoolean( sTID('maximizeCompatibility'), true );
	desc19.putObject( cTID('As  '), cTID('Pht8'), desc20 );
    desc19.putPath( cTID('In  '), new File( fileNameAndPath ) );
    desc19.putBoolean( cTID('LwCs'), true );
    executeAction( cTID('save'), desc19, DialogModes.NO );
};*/