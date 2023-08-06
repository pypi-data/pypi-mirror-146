"""
   Copyright 2015 University of Auckland

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
import os

from opencmiss.zinc.streamregion import StreaminformationRegion
from opencmiss.argon.argonerror import ArgonError


def fileNameToRelativePath(fileName, basePath):
    if (basePath is None) or (not os.path.isabs(fileName)) or (os.path.commonprefix([fileName, basePath]) == ""):
        return fileName
    return os.path.relpath(fileName, basePath)


class ArgonModelSourceFile(object):

    def __init__(self, fileName=None, dictInput=None):
        self._time = None
        self._format = None
        self._edit = False
        self._region_name = None
        self._loaded = False
        if fileName is not None:
            self._fileName = fileName
        else:
            self._deserialize(dictInput)

    def getType(self):
        return "FILE"

    def addToZincStreaminformationRegion(self, streamInfo):
        if self._edit:
            return
        if not self._fileName:
            self._edit = True
            return
        resource = streamInfo.createStreamresourceFile(self._fileName)
        self._loaded = True
        if self._time is not None:
            time = self._time
            if not isinstance(self._time, float):
                time = float(self._time)
            streamInfo.setResourceAttributeReal(resource, StreaminformationRegion.ATTRIBUTE_TIME, time)
        # if self._format is not None:
        #    if format == "EX":
        #        #can't set per-resource file format
        #        #streamInfo.setResourceFileFormat(resource, StreaminformationRegion.FILE_FORMAT_EX)

    def unloaded(self):
        self._loaded = False

    def getFileName(self):
        return self._fileName

    def setFileName(self, fileName):
        self._fileName = fileName

    def getRegionName(self):
        return self._region_name

    def setRegionName(self, region_name):
        self._region_name = region_name

    def getTime(self):
        return self._time

    def setTime(self, time):
        self._time = time

    def getDisplayName(self):
        editText = "[To Apply] " if self._edit else ""
        if self._time is None:
            timeText = ""
        else:
            timeText = ", time " + repr(self._time)
        displayFileName = os.path.basename(self._fileName)
        return editText + "File " + displayFileName + timeText

    def isLoaded(self):
        return self._loaded

    def isEdit(self):
        return self._edit

    def setEdit(self, edit):
        self._edit = edit

    def _deserialize(self, dictInput):
        # convert to absolute file path so can save Neon file to new location and get correct relative path
        self._fileName = os.path.abspath(dictInput["FileName"])
        if "Time" in dictInput:
            self._time = dictInput["Time"]
        if "Format" in dictInput:
            self._format = dictInput["Format"]
        if "Edit" in dictInput:
            self._edit = dictInput["Edit"]
        if "RegionName" in dictInput:
            self._region_name = dictInput["RegionName"]

    def serialize(self, basePath=None):
        dictOutput = {}
        dictOutput["Type"] = self.getType()
        dictOutput["FileName"] = fileNameToRelativePath(self._fileName, basePath)
        if self._region_name is not None:
            dictOutput["RegionName"] = self._region_name
        if self._time is not None:
            dictOutput["Time"] = self._time
        if self._edit:
            dictOutput["Edit"] = True
        return dictOutput

def deserializeArgonModelSource(dictInput):
    """
    Factory method for creating the appropriate neon model source type from the dict serialization
    """
    if "Type" not in dictInput:
        raise ArgonError("Model source is missing Type attribute")
    modelSource = None
    typeString = dictInput["Type"]
    if typeString == "FILE":
        modelSource = ArgonModelSourceFile(dictInput=dictInput)
    else:
        raise ArgonError("Model source has unrecognised Type " + typeString)
    return modelSource
