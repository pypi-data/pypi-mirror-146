
import os
import sys

# Initialize the runtime path
_runtimePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
if os.path.exists(os.path.join(_runtimePath, "_PyAnyCAD.pyd")) == False:
    print("Failed to find AnyCAD Runtime!")
    sys.exit(1)
    
sys.path.append(os.path.dirname(__file__))
sys.path.append(_runtimePath)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "x64")))

import PyAnyCAD as AnyCAD

class PyWindow3D:

    def __init__(self, viewer):
        self.viewer = viewer

    def RequestUpdate(self, flag):
        self.viewer.GetContext().RequestUpdate(flag)

    def ShowSceneNode(self, node):
        self.viewer.GetContext().GetScene().AddNode(node)

    def ShowTopoShape(self, shape, material):
        node = AnyCAD.BrepSceneNode.Create(shape, material, None, 0.1)
        self.ShowSceneNode(node)
    def GetViewer(self):
        return self.viewer
    def Run(self):
        self.viewer.Run(None);
    def Destroy(self):
        self.viewer.Destroy();

class GlobalInstance():
    def __init__(self):
        AnyCAD.Application.Instance().Initialize(_runtimePath)
        self.window = None

    def CreateWindow(self, width, height):
        window = AnyCAD.Application.Instance().CreateWindow3D("AnyCAD for Python", width, height, True)
        if window == None:
            return None
        self.window = PyWindow3D(window)
        return self.window

    def Destroy(self):
        self.window.Destroy()
        self.window = None
        AnyCAD.Application.Instance().Destroy()

