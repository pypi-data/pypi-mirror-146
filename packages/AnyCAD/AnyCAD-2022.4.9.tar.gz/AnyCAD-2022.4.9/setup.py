# -*- coding:utf-8 -*-

from setuptools import setup, find_packages,Extension

setup(
    name = 'AnyCAD',
    version = '2022.4.9',
    keywords='AnyCAD',
    description = 'a library for 3D Graphics/Geometry Developer',
    license = 'MIT License',
    url = 'http://www.anycad.cn',
    author = 'AnyCAD',
    author_email = 'anycad@anycad.cn',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    data_files=[('.', ['AnyCAD/_PyAnyCAD.pyd',
    'AnyCAD/AnyCAD.Common.Core.dll',
    'AnyCAD/AnyCAD.Common.Glad.dll',
    'AnyCAD/AnyCAD.Common.SDL2.dll',
    'AnyCAD/AnyCAD.Common.Zip.dll',
    'AnyCAD/AnyCAD.Data.Kernel.dll',
    'AnyCAD/AnyCAD.Data.View.dll',
    'AnyCAD/AnyCAD.Geometry.Builder.dll',
    'AnyCAD/AnyCAD.Geometry.Interop.dll',
    'AnyCAD/AnyCAD.Geometry.Kernel.dll',
    'AnyCAD/AnyCAD.Graphics.Asset.dll',
    'AnyCAD/AnyCAD.Graphics.Data.dll',
    'AnyCAD/AnyCAD.Graphics.Interop.dll',
    'AnyCAD/AnyCAD.Graphics.Kernel.dll',
    'AnyCAD/AnyCAD.Graphics.Renderer.dll', 
    'AnyCAD/AnyCAD.Graphics.View.dll',
    'AnyCAD/AnyCAD.Graphics.Window.dll',
    'AnyCAD/SamCoreInterop.dll',
    'AnyCAD/SamCoreKernel.dll',
    'AnyCAD/SamCoreModeling.dll'
    ])], 
)