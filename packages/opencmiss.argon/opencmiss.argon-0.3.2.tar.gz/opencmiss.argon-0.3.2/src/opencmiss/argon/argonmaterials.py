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
import json

from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.argon.argonerror import ArgonError


class ArgonMaterials(object):
    """
    Manages and serializes Zinc Materials.
    """

    def __init__(self, zincContext):
        self._zincContext = zincContext
        self._materialsmodule = zincContext.getMaterialmodule()

    def getZincContext(self):
        return self._zincContext

    def deserialize(self, dictInput):
        materialsDescription = json.dumps(dictInput)
        result = self._materialsmodule.readDescription(materialsDescription)
        if result != ZINC_OK:
            raise ArgonError("Failed to read materials")

    def serialize(self):
        materialsDescription = self._materialsmodule.writeDescription()
        dictOutput = json.loads(materialsDescription)
        return dictOutput
