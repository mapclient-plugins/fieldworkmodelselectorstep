'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
import json

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint

from mapclientplugins.fieldworkmodelselectorstep.widgets.configuredialog import ConfigureDialog
from mapclientplugins.fieldworkmodelselectorstep.fieldworkmodelselectordata import StepState


class FieldworkModelSelectorStep(WorkflowStepMountPoint):
    '''
    Select a fieldwork model from a dictionary of models.
    '''

    def __init__(self, location):
        super(FieldworkModelSelectorStep, self).__init__('Fieldwork Model Selector', location)
        self._category = 'Fieldwork'
        self._state = StepState()
        # self._icon = QtGui.QImage(':/zincmodelsource/images/zinc_model_icon.png')   # change this
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmodeldict'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'ju#fieldworkmodel'))
        self.model = None
        self.modelDict = None

    def configure(self):
        d = ConfigureDialog(self._state, self._main_window)
        d.setModal(True)
        if d.exec_():
            self._state = d.getState()
            # self.serialize()

        self._configured = d.validate()
        if self._configured and self._configuredObserver:
            self._configuredObserver()

    def getIdentifier(self):
        return self._state._identifier

    def setIdentifier(self, identifier):
        self._state._identifier = identifier

    def serialize(self):
        '''
        Add code to serialize this step to disk. Returns a json string for
        mapclient to serialise.
        '''
        config = {'identifier': self._state._identifier,
                  'modelName': self._state._modelName,
                  }
        return json.dumps(config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        '''
        Add code to deserialize this step from disk. Parses a json string
        given by mapclient
        '''
        config = json.loads(string)
        self._state._identifier = config['identifier']
        self._state._modelName = config['modelName']

        d = ConfigureDialog(self._state)
        self._configured = d.validate()

    def setPortData(self, index, dataIn):
        # if not isinstance(dataIn, dict):
        # raise TypeError, 'FieldworkModelSelectorStep expects a dictionary as input'

        print(dataIn)
        self.modelDict = dataIn

    def execute(self):
        self.model = self.modelDict[self._state._modelName]
        self._doneExecution()

    def getPortData(self, index):
        return self.model
