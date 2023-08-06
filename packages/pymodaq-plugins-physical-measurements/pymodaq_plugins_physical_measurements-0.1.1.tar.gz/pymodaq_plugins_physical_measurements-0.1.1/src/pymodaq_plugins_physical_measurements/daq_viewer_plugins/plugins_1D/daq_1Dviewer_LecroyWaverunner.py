from qtpy.QtCore import Signal, QThread
from qtpy import QtWidgets
import numpy as np
import time
from easydict import EasyDict as edict
from pymodaq.daq_utils.daq_utils import ThreadCommand, getLineInfo, DataFromPlugins, Axis
from pymodaq.daq_viewer.utility_classes import DAQ_Viewer_base, comon_parameters
from pyvisa import ResourceManager
# Import the pywin32 library, this library allow the control of other applications.
# Used here for LeCroy.ActiveDSOCtrl.1
# The methods of ActiveDSO are described in the documentation Lecroy ActiveDSO Developers Guide
import win32com.client

# It seems important to initialize active_dso outside the class (???)
# If not pymodaq will not allow the initialization of the detector.
active_dso = win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")

"""
Documentation
-------------
The Lecroy documentation can be found at
    pymodaq_plugins_lecroy/hardware
Prerequisite
------------
This plugin has been designed for Lecroy Waverunner oscilloscopes (tested with
waverunner 610Zi and waverunner 9104 ).
This plugin necessarily needs a Windows operating system (tested with Windows 10).
You would need to install (at least):
    - Lecroy ActiveDSO :
    https://teledynelecroy.com/support/softwaredownload/activedso.aspx?capid=106&mid=533&smid=
    - NI-VISA :
    https://www.ni.com/fr-fr/support/downloads/drivers/download.ni-visa.html#305862
The plugin has been tested with pymodaq 3.1.2.
How to use / bugs
-----------------
The user should be aware that the program will probably freeze (and the scope will have
to be restarted) in the following cases :
    - If the user selects in pymodaq a channel that is not activated on the scope
    - If the user change some parameters of the scope (like the horizontal scale) while
        pymodaq acquisition is running.
        To prevent from this error the user should stop the pymodaq acquisition (STOP
        button in the GUI interface), then change the oscilloscope parameter of his
        choice, then rerun the acquisition. See also the comments in the grab_data
        function below.
Issues
------
If you see any misbehavior you can raise an issue on the github repository :
    https://github.com/CEMES-CNRS/pymodaq_plugins_physical_measurements/issues
"""


class DAQ_1DViewer_LecroyWaverunner(DAQ_Viewer_base):
    """
    """

    # Checking VISA ressources
    VISA_rm = ResourceManager()
    resources = list(VISA_rm.list_resources())

    params = comon_parameters + [
            {'title': 'VISA:',
             'name': 'VISA_ressources',
             'type': 'list',
             'limits': resources},
            {'title': 'Channels:',
             'name': 'channels',
             'type': 'itemselect',
             'value': dict(all_items=[
                 "C1", "C2", "C3", "C4", "F1", "F2", "F3", "F4"], selected=["C1"])},
        ]

    def __init__(self, parent=None, params_state=None):
        super().__init__(parent, params_state)

        self.controller = None
        self.x_axis = None
        self.number_of_segments = None
        self.sample_mode = None

    def commit_settings(self, param):
        """
        """

    def ini_detector(self, controller=None):
        """Detector communication initialization
        Parameters
        ----------
        controller: (object) custom object of a PyMoDAQ plugin (Slave case). None if
            only one detector by controller (Master case)
        Returns
        -------
        self.status (edict): with initialization status: three fields:
            * info (str)
            * controller (object) initialized controller
            *initialized: (bool): False if initialization failed otherwise True
        """

        try:
            self.status.update(edict(
                initialized=False, info="", x_axis=None, y_axis=None, controller=None))
            if self.settings.child('controller_status').value() == "Slave":
                if controller is None:
                    raise Exception('no controller has been defined externally while'
                                    'this detector is a slave one')
                else:
                    self.controller = controller
            else:
                self.controller = active_dso
                usb_address = "USBTMC:" + self.settings.child('VISA_ressources').value()
                self.controller.MakeConnection(usb_address)
                # set the timeout of the scope to 10 seconds
                # may be not needed
                self.controller.setTimeout(10)

            channel = self.settings.child('channels').value()['selected']
            waveform = self.controller.GetScaledWaveformWithTimes(channel[0], 1e8, 0)
            data_x_axis = np.array(waveform[0])
            self.x_axis = Axis(data=data_x_axis, label="time", units="s")
            self.emit_x_axis()

            self.controller.WriteString(
                r"""vbs? 'return=app.acquisition.horizontal.numsegments' """,
                1)
            self.number_of_segments = self.controller.ReadString(8)

            self.controller.WriteString(
                r"""vbs? 'return=app.acquisition.horizontal.samplemode' """, 1)
            self.sample_mode = self.controller.ReadString(8)

            self.status.info = "Whatever info you want to log"
            self.status.initialized = True
            self.status.controller = self.controller
            return self.status

        except Exception as e:
            self.emit_status(ThreadCommand(
                'Update_Status', [getLineInfo() + str(e), 'log']))
            self.status.info = getLineInfo() + str(e)
            self.status.initialized = False
            return self.status

    def close(self):
        """
        Terminate the communication protocol
        """
        self.controller.Disconnect()

    def grab_data(self, Naverage=1, **kwargs):
        """
        Start a new acquisition.
        Grab the current values.
        Send the
        Parameters
        ----------
        Naverage: (int) Number of hardware averaging
        kwargs: (dict) of others optionals arguments
        """

        # The following seems to be important to refresh the scope buffer.
        # Otherwise a long scan will crash the daq_scan.
        self.controller.DeviceClear(False)
        QtWidgets.QApplication.processEvents()
        QThread.msleep(100)
        QtWidgets.QApplication.processEvents()

        channel = self.settings.child('channels').value()['selected']
        waveform = self.controller.GetScaledWaveformWithTimes(
            channel[0], 1e8, 0)

        if self.sample_mode == "Sequence":
            while True:
                self.controller.WriteString(
                    r"""vbs? 'return=app.acquisition.horizontal.acquiredsegments' """,
                    1)
                acquired_segments = self.controller.ReadString(8)
                if acquired_segments == self.number_of_segments:
                    break

                time.sleep(0.01)
        else:
            pass

        # The ErrorFlag property checks that there is no error concerning ActiveDSO.
        # If the user changes some parameters on the oscilloscope (for example the
        # horizontal scale) while pymodaq acquisition is running, it will raise this
        # error. We do not know how to deal with this problem.
        # If the error is raised you will probably have to restart the oscilloscope to
        # get the communication back.
        # Restarting can be done with a little script using the DeviceClear(True) method
        # of ActiveDSO. It is much faster than doing it manually.
        #
        # To prevent the error, the user should use the STOP button on pymodaq GUI, then
        # change the parameter of his choice on the oscilloscope and then RUN pymodaq
        # acquisition.
        if self.controller.ErrorFlag:
            raise Exception(self.controller.ErrorString)

        data = [np.array(waveform[1])]

        self.data_grabed_signal.emit([DataFromPlugins(
            name='Lecroy Waverunner',
            data=data,
            type='Data1D',
            labels=["", ""]
        )])

    def callback(self):
        """optional asynchrone method called when the detector has finished its
        acquisition of data
        """

    def stop(self):

        return ''