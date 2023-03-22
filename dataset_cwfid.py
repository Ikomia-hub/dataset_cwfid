from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits PyDataProcess.CPluginProcessInterface from Ikomia API
# --------------------
class IkomiaPlugin(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def get_process_factory(self):
        from dataset_cwfid.dataset_cwfid_process import DatasetCwfidFactory
        # Instantiate process object
        return DatasetCwfidFactory()

    def get_widget_factory(self):
        from dataset_cwfid.dataset_cwfid_widget import DatasetCwfidWidgetFactory
        # Instantiate associated widget object
        return DatasetCwfidWidgetFactory()
