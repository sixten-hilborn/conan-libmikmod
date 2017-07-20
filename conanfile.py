from conans import ConanFile, ConfigureEnvironment, CMake
from conans.tools import download, unzip, replace_in_file
import os

class LibmikmodConan(ConanFile):
    name = "libmikmod"
    version = "3.3.11.1"
    description = ""
    folder = "libmikmod-%s" % version
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = (
        'shared=True',
        'fPIC=True'
    )
    generators = "cmake"
    url = "https://github.com/sixten-hilborn/conan-libmikmod"
    license = "LGPL - http://www.gnu.org/copyleft/lesser.html"


    def source(self):
        zip_name = "%s.tar.gz" % self.folder
        download("https://sourceforge.net/projects/mikmod/files/{0}/{1}/{2}/download".format(self.name, self.version, zip_name), zip_name)
        unzip(zip_name)
        os.unlink(zip_name)
        replace_in_file("%s/CMakeLists.txt" % self.folder, 'PROJECT(libmikmod C)', '''PROJECT(libmikmod C)
include(../conanbuildinfo.cmake)
conan_basic_setup()
''')

    def build(self):
        cmake = CMake(self)
        defs = {
            'CMAKE_INSTALL_PREFIX': os.path.join(self.conanfile_directory, 'install'),
            'CMAKE_POSITION_INDEPENDENT_CODE': self.options.fPIC,
            'ENABLE_DOC': False
        }
        src = os.path.join(self.conanfile_directory, self.folder)
        cmake.configure(build_dir='build', source_dir=src, defs=defs)
        cmake.build(target='install')

    def package(self):
        """ Define your conan structure: headers, libs and data. After building your
            project, this method is called to create a defined structure:
        """
        folder = 'install'
        self.copy(pattern="*.h", dst="include", src=folder, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=folder, keep_path=False)
        self.copy(pattern="*.dll*", dst="bin", src=folder, keep_path=False)
        self.copy(pattern="*.a", dst="lib", src=folder, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=folder, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=folder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["mikmod"]
