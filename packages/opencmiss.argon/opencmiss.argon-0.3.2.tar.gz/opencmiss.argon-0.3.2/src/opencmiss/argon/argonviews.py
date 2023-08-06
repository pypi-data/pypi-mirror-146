"""
   Copyright 2016 University of Auckland

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from opencmiss.argon.argonsceneviewer import ArgonSceneviewer

LAYOUT1 = {
    "Name": "Layout1",
    "Scenes": [
        {
            "Row": 0,
            "Col": 0,
            "Sceneviewer": {},
        }
    ]
}

LAYOUT2x2GRID = {
    "Name": "Layout2x2Grid",
    "GridSpecification": {
        "NumRows": 2,
        "NumCols": 2,
        "Left": None,
        "Bottom": None,
        "Right": None,
        "Top": None,
        "WidthSpace": None,
        "HeightSpace": None,
        "WidthRatios": None,
        "HeightRatios": None
    },
    "Scenes": [
        {
            "Row": 1,
            "Col": 1,
            "Sceneviewer": {},
        },
        {
            "Row": 0,
            "Col": 1,
            "Sceneviewer": {},
        },
        {
            "Row": 1,
            "Col": 0,
            "Sceneviewer": {},
        },
        {
            "Row": 0,
            "Col": 0,
            "Sceneviewer": {},
        }
    ]
}

LAYOUTS = [
    LAYOUT1,
    LAYOUT2x2GRID,
]


class ArgonViewManager(object):
    """
    Manages and serializes ArgonViews.
    """

    def __init__(self, zincContext):
        self._zincContext = zincContext
        self._views = []
        self._activeView = None

    def getZincContext(self):
        return self._zincContext

    def deserialize(self, d):
        self._activeView = d["ActiveView"] if "ActiveView" in d else None
        if "Children" in d:
            for i in d["Children"]:
                view = ArgonView(self._zincContext)
                view.deserialize(i)
                self._views.append(view)

    def serialize(self):
        dictOutput = {}
        if self._activeView:
            dictOutput["ActiveView"] = self._activeView
        dictOutput["Children"] = []
        if self._views:
            tmpOutput = []
            for view in self._views:
                tmpOutput.append(view.serialize())
            dictOutput["Children"] = tmpOutput
        return dictOutput

    def getActiveView(self):
        return self._activeView

    def setActiveView(self, view):
        self._activeView = view

    def getView(self, index):
        return self._views[index]

    def getViews(self):
        return self._views

    def viewCount(self):
        return len(self._views)

    def setViews(self, views):
        self._views = views

    def addViewByType(self, view_type, name=None):
        for layout in LAYOUTS:
            if layout["Name"] == view_type:
                new_view = ArgonView(self._zincContext)
                new_view.deserialize(layout)
                if name is None:
                    name = view_type
                if self._name_in_use(name):
                    name = self._next_available_name(name)
                new_view.setName(name)
                self._views.append(new_view)
                return new_view

    def removeView(self, identifier):
        del self._views[identifier]

    def _name_in_use(self, name):
        for view in self._views:
            if view.getName() == name:
                return True

        return False

    def _next_available_name(self, name_stem):
        iteration = 1
        while self._name_in_use(f"{name_stem}_{iteration}"):
            iteration += 1

        return f"{name_stem}_{iteration}"

    def updateSceneviewers(self, view_index, sceneviewers_info):
        if 0 <= view_index < len(self._views):
            view = self._views[view_index]
            for sceneviewer_info in sceneviewers_info:
                view.updateSceneviewer(sceneviewer_info["Row"], sceneviewer_info["Col"], sceneviewer_info["Sceneviewer"])


class ArgonView(object):
    """
    Defines and serializes a single view.
    """

    def __init__(self, zincContext):
        self._zincContext = zincContext
        self._name = None
        self._gridSpecification = None
        self._scenes = []

    def getZincContext(self):
        return self._zincContext

    def deserialize(self, d):
        self._name = d["Name"] if "Name" in d else None
        self._gridSpecification = d["GridSpecification"] if "GridSpecification" in d else None

        if "Scenes" in d:
            for s in d["Scenes"]:
                scene = {"Row": 0, "Col": 0}
                if "Row" in s:
                    scene["Row"] = s["Row"]
                if "Col" in s:
                    scene["Col"] = s["Col"]
                if "Sceneviewer" in s:
                    sceneviewer = ArgonSceneviewer(self._zincContext)
                    sceneviewer.deserialize(s["Sceneviewer"])
                    scene["Sceneviewer"] = sceneviewer

                self._scenes.append(scene)

    def serialize(self):
        dictOutput = {}
        if self._name:
            dictOutput["Name"] = self._name
        if self._gridSpecification:
            dictOutput["GridSpecification"] = self._gridSpecification
        dictOutput["Scenes"] = []
        if self._scenes:
            for scene in self._scenes:
                tmp_output = {
                    "Row": scene["Row"],
                    "Col": scene["Col"],
                    "Sceneviewer": scene["Sceneviewer"].serialize(),
                }
                dictOutput["Scenes"].append(tmp_output)
        return dictOutput

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getScenes(self):
        return self._scenes

    def getGridSpecification(self):
        return self._gridSpecification

    def updateSceneviewer(self, row, col, sceneviewer):
        for scene in self._scenes:
            if scene["Row"] == row and scene["Col"] == col:
                scene["Sceneviewer"].updateParameters(sceneviewer)
