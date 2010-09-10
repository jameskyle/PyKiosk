#
#  PyKioskAppDelegate.py
#  PyKiosk
#
#  Created by James Kyle on 9/8/10.
#  Copyright KSpace MRI 2010. All rights reserved.
#

from Foundation import *
from AppKit import *

class PyKioskAppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
