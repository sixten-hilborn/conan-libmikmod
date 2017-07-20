from conans import ConanFile, CMake
import os

############### CONFIGURE THESE VALUES ##################
default_user = "hilborn"
default_channel = "stable"
#########################################################

channel = os.getenv("CONAN_CHANNEL", default_channel)
username = os.getenv("CONAN_USERNAME", default_user)


class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "libmikmod/3.3.11.1@%s/%s" % (username, channel)

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_dir='.')
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        self.run("cd bin && .%sexample" % (os.sep))