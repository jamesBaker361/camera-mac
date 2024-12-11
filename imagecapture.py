import objc
from Foundation import NSObject
from ImageCaptureCore import ICDeviceBrowser, ICCameraDevice

class DeviceBrowserDelegate(NSObject):
    def init(self):
        self = objc.super(DeviceBrowserDelegate, self).init()
        if self:
            self.devices = []
        return self

    def deviceBrowser_didAddDevice_moreComing_(self, browser, device, more_coming):
        print(f"Device added: {device.name()}")
        self.devices.append(device)

    def deviceBrowser_didRemoveDevice_moreGoing_(self, browser, device, more_going):
        print(f"Device removed: {device.name()}")
        self.devices.remove(device)

delegate = DeviceBrowserDelegate.alloc().init()
device_browser = ICDeviceBrowser.alloc().init()
device_browser.setDelegate_(delegate)
device_browser.start()

# Keep the script running to allow detection
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping device browser...")
    device_browser.stop()
