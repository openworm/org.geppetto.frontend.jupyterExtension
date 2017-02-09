import logging
from collections import defaultdict
import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Float, Dict)

from IPython.core.debugger import Tracer

# Current variables
record_variables = defaultdict(list)
current_project = None
current_experiment = None
current_model = None
current_python_model = None
events_controller = None
# gui_controller = defaultdict(list)


class EventsSync(widgets.Widget):
    _model_name = Unicode('EventsSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)
    _events = {
        'Select': 'experiment:selection_changed'
    }
    _eventsCallbacks = {}

    def __init__(self, **kwargs):
        super(EventsSync, self).__init__(**kwargs)

        self.on_msg(self._handle_event)

    def _handle_event(self, _, content, buffers):
        if content.get('event', '') == self._events['Select']:
            logging.debug("Event triggered")
            for callback in self._eventsCallbacks[self._events['Select']]:
                try:
                    callback(content.get('data', ''),
                             content.get('geometryIdentifier', ''),
                             content.get('point', ''))
                except Exception as e:
                    logging.exception( "Unexpected error executing callback on event triggered:")
                    raise

    def register_to_event(self, events, callback):
        for event in events:
            if event not in self._eventsCallbacks:
                self._eventsCallbacks[event] = []
            self._eventsCallbacks[event].append(callback)
            logging.debug("Registring event " + str(event) +
                          " with callback " + str(callback))

    def unregister_to_event(self, events, callback):
        for event in events:
            self._eventsCallbacks[event].remove(callback)
            logging.debug("Unregistring event " + str(event) +
                          " with callback " + str(callback))


class ExperimentSync(widgets.Widget):
    _model_name = Unicode('ExperimentSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    name = Unicode('').tag(sync=True)
    id = Unicode('').tag(sync=True)
    lastModified = Unicode('').tag(sync=True)
    status = Unicode('').tag(sync=True)

    def __init__(self, **kwargs):
        super(ExperimentSync, self).__init__(**kwargs)


class ProjectSync(widgets.Widget):
    _model_name = Unicode('ProjectSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    experiments = List(Instance(ExperimentSync)).tag(
        sync=True, **widgets.widget_serialization)

    def __init__(self, **kwargs):
        super(ProjectSync, self).__init__(**kwargs)

    def addExperiment(self, experiment):
        self.experiments = [i for i in self.experiments] + [experiment]


class StateVariableSync(widgets.Widget):
    _model_name = Unicode('StateVariableSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    units = Unicode('').tag(sync=True)
    timeSeries = List(Float).tag(sync=True)

    python_variable = None

    def __init__(self, **kwargs):
        super(StateVariableSync, self).__init__(**kwargs)

        # Add it to the syncvalues
        if 'python_variable' in kwargs and kwargs["python_variable"] is not None:
            record_variables[kwargs["python_variable"]["record_variable"]] = self

class DerivedStateVariableSync(widgets.Widget):
    _model_name = Unicode('DerivedStateVariableSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    units = Unicode('').tag(sync=True)
    inputs = List(Unicode).tag(sync=True)
    timeSeries = List(Float).tag(sync=True)
    normalizationFunction = Unicode('').tag(sync=True)

    inputs_raw = []

    def __init__(self, **kwargs):
        super(DerivedStateVariableSync, self).__init__(**kwargs)

        if self.inputs_raw != None and len(self.inputs_raw) > 0:
            self.inputs = [input_raw.id for input_raw in self.inputs_raw]


class GeometrySync():
    id = ''
    name = ''

    bottomRadius = -1
    topRadius = -1
    positionX = -1
    positionY = -1
    positionZ = -1
    distalX = -1
    distalY = -1
    distalZ = -1

    python_variable = None

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')

        self.bottomRadius = kwargs.get('bottomRadius')
        self.topRadius = kwargs.get('topRadius')
        self.positionX = kwargs.get('positionX')
        self.positionY = kwargs.get('positionY')
        self.positionZ = kwargs.get('positionZ')
        self.distalX = kwargs.get('distalX')
        self.distalY = kwargs.get('distalY')
        self.distalZ = kwargs.get('distalZ')

        self.python_variable = kwargs.get('python_variable')

    def get_geometry_dict(self):
        return {'id': self.id,
                'name': self.name,
                'bottomRadius': self.bottomRadius,
                'positionX': self.positionX,
                'positionY': self.positionY,
                'positionZ': self.positionZ,
                'topRadius': self.topRadius,
                'distalX': self.distalX,
                'distalY': self.distalY,
                'distalZ': self.distalZ,
                'sectionName': self.python_variable["section"].hname()
               }
    def __str__(self):
        return "Geometry Sync => " + "Id: " + self.id + ", Name: " + self.name + ", Bottom Radius: " + str(self.bottomRadius) + ", Position X: " + str(self.positionX) + ", Position Y: " + str(self.positionY) + ", Position Z: " + str(self.positionZ) + ", Top Radius: " + str(self.topRadius) + ", Distal X: " + str(self.distalX) + ", Distal Y: " + str(self.distalY) + ", Distal Z: " + str(self.distalZ)


class ModelSync(widgets.Widget):
    _model_name = Unicode('ModelSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    stateVariables = List(Instance(StateVariableSync)).tag(
        sync=True, **widgets.widget_serialization)
    # stateVariables2Geometry = Dict().tag(
    #     sync=True)
    geometries = List(Dict).tag(
        sync=True)
    geometries_raw = []
    derived_state_variables = List(Instance(DerivedStateVariableSync)).tag(
        sync=True, **widgets.widget_serialization)

    def __init__(self, **kwargs):
        super(ModelSync, self).__init__(**kwargs)

    def addStateVariable(self, stateVariable):
        self.stateVariables = [
            i for i in self.stateVariables] + [stateVariable]
        # self.stateVariables2Geometry[stateVariable.id] = stateVariable["python_variable"]["segment"]

        # segment = stateVariable["python_variable"]["segment"]
        # segment.x
        # section = stateVariable["python_variable"]["segment"].parent()
        # section.nseg
        # var geometries = []
        # neuron_utils.secs



    def addDerivedStateVariable(self, derived_state_variable):
        self.derived_state_variables = [
            i for i in self.derived_state_variables] + [derived_state_variable]
        logging.debug("derived")            
        logging.debug(self.derived_state_variables)            

    def addGeometries(self, geometries):
        self.geometries_raw = [i for i in self.geometries_raw] + geometries
        self.geometries = [i for i in self.geometries] + [i.get_geometry_dict() for i in geometries]

    def sync(self, hard_reload = False):
        self.send({"type": "load", "hard_reload": hard_reload})

    def draw(self,x,y,z,radius):
        self.send({"type": "draw_sphere", "content": {"x":x,"y":y,"z":z,"radius":radius}})

    def highlight_visual_group_element(self, visual_group_element):
        self.send({"type": "highlight_visual_group_element", 'visual_group_element': visual_group_element})