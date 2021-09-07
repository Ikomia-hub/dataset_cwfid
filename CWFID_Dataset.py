from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits PyDataProcess.CPluginProcessInterface from Ikomia API
# --------------------
class CWFID_Dataset(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        from CWFID_Dataset.CWFID_Dataset_process import CWFID_DatasetProcessFactory
        # Instantiate process object
        return CWFID_DatasetProcessFactory()

    def getWidgetFactory(self):
        from CWFID_Dataset.CWFID_Dataset_widget import CWFID_DatasetWidgetFactory
        # Instantiate associated widget object
        return CWFID_DatasetWidgetFactory()
