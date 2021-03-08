from ikomia import dataprocess
import CWFID_Dataset_process as processMod
import CWFID_Dataset_widget as widgetMod


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits PyDataProcess.CPluginProcessInterface from Ikomia API
# --------------------
class CWFID_Dataset(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        # Instantiate process object
        return processMod.CWFID_DatasetProcessFactory()

    def getWidgetFactory(self):
        # Instantiate associated widget object
        return widgetMod.CWFID_DatasetWidgetFactory()
