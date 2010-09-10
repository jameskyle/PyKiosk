#
#  main.py
#  PyKiosk
#
#  Created by James Kyle on 9/8/10.
#  Copyright KSpace MRI 2010. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import PyKioskAppDelegate
import SelectionView

# pass control to AppKit
AppHelper.runEventLoop()
