# Auto-generated file that reads from H files in the libkis folder 
# The purpose is to use as auto-complete in Python IDEs 

# auto-generated from: Canvas.h 
class Canvas:
    """  Canvas wraps the canvas inside a view on an image/document.
    It is responsible for the view parameters of the document:
    zoom, rotation, mirror, wraparound and instant preview.
       """

    def Canvas(canvas,parent):
        """ 
Canvas wraps the canvas inside a view on an image/document. It is responsible for the view parameters of the document: zoom, rotation, mirror, wraparound and instant preview./class KRITALIBKIS_EXPORT Canvas : public QObject{Q_OBJECT

canvas:  KoCanvasBase
parent:  QObject
return:  void
 """ 

    def setZoomLevel(value):
        """ 
@brief setZoomLevel set the zoomlevel to the given @p value. 1.0 is 100%.

value:   qreal
return:  void
 """ 

    def setRotation(angle):
        """ 
@brief setRotation set the rotation of the canvas to the given  @param angle in degrees.

angle:   qreal
return:  void
 """ 

    def setMirror(value):
        """ 
@brief setMirror turn the canvas mirroring on or off depending on @param value

value:   bool
return:  void
 """ 

    def setWrapAroundMode(enable):
        """ 
@brief setWrapAroundMode set wraparound mode to  @param enable

enable:  bool
return:  void
 """ 

    def setLevelOfDetailMode(enable):
        """ 
@brief setLevelOfDetailMode sets Instant Preview to @param enable

enable:  bool
return:  void
 """ 



# auto-generated from: Channel.h 
class Channel:
    """  A Channel represents a single channel in a Node. Krita does not
    use channels to store local selections: these are strictly the
    color and alpha channels.
       """

    def Channel(node,channel,parent):
        """ 
A Channel represents a single channel in a Node. Krita does not use channels to store local selections: these are strictly the color and alpha channels./class KRITALIBKIS_EXPORT Channel : public QObject{Q_OBJECT

node:     KisNodeSP
channel:  KoChannelInfo
parent:   QObject
return:   void
 """ 

    def setVisible(value):
        """ 
@brief setvisible set the visibility of the channel to the given value.

value:   bool
return:  void
 """ 

    def pixelData(rect):
        """ 
Read the values of the channel into the a byte array for each pixel in the rect from the Node this channel is part of, and returns it. Note that if Krita is built with OpenEXR and the Node has the 16 bits floating point channel depth type, Krita returns 32 bits float for every channel; the libkis scripting API does not support half.

rect:    QRect
return:  QByteArray
 """ 

    def setPixelData(value,rect):
        """ 
@brief setPixelData writes the given data to the relevant channel in the Node. This is only possible for Nodes that have a paintDevice, so nothing will happen when trying to write to e.g. a group layer. Note that if Krita is built with OpenEXR and the Node has the 16 bits floating point channel depth type, Krita expects to be given a 4 byte, 32 bits float for every channel; the libkis scripting API does not support half. @param value a byte array with exactly enough bytes. @param rect the rectangle to write the bytes into

value:   QByteArray
rect:    QRect
return:  void
 """ 



# auto-generated from: CloneLayer.h 
class CloneLayer:
    """  @brief The CloneLayer class
    A clone layer is a layer that takes a reference inside the image
    and shows the exact same pixeldata.
   
    If the original is updated, the clone layer will update too.
       """

    def CloneLayer(image,name,source,parent):
        """ 
@brief The CloneLayer class A clone layer is a layer that takes a reference inside the image and shows the exact same pixeldata. If the original is updated, the clone layer will update too./class KRITALIBKIS_EXPORT CloneLayer : public Node{Q_OBJECTQ_DISABLE_COPY(CloneLayer)

image:   KisImageSP
name:    QString
source:  KisLayerSP
parent:  QObject
return:  void
 """ 

    def CloneLayer(layer,parent):
        """ 
@brief CloneLayer function for wrapping a preexisting node into a clonelayer object. @param layer the clone layer @param parent the parent QObject

layer:   KisCloneLayerSP
parent:  QObject
return:  void
 """ 



# auto-generated from: DockWidget.h 
class DockWidget:
    """  DockWidget is the base class for custom Dockers. Dockers are created by a
    factory class which needs to be registered by calling Application.addDockWidgetFactory:
   
    @code
    class HelloDocker(DockWidget):
      def __init__(self):
          super().__init__()
          label = QLabel("Hello", self)
          self.setWidget(label)
          self.label = label
          self.setWindowTitle("Hello Docker")
   
    def canvasChanged(self, canvas):
          self.label.setText("Hellodocker: canvas changed");
   
    Application.addDockWidgetFactory(DockWidgetFactory("hello", DockWidgetFactoryBase.DockRight, HelloDocker))
   
    @endcode
   
    One docker per window will be created, not one docker per canvas or view. When the user
    switches between views/canvases, canvasChanged will be called. You can override that
    method to reset your docker's internal state, if necessary.
       """

    def setCanvas(canvas):
        """ 
DockWidget is the base class for custom Dockers. Dockers are created by a factory class which needs to be registered by calling Application.addDockWidgetFactory: @code class HelloDocker(DockWidget):   def __init__(self):       super().__init__()       label = QLabel("Hello", self)       self.setWidget(label)       self.label = label       self.setWindowTitle("Hello Docker") def canvasChanged(self, canvas):       self.label.setText("Hellodocker: canvas changed"); Application.addDockWidgetFactory(DockWidgetFactory("hello", DockWidgetFactoryBase.DockRight, HelloDocker)) @endcode One docker per window will be created, not one docker per canvas or view. When the user switches between views/canvases, canvasChanged will be called. You can override that method to reset your docker's internal state, if necessary./class KRITALIBKIS_EXPORT DockWidget : public QDockWidget, public KoCanvasObserverBase{Q_OBJECTQ_DISABLE_COPY(DockWidget)public:explicit DockWidget();~DockWidget() override;protected Q_SLOTS: /Krita API

canvas:  KoCanvasBase
return:  void
 """ 

    def canvasChanged(canvas):
        """ 
@brief canvasChanged is called whenever the current canvas is changed in the mainwindow this dockwidget instance is shown in. @param canvas The new canvas.

canvas:  Canvas
return:  void
 """ 



# auto-generated from: DockWidgetFactoryBase.h 
class DockWidgetFactoryBase:
    """  @brief The DockWidgetFactoryBase class is the base class for plugins that want
    to add a dock widget to every window. You do not need to implement this class
    yourself, but create a DockWidget implementation and then add the DockWidgetFactory
    to the Krita instance like this:
   
    @code
    class HelloDocker(DockWidget):
      def __init__(self):
          super().__init__()
          label = QLabel("Hello", self)
          self.setWidget(label)
          self.label = label
   
    def canvasChanged(self, canvas):
          self.label.setText("Hellodocker: canvas changed");
   
    Application.addDockWidgetFactory(DockWidgetFactory("hello", DockWidgetFactoryBase.DockRight, HelloDocker))
   
    @endcode
       """

    def DockWidgetFactoryBase(_id,_dockPosition):
        """ 
@brief The DockWidgetFactoryBase class is the base class for plugins that want to add a dock widget to every window. You do not need to implement this class yourself, but create a DockWidget implementation and then add the DockWidgetFactory to the Krita instance like this: @code class HelloDocker(DockWidget):   def __init__(self):       super().__init__()       label = QLabel("Hello", self)       self.setWidget(label)       self.label = label def canvasChanged(self, canvas):       self.label.setText("Hellodocker: canvas changed"); Application.addDockWidgetFactory(DockWidgetFactory("hello", DockWidgetFactoryBase.DockRight, HelloDocker)) @endcode/class KRITALIBKIS_EXPORT DockWidgetFactoryBase : public KoDockFactoryBase{

_id:            QString
_dockPosition:  DockPosition
return:         void
 """ 



# auto-generated from: Document.h 
class Document:
    """  The Document class encapsulates a Krita Document/Image. A Krita document is an Image with
    a filename. Libkis does not differentiate between a document and an image, like Krita does
    internally.
       """

    def Document(document,ownsDocument,parent):
        """ 
The Document class encapsulates a Krita Document/Image. A Krita document is an Image with a filename. Libkis does not differentiate between a document and an image, like Krita does internally./class KRITALIBKIS_EXPORT Document : public QObject{Q_OBJECTQ_DISABLE_COPY(Document)

document:      KisDocument
ownsDocument:  bool
parent:        QObject
return:        void
 """ 

    def setBatchmode(value):
        """ 
Set batchmode to @p value. If batchmode is true, then there should be no popups or dialogs shown to the user.

value:   bool
return:  void
 """ 

    def setActiveNode(value):
        """ 
@brief setActiveNode make the given node active in the currently active view and window @param value the node to make active.

value:   Node
return:  void
 """ 

    def nodeByName(name):
        """ 
@brief nodeByName searches the node tree for a node with the given name and returns it @param name the name of the node @return the first node with the given name or 0 if no node is found

name:    QString
return:  Node
 """ 

    def nodeByUniqueID(id):
        """ 
@brief nodeByUniqueID searches the node tree for a node with the given name and returns it. @param uuid the unique id of the node @return the node with the given unique id, or 0 if no node is found.

id:      QUuid
return:  Node
 """ 

    def setColorProfile(colorProfile):
        """ 
@brief setColorProfile set the color profile of the image to the given profile. The profile has to be registered with krita and be compatible with the current color model and depth; the image data is <i>not</i> converted. @param colorProfile @return false if the colorProfile name does not correspond to to a registered profile or if assigning the profile failed.

colorProfile:  QString
return:        bool
 """ 

    def setColorSpace(colorModel,colorDepth,colorProfile):
        """ 
@brief setColorSpace convert the nodes and the image to the given colorspace. The conversion is done with Perceptual as intent, High Quality and No LCMS Optimizations as flags and no blackpoint compensation. @param colorModel A string describing the color model of the image: <ul> <li>A: Alpha mask</li> <li>RGBA: RGB with alpha channel (The actual order of channels is most often BGR!)</li> <li>XYZA: XYZ with alpha channel</li> <li>LABA: LAB with alpha channel</li> <li>CMYKA: CMYK with alpha channel</li> <li>GRAYA: Gray with alpha channel</li> <li>YCbCrA: YCbCr with alpha channel</li> </ul> @param colorDepth A string describing the color depth of the image: <ul> <li>U8: unsigned 8 bits integer, the most common type</li> <li>U16: unsigned 16 bits integer</li> <li>F16: half, 16 bits floating point. Only available if Krita was built with OpenEXR</li> <li>F32: 32 bits floating point</li> </ul> @param colorProfile a valid color profile for this color model and color depth combination. @return false the combination of these arguments does not correspond to a colorspace.

colorModel:    QString
colorDepth:    QString
colorProfile:  QString
return:        bool
 """ 

    def setBackgroundColor(color):
        """ 
@brief setBackgroundColor sets the background color of the document. It will trigger a projection update. @param color A QColor. The color will be converted from sRGB. @return bool

color:   QColor
return:  bool
 """ 

    def setDocumentInfo(document):
        """ 
@brief setDocumentInfo set the Document information to the information contained in document @param document A string containing a valid XML document that conforms to the document-info DTD that can be found here: https://phabricator.kde.org/source/krita/browse/master/krita/dtd/

document:  QString
return:    void
 """ 

    def setFileName(value):
        """ 
@brief setFileName set the full path of the document to @param value

value:   QString
return:  void
 """ 

    def setHeight(value):
        """ 
@brief setHeight resize the document to @param value height. This is a canvas resize, not a scale.

value:   int
return:  void
 """ 

    def setName(value):
        """ 
@brief setName sets the name of the document to @p value. This is the title field in the @ref documentInfo

value:   QString
return:  void
 """ 

    def setResolution(value):
        """ 
@brief setResolution set the resolution of the image; this does not scale the image @param value the resolution in pixels per inch

value:   int
return:  void
 """ 

    def setSelection(value):
        """ 
@brief setSelection set or replace the global selection @param value a valid selection object.

value:   Selection
return:  void
 """ 

    def setWidth(value):
        """ 
@brief setWidth resize the document to @param value width. This is a canvas resize, not a scale.

value:   int
return:  void
 """ 

    def setXRes(xRes):
        """ 
@brief setXRes set the horizontal resolution of the image to xRes in pixels per inch

xRes:    double
return:  void
 """ 

    def setYRes(yRes):
        """ 
@brief setYRes set the vertical resolution of the image to yRes in pixels per inch

yRes:    double
return:  void
 """ 

    def pixelData(x,y,w,h):
        """ 
@brief pixelData reads the given rectangle from the image projection and returns it as a byte array. The pixel data starts top-left, and is ordered row-first. The byte array can be interpreted as follows: 8 bits images have one byte per channel, and as many bytes as there are channels. 16 bits integer images have two bytes per channel, representing an unsigned short. 16 bits float images have two bytes per channel, representing a half, or 16 bits float. 32 bits float images have four bytes per channel, representing a float. You can read outside the image boundaries; those pixels will be transparent black. The order of channels is: <ul> <li>Integer RGBA: Blue, Green, Red, Alpha <li>Float RGBA: Red, Green, Blue, Alpha <li>LabA: L, a, b, Alpha <li>CMYKA: Cyan, Magenta, Yellow, Key, Alpha <li>XYZA: X, Y, Z, A <li>YCbCrA: Y, Cb, Cr, Alpha </ul> The byte array is a copy of the original image data. In Python, you can use bytes, bytearray and the struct module to interpret the data and construct, for instance, a Pillow Image object. @param x x position from where to start reading @param y y position from where to start reading @param w row length to read @param h number of rows to read @return a QByteArray with the pixel data. The byte array may be empty.

x:       int
y:       int
w:       int
h:       int
return:  QByteArray
 """ 

    def crop(x,y,w,h):
        """ 
@brief crop the image to rectangle described by @p x, @p y, @p w and @p h @param x x coordinate of the top left corner @param y y coordinate of the top left corner @param w width @param h height

x:       int
y:       int
w:       int
h:       int
return:  void
 """ 

    def exportImage(filename,exportConfiguration):
        """ 
@brief exportImage export the image, without changing its URL to the given path. @param filename the full path to which the image is to be saved @param exportConfiguration a configuration object appropriate to the file format. An InfoObject will used to that configuration. The supported formats have specific configurations that must be used when in batchmode. They are described below:\b png <ul> <li>alpha: bool (True or False) <li>compression: int (1 to 9) <li>forceSRGB: bool (True or False) <li>indexed: bool (True or False) <li>interlaced: bool (True or False) <li>saveSRGBProfile: bool (True or False) <li>transparencyFillcolor: rgb (Ex:[255,255,255]) </ul>\b jpeg <ul> <li>baseline: bool (True or False) <li>exif: bool (True or False) <li>filters: bool (['ToolInfo', 'Anonymizer']) <li>forceSRGB: bool (True or False) <li>iptc: bool (True or False) <li>is_sRGB: bool (True or False) <li>optimize: bool (True or False) <li>progressive: bool (True or False) <li>quality: int (0 to 100) <li>saveProfile: bool (True or False) <li>smoothing: int (0 to 100) <li>subsampling: int (0 to 3) <li>transparencyFillcolor: rgb (Ex:[255,255,255]) <li>xmp: bool (True or False) </ul> @return true if the export succeeded, false if it failed.

filename:             QString
exportConfiguration:  InfoObject
return:               bool
 """ 

    def resizeImage(x,y,w,h):
        """ 
@brief resizeImage resizes the canvas to the given left edge, top edge, width and height. Note: This doesn't scale, use scale image for that. @param x the new left edge @param y the new top edge @param w the new width @param h the new height

x:       int
y:       int
w:       int
h:       int
return:  void
 """ 

    def scaleImage(w,h,xres,yres,strategy):
        """ 
@brief scaleImage @param w the new width @param h the new height @param xres the new xres @param yres the new yres @param strategy the scaling strategy. There's several ones amongst these that aren't available in the regular UI. The list of filters is extensible and can be retrieved with Krita::filter <ul> <li>Hermite</li> <li>Bicubic - Adds pixels using the color of surrounding pixels. Produces smoother tonal gradations than Bilinear.</li> <li>Box - Replicate pixels in the image. Preserves all the original detail, but can produce jagged effects.</li> <li>Bilinear - Adds pixels averaging the color values of surrounding pixels. Produces medium quality results when the image is scaled from half to two times the original size.</li> <li>Bell</li> <li>BSpline</li> <li>Kanczos3 - Offers similar results than Bicubic, but maybe a little bit sharper. Can produce light and dark halos along strong edges.</li> <li>Mitchell</li> </ul>

w:         int
h:         int
xres:      int
yres:      int
strategy:  QString
return:    void
 """ 

    def rotateImage(radians):
        """ 
@brief rotateImage Rotate the image by the given radians. @param radians the amount you wish to rotate the image in radians

radians:  double
return:   void
 """ 

    def shearImage(angleX,angleY):
        """ 
@brief shearImage shear the whole image. @param angleX the X-angle in degrees to shear by @param angleY the Y-angle in degrees to shear by

angleX:  double
angleY:  double
return:  void
 """ 

    def saveAs(filename):
        """ 
@brief saveAs save the document under the @p filename. The document's filename will be reset to @p filename. @param filename the new filename (full path) for the document @return true if saving succeeded, false otherwise.

filename:  QString
return:    bool
 """ 

    def createNode(name,nodeType):
        """ 
@brief createNode create a new node of the given type. The node is not added to the node hierarchy; you need to do that by finding the right parent node, getting its list of child nodes and adding the node in the right place, then calling Node::SetChildNodes @param name The name of the node @param nodeType The type of the node. Valid types are: <ul>  <li>paintlayer  <li>grouplayer  <li>filelayer  <li>filterlayer  <li>filllayer  <li>clonelayer  <li>vectorlayer  <li>transparencymask  <li>filtermask  <li>transformmask  <li>selectionmask </ul> When relevant, the new Node will have the colorspace of the image by default; that can be changed with Node::setColorSpace. The settings and selections for relevant layer and mask types can also be set after the Node has been created.@coded = Application.createDocument(1000, 1000, "Test", "RGBA", "U8", "", 120.0)root = d.rootNode();print(root.childNodes())l2 = d.createNode("layer2", "paintLayer")print(l2)root.addChildNode(l2, None)print(root.childNodes())@endcode @return the new Node.

name:      QString
nodeType:  QString
return:    Node
 """ 

    def createGroupLayer(name):
        """ 
@brief createGroupLayer Returns a grouplayer object. Grouplayers are nodes that can have other layers as children and have the passthrough mode. @param name the name of the layer. @return a GroupLayer object.

name:    QString
return:  GroupLayer
 """ 

    def createFileLayer(name,fileName,scalingMethod):
        """ 
@brief createFileLayer returns a layer that shows an external image. @param name name of the file layer. @param fileName the absolute filename of the file referenced. Symlinks will be resolved. @param scalingMethod how the dimensions of the file are interpreted        can be either "None", "ImageToSize" or "ImageToPPI" @return a FileLayer

name:           QString
fileName:       QString
scalingMethod:  QString
return:         FileLayer
 """ 

    def createFilterLayer(name,filter,selection):
        """ 
@brief createFilterLayer creates a filter layer, which is a layer that represents a filter applied non-destructively. @param name name of the filterLayer @param filter the filter that this filter layer will us. @param selection the selection. @return a filter layer object.

name:       QString
filter:     Filter
selection:  Selection
return:     FilterLayer
 """ 

    def createFillLayer(name,generatorName,configuration,selection):
        """ 
@brief createFillLayer creates a fill layer object, which is a layer @param name @param generatorName - name of the generation filter. @param configuration - the configuration for the generation filter. @param selection - the selection. @return a filllayer object. @code from krita import  d = Krita.instance().activeDocument() i = InfoObject(); i.setProperty("pattern", "Cross01.pat") s = Selection(); s.select(0, 0, d.width(), d.height(), 255) n = d.createFillLayer("test", "pattern", i, s) r = d.rootNode(); c = r.childNodes(); r.addChildNode(n, c[0]) d.refreshProjection() @endcode

name:           QString
generatorName:  QString
configuration:  InfoObject
selection:      Selection
return:         FillLayer
 """ 

    def createCloneLayer(name,source):
        """ 
@brief createCloneLayer @param name @param source @return

name:    QString
source:  Node
return:  CloneLayer
 """ 

    def createVectorLayer(name):
        """ 
@brief createVectorLayer Creates a vector layer that can contain vector shapes. @param name the name of this layer. @return a VectorLayer.

name:    QString
return:  VectorLayer
 """ 

    def createFilterMask(name,filter,selection):
        """ 
@brief createFilterMask Creates a filter mask object that much like a filterlayer can apply a filter non-destructively. @param name the name of the layer. @param filter the filter assigned. @param selection the selection to be used by the filter mask @return a FilterMask

name:       QString
filter:     Filter
selection:  Selection
return:     FilterMask
 """ 

    def createFilterMask(name,filter,selection_source):
        """ 
@brief createFilterMask Creates a filter mask object that much like a filterlayer can apply a filter non-destructively. @param name the name of the layer. @param filter the filter assigned. @param selection_source a node from which the selection should be initialized @return a FilterMask

name:              QString
filter:            Filter
selection_source:  Node
return:            FilterMask
 """ 

    def createSelectionMask(name):
        """ 
@brief createSelectionMask Creates a selection mask, which can be used to store selections. @param name - the name of the layer. @return a SelectionMask

name:    QString
return:  SelectionMask
 """ 

    def createTransformMask(name):
        """ 
@brief createTransformMask Creates a transform mask, which can be used to apply a transformation non-destructively. @param name - the name of the layer mask. @return a TransformMask

name:    QString
return:  TransformMask
 """ 

    def projection(x,y,w,h):
        """ 
@brief projection creates a QImage from the rendered image or a cutout rectangle.

x:       int
y:       int
w:       int
h:       int
return:  QImage
 """ 

    def thumbnail(w,h):
        """ 
@brief thumbnail create a thumbnail of the given dimensions. If the requested size is too big a null QImage is created. @return a QImage representing the layer contents.

w:       int
h:       int
return:  QImage
 """ 

    def setHorizontalGuides(lines):
        """ 
@brief setHorizontalGuides replace all existing horizontal guides with the entries in the list. @param lines a list of floats containing the new guides.

lines:   QList>
return:  void
 """ 

    def setVerticalGuides(lines):
        """ 
@brief setVerticalGuides replace all existing horizontal guides with the entries in the list. @param lines a list of floats containing the new guides.

lines:   QList>
return:  void
 """ 

    def setGuidesVisible(visible):
        """ 
@brief setGuidesVisible set guides visible on this document. @param visible whether or not the guides are visible.

visible:  bool
return:   void
 """ 

    def setGuidesLocked(locked):
        """ 
@brief setGuidesLocked set guides locked on this document @param locked whether or not to lock the guides on this document.

locked:  bool
return:  void
 """ 

    def importAnimation(files,firstFrame,step):
        """ 
@brief Import an image sequence of files from a directory. This will grab all images from the directory and import them with a potential offset (firstFrame) and step (images on 2s, 3s, etc) @returns whether the animation import was successful

files:       QList>
firstFrame:  int
step:        int
return:      bool
 """ 

    def setFramesPerSecond(fps):
        """ 
@brief set frames per second of document

fps:     int
return:  void
 """ 

    def setFullClipRangeStartTime(startTime):
        """ 
@brief set start time of animation

startTime:  int
return:     void
 """ 

    def setFullClipRangeEndTime(endTime):
        """ 
@brief set full clip range end time

endTime:  int
return:   void
 """ 

    def setPlayBackRange(start,stop):
        """ 
@brief set temporary playback range of document

start:   int
stop:    int
return:  void
 """ 

    def setCurrentTime(time):
        """ 
@brief set current time of document's animation

time:    int
return:  void
 """ 

    def annotationDescription(type):
        """ 
@brief annotationDescription gets the pretty description for the current annotation @param type the type of the annotation @return a string that can be presented to the user

type:    QString
return:  QString
 """ 

    def annotation(type):
        """ 
@brief annotation the actual data for the annotation for this type. It's a simple QByteArray, what's in it depends on the type of the annotation @param type the type of the annotation @return a bytearray, possibly empty if this type of annotation doesn't exist

type:    QString
return:  QByteArray
 """ 

    def setAnnotation(type,description,annotation):
        """ 
@brief setAnnotation Add the given annotation to the document @param type the unique type of the annotation @param description the user-visible description of the annotation @param annotation the annotation itself

type:         QString
description:  QString
annotation:   QByteArray
return:       void
 """ 

    def removeAnnotation(type):
        """ 
@brief removeAnnotation remove the specified annotation from the image @param type the type defining the annotation

type:    QString
return:  void
 """ 

    def setOwnsDocument(ownsDocument):
        """ 
@brief removeAnnotation remove the specified annotation from the image @param type the type defining the annotation/void removeAnnotation(const QString &type);private:friend class Krita;friend class Window;friend class Filter;friend class View;friend class VectorLayer;friend class Shape;

ownsDocument:  bool
return:        void
 """ 



# auto-generated from: Extension.h 
class Extension:
    """  An Extension is the base for classes that extend Krita. An Extension
    is loaded on startup, when the setup() method will be executed.
   
    The extension instance should be added to the Krita Application object
    using Krita.instance().addViewExtension or Application.addViewExtension
    or Scripter.addViewExtension.
   
    Example:
   
    @code
    import sys
    from PyQt5.QtGui import 
    from PyQt5.QtWidgets import 
    from krita import 
    class HelloExtension(Extension):
   
    def __init__(self, parent):
        super().__init__(parent)
   
    def hello(self):
        QMessageBox.information(QWidget(), "Test", "Hello! This is Krita " + Application.version())
   
    def setup(self):
        qDebug("Hello Setup")
   
    def createActions(self, window)
        action = window.createAction("hello")
        action.triggered.connect(self.hello)
   
    Scripter.addExtension(HelloExtension(Krita.instance()))
   
    @endcode
       """

    def Extension(parent):
        """ 
Create a new extension. The extension will be owned by @p parent.

parent:  QObject
return:  void
 """ 

    def createActions(window):
        """ 
Override this function to setup your Extension. You can use it to integrate with the Krita application instance./virtual void setup() = 0;

window:  Window
return:  void
 """ 



# auto-generated from: FileLayer.h 
class FileLayer:
    """  @brief The FileLayer class
    A file layer is a layer that can reference an external image
    and show said reference in the layer stack.
   
    If the external image is updated, Krita will try to update the
    file layer image as well.
       """

    def FileLayer(layer,parent):
        """ 
@brief The FileLayer class A file layer is a layer that can reference an external image and show said reference in the layer stack. If the external image is updated, Krita will try to update the file layer image as well./class KRITALIBKIS_EXPORT FileLayer : public Node{Q_OBJECTQ_DISABLE_COPY(FileLayer)public:explicit FileLayer(KisImageSP image,const QString name = QString(),const QString baseName=QString(),const QString fileName=QString(),const QString scalingMethod=QString(),

layer:   KisFileLayerSP
parent:  QObject
return:  void
 """ 

    def setProperties(fileName,scalingMethod):
        """ 
@brief setProperties Change the properties of the file layer. @param fileName - A String containing the absolute file name. @param scalingMethod - a string with the scaling method, defaults to "None",  other options are "ToImageSize" and "ToImagePPI"

fileName:       QString
scalingMethod:  QString
return:         void
 """ 

    def getFileNameFromAbsolute(basePath,filePath):
        """ 
@brief getFileNameFromAbsolute referenced from the fileLayer dialog, this will jumps through all the hoops to ensure that an appropriate filename will be gotten. @param baseName the location of the document. @param absolutePath the absolute location of the file referenced. @return the appropriate relative path.

basePath:  QString
filePath:  QString
return:    QString
 """ 



# auto-generated from: FillLayer.h 
class FillLayer:
    """  @brief The FillLayer class
    A fill layer is much like a filter layer in that it takes a name
    and filter. It however specializes in filters that fill the whole canvas,
    such as a pattern or full color fill.
       """

    def FillLayer(image,name,filterConfig,selection,parent):
        """ 
@brief FillLayer Create a new fill layer with the given generator plugin @param image the image this fill layer will belong to @param name "pattern" or "color" @param filterConfig a configuration object appropriate to the given generator plugin For a "pattern" fill layer, the InfoObject can contain a single "pattern" parameter with the name of a pattern as known to the resource system: "pattern" = "Cross01.pat". For a "color" fill layer, the InfoObject can contain a single "color" parameter with a QColor, a string that QColor can parse (see https://doc.qt.io/qt-5/qcolor.html#setNamedColor) or an XML description of the color, which can be derived from a @see ManagedColor. @param selection a selection object, can be empty @param parent

image:         KisImageSP
name:          QString
filterConfig:  KisFilterConfigurationSP
selection:     Selection
parent:        QObject
return:        void
 """ 

    def FillLayer(layer,parent):
        """ 
@brief FillLayer Create a new fill layer with the given generator plugin @param image the image this fill layer will belong to @param name "pattern" or "color" @param filterConfig a configuration object appropriate to the given generator plugin For a "pattern" fill layer, the InfoObject can contain a single "pattern" parameter with the name of a pattern as known to the resource system: "pattern" = "Cross01.pat". For a "color" fill layer, the InfoObject can contain a single "color" parameter with a QColor, a string that QColor can parse (see https://doc.qt.io/qt-5/qcolor.html#setNamedColor) or an XML description of the color, which can be derived from a @see ManagedColor. @param selection a selection object, can be empty @param parent/

layer:   KisGeneratorLayerSP
parent:  QObject
return:  void
 """ 

    def setGenerator(generatorName,filterConfig):
        """ 
@brief setGenerator set the given generator for this fill layer @param generatorName "pattern" or "color" @param filterConfig a configuration object appropriate to the given generator plugin @return true if the generator was correctly created and set on the layer

generatorName:  QString
filterConfig:   InfoObject
return:         bool
 """ 



# auto-generated from: Filter.h 
class Filter:
    """  Filter: represents a filter and its configuration. A filter is identified by
    an internal name. The configuration for each filter is defined as an InfoObject:
    a map of name and value pairs.
   
    Currently available filters are:
   
    'autocontrast', 'blur', 'bottom edge detections', 'brightnesscontrast', 'burn', 'colorbalance', 'colortoalpha', 'colortransfer',
    'desaturate', 'dodge', 'emboss', 'emboss all directions', 'emboss horizontal and vertical', 'emboss horizontal only',
    'emboss laplascian', 'emboss vertical only', 'gaussian blur', 'gaussiannoisereducer', 'gradientmap', 'halftone', 'hsvadjustment',
    'indexcolors', 'invert', 'left edge detections', 'lens blur', 'levels', 'maximize', 'mean removal', 'minimize', 'motion blur',
    'noise', 'normalize', 'oilpaint', 'perchannel', 'phongbumpmap', 'pixelize', 'posterize', 'raindrops', 'randompick',
    'right edge detections', 'roundcorners', 'sharpen', 'smalltiles', 'sobel', 'threshold', 'top edge detections', 'unsharp',
    'wave', 'waveletnoisereducer']
       """

    def setName(name):
        """ 
@brief setName set the filter's name to the given name.

name:    QString
return:  void
 """ 

    def setConfiguration(value):
        """ 
@brief setConfiguration set the configuration object for the filter

value:   InfoObject
return:  void
 """ 

    def apply(node,x,y,w,h):
        """ 
@brief Apply the filter to the given node. @param node the node to apply the filter to @param x @param y @param w @param h describe the rectangle the filter should be apply. This is always in image pixel coordinates and not relative to the x, y of the node. @return @c true if the filter was applied successfully, or @c false if the filter could not be applied because the node is locked or does not have an editable paint device.

node:    Node
x:       int
y:       int
w:       int
h:       int
return:  bool
 """ 

    def startFilter(node,x,y,w,h):
        """ 
@brief startFilter starts the given filter on the given node. @param node the node to apply the filter to @param x @param y @param w @param h describe the rectangle the filter should be apply. This is always in image pixel coordinates and not relative to the x, y of the node.

node:    Node
x:       int
y:       int
w:       int
h:       int
return:  bool
 """ 



# auto-generated from: FilterLayer.h 
class FilterLayer:
    """  @brief The FilterLayer class
    A filter layer will, when compositing, take the composited
    image up to the point of the loction of the filter layer
    in the stack, create a copy and apply a filter.
   
    This means you can use blending modes on the filter layers,
    which will be used to blend the filtered image with the original.
   
    Similarly, you can activate things like alpha inheritance, or
    you can set grayscale pixeldata on the filter layer to act as
    a mask.
   
    Filter layers can be animated.
       """

    def FilterLayer(image,name,filter,selection,parent):
        """ 
@brief The FilterLayer class A filter layer will, when compositing, take the composited image up to the point of the loction of the filter layer in the stack, create a copy and apply a filter. This means you can use blending modes on the filter layers, which will be used to blend the filtered image with the original. Similarly, you can activate things like alpha inheritance, or you can set grayscale pixeldata on the filter layer to act as a mask. Filter layers can be animated./class KRITALIBKIS_EXPORT FilterLayer : public Node{Q_OBJECTQ_DISABLE_COPY(FilterLayer)

image:      KisImageSP
name:       QString
filter:     Filter
selection:  Selection
parent:     QObject
return:     void
 """ 

    def FilterLayer(layer,parent):
        """ 
@brief The FilterLayer class A filter layer will, when compositing, take the composited image up to the point of the loction of the filter layer in the stack, create a copy and apply a filter. This means you can use blending modes on the filter layers, which will be used to blend the filtered image with the original. Similarly, you can activate things like alpha inheritance, or you can set grayscale pixeldata on the filter layer to act as a mask. Filter layers can be animated./class KRITALIBKIS_EXPORT FilterLayer : public Node{Q_OBJECTQ_DISABLE_COPY(FilterLayer)public:

layer:   KisAdjustmentLayerSP
parent:  QObject
return:  void
 """ 

    def setFilter(filter):
        """ 
@brief type Krita has several types of nodes, split in layers and masks. Group layers can contain other layers, any layer can contain masks. @return "filterlayer"/QString type() const override;

filter:  Filter
return:  void
 """ 



# auto-generated from: FilterMask.h 
class FilterMask:
    """  @brief The FilterMask class
    A filter mask, unlike a filter layer, will add a non-destructive filter
    to the composited image of the node it is attached to.
   
    You can set grayscale pixeldata on the filter mask to adjust where the filter is applied.
   
    Filtermasks can be animated.
       """

    def FilterMask(image,name,filter,parent):
        """ 
@brief The FilterMask class A filter mask, unlike a filter layer, will add a non-destructive filter to the composited image of the node it is attached to. You can set grayscale pixeldata on the filter mask to adjust where the filter is applied. Filtermasks can be animated./class KRITALIBKIS_EXPORT FilterMask : public Node{Q_OBJECTQ_DISABLE_COPY(FilterMask)

image:   KisImageSP
name:    QString
filter:  Filter
parent:  QObject
return:  void
 """ 

    def FilterMask(image,mask,parent):
        """ 
@brief The FilterMask class A filter mask, unlike a filter layer, will add a non-destructive filter to the composited image of the node it is attached to. You can set grayscale pixeldata on the filter mask to adjust where the filter is applied. Filtermasks can be animated./class KRITALIBKIS_EXPORT FilterMask : public Node{Q_OBJECTQ_DISABLE_COPY(FilterMask)public:

image:   KisImageSP
mask:    KisFilterMaskSP
parent:  QObject
return:  void
 """ 

    def setFilter(filter):
        """ 
@brief type Krita has several types of nodes, split in layers and masks. Group layers can contain other layers, any layer can contain masks. @return The type of the node. Valid types are: <ul>  <li>paintlayer  <li>grouplayer  <li>filelayer  <li>filterlayer  <li>filllayer  <li>clonelayer  <li>vectorlayer  <li>transparencymask  <li>filtermask  <li>transformmask  <li>selectionmask  <li>colorizemask </ul> If the Node object isn't wrapping a valid Krita layer or mask object, and empty string is returned./QString type() const override;

filter:  Filter
return:  void
 """ 



# auto-generated from: GroupLayer.h 
class GroupLayer:
    """  @brief The GroupLayer class
    A group layer is a layer that can contain other layers.
    In Krita, layers within a group layer are composited
    first before they are added into the composition code for where
    the group is in the stack. This has a significant effect on how
    it is interpreted for blending modes.
   
    PassThrough changes this behaviour.
   
    Group layer cannot be animated, but can contain animated layers or masks.
       """

    def GroupLayer(image,name,parent):
        """ 
@brief The GroupLayer class A group layer is a layer that can contain other layers. In Krita, layers within a group layer are composited first before they are added into the composition code for where the group is in the stack. This has a significant effect on how it is interpreted for blending modes. PassThrough changes this behaviour. Group layer cannot be animated, but can contain animated layers or masks./class KRITALIBKIS_EXPORT GroupLayer : public Node{Q_OBJECTQ_DISABLE_COPY(GroupLayer)

image:   KisImageSP
name:    QString
parent:  QObject
return:  void
 """ 

    def GroupLayer(layer,parent):
        """ 
@brief The GroupLayer class A group layer is a layer that can contain other layers. In Krita, layers within a group layer are composited first before they are added into the composition code for where the group is in the stack. This has a significant effect on how it is interpreted for blending modes. PassThrough changes this behaviour. Group layer cannot be animated, but can contain animated layers or masks./class KRITALIBKIS_EXPORT GroupLayer : public Node{Q_OBJECTQ_DISABLE_COPY(GroupLayer)public:

layer:   KisGroupLayerSP
parent:  QObject
return:  void
 """ 

    def setPassThroughMode(passthrough):
        """ 
@brief setPassThroughMode This changes the way how compositing works. Instead of compositing all the layers before compositing it with the rest of the image, the group layer becomes a sort of formal way to organise everything. Passthrough mode is the same as it is in photoshop, and the inverse of SVG's isolation attribute(with passthrough=false being the same as isolation="isolate"). @param passthrough whether or not to set the layer to passthrough.

passthrough:  bool
return:       void
 """ 



# auto-generated from: GroupShape.h 
class GroupShape:
    """  @brief The GroupShape class
    A group shape is a vector object with child shapes.
       """

    def GroupShape(parent):
        """ 
@brief The GroupShape class A group shape is a vector object with child shapes./class KRITALIBKIS_EXPORT GroupShape : public Shape{Q_OBJECT

parent:  QObject
return:  void
 """ 

    def GroupShape(shape,parent):
        """ 
@brief The GroupShape class A group shape is a vector object with child shapes./class KRITALIBKIS_EXPORT GroupShape : public Shape{Q_OBJECTpublic:

shape:   KoShapeGroup
parent:  QObject
return:  void
 """ 



# auto-generated from: InfoObject.h 
class InfoObject:
    """  InfoObject wrap a properties map. These maps can be used to set the
    configuration for filters.
       """

    def InfoObject(configuration):
        """ 
InfoObject wrap a properties map. These maps can be used to set the configuration for filters./class KRITALIBKIS_EXPORT InfoObject : public QObject{Q_OBJECT

configuration:  KisPropertiesConfigurationSP
return:         void
 """ 

    def InfoObject(parent):
        """ 
Create a new, empty InfoObject.

parent:  QObject
return:  void
 """ 

    def setProperties(propertyMap):
        """ 
Add all properties in the @p propertyMap to this InfoObject

propertyMap:  QMap>
return:       void
 """ 

    def setProperty(key,value):
        """ 
set the property identified by @p key to @p value If you want create a property that represents a color, you can use a QColor or hex string, as defined in https://doc.qt.io/qt-5/qcolor.html#setNamedColor.

key:     QString
value:   QVariant
return:  void
 """ 

    def property(key):
        """ 
return the value for the property identified by key, or None if there is no such key.

key:     QString
return:  QVariant
 """ 



# auto-generated from: Krita.h 
class Krita:
    """  Krita is a singleton class that offers the root access to the Krita object hierarchy.
   
    The Krita.instance() is aliased as two builtins: Scripter and Application.
       """

    def Krita(parent):
        """ 
Krita is a singleton class that offers the root access to the Krita object hierarchy. The Krita.instance() is aliased as two builtins: Scripter and Application./class KRITALIBKIS_EXPORT Krita : public QObject{Q_OBJECT

parent:  QObject
return:  void
 """ 

    def setActiveDocument(value):
        """ 
@brief setActiveDocument activates the first view that shows the given document @param value the document we want to activate

value:   Document
return:  void
 """ 

    def setBatchmode(value):
        """ 
@brief setBatchmode sets the batchmode to @param value; if true, scripts should not show dialogs or messageboxes.

value:   bool
return:  void
 """ 

    def action(name):
        """ 
@return the action that has been registered under the given name, or 0 if no such action exists.

name:    QString
return:  QAction
 """ 

    def filter(name):
        """ 
@brief filter construct a Filter object with a default configuration. @param name the name of the filter. Use Krita.instance().filters() to get a list of all possible filters. @return the filter or None if there is no such filter.

name:    QString
return:  Filter
 """ 

    def colorDepths(colorModel):
        """ 
@brief colorDepths creates a list with the names of all color depths compatible with the given color model. @param colorModel the id of a color model. @return a list of all color depths or a empty list if there is no such color depths.

colorModel:  QString
return:      QStringList
 """ 

    def profiles(colorModel,colorDepth):
        """ 
@brief profiles creates a list with the names of all color profiles compatible with the given color model and color depth. @param colorModel A string describing the color model of the image: <ul> <li>A: Alpha mask</li> <li>RGBA: RGB with alpha channel (The actual order of channels is most often BGR!)</li> <li>XYZA: XYZ with alpha channel</li> <li>LABA: LAB with alpha channel</li> <li>CMYKA: CMYK with alpha channel</li> <li>GRAYA: Gray with alpha channel</li> <li>YCbCrA: YCbCr with alpha channel</li> </ul> @param colorDepth A string describing the color depth of the image: <ul> <li>U8: unsigned 8 bits integer, the most common type</li> <li>U16: unsigned 16 bits integer</li> <li>F16: half, 16 bits floating point. Only available if Krita was built with OpenEXR</li> <li>F32: 32 bits floating point</li> </ul> @return a list with valid names

colorModel:  QString
colorDepth:  QString
return:      QStringList
 """ 

    def addProfile(profilePath):
        """ 
@brief addProfile load the given profile into the profile registry. @param profilePath the path to the profile. @return true if adding the profile succeeded.

profilePath:  QString
return:       bool
 """ 

    def resources(type):
        """ 
@brief resources returns a list of Resource objects of the given type @param type Valid types are: <ul> <li>pattern</li> <li>gradient</li> <li>brush</li> <li>preset</li> <li>palette</li> <li>workspace</li> </ul>

type:    QString
return:  QMap>
 """ 

    def createDocument(width,height,name,colorModel,colorDepth,profile,resolution):
        """ 
@brief createDocument creates a new document and image and registers the document with the Krita application. Unless you explicitly call Document::close() the document will remain known to the Krita document registry. The document and its image will only be deleted when Krita exits. The document will have one transparent layer. To create a new document and show it, do something like:@codefrom Krita import def add_document_to_window():d = Application.createDocument(100, 100, "Test", "RGBA", "U8", "", 120.0)Application.activeWindow().addView(d)add_document_to_window()@endcode @param width the width in pixels @param height the height in pixels @param name the name of the image (not the filename of the document) @param colorModel A string describing the color model of the image: <ul> <li>A: Alpha mask</li> <li>RGBA: RGB with alpha channel (The actual order of channels is most often BGR!)</li> <li>XYZA: XYZ with alpha channel</li> <li>LABA: LAB with alpha channel</li> <li>CMYKA: CMYK with alpha channel</li> <li>GRAYA: Gray with alpha channel</li> <li>YCbCrA: YCbCr with alpha channel</li> </ul> @param colorDepth A string describing the color depth of the image: <ul> <li>U8: unsigned 8 bits integer, the most common type</li> <li>U16: unsigned 16 bits integer</li> <li>F16: half, 16 bits floating point. Only available if Krita was built with OpenEXR</li> <li>F32: 32 bits floating point</li> </ul> @param profile The name of an icc profile that is known to Krita. If an empty string is passed, the default is taken. @param resolution the resolution in points per inch. @return the created document.

width:       int
height:      int
name:        QString
colorModel:  QString
colorDepth:  QString
profile:     QString
resolution:  double
return:      Document
 """ 

    def openDocument(filename):
        """ 
@brief openDocument creates a new Document, registers it with the Krita application and loads the given file. @param filename the file to open in the document @return the document

filename:  QString
return:    Document
 """ 

    def addExtension(extension):
        """ 
@brief addExtension add the given plugin to Krita. There will be a single instance of each Extension in the Krita process. @param extension the extension to add.

extension:  Extension
return:     void
 """ 

    def addDockWidgetFactory(factory):
        """ 
@brief addDockWidgetFactory Add the given docker factory to the application. For scripts loaded on startup, this means that every window will have one of the dockers created by the factory. @param factory The factory object.

factory:  DockWidgetFactoryBase
return:   void
 """ 

    def writeSetting(group,name,value):
        """ 
@brief writeSetting write the given setting under the given name to the kritarc file in the given settings group. @param group The group the setting belongs to. If empty, then the setting is written in the general section @param name The name of the setting @param value The value of the setting. Script settings are always written as strings.

group:   QString
name:    QString
value:   QString
return:  void
 """ 

    def readSetting(group,name,defaultValue):
        """ 
@brief readSetting read the given setting value from the kritarc file. @param group The group the setting is part of. If empty, then the setting is read from the general group. @param name The name of the setting @param defaultValue The default value of the setting @return a string representing the setting.

group:         QString
name:          QString
defaultValue:  QString
return:        QString
 """ 

    def icon(iconName):
        """ 
@brief icon This allows you to get icons from Krita's internal icons. @param iconName name of the icon. @return the icon related to this name.

iconName:  QString
return:    QIcon
 """ 

    def QString(text):
        """ 
@brief instance retrieve the singleton instance of the Application object./static Krita instance();/Internal only: for use with mikro.pystatic QObject fromVariant(const QVariant& v);

text:    QString
return:  static
 """ 

    def QString(context,text):
        """ 
@brief instance retrieve the singleton instance of the Application object./static Krita instance();/Internal only: for use with mikro.pystatic QObject fromVariant(const QVariant& v);

context:  QString
text:     QString
return:   static
 """ 

    def mainWindowIsBeingCreated(window):
        """ 
@brief instance retrieve the singleton instance of the Application object./static Krita instance();/Internal only: for use with mikro.pystatic QObject fromVariant(const QVariant& v);static QString krita_i18n(const QString &text);static QString krita_i18nc(const QString &context, const QString &text);private Q_SLOTS:

window:  KisMainWindow
return:  void
 """ 



# auto-generated from: libkis.h 
    """ Class not documented    """



# auto-generated from: LibKisUtils.h 
    """ Class not documented    """

    def createNodeList(kisnodes,image):
        """ 
Missing function documentation

kisnodes:  KisNodeList
image:     KisImageWSP
return:    QList>
 """ 



# auto-generated from: ManagedColor.h 
class ManagedColor:
    """  @brief The ManagedColor class is a class to handle colors that are color managed.
    A managed color is a color of which we know the model(RGB, LAB, CMYK, etc), the bitdepth and
    the specific properties of its colorspace, such as the whitepoint, chromacities, trc, etc, as represented
    by the color profile.
   
    Krita has two color management systems. LCMS and OCIO.
    LCMS is the one handling the ICC profile stuff, and the major one handling that ManagedColor deals with.
    OCIO support is only in the display of the colors. ManagedColor has some support for it in colorForCanvas()
   
    All colors in Krita are color managed. QColors are understood as RGB-type colors in the sRGB space.
   
    We recommend you make a color like this:
   
    @code
    colorYellow = ManagedColor("RGBA", "U8", "")
    QVector<float> yellowComponents = colorYellow.components()
    yellowComponents[0] = 1.0
    yellowComponents[1] = 1.0
    yellowComponents[2] = 0
    yellowComponents[3] = 1.0
   
    colorYellow.setComponents(yellowComponents)
    QColor yellow = colorYellow.colorForCanvas(canvas)
    @endcode
       """

    def ManagedColor(parent):
        """ 
@brief ManagedColor Create a ManagedColor that is black and transparent.

parent:  QObject
return:  void
 """ 

    def ManagedColor(colorModel,colorDepth,colorProfile,parent):
        """ 
@brief ManagedColor create a managed color with the given color space properties. @see setColorModel() for more details.

colorModel:    QString
colorDepth:    QString
colorProfile:  QString
parent:        QObject
return:        void
 """ 

    def ManagedColor(color,parent):
        """ 
@brief ManagedColor create a managed color with the given color space properties. @see setColorModel() for more details./

color:   KoColor
parent:  QObject
return:  void
 """ 

    def colorForCanvas(canvas):
        """ 
@brief colorForCanvas @param canvas the canvas whose color management you'd like to use. In Krita, different views have separate canvasses, and these can have different OCIO configurations active. @return the QColor as it would be displaying on the canvas. This result can be used to draw widgets with the correct configuration applied.

canvas:  Canvas
return:  QColor
 """ 

    def ManagedColor(qcolor,canvas):
        """ 
@brief fromQColor is the (approximate) reverse of colorForCanvas() @param qcolor the QColor to convert to a KoColor. @param canvas the canvas whose color management you'd like to use. @return the approximated ManagedColor, to use for canvas resources.

qcolor:  QColor
canvas:  Canvas
return:  static
 """ 

    def setColorProfile(colorProfile):
        """ 
@brief setColorProfile set the color profile of the image to the given profile. The profile has to be registered with krita and be compatible with the current color model and depth; the image data is <i>not</i> converted. @param colorProfile @return false if the colorProfile name does not correspond to to a registered profile or if assigning the profile failed.

colorProfile:  QString
return:        bool
 """ 

    def setColorSpace(colorModel,colorDepth,colorProfile):
        """ 
@brief setColorSpace convert the nodes and the image to the given colorspace. The conversion is done with Perceptual as intent, High Quality and No LCMS Optimizations as flags and no blackpoint compensation. @param colorModel A string describing the color model of the image: <ul> <li>A: Alpha mask</li> <li>RGBA: RGB with alpha channel (The actual order of channels is most often BGR!)</li> <li>XYZA: XYZ with alpha channel</li> <li>LABA: LAB with alpha channel</li> <li>CMYKA: CMYK with alpha channel</li> <li>GRAYA: Gray with alpha channel</li> <li>YCbCrA: YCbCr with alpha channel</li> </ul> @param colorDepth A string describing the color depth of the image: <ul> <li>U8: unsigned 8 bits integer, the most common type</li> <li>U16: unsigned 16 bits integer</li> <li>F16: half, 16 bits floating point. Only available if Krita was built with OpenEXR</li> <li>F32: 32 bits floating point</li> </ul> @param colorProfile a valid color profile for this color model and color depth combination. @return false the combination of these arguments does not correspond to a colorspace.

colorModel:    QString
colorDepth:    QString
colorProfile:  QString
return:        bool
 """ 

    def setComponents(values):
        """ 
@brief setComponents Set the channel/components with normalized values. For integer colorspace, this obviously means the limit is between 0.0-1.0, but for floating point colorspaces, 2.4 or 103.5 are still meaningful (if bright) values. @param values the QVector containing the new channel/component values. These should be normalized.

values:  QVector>
return:  void
 """ 

    def fromXML(xml):
        """ 
Unserialize a color following Create's swatch color specification available at https://web.archive.org/web/20110826002520/http://create.freedesktop.org/wiki/Swatches_-_color_file_format/Draft @param xml an XML color @return the unserialized color, or an empty color object if the function failed         to unserialize the color

xml:     QString
return:  void
 """ 



# auto-generated from: Node.h 
class Node:
    """  Node represents a layer or mask in a Krita image's Node hierarchy. Group layers can contain
    other layers and masks; layers can contain masks.
   
       """

    def Node(image,node,parent):
        """ 
Node represents a layer or mask in a Krita image's Node hierarchy. Group layers can contain other layers and masks; layers can contain masks./class KRITALIBKIS_EXPORT Node : public QObject{Q_OBJECTQ_DISABLE_COPY(Node)

image:   KisImageSP
node:    KisNodeSP
parent:  QObject
return:  static
 """ 

    def setAlphaLocked(value):
        """ 
@brief setAlphaLocked set the layer to value if the node is paint layer.

value:   bool
return:  void
 """ 

    def setBlendingMode(value):
        """ 
@brief setBlendingMode set the blending mode of the node to the given value @param value one of the string values from @see KoCompositeOpRegistry.h

value:   QString
return:  void
 """ 

    def addChildNode(child,above):
        """ 
@brief addChildNode adds the given node in the list of children. @param child the node to be added @param above the node above which this node will be placed @return false if adding the node failed

child:   Node
above:   Node
return:  bool
 """ 

    def removeChildNode(child):
        """ 
@brief removeChildNode removes the given node from the list of children. @param child the node to be removed

child:   Node
return:  bool
 """ 

    def setChildNodes(nodes):
        """ 
@brief setChildNodes this replaces the existing set of child nodes with the new set. @param nodes The list of nodes that will become children, bottom-up -- the first node, is the bottom-most node in the stack.

nodes:   QList>
return:  void
 """ 

    def setColorProfile(colorProfile):
        """ 
@brief setColorProfile set the color profile of the image to the given profile. The profile has to be registered with krita and be compatible with the current color model and depth; the image data is <i>not</i> converted. @param colorProfile @return if assigning the color profile worked

colorProfile:  QString
return:        bool
 """ 

    def setColorSpace(colorModel,colorDepth,colorProfile):
        """ 
@brief setColorSpace convert the node to the given colorspace @param colorModel A string describing the color model of the node: <ul> <li>A: Alpha mask</li> <li>RGBA: RGB with alpha channel (The actual order of channels is most often BGR!)</li> <li>XYZA: XYZ with alpha channel</li> <li>LABA: LAB with alpha channel</li> <li>CMYKA: CMYK with alpha channel</li> <li>GRAYA: Gray with alpha channel</li> <li>YCbCrA: YCbCr with alpha channel</li> </ul> @param colorDepth A string describing the color depth of the image: <ul> <li>U8: unsigned 8 bits integer, the most common type</li> <li>U16: unsigned 16 bits integer</li> <li>F16: half, 16 bits floating point. Only available if Krita was built with OpenEXR</li> <li>F32: 32 bits floating point</li> </ul> @param colorProfile a valid color profile for this color model and color depth combination.

colorModel:    QString
colorDepth:    QString
colorProfile:  QString
return:        bool
 """ 

    def setPinnedToTimeline(pinned):
        """ 
@brief Sets whether or not node should be pinned to the Timeline Docker, regardless of selection activity.

pinned:  bool
return:  void
 """ 

    def setCollapsed(collapsed):
        """ 
Sets the state of the node to the value of @param collapsed

collapsed:  bool
return:     void
 """ 

    def setColorLabel(index):
        """ 
@brief setColorLabel sets a color label index associated to the layer.  The actual color of the label and the number of available colors is defined by Krita GUI configuration. @param index an integer corresponding to the set of available color labels.

index:   int
return:  void
 """ 

    def setInheritAlpha(value):
        """ 
set the Inherit Alpha flag to the given value

value:   bool
return:  void
 """ 

    def setLocked(value):
        """ 
set the Locked flag to the give value

value:   bool
return:  void
 """ 

    def setName(name):
        """ 
rename the Node to the given name

name:    QString
return:  void
 """ 

    def setOpacity(value):
        """ 
set the opacity of the Node to the given value. The opacity is a value between 0 and 255.

value:   int
return:  void
 """ 

    def hasKeyframeAtTime(frameNumber):
        """ 
Check to see if frame number on layer is a keyframe

frameNumber:  int
return:       bool
 """ 

    def setVisible(visible):
        """ 
Set the visibility of the current node to @param visible

visible:  bool
return:   void
 """ 

    def pixelData(x,y,w,h):
        """ 
@brief pixelData reads the given rectangle from the Node's paintable pixels, if those exist, and returns it as a byte array. The pixel data starts top-left, and is ordered row-first. The byte array can be interpreted as follows: 8 bits images have one byte per channel, and as many bytes as there are channels. 16 bits integer images have two bytes per channel, representing an unsigned short. 16 bits float images have two bytes per channel, representing a half, or 16 bits float. 32 bits float images have four bytes per channel, representing a float. You can read outside the node boundaries; those pixels will be transparent black. The order of channels is: <ul> <li>Integer RGBA: Blue, Green, Red, Alpha <li>Float RGBA: Red, Green, Blue, Alpha <li>GrayA: Gray, Alpha <li>Selection: selectedness <li>LabA: L, a, b, Alpha <li>CMYKA: Cyan, Magenta, Yellow, Key, Alpha <li>XYZA: X, Y, Z, A <li>YCbCrA: Y, Cb, Cr, Alpha </ul> The byte array is a copy of the original node data. In Python, you can use bytes, bytearray and the struct module to interpret the data and construct, for instance, a Pillow Image object. If you read the pixeldata of a mask, a filter or generator layer, you get the selection bytes, which is one channel with values in the range from 0..255. If you want to change the pixels of a node you can write the pixels back after manipulation with setPixelData(). This will only succeed on nodes with writable pixel data, e.g not on groups or file layers. @param x x position from where to start reading @param y y position from where to start reading @param w row length to read @param h number of rows to read @return a QByteArray with the pixel data. The byte array may be empty.

x:       int
y:       int
w:       int
h:       int
return:  QByteArray
 """ 

    def pixelDataAtTime(x,y,w,h,time):
        """ 
@brief pixelDataAtTime a basic function to get pixeldata from an animated node at a given time. @param x the position from the left to start reading. @param y the position from the top to start reader @param w the row length to read @param h the number of rows to read @param time the frame number @return a QByteArray with the pixel data. The byte array may be empty.

x:       int
y:       int
w:       int
h:       int
time:    int
return:  QByteArray
 """ 

    def projectionPixelData(x,y,w,h):
        """ 
@brief projectionPixelData reads the given rectangle from the Node's projection (that is, what the node looks like after all sub-Nodes (like layers in a group or masks on a layer) have been applied, and returns it as a byte array. The pixel data starts top-left, and is ordered row-first. The byte array can be interpreted as follows: 8 bits images have one byte per channel, and as many bytes as there are channels. 16 bits integer images have two bytes per channel, representing an unsigned short. 16 bits float images have two bytes per channel, representing a half, or 16 bits float. 32 bits float images have four bytes per channel, representing a float. You can read outside the node boundaries; those pixels will be transparent black. The order of channels is: <ul> <li>Integer RGBA: Blue, Green, Red, Alpha <li>Float RGBA: Red, Green, Blue, Alpha <li>GrayA: Gray, Alpha <li>Selection: selectedness <li>LabA: L, a, b, Alpha <li>CMYKA: Cyan, Magenta, Yellow, Key, Alpha <li>XYZA: X, Y, Z, A <li>YCbCrA: Y, Cb, Cr, Alpha </ul> The byte array is a copy of the original node data. In Python, you can use bytes, bytearray and the struct module to interpret the data and construct, for instance, a Pillow Image object. If you read the projection of a mask, you get the selection bytes, which is one channel with values in the range from 0..255. If you want to change the pixels of a node you can write the pixels back after manipulation with setPixelData(). This will only succeed on nodes with writable pixel data, e.g not on groups or file layers. @param x x position from where to start reading @param y y position from where to start reading @param w row length to read @param h number of rows to read @return a QByteArray with the pixel data. The byte array may be empty.

x:       int
y:       int
w:       int
h:       int
return:  QByteArray
 """ 

    def setPixelData(value,x,y,w,h):
        """ 
@brief setPixelData writes the given bytes, of which there must be enough, into the Node, if the Node has writable pixel data: <ul> <li>paint layer: the layer's original pixels are overwritten <li>filter layer, generator layer, any mask: the embedded selection's pixels are overwritten. <b>Note:</b> for these </ul> File layers, Group layers, Clone layers cannot be written to. Calling setPixelData on those layer types will silently do nothing. @param value the byte array representing the pixels. There must be enough bytes available. Krita will take the raw pointer from the QByteArray and start reading, not stopping before (number of channels  size of channel  w  h) bytes are read. @param x the x position to start writing from @param y the y position to start writing from @param w the width of each row @param h the number of rows to write @return true if writing the pixeldata worked

value:   QByteArray
x:       int
y:       int
w:       int
h:       int
return:  bool
 """ 

    def move(x,y):
        """ 
 move the pixels to the given x, y location in the image coordinate space.

x:       int
y:       int
return:  void
 """ 

    def save(filename,xRes,yRes,exportConfiguration,exportRect):
        """ 
@brief save exports the given node with this filename. The extension of the filename determines the filetype. @param filename the filename including extension @param xRes the horizontal resolution in pixels per pt (there are 72 pts in an inch) @param yRes the horizontal resolution in pixels per pt (there are 72 pts in an inch) @param exportConfiguration a configuration object appropriate to the file format. @param exportRect the export bounds for saving a node as a QRect If \p exportRect is empty, then save exactBounds() of the node. If you'd like to save the image- aligned area of the node, just pass image->bounds() there. See Document->exportImage for InfoObject details. @return true if saving succeeded, false if it failed.

filename:             QString
xRes:                 double
yRes:                 double
exportConfiguration:  InfoObject
exportRect:           QRect
return:               bool
 """ 

    def scaleNode(origin,width,height,strategy):
        """ 
@brief scaleNode @param origin the origin point @param width the width @param height the height @param strategy the scaling strategy. There's several ones amongst these that aren't available in the regular UI. <ul> <li>Hermite</li> <li>Bicubic - Adds pixels using the color of surrounding pixels. Produces smoother tonal gradations than Bilinear.</li> <li>Box - Replicate pixels in the image. Preserves all the original detail, but can produce jagged effects.</li> <li>Bilinear - Adds pixels averaging the color values of surrounding pixels. Produces medium quality results when the image is scaled from half to two times the original size.</li> <li>Bell</li> <li>BSpline</li> <li>Lanczos3 - Offers similar results than Bicubic, but maybe a little bit sharper. Can produce light and dark halos along strong edges.</li> <li>Mitchell</li> </ul>

origin:    QPointF
width:     int
height:    int
strategy:  QString
return:    void
 """ 

    def rotateNode(radians):
        """ 
@brief rotateNode rotate this layer by the given radians. @param radians amount the layer should be rotated in, in radians.

radians:  double
return:   void
 """ 

    def cropNode(x,y,w,h):
        """ 
@brief cropNode crop this layer. @param x the left edge of the cropping rectangle. @param y the top edge of the cropping rectangle @param w the right edge of the cropping rectangle @param h the bottom edge of the cropping rectangle

x:       int
y:       int
w:       int
h:       int
return:  void
 """ 

    def shearNode(angleX,angleY):
        """ 
@brief shearNode perform a shear operation on this node. @param angleX the X-angle in degrees to shear by @param angleY the Y-angle in degrees to shear by

angleX:  double
angleY:  double
return:  void
 """ 

    def thumbnail(w,h):
        """ 
@brief thumbnail create a thumbnail of the given dimensions. The thumbnail is sized according to the layer dimensions, not the image dimensions. If the requested size is too big a null QImage is created. If the current node cannot generate a thumbnail, a transparent QImage of the requested size is generated. @return a QImage representing the layer contents.

w:       int
h:       int
return:  QImage
 """ 

    def setLayerStyleFromAsl(asl):
        """ 
@brief setLayerStyleFromAsl set a new layer style for this node. @param aslContent a string formatted in ASL format containing the layer style @return true if layer style was set, false if failed.

asl:     QString
return:  bool
 """ 

    def Node(image,node,parent):
        """ 
@brief uniqueId uniqueId of the node @return a QUuid representing a unique id to identify the node/QUuid uniqueId() const;private:friend class Filter;friend class Document;friend class Selection;friend class GroupLayer;friend class FileLayer;friend class FilterLayer;friend class FillLayer;friend class VectorLayer;friend class FilterMask;friend class SelectionMask;friend class TransformMask;friend class CloneLayer;

image:   KisImageSP
node:    KisNodeSP
parent:  QObject
return:  void
 """ 



# auto-generated from: Notifier.h 
class Notifier:
    """  The Notifier can be used to be informed of state changes in the Krita application.
       """

    def Notifier(parent):
        """ 
The Notifier can be used to be informed of state changes in the Krita application./class KRITALIBKIS_EXPORT Notifier : public QObject{Q_OBJECTQ_DISABLE_COPY(Notifier)Q_PROPERTY(bool Active READ active WRITE setActive)

parent:  QObject
return:  void
 """ 

    def setActive(value):
        """ 
Enable or disable the Notifier

value:   bool
return:  void
 """ 

    def imageCreated(image):
        """ 
@brief imageCreated is emitted whenever a new image is created and registered with the application.

image:   Document
return:  void
 """ 

    def imageSaved(filename):
        """ 
@brief imageSaved is emitted whenever a document is saved. @param filename the filename of the document that has been saved.

filename:  QString
return:    void
 """ 

    def imageClosed(filename):
        """ 
@brief imageClosed is emitted whenever the last view on an image is closed. The image does not exist anymore in Krita @param filename the filename of the image.

filename:  QString
return:    void
 """ 

    def viewCreated(view):
        """ 
@brief viewCreated is emitted whenever a new view is created. @param view the view

view:    View
return:  void
 """ 

    def viewClosed(view):
        """ 
@brief viewClosed is emitted whenever a view is closed @param view the view

view:    View
return:  void
 """ 

    def windowIsBeingCreated(window):
        """ 
@brief windowCreated is emitted whenever a window is being created @param window the window; this is called from the constructor of the window, before the xmlgui file is loaded

window:  Window
return:  void
 """ 

    def imageCreated(document):
        """ 
@brief configurationChanged is emitted every time Krita's configuration has changed./void configurationChanged();private Q_SLOTS:

document:  KisDocument
return:    void
 """ 

    def viewCreated(view):
        """ 
@brief configurationChanged is emitted every time Krita's configuration has changed./void configurationChanged();private Q_SLOTS:void imageCreated(KisDocument document);

view:    KisView
return:  void
 """ 

    def viewClosed(view):
        """ 
@brief configurationChanged is emitted every time Krita's configuration has changed./void configurationChanged();private Q_SLOTS:void imageCreated(KisDocument document);

view:    KisView
return:  void
 """ 

    def windowIsBeingCreated(window):
        """ 
@brief configurationChanged is emitted every time Krita's configuration has changed./void configurationChanged();private Q_SLOTS:void imageCreated(KisDocument document);void viewCreated(KisView view);void viewClosed(KisView view);

window:  KisMainWindow
return:  void
 """ 



# auto-generated from: Palette.h 
class Palette:
    """  @brief The Palette class
    Palette is a resource object that stores organised color data.
    It's purpose is to allow artists to save colors and store them.
   
    An example for printing all the palettes and the entries:
   
    @code
   import sys
   from krita import 
   
   resources = Application.resources("palette")
   
   for (k, v) in resources.items():
   print(k)
   palette = Palette(v)
   for x in range(palette.numberOfEntries()):
   entry = palette.colorSetEntryByIndex(x)
   c = palette.colorForEntry(entry);
   print(x, entry.name(), entry.id(), entry.spotColor(), c.toQString())
    @endcode
       """

    def Palette(resource):
        """ 
@brief The Palette class Palette is a resource object that stores organised color data. It's purpose is to allow artists to save colors and store them. An example for printing all the palettes and the entries: @codeimport sysfrom krita import resources = Application.resources("palette")for (k, v) in resources.items():print(k)palette = Palette(v)for x in range(palette.numberOfEntries()):entry = palette.colorSetEntryByIndex(x)c = palette.colorForEntry(entry);print(x, entry.name(), entry.id(), entry.spotColor(), c.toQString()) @endcode/class KRITALIBKIS_EXPORT Palette : public QObject{

resource:  Resource
return:    void
 """ 

    def setColumnCount(columns):
        """ 
@brief setColumnCount Set the amount of columns this palette should use.

columns:  int
return:   void
 """ 

    def setComment(comment):
        """ 
@brief setComment set the comment or description associated with the palette. @param comment

comment:  QString
return:   void
 """ 

    def addGroup(name):
        """ 
@brief addGroup @param name of the new group @return whether adding the group was successful.

name:    QString
return:  bool
 """ 

    def removeGroup(name,keepColors):
        """ 
@brief removeGroup @param name the name of the group to remove. @param keepColors whether or not to delete all the colors inside, or to move them to the default group. @return

name:        QString
keepColors:  bool
return:      bool
 """ 

    def colorSetEntryByIndex(index):
        """ 
@brief colorSetEntryByIndex get the colorsetEntry from the global index. @param index the global index @return the colorset entry

index:   int
return:  Swatch
 """ 

    def colorSetEntryFromGroup(index,groupName):
        """ 
@brief colorSetEntryFromGroup @param index index in the group. @param groupName the name of the group to get the color from. @return the colorsetentry.

index:      int
groupName:  QString
return:     Swatch
 """ 

    def addEntry(entry,groupName):
        """ 
@brief addEntry add an entry to a group. Gets appended to the end. @param entry the entry @param groupName the name of the group to add to.

entry:      Swatch
groupName:  QString
return:     void
 """ 

    def removeEntry(index,groupName):
        """ 
@brief removeEntry remove the entry at @p index from the group @p groupName.

index:      int
groupName:  QString
return:     void
 """ 

    def changeGroupName(oldGroupName,newGroupName):
        """ 
@brief changeGroupName change the group name. @param oldGroupName the old groupname to change. @param newGroupName the new name to change it into. @return whether successful. Reasons for failure include not knowing have oldGroupName

oldGroupName:  QString
newGroupName:  QString
return:        bool
 """ 

    def moveGroup(groupName,groupNameInsertBefore):
        """ 
@brief moveGroup move the group to before groupNameInsertBefore. @param groupName group to move. @param groupNameInsertBefore group to inset before. @return whether successful. Reasons for failure include either group not existing.

groupName:              QString
groupNameInsertBefore:  QString
return:                 bool
 """ 



# auto-generated from: PaletteView.h 
class PaletteView:
    """  @class PaletteView
    @brief The PaletteView class is a wrapper around a MVC method for handling
    palettes. This class shows a nice widget that can drag and drop, edit colors in a colorset
    and will handle adding and removing entries if you'd like it to.
       """

    def PaletteView(parent):
        """ 
@class PaletteView @brief The PaletteView class is a wrapper around a MVC method for handling palettes. This class shows a nice widget that can drag and drop, edit colors in a colorset and will handle adding and removing entries if you'd like it to./class KRITALIBKIS_EXPORT PaletteView : public QWidget{Q_OBJECT

parent:  QWidget
return:  void
 """ 

    def setPalette(palette):
        """ 
@brief setPalette Set a new palette. @param palette

palette:  Palette
return:   void
 """ 

    def addEntryWithDialog(color):
        """ 
@brief addEntryWithDialog This gives a simple dialog for adding colors, with options like adding name, id, and to which group the color should be added. @param color the default color to add @return whether it was successful.

color:   ManagedColor
return:  bool
 """ 

    def trySelectClosestColor(color):
        """ 
@brief trySelectClosestColor tries to select the closest color to the one given. It does not force a change on the active color. @param color the color to compare to.

color:   ManagedColor
return:  void
 """ 

    def entrySelectedForeGround(entry):
        """ 
@brief entrySelectedForeGround fires when a swatch is selected with leftclick. @param entry

entry:   Swatch
return:  void
 """ 

    def entrySelectedBackGround(entry):
        """ 
@brief entrySelectedBackGround fires when a swatch is selected with rightclick. @param entry

entry:   Swatch
return:  void
 """ 

    def fgSelected(swatch):
        """ 
@brief entrySelectedBackGround fires when a swatch is selected with rightclick. @param entry/void entrySelectedBackGround(Swatch entry);private Q_SLOTS:

swatch:  KisSwatch
return:  void
 """ 

    def bgSelected(swatch):
        """ 
@brief entrySelectedBackGround fires when a swatch is selected with rightclick. @param entry/void entrySelectedBackGround(Swatch entry);private Q_SLOTS:

swatch:  KisSwatch
return:  void
 """ 



# auto-generated from: PresetChooser.h 
class PresetChooser:
    """  @brief The PresetChooser widget wraps the KisPresetChooser widget.
    The widget provides for selecting brush presets. It has a tagging
    bar and a filter field. It is not automatically synchronized with
    the currently selected preset in the current Windows.
       """

    def PresetChooser(parent):
        """ 
@brief The PresetChooser widget wraps the KisPresetChooser widget. The widget provides for selecting brush presets. It has a tagging bar and a filter field. It is not automatically synchronized with the currently selected preset in the current Windows./class KRITALIBKIS_EXPORT PresetChooser : public KisPresetChooser{Q_OBJECT

parent:  QWidget
return:  void
 """ 

    def setCurrentPreset(resource):
        """ 
Make the given preset active.

resource:  Resource
return:    void
 """ 

    def presetSelected(resource):
        """ 
Emitted whenever a user selects the given preset.

resource:  Resource
return:    void
 """ 

    def presetClicked(resource):
        """ 
Emitted whenever a user clicks on the given preset.

resource:  Resource
return:    void
 """ 

    def slotResourceSelected(resource):
        """ 
Emitted whenever a user clicks on the given preset./void presetClicked(Resource resource);private Q_SLOTS:

resource:  KoResourceSP
return:    void
 """ 

    def slotResourceClicked(resource):
        """ 
Emitted whenever a user clicks on the given preset./void presetClicked(Resource resource);private Q_SLOTS:

resource:  KoResourceSP
return:    void
 """ 



# auto-generated from: Resource.h 
class Resource:
    """  A Resource represents a gradient, pattern, brush tip, brush preset, palette or
    workspace definition.
   
    @code
    allPresets = Application.resources("preset")
    for preset in allPresets:
        print(preset.name())
    @endcode
   
    Resources are identified by their type, name and filename. If you want to change
    the contents of a resource, you should read its data using data(), parse it and
    write the changed contents back.
       """

    def Resource(resourceId,type,name,filename,image,parent):
        """ 
A Resource represents a gradient, pattern, brush tip, brush preset, palette or workspace definition. @code allPresets = Application.resources("preset") for preset in allPresets:     print(preset.name()) @endcode Resources are identified by their type, name and filename. If you want to change the contents of a resource, you should read its data using data(), parse it and write the changed contents back./class KRITALIBKIS_EXPORT Resource : public QObject{Q_OBJECT

resourceId:  int
type:        QString
name:        QString
filename:    QString
image:       QImage
parent:      QObject
return:      void
 """ 

    def Resource(resource,type,parent):
        """ 
A Resource represents a gradient, pattern, brush tip, brush preset, palette or workspace definition. @code allPresets = Application.resources("preset") for preset in allPresets:     print(preset.name()) @endcode Resources are identified by their type, name and filename. If you want to change the contents of a resource, you should read its data using data(), parse it and write the changed contents back./class KRITALIBKIS_EXPORT Resource : public QObject{Q_OBJECTpublic:

resource:  KoResourceSP
type:      QString
parent:    QObject
return:    void
 """ 

    def Resource(rhs):
        """ 
A Resource represents a gradient, pattern, brush tip, brush preset, palette or workspace definition. @code allPresets = Application.resources("preset") for preset in allPresets:     print(preset.name()) @endcode Resources are identified by their type, name and filename. If you want to change the contents of a resource, you should read its data using data(), parse it and write the changed contents back./class KRITALIBKIS_EXPORT Resource : public QObject{Q_OBJECTpublic:Resource(int resourceId, const QString &type, const QString &name, const QString &filename, const QImage &image, QObject parent = 0);Resource(KoResourceSP resource, const QString &type, QObject parent = 0);

rhs:     Resource
return:  void
 """ 

    def setName(value):
        """ 
setName changes the user-visible name of the current resource.

value:   QString
return:  void
 """ 

    def setImage(image):
        """ 
Change the image for this resource.

image:   QImage
return:  void
 """ 



# auto-generated from: Scratchpad.h 
class Scratchpad:
    """  @brief The Scratchpad class
    A scratchpad is a type of blank canvas area that can be painted on
    with the normal painting devices
   
       """

    def Scratchpad(view, defaultColor,parent):
        """ 
@brief The Scratchpad class A scratchpad is a type of blank canvas area that can be painted on with the normal painting devices/class KRITALIBKIS_EXPORT Scratchpad: public QWidget{Q_OBJECT

view:           View
 defaultColor:  QColor
parent:         QWidget
return:         void
 """ 

    def setFillColor(color):
        """ 
@brief Fill the entire scratchpad with a color @param Color to fill the canvas with

color:   QColor
return:  void
 """ 

    def setModeManually(value):
        """ 
@brief Switches between a GUI controlling the current mode and when mouse clicks control mode @param Setting to true allows GUI to control the mode with explicitly setting mode

value:   bool
return:  void
 """ 

    def setMode(modeName):
        """ 
@brief Manually set what mode scratchpad is in. Ignored if "setModeManually is set to false @param Available options are: "painting", "panning", and "colorsampling"

modeName:  QString
return:    void
 """ 

    def linkCanvasZoom(value):
        """ 
@brief Makes a connection between the zoom of the canvas and scratchpad area so they zoom in sync @param Should the scratchpad share the zoom level. Default is true

value:   bool
return:  void
 """ 

    def loadScratchpadImage(image):
        """ 
@brief Load image data to the scratchpad @param Image object to load

image:   QImage
return:  void
 """ 



# auto-generated from: Selection.h 
class Selection:
    """  Selection represents a selection on Krita. A selection is
    not necessarily associated with a particular Node or Image.
   
    @code
    from krita import 
   
    d = Application.activeDocument()
    n = d.activeNode()
    r = n.bounds()
    s = Selection()
    s.select(r.width() / 3, r.height() / 3, r.width() / 3, r.height() / 3, 255)
    s.cut(n)
    @endcode
       """

    def Selection(selection,parent):
        """ 
For internal use only.

selection:  KisSelectionSP
parent:     QObject
return:     void
 """ 

    def Selection(parent):
        """ 
Create a new, empty selection object.

parent:  QObject
return:  void
 """ 

    def move(x,y):
        """ 
Move the selection's top-left corner to the given coordinates.

x:       int
y:       int
return:  void
 """ 

    def contract(value):
        """ 
Make the selection's width and height smaller by the given value. This will not move the selection's top-left position.

value:   int
return:  void
 """ 

    def copy(node):
        """ 
@brief copy copies the area defined by the selection from the node to the clipboard. @param node the node from where the pixels will be copied.

node:    Node
return:  void
 """ 

    def cut(node):
        """ 
@brief cut erases the area defined by the selection from the node and puts a copy on the clipboard. @param node the node from which the selection will be cut.

node:    Node
return:  void
 """ 

    def paste(destination,x,y):
        """ 
@brief paste pastes the content of the clipboard to the given node, limited by the area of the current selection. @param destination the node where the pixels will be written @param x: the x position at which the clip will be written @param y: the y position at which the clip will be written

destination:  Node
x:            int
y:            int
return:       void
 """ 

    def border(xRadius,yRadius):
        """ 
Border the selection with the given radius.

xRadius:  int
yRadius:  int
return:   void
 """ 

    def feather(radius):
        """ 
Feather the selection with the given radius.

radius:  int
return:  void
 """ 

    def grow(xradius,yradius):
        """ 
Grow the selection with the given radius.

xradius:  int
yradius:  int
return:   void
 """ 

    def shrink(xRadius,yRadius,edgeLock):
        """ 
Shrink the selection with the given radius.

xRadius:   int
yRadius:   int
edgeLock:  bool
return:    void
 """ 

    def resize(w,h):
        """ 
Resize the selection to the given width and height. The top-left position will not be moved.

w:       int
h:       int
return:  void
 """ 

    def select(x,y,w,h,value):
        """ 
Select the given area. The value can be between 0 and 255; 0 is totally unselected, 255 is totally selected.

x:       int
y:       int
w:       int
h:       int
value:   int
return:  void
 """ 

    def selectAll(node,value):
        """ 
Select all pixels in the given node. The value can be between 0 and 255; 0 is totally unselected, 255 is totally selected.

node:    Node
value:   int
return:  void
 """ 

    def replace(selection):
        """ 
Replace the current selection's selection with the one of the given selection.

selection:  Selection
return:     void
 """ 

    def add(selection):
        """ 
Add the given selection's selected pixels to the current selection.

selection:  Selection
return:     void
 """ 

    def subtract(selection):
        """ 
Subtract the given selection's selected pixels from the current selection.

selection:  Selection
return:     void
 """ 

    def intersect(selection):
        """ 
Intersect the given selection with this selection.

selection:  Selection
return:     void
 """ 

    def symmetricdifference(selection):
        """ 
Intersect with the inverse of the given selection with this selection.

selection:  Selection
return:     void
 """ 

    def pixelData(x,y,w,h):
        """ 
@brief pixelData reads the given rectangle from the Selection's mask and returns it as a byte array. The pixel data starts top-left, and is ordered row-first. The byte array will contain one byte for every pixel, representing the selectedness. 0 is totally unselected, 255 is fully selected. You can read outside the Selection's boundaries; those pixels will be unselected. The byte array is a copy of the original selection data. @param x x position from where to start reading @param y y position from where to start reading @param w row length to read @param h number of rows to read @return a QByteArray with the pixel data. The byte array may be empty.

x:       int
y:       int
w:       int
h:       int
return:  QByteArray
 """ 

    def setPixelData(value,x,y,w,h):
        """ 
@brief setPixelData writes the given bytes, of which there must be enough, into the Selection. @param value the byte array representing the pixels. There must be enough bytes available. Krita will take the raw pointer from the QByteArray and start reading, not stopping before (w  h) bytes are read. @param x the x position to start writing from @param y the y position to start writing from @param w the width of each row @param h the number of rows to write

value:   QByteArray
x:       int
y:       int
w:       int
h:       int
return:  void
 """ 



# auto-generated from: SelectionMask.h 
class SelectionMask:
    """  @brief The SelectionMask class
    A selection mask is a mask type node that can be used
    to store selections. In the gui, these are referred to
    as local selections.
   
    A selection mask can hold both raster and vector selections, though
    the API only supports raster selections.
       """

    def SelectionMask(image,name,parent):
        """ 
@brief The SelectionMask class A selection mask is a mask type node that can be used to store selections. In the gui, these are referred to as local selections. A selection mask can hold both raster and vector selections, though the API only supports raster selections./class KRITALIBKIS_EXPORT SelectionMask : public Node{Q_OBJECTQ_DISABLE_COPY(SelectionMask)

image:   KisImageSP
name:    QString
parent:  QObject
return:  void
 """ 

    def SelectionMask(image,mask,parent):
        """ 
@brief The SelectionMask class A selection mask is a mask type node that can be used to store selections. In the gui, these are referred to as local selections. A selection mask can hold both raster and vector selections, though the API only supports raster selections./class KRITALIBKIS_EXPORT SelectionMask : public Node{Q_OBJECTQ_DISABLE_COPY(SelectionMask)public:

image:   KisImageSP
mask:    KisSelectionMaskSP
parent:  QObject
return:  void
 """ 

    def setSelection(selection):
        """ 
@brief type Krita has several types of nodes, split in layers and masks. Group layers can contain other layers, any layer can contain masks. @return selectionmask If the Node object isn't wrapping a valid Krita layer or mask object, and empty string is returned./virtual QString type() const override;Selection selection() const;

selection:  Selection
return:     void
 """ 



# auto-generated from: Shape.h 
class Shape:
    """  @brief The Shape class
    The shape class is a wrapper around Krita's vector objects.
   
    Some example code to parse through interesting information in a given vector layer with shapes.
    @code
   import sys
   from krita import 
   
   doc = Application.activeDocument()
   
   root = doc.rootNode()
   
   for layer in root.childNodes():
   print (str(layer.type())+" "+str(layer.name()))
   if (str(layer.type())=="vectorlayer"):
   for shape in layer.shapes():
   print(shape.name())
   print(shape.toSvg())
    @endcode
       """

    def Shape(shape,parent):
        """ 
@brief The Shape class The shape class is a wrapper around Krita's vector objects. Some example code to parse through interesting information in a given vector layer with shapes. @codeimport sysfrom krita import doc = Application.activeDocument()root = doc.rootNode()for layer in root.childNodes():print (str(layer.type())+" "+str(layer.name()))if (str(layer.type())=="vectorlayer"):for shape in layer.shapes():print(shape.name())print(shape.toSvg()) @endcode/class KRITALIBKIS_EXPORT Shape : public QObject{Q_OBJECTQ_DISABLE_COPY(Shape)

shape:   KoShape
parent:  QObject
return:  void
 """ 

    def setName(name):
        """ 
@brief setName @param name which name the shape should have.

name:    QString
return:  void
 """ 

    def setZIndex(zindex):
        """ 
@brief setZIndex @param zindex set the shape zindex value.

zindex:  int
return:  void
 """ 

    def setSelectable(selectable):
        """ 
@brief setSelectable @param selectable whether the shape should be user selectable.

selectable:  bool
return:      void
 """ 

    def setGeometryProtected(protect):
        """ 
@brief setGeometryProtected @param protect whether the shape should be geometry protected from the user.

protect:  bool
return:   void
 """ 

    def setVisible(visible):
        """ 
@brief setVisible @param visible whether the shape should be visible.

visible:  bool
return:   void
 """ 

    def setPosition(point):
        """ 
@brief setPosition set the position of the shape. @param point the new position in points

point:   QPointF
return:  void
 """ 

    def setTransformation(matrix):
        """ 
@brief setTransformation set the 2D transformation matrix of the shape. @param matrix the new 2D transformation matrix.

matrix:  QTransform
return:  void
 """ 

    def updateAbsolute(box):
        """ 
@brief updateAbsolute queue the shape update in the specified rectangle. @param box the RectF rectangle to update.

box:     QRectF
return:  void
 """ 

    def toSvg(prependStyles,stripTextMode):
        """ 
@brief toSvg convert the shape to svg, will not include style definitions. @param prependStyles prepend the style data. Default: false @param stripTextMode enable strip text mode. Default: true @return the svg in a string./

prependStyles:  bool
stripTextMode:  bool
return:         QString
 """ 



# auto-generated from: Swatch.h 
class Swatch:
    """  @brief The Swatch class is a thin wrapper around the KisSwatch class.
   
    A Swatch is a single color that is part of a palette, that has a name
    and an id. A Swatch color can be a spot color.
       """

    def Swatch(kisSwatch):
        """ 
@brief The Swatch class is a thin wrapper around the KisSwatch class. A Swatch is a single color that is part of a palette, that has a name and an id. A Swatch color can be a spot color./class KRITALIBKIS_EXPORT Swatch{private:friend class Palette;

kisSwatch:  KisSwatch
return:     void
 """ 

    def Swatch(rhs):
        """ 
@brief The Swatch class is a thin wrapper around the KisSwatch class. A Swatch is a single color that is part of a palette, that has a name and an id. A Swatch color can be a spot color./class KRITALIBKIS_EXPORT Swatch{private:friend class Palette;friend class PaletteView;Swatch(const KisSwatch &kisSwatch);public:Swatch();

rhs:     Swatch
return:  void
 """ 

    def setName(name):
        """ 
@brief The Swatch class is a thin wrapper around the KisSwatch class. A Swatch is a single color that is part of a palette, that has a name and an id. A Swatch color can be a spot color./class KRITALIBKIS_EXPORT Swatch{private:friend class Palette;friend class PaletteView;Swatch(const KisSwatch &kisSwatch);public:Swatch();virtual ~Swatch();Swatch(const Swatch &rhs);Swatch &operator=(const Swatch &rhs);

name:    QString
return:  void
 """ 

    def setId(id):
        """ 
@brief The Swatch class is a thin wrapper around the KisSwatch class. A Swatch is a single color that is part of a palette, that has a name and an id. A Swatch color can be a spot color./class KRITALIBKIS_EXPORT Swatch{private:friend class Palette;friend class PaletteView;Swatch(const KisSwatch &kisSwatch);public:Swatch();virtual ~Swatch();Swatch(const Swatch &rhs);Swatch &operator=(const Swatch &rhs);QString name() const;void setName(const QString &name);

id:      QString
return:  void
 """ 

    def setColor(color):
        """ 
@brief The Swatch class is a thin wrapper around the KisSwatch class. A Swatch is a single color that is part of a palette, that has a name and an id. A Swatch color can be a spot color./class KRITALIBKIS_EXPORT Swatch{private:friend class Palette;friend class PaletteView;Swatch(const KisSwatch &kisSwatch);public:Swatch();virtual ~Swatch();Swatch(const Swatch &rhs);Swatch &operator=(const Swatch &rhs);QString name() const;void setName(const QString &name);QString id() const;void setId(const QString &id);

color:   ManagedColor
return:  void
 """ 

    def setSpotColor(spotColor):
        """ 
@brief The Swatch class is a thin wrapper around the KisSwatch class. A Swatch is a single color that is part of a palette, that has a name and an id. A Swatch color can be a spot color./class KRITALIBKIS_EXPORT Swatch{private:friend class Palette;friend class PaletteView;Swatch(const KisSwatch &kisSwatch);public:Swatch();virtual ~Swatch();Swatch(const Swatch &rhs);Swatch &operator=(const Swatch &rhs);QString name() const;void setName(const QString &name);QString id() const;void setId(const QString &id);ManagedColor color() const;void setColor(ManagedColor color);

spotColor:  bool
return:     void
 """ 



# auto-generated from: TransformMask.h 
class TransformMask:
    """  @brief The TransformMask class
    A transform mask is a mask type node that can be used
    to store transformations.
       """

    def TransformMask(image,name,parent):
        """ 
@brief The TransformMask class A transform mask is a mask type node that can be used to store transformations./class KRITALIBKIS_EXPORT TransformMask : public Node{Q_OBJECTQ_DISABLE_COPY(TransformMask)

image:   KisImageSP
name:    QString
parent:  QObject
return:  void
 """ 

    def TransformMask(image,mask,parent):
        """ 
@brief The TransformMask class A transform mask is a mask type node that can be used to store transformations./class KRITALIBKIS_EXPORT TransformMask : public Node{Q_OBJECTQ_DISABLE_COPY(TransformMask)public:

image:   KisImageSP
mask:    KisTransformMaskSP
parent:  QObject
return:  void
 """ 



# auto-generated from: VectorLayer.h 
class VectorLayer:
    """  @brief The VectorLayer class
    A vector layer is a special layer that stores
    and shows vector shapes.
   
    Vector shapes all have their coordinates in points, which
    is a unit that represents 1/72th of an inch. Keep this in
    mind wen parsing the bounding box and position data.
       """

    def VectorLayer(shapeController,image,name,parent):
        """ 
@brief The VectorLayer class A vector layer is a special layer that stores and shows vector shapes. Vector shapes all have their coordinates in points, which is a unit that represents 1/72th of an inch. Keep this in mind wen parsing the bounding box and position data./class KRITALIBKIS_EXPORT VectorLayer : public Node{Q_OBJECTQ_DISABLE_COPY(VectorLayer)

shapeController:  KoShapeControllerBase
image:            KisImageSP
name:             QString
parent:           QObject
return:           void
 """ 

    def VectorLayer(layer,parent):
        """ 
@brief The VectorLayer class A vector layer is a special layer that stores and shows vector shapes. Vector shapes all have their coordinates in points, which is a unit that represents 1/72th of an inch. Keep this in mind wen parsing the bounding box and position data./class KRITALIBKIS_EXPORT VectorLayer : public Node{Q_OBJECTQ_DISABLE_COPY(VectorLayer)public:

layer:   KisShapeLayerSP
parent:  QObject
return:  void
 """ 

    def addShapesFromSvg(svg):
        """ 
@brief addShapesFromSvg add shapes to the layer from a valid svg. @param svg valid svg string. @return the list of shapes added to the layer from the svg.

svg:     QString
return:  QList>
 """ 



# auto-generated from: View.h 
class View:
    """  View represents one view on a document. A document can be
    shown in more than one view at a time.
       """

    def View(view,parent):
        """ 
View represents one view on a document. A document can be shown in more than one view at a time./class KRITALIBKIS_EXPORT View : public QObject{Q_OBJECTQ_DISABLE_COPY(View)

view:    KisView
parent:  QObject
return:  void
 """ 

    def setDocument(document):
        """ 
Reset the view to show @p document.

document:  Document
return:    void
 """ 

    def activateResource(resource):
        """ 
@brief activateResource activates the given resource. @param resource: a pattern, gradient or paintop preset

resource:  Resource
return:    void
 """ 

    def setForeGroundColor(color):
        """ 
@brief foregroundColor allows access to the currently active color. This is nominally per canvas/view, but in practice per mainwindow. @codecolor = Application.activeWindow().activeView().foregroundColor()components = color.components()components[0] = 1.0components[1] = 0.6components[2] = 0.7color.setComponents(components)Application.activeWindow().activeView().setForeGroundColor(color) @endcode/

color:   ManagedColor
return:  void
 """ 

    def setBackGroundColor(color):
        """ 
@brief foregroundColor allows access to the currently active color. This is nominally per canvas/view, but in practice per mainwindow. @codecolor = Application.activeWindow().activeView().foregroundColor()components = color.components()components[0] = 1.0components[1] = 0.6components[2] = 0.7color.setComponents(components)Application.activeWindow().activeView().setForeGroundColor(color) @endcode/ManagedColor foregroundColor() const;void setForeGroundColor(ManagedColor color);

color:   ManagedColor
return:  void
 """ 

    def setCurrentBrushPreset(resource):
        """ 
@brief foregroundColor allows access to the currently active color. This is nominally per canvas/view, but in practice per mainwindow. @codecolor = Application.activeWindow().activeView().foregroundColor()components = color.components()components[0] = 1.0components[1] = 0.6components[2] = 0.7color.setComponents(components)Application.activeWindow().activeView().setForeGroundColor(color) @endcode/ManagedColor foregroundColor() const;void setForeGroundColor(ManagedColor color);ManagedColor backgroundColor() const;void setBackGroundColor(ManagedColor color);

resource:  Resource
return:    void
 """ 

    def setCurrentPattern(resource):
        """ 
@brief foregroundColor allows access to the currently active color. This is nominally per canvas/view, but in practice per mainwindow. @codecolor = Application.activeWindow().activeView().foregroundColor()components = color.components()components[0] = 1.0components[1] = 0.6components[2] = 0.7color.setComponents(components)Application.activeWindow().activeView().setForeGroundColor(color) @endcode/ManagedColor foregroundColor() const;void setForeGroundColor(ManagedColor color);ManagedColor backgroundColor() const;void setBackGroundColor(ManagedColor color);Resource currentBrushPreset() const;void setCurrentBrushPreset(Resource resource);

resource:  Resource
return:    void
 """ 

    def setCurrentGradient(resource):
        """ 
@brief foregroundColor allows access to the currently active color. This is nominally per canvas/view, but in practice per mainwindow. @codecolor = Application.activeWindow().activeView().foregroundColor()components = color.components()components[0] = 1.0components[1] = 0.6components[2] = 0.7color.setComponents(components)Application.activeWindow().activeView().setForeGroundColor(color) @endcode/ManagedColor foregroundColor() const;void setForeGroundColor(ManagedColor color);ManagedColor backgroundColor() const;void setBackGroundColor(ManagedColor color);Resource currentBrushPreset() const;void setCurrentBrushPreset(Resource resource);Resource currentPattern() const;void setCurrentPattern(Resource resource);

resource:  Resource
return:    void
 """ 

    def setCurrentBlendingMode(blendingMode):
        """ 
@brief foregroundColor allows access to the currently active color. This is nominally per canvas/view, but in practice per mainwindow. @codecolor = Application.activeWindow().activeView().foregroundColor()components = color.components()components[0] = 1.0components[1] = 0.6components[2] = 0.7color.setComponents(components)Application.activeWindow().activeView().setForeGroundColor(color) @endcode/ManagedColor foregroundColor() const;void setForeGroundColor(ManagedColor color);ManagedColor backgroundColor() const;void setBackGroundColor(ManagedColor color);Resource currentBrushPreset() const;void setCurrentBrushPreset(Resource resource);Resource currentPattern() const;void setCurrentPattern(Resource resource);Resource currentGradient() const;void setCurrentGradient(Resource resource);

blendingMode:  QString
return:        void
 """ 

    def setHDRExposure(exposure):
        """ 
@brief foregroundColor allows access to the currently active color. This is nominally per canvas/view, but in practice per mainwindow. @codecolor = Application.activeWindow().activeView().foregroundColor()components = color.components()components[0] = 1.0components[1] = 0.6components[2] = 0.7color.setComponents(components)Application.activeWindow().activeView().setForeGroundColor(color) @endcode/ManagedColor foregroundColor() const;void setForeGroundColor(ManagedColor color);ManagedColor backgroundColor() const;void setBackGroundColor(ManagedColor color);Resource currentBrushPreset() const;void setCurrentBrushPreset(Resource resource);Resource currentPattern() const;void setCurrentPattern(Resource resource);Resource currentGradient() const;void setCurrentGradient(Resource resource);QString currentBlendingMode() const;void setCurrentBlendingMode(const QString &blendingMode);

exposure:  float
return:    void
 """ 

    def setHDRGamma(gamma):
        """ 
@brief foregroundColor allows access to the currently active color. This is nominally per canvas/view, but in practice per mainwindow. @codecolor = Application.activeWindow().activeView().foregroundColor()components = color.components()components[0] = 1.0components[1] = 0.6components[2] = 0.7color.setComponents(components)Application.activeWindow().activeView().setForeGroundColor(color) @endcode/ManagedColor foregroundColor() const;void setForeGroundColor(ManagedColor color);ManagedColor backgroundColor() const;void setBackGroundColor(ManagedColor color);Resource currentBrushPreset() const;void setCurrentBrushPreset(Resource resource);Resource currentPattern() const;void setCurrentPattern(Resource resource);Resource currentGradient() const;void setCurrentGradient(Resource resource);QString currentBlendingMode() const;void setCurrentBlendingMode(const QString &blendingMode);float HDRExposure() const;void setHDRExposure(float exposure);

gamma:   float
return:  void
 """ 

    def setPaintingOpacity(opacity):
        """ 
@brief foregroundColor allows access to the currently active color. This is nominally per canvas/view, but in practice per mainwindow. @codecolor = Application.activeWindow().activeView().foregroundColor()components = color.components()components[0] = 1.0components[1] = 0.6components[2] = 0.7color.setComponents(components)Application.activeWindow().activeView().setForeGroundColor(color) @endcode/ManagedColor foregroundColor() const;void setForeGroundColor(ManagedColor color);ManagedColor backgroundColor() const;void setBackGroundColor(ManagedColor color);Resource currentBrushPreset() const;void setCurrentBrushPreset(Resource resource);Resource currentPattern() const;void setCurrentPattern(Resource resource);Resource currentGradient() const;void setCurrentGradient(Resource resource);QString currentBlendingMode() const;void setCurrentBlendingMode(const QString &blendingMode);float HDRExposure() const;void setHDRExposure(float exposure);float HDRGamma() const;void setHDRGamma(float gamma);

opacity:  qreal
return:   void
 """ 

    def setBrushSize(brushSize):
        """ 
@brief foregroundColor allows access to the currently active color. This is nominally per canvas/view, but in practice per mainwindow. @codecolor = Application.activeWindow().activeView().foregroundColor()components = color.components()components[0] = 1.0components[1] = 0.6components[2] = 0.7color.setComponents(components)Application.activeWindow().activeView().setForeGroundColor(color) @endcode/ManagedColor foregroundColor() const;void setForeGroundColor(ManagedColor color);ManagedColor backgroundColor() const;void setBackGroundColor(ManagedColor color);Resource currentBrushPreset() const;void setCurrentBrushPreset(Resource resource);Resource currentPattern() const;void setCurrentPattern(Resource resource);Resource currentGradient() const;void setCurrentGradient(Resource resource);QString currentBlendingMode() const;void setCurrentBlendingMode(const QString &blendingMode);float HDRExposure() const;void setHDRExposure(float exposure);float HDRGamma() const;void setHDRGamma(float gamma);qreal paintingOpacity() const;void setPaintingOpacity(qreal opacity);

brushSize:  qreal
return:     void
 """ 

    def setPaintingFlow(flow):
        """ 
@brief foregroundColor allows access to the currently active color. This is nominally per canvas/view, but in practice per mainwindow. @codecolor = Application.activeWindow().activeView().foregroundColor()components = color.components()components[0] = 1.0components[1] = 0.6components[2] = 0.7color.setComponents(components)Application.activeWindow().activeView().setForeGroundColor(color) @endcode/ManagedColor foregroundColor() const;void setForeGroundColor(ManagedColor color);ManagedColor backgroundColor() const;void setBackGroundColor(ManagedColor color);Resource currentBrushPreset() const;void setCurrentBrushPreset(Resource resource);Resource currentPattern() const;void setCurrentPattern(Resource resource);Resource currentGradient() const;void setCurrentGradient(Resource resource);QString currentBlendingMode() const;void setCurrentBlendingMode(const QString &blendingMode);float HDRExposure() const;void setHDRExposure(float exposure);float HDRGamma() const;void setHDRGamma(float gamma);qreal paintingOpacity() const;void setPaintingOpacity(qreal opacity);qreal brushSize() const;void setBrushSize(qreal brushSize);

flow:    qreal
return:  void
 """ 

    def showFloatingMessage(message,icon,timeout,priority):
        """ 
@brief showFloatingMessage displays a floating message box on the top-left corner of the canvas @param message: Message to be displayed inside the floating message box @param icon: Icon to be displayed inside the message box next to the message string @param timeout: Milliseconds until the message box disappears @param priority: 0 = High, 1 = Medium, 2 = Low. Higher priority messages will be displayed in place of lower priority messages

message:   QString
icon:      QIcon
timeout:   int
priority:  int
return:    void
 """ 



# auto-generated from: Window.h 
class Window:
    """  Window represents one Krita mainwindow. A window can have any number
    of views open on any number of documents.
       """

    def Window(window,parent):
        """ 
Window represents one Krita mainwindow. A window can have any number of views open on any number of documents./class KRITALIBKIS_EXPORT Window : public QObject{Q_OBJECT

window:  KisMainWindow
parent:  QObject
return:  void
 """ 

    def addView(document):
        """ 
Open a new view on the given document in this window

document:  Document
return:    View
 """ 

    def showView(view):
        """ 
Make the given view active in this window. If the view does not belong to this window, nothing happens.

view:    View
return:  void
 """ 

    def createAction(id,text):
        """ 
@brief createAction creates a QAction object and adds it to the action manager for this Window. @param id The unique id for the action. This will be used to     propertize the action if any .action file is present @param text The user-visible text of the action. If empty, the text from the    .action file is used. @param menuLocation a /-separated string that describes which menu the action should     be places in. Default is "tools/scripts" @return the new action.

id:      QString
text:    QString
return:  QAction
 """ 


