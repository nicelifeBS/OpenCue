#  Copyright (c) 2018 Sony Pictures Imageworks Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from PySide2 import QtWidgets

from opencue.compiled_proto import depend_pb2
import Constants
import Logger
import Utils
from AbstractTreeWidget import AbstractTreeWidget
from AbstractWidgetItem import AbstractWidgetItem
from MenuActions import MenuActions


logger = Logger.getLogger(__file__)


class DependMonitorTree(AbstractTreeWidget):
    def __init__(self, parent, object):
        self.startColumnsForType(Constants.TYPE_DEPEND)
        self.addColumn("Type", 130, id=1,
                       data=lambda depend: depend_pb2.DependType.Name(depend.type()))
        self.addColumn("Target", 60, id=2,
                       data=lambda depend: depend_pb2.DependTarget.Name(depend.target()))
        self.addColumn("Active", 50, id=3,
                       data=lambda depend:(depend.isActive()))
#        self.addColumn("Job", 230, id=4,
#                       data=lambda depend:(depend.dependErJob()))
#        self.addColumn("Layer", 50, id=5,
#                       data=lambda depend:(depend.dependErLayer()))
#        self.addColumn("Frame", 100, id=6,
#                       data=lambda depend:(depend.dependErFrame()))
        self.addColumn("OnJob", 300, id=7,
                       data=lambda depend:(depend.dependOnJob()))
        self.addColumn("OnLayer", 200, id=8,
                       data=lambda depend:(depend.dependOnLayer()))
        self.addColumn("OnFrame", 100, id=9,
                       data=lambda depend:(depend.dependOnFrame()))

        self.rpcObject = object

        AbstractTreeWidget.__init__(self, parent)

        # Used to build right click context menus
        self.__menuActions = MenuActions(self, self.updateSoon, self.selectedObjects)

        self.setUpdateInterval(60)

    def _createItem(self, object):
        """Creates and returns the proper item"""
        return DependWidgetItem(object, self)

    def _getUpdate(self):
        """Returns the proper data from the cuebot"""
        try:
            if hasattr(self.rpcObject, "getDepends"):
                return self.rpcObject.getDepends()
            return self.rpcObject.getWhatThisDependsOn()
        except Exception as e:
            map(logger.warning, Utils.exceptionOutput(e))
            return []

    def contextMenuEvent(self, e):
        """When right clicking on an item, this raises a context menu"""

        menu = QtWidgets.QMenu()

        self.__menuActions.dependencies().addAction(menu, "satisfy")
        #self.__menuActions.dependencies().addAction(menu, "unsatisfy")

        menu.exec_(e.globalPos())

################################################################################

class DependWidgetItem(AbstractWidgetItem):
    def __init__(self, object, parent):
        AbstractWidgetItem.__init__(self, Constants.TYPE_DEPEND, object, parent)