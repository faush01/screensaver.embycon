import sys
import xbmcaddon
import xbmcgui
import xbmc

Addon = xbmcaddon.Addon('screensaver.embycon')

__scriptname__ = Addon.getAddonInfo('name')
__path__ = Addon.getAddonInfo('path')


class Screensaver(xbmcgui.WindowXMLDialog):
    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback):
            self.exit_callback = exit_callback

        def onScreensaverDeactivated(self):
            xbmc.log('EmbyCon.Screensaver: sending exit_callback')
            self.exit_callback()

    def onInit(self):
        xbmc.log('EmbyCon.Screensaver: onInit')
        self.monitor = self.ExitMonitor(self.exit)

    def exit(self):
        xbmc.log('EmbyCon.Screensaver: Exit requested')

        #xbmc.executebuiltin("RunScript(plugin.video.embycon,0,?mode=CHANGE_USER)")

        screen_saver_image = self.getControl(3000)
        screen_saver_image.setVisible(False)

        screen_saver_label = self.getControl(3001)
        screen_saver_label.setLabel("Closing...")

        embycon_addon = xbmcaddon.Addon("plugin.video.embycon")
        wait_on_select = embycon_addon.getSetting('changeUserOnScreenSaver') == 'true'

        loops = 0
        while wait_on_select and not xbmc.getCondVisibility("Window.IsVisible(selectdialog)") and loops < 20:
            loops = loops + 1
            xbmc.log("EmbyCon.Screensaver, waiting 500 ms for selectdialog : " + str(loops))
            xbmc.sleep(500)

        if xbmc.getCondVisibility("Window.IsVisible(selectdialog)"):
            xbmc.log("EmbyCon.Screensaver selectdialog is visible")
        else:
            xbmc.log("EmbyCon.Screensaver selectdialog did not show")

        self.close()


if __name__ == '__main__':
    xbmc.log('EmbyCon.Screensaver Started')
    screensaver_gui = Screensaver('screen_saver.xml', __path__, 'default')
    screensaver_gui.doModal()
    xbmc.log('EmbyCon.Screensaver Exited')
    del screensaver_gui
    sys.modules.clear()
