#
#  SelectionView.py
#  PyKiosk
#
#  Created by James Kyle on 9/8/10.
#  Copyright (c) 2010 KSpace MRI. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *
from Quartz import *
from Quartz.QuartzCore import *

class SelectionView(NSView):
    def initWithFrame_(self, frame):
        self = super(SelectionView, self).initWithFrame_(frame)
        
        self.selectedIndex = 0
        self.menuLayer = CALayer.layer()
        self.selectionLayer = CALayer.layer()
        self.names = []
        
        return self
    
    def awakeFromNib(self):
        NSLog("awakeFromNib")

        self.names = [u"Movies", u"Music", u"Podcasts", u"Photos", u"Internet"]
        
        # hide the cursor
        NSCursor.hide()
        
        # go full screen, this is what makes it a kiosk
        self.enterFullScreenMode_withOptions_(self.window().screen(), None)
        
        # make window first responder for key strokes
        self.window().makeFirstResponder_(self)
        
        # set up the individual layers for the kiosk
        self.setupLayers()
        
        # bring the window to the front
        self.window().makeKeyAndOrderFront_(self)
        

    def setupLayers(self):
    
        # Make a quartz composition layer.
        # Running a QCComposition can impact performance
        rootLayer = QCCompositionLayer.compositionLayerWithFile_(
                     NSBundle.mainBundle().pathForResource_ofType_(
                     u"Background", "qtz"))

        # set the QCCompositionlayer as the root layer
        # and then turn on wantsLayer. This order prevents 
        # the view from creating its own layer
        self.setLayer_(rootLayer)
        self.setWantsLayer_(YES)

        
        # Setup the menulayers array. The selectable menu items.
        self.menuLayer.setFrame_(rootLayer.frame())
        self.menuLayer.setLayoutManager_(CAConstraintLayoutManager.layoutManager())
        rootLayer.addSublayer_(self.menuLayer)
        
        # setup and calculate the size and location of the individually 
        # selectable items
        width = 400.0
        height = 50.0
        spacing = 20.0
        fontSize = 32.0
        initialOffset = ((self.bounds().size.height/2 - 
                         (height*5 + spacing*4)/2.0) + 50)
                         
        # create whiteColor. It's used to draw the text and also 
        # in the selectionLayer
        whiteColor = CGColorCreateGenericRGB(1.0, 1.0, 1.0, 1.0)
        
        # iterate of the list of selection names and create layers for them
        # the menuItemLayers are also positioned during this loop
        
        for name in self.names:
            menuItemLayer = CATextLayer.layer()
            menuItemLayer.setString_(name)
            menuItemLayer.setFontSize_(fontSize)
            menuItemLayer.setForegroundColor_(whiteColor)
            menuItemLayer.addConstraint_(
            CAConstraint.constraintWithAttribute_relativeTo_attribute_offset_(
                    kCAConstraintMaxY, 
                    u"superlayer", 
                    kCAConstraintMaxY, 
                    -(self.names.index(name)*height+spacing+initialOffset)))
            
            menuItemLayer.addConstraint_(
            CAConstraint.constraintWithAttribute_relativeTo_attribute_(
                    kCAConstraintMidX, 
                    u"superlayer", 
                    kCAConstraintMidX))
                    
            self.menuLayer.addSublayer_(menuItemLayer)
            
        self.menuLayer.layoutIfNeeded()
        
        # set up selectionlayer. 
        # Displays the currently selected item
        
        # use an additional layer, selectionLayer
        # to indicate that the current item is selected
        self.selectionLayer.setBounds_(CGRectMake(0.0, 0.0, width, height))
        self.selectionLayer.setBorderWidth_(2.0)
        self.selectionLayer.setCornerRadius_(25)
        self.selectionLayer.setBorderColor_(whiteColor)
        
        filter = CIFilter.filterWithName_(u"CIBloom")
        filter.setDefaults()
        filter.setName_(u"pulseFilter")
        self.selectionLayer.setFilters_(NSArray.arrayWithObject_(filter))
        
        # The selectionlayer shows a subtle pulse as it is displayed.
        # this action of the code creates the pulse animation
        # setting the filters.pulsefilter.inputeintensity to range from 0 to 2.
        # this will happen every second, autoreverse, and repeat forever
        pulseAnimation = CABasicAnimation.animation()
        pulseAnimation.setKeyPath_(u"filters.pulseFilter.inputIntensity")
        pulseAnimation.setFromValue_(0.0)
        pulseAnimation.setToValue_(2.0)
        pulseAnimation.setDuration_(1.0)
        pulseAnimation.setRepeatCount_(1e100)
        pulseAnimation.setAutoreverses_(YES)
        pulseAnimation.setTimingFunction_(
            CAMediaTimingFunction.functionWithName_(
                    kCAMediaTimingFunctionEaseInEaseOut))
                    
        self.selectionLayer.addAnimation_forKey_(pulseAnimation, u"pulseAnimation")
        
        # set the first item as selected
        self.changeSelectedIndex(0)
        
        # finally, the selection layer is added to the root layer
        rootLayer.addSublayer_(self.selectionLayer)
        
        CGColorRelease(whiteColor)
                     
        NSLog("Set up layers")


    def changeSelectedIndex(self, index):
        self.selectedIndex = index
        
        if self.selectedIndex == len(self.names):
            self.selectedIndex = len(self.names) - 1
        if self.selectedIndex < 0:
            self.selectedIndex = 0
            
        selectedLayer = self.menuLayer.sublayers().objectAtIndex_(self.selectedIndex)
        
        self.selectionLayer.setPosition_(selectedLayer.position())
        
    def moveUp_(self, sender):
        self.changeSelectedIndex(self.selectedIndex - 1)
        
    def moveDown_(self, sender):
        self.changeSelectedIndex(self.selectedIndex + 1)