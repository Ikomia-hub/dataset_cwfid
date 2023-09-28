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

    def set_values(self, param_map):
        # Set parameters values from Ikomia application
        # Parameters values are stored as string and accessible like a python dict
        # Example : self.windowSize = int(paramMap["windowSize"])
        self.image_folder = param_map["image_folder"]

    def get_values(self):
        # Send parameters values to Ikomia application
        # Create the specific dict structure (string container)
        param_map = {}
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
        # Example :  self.add_input(PyDataProcess.CImageProcessIO())
        #           self.add_output(PyDataProcess.CImageProcessIO())
        self.add_output(datasetio.IkDatasetIO("other"))
        self.add_output(dataprocess.CNumericIO())

        # Create parameters class
        if param is None:
            self.set_param_object(DatasetCwfidParam())
        else:
            self.set_param_object(copy.deepcopy(param))

    def get_progress_steps(self):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        return 1

    def run(self):
        # Core function of your process
        # Call begin_task_run for initialization
        self.begin_task_run()

        # Get parameters :
        param = self.get_param_object()

        # Get dataset output :
        output = self.get_output(0)
        output.data = load_cwfid_dataset(param.image_folder)
        output.has_bckgnd_class = True

        # Class labels output
        numeric_out = self.get_output(1)
        numeric_out.clear_data()
        numeric_out.set_output_type(dataprocess.NumericOutputType.TABLE)

        class_ids = []
        for i in range(len(output.data["metadata"]["category_names"])):
            class_ids.append(i)
        numeric_out.add_value_list(class_ids, "Id", list(output.data["metadata"]["category_names"].values()))

        # Step progress bar:
        self.emit_step_progress()

        # Call end_task_run to finalize process
        self.end_task_run()


# --------------------
# - Factory class to build process object
# - Inherits PyDataProcess.CProcessFactory from Ikomia API
# --------------------
class DatasetCwfidFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # Set process information as string here
        self.info.name = "dataset_cwfid"
        self.info.short_description = "Load Crop/Weed Field Image Dataset (CWFID) for semantic segmentation"
        self.info.authors = "Sebastian Haug, Jörn Ostermann"
        self.info.article = "A Crop/Weed Field Image Dataset for the Evaluation of Computer Vision Based Precision " \
                            "Agriculture Tasks"
        self.info.journal = "ECCV"
        self.info.year = 2014
        # URL of documentation
        self.info.documentation_link = "https://github.com/cwfid/dataset"
        # relative path -> as displayed in Ikomia application process tree
        self.info.path = "Plugins/Python/Dataset"
        self.info.version = "1.2.1"
        self.info.icon_path = "icons/cwfid.png"
        self.info.license = "MIT License"
        # Code source repository
        self.info.repository = "https://github.com/Ikomia-hub/dataset_cwfid"
        self.info.original_repository = "https://github.com/cwfid/dataset"
        # Keywords used for search
        self.info.keywords = "crop,weed,segmentation,dataset,agriculture"

    def create(self, param=None):
        # Create process object
        return DatasetCwfid(self.info.name, param)
