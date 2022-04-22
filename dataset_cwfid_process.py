import copy
from ikomia import core, dataprocess
from ikomia.dnn import dataset, datasetio
from dataset_cwfid.load_cwfid_dataset import load_cwfid_dataset


# --------------------
# - Class to handle the process parameters
# - Inherits PyCore.CProtocolTaskParam from Ikomia API
# --------------------
class DatasetCwfidParam(core.CWorkflowTaskParam):

    def __init__(self):
        core.CWorkflowTaskParam.__init__(self)
        # Place default value initialization here
        # Example : self.windowSize = 25
        self.image_folder = ""

    def setParamMap(self, param_map):
        # Set parameters values from Ikomia application
        # Parameters values are stored as string and accessible like a python dict
        # Example : self.windowSize = int(paramMap["windowSize"])
        self.image_folder = param_map["image_folder"]

    def getParamMap(self):
        # Send parameters values to Ikomia application
        # Create the specific dict structure (string container)
        param_map = core.ParamMap()
        # Example : paramMap["windowSize"] = str(self.windowSize)
        param_map["image_folder"]=self.image_folder
        return param_map


# --------------------
# - Class which implements the process
# - Inherits PyCore.CProtocolTask or derived from Ikomia API
# --------------------
class DatasetCwfid(core.CWorkflowTask):

    def __init__(self, name, param):
        core.CWorkflowTask.__init__(self, name)
        # Add input/output of the process here
        # Example :  self.addInput(PyDataProcess.CImageProcessIO())
        #           self.addOutput(PyDataProcess.CImageProcessIO())
        self.addOutput(datasetio.IkDatasetIO("other"))
        self.addOutput(dataprocess.CNumericIO())

        # Create parameters class
        if param is None:
            self.setParam(DatasetCwfidParam())
        else:
            self.setParam(copy.deepcopy(param))

    def getProgressSteps(self):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        return 1

    def run(self):
        # Core function of your process
        # Call beginTaskRun for initialization
        self.beginTaskRun()

        # Get parameters :
        param = self.getParam()

        # Get dataset output :
        output = self.getOutput(0)
        output.data = load_cwfid_dataset(param.image_folder)
        output.has_bckgnd_class = True

        # Class labels output
        numeric_out = self.getOutput(1)
        numeric_out.clearData()
        numeric_out.setOutputType(dataprocess.NumericOutputType.TABLE)

        class_ids = []
        for i in range(len(output.data["metadata"]["category_names"])):
            class_ids.append(i)
        numeric_out.addValueList(class_ids, "Id", list(output.data["metadata"]["category_names"].values()))

        # Step progress bar:
        self.emitStepProgress()

        # Call endTaskRun to finalize process
        self.endTaskRun()


# --------------------
# - Factory class to build process object
# - Inherits PyDataProcess.CProcessFactory from Ikomia API
# --------------------
class DatasetCwfidFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # Set process information as string here
        self.info.name = "dataset_cwfid"
        self.info.shortDescription = "Load Crop/Weed Field Image Dataset (CWFID) for semantic segmentation"
        self.info.description = "Load Crop/Weed Field Image Dataset (CWFID) for semantic segmentation." \
                                "This dataset comprises field images, vegetation segmentation masks and " \
                                "crop/weed plant type annotations. The paper provides details, " \
                                "e.g. on the field setting, acquisition conditions, image and ground truth data format."
        self.info.authors = "Sebastian Haug, Jörn Ostermann"
        self.info.article = "A Crop/Weed Field Image Dataset for the Evaluation of Computer Vision Based Precision " \
                            "Agriculture Tasks"
        self.info.journal = "ECCV"
        self.info.year = 2014
        # URL of documentation
        self.info.documentationLink = "https://github.com/cwfid/dataset"
        # relative path -> as displayed in Ikomia application process tree
        self.info.path = "Plugins/Python/Dataset"
        self.info.version = "1.1.0"
        self.info.iconPath = "icons/cwfid.png"
        self.info.license = "MIT License"
        # Code source repository
        self.info.repository = "https://github.com/Ikomia-dev/CWFID_Dataset"
        # Keywords used for search
        self.info.keywords = "crop,weed,segmentation,dataset,agriculture"

    def create(self, param=None):
        # Create process object
        return DatasetCwfid(self.info.name, param)
