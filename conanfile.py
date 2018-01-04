#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibmikmodConan(ConanFile):
    name = "libmikmod"
    version = "3.3.11.1"
    url = "https://github.com/sixten-hilborn/conan-libmikmod"
    description = "Module player and library supporting many formats, including mod, s3m, it, and xm."
    
    # Indicates License type of the packaged library
    license = "LGPL - http://www.gnu.org/copyleft/lesser.html"
    
    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]
    
    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt.patch"]
    generators = "cmake" 
    
    # Options may need to change depending on the packaged library. 
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = (
        'shared=True',
        'fPIC=True'
    )
    
    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    
    def source(self):
        extracted_dir = self.name + "-" + self.version
        tools.get("https://sourceforge.net/projects/mikmod/files/{0}/{1}/{2}.tar.gz".format(self.name, self.version, extracted_dir))

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

        tools.patch(patch_file="CMakeLists.txt.patch", base_path=self.source_subfolder)

        
    def build(self):
        cmake = CMake(self)
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.definitions['ENABLE_STATIC'] = not self.options.shared
        cmake.definitions['ENABLE_DOC'] = False
        cmake.configure(build_folder=self.build_subfolder, source_folder=self.source_subfolder)
        cmake.build()
        cmake.install()


    def package(self):
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can replace all the steps below with the word "pass"
        include_folder = os.path.join(self.source_subfolder, "include")
        self.copy(pattern="LICENSE")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
