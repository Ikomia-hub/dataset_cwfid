from ikomia import utils, core, dataprocess
from ikomia.utils import qtconversion, pyqtutils
from dataset_cwfid.dataset_cwfid_process import DatasetCwfidParam
# PyQt GUI framework
from PyQt5.QtWidgets import *


# --------------------
# - Class which implements widget associated with the process
# - Inherits PyCore.CProtocolTaskWidget from Ikomia API
# --------------------
class DatasetCwfidWidget(core.CWorkflowTaskWidget):

    def __init__(self, param, parent):
        core.CWorkflowTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = DatasetCwfidParam()
        else:
            self.parameters = param

        # Create layout : QGridLayout by default
        self.grid_layout = QGridLayout()
        # PyQt -> Qt wrapping
        layout_ptr = qtconversion.PyQtToQt(self.grid_layout)

        self.browse_img_folder = pyqtutils.append_browse_file(self.grid_layout, label="Image folder", filter="",
                                                              path=self.parameters.image_folder,
                                                              mode=QFileDialog.Directory)

        # Set widget layout
        self.setLayout(layout_ptr)

    def onApply(self):
        # Apply button clicked slot

        # Get parameters from widget
        # Example : self.parameters.windowSize = self.spinWindowSize.value()
        self.parameters.image_folder = self.browse_img_folder.path
        # Send signal to launch the process
        self.emitApply(self.parameters)


# --------------------
# - Factory class to build process widget object
# - Inherits PyDataProcess.CWidgetFactory from Ikomia API
# --------------------
class DatasetCwfidWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the name of the process -> it must be the same as the one declared in the process factory class
        self.name = "dataset_cwfid"

    def create(self, param):
        # Create widget object
        return DatasetCwfidWidget(param, None)
