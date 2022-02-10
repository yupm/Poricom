"""
Poricom
Copyright (C) `2021-2022` `<Alarcon Ace Belen>`

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from PyQt5.QtGui import QPixmap
from os.path import isfile, join, splitext, normpath, abspath, exists, dirname
from os import listdir

from default import cfg

class Tracker:
    
    def __init__(self, filename=cfg["HOME_IMAGE"]):

        self._p_image = PImage(filename)
        self._p_mask = PImage(filename)

        self._filepath = abspath(dirname(filename))
        self._write_mode = False

        self._image_list = []

        self._language = "jpn"
        self._orientation = "_vert"

        self._better_ocr = False
        self._ocr_model = None
    
    @property
    def p_image(self): 
        return self._p_image

    @p_image.setter
    def p_image(self, image):
        # TODO: use match case when 3.10 comes out
        if (type(image) is str and PImage(image).is_valid()):
            self._p_image = PImage(image)
            self._p_image.filename = abspath(image)
            self._filepath = abspath(dirname(image))

    @property
    def p_mask(self):
        return self._p_mask
    
    @p_mask.setter
    def p_mask(self, image):
        self._p_mask = image

    @property
    def filepath(self):
        return self._filepath
    
    @filepath.setter
    def filepath(self, filepath):
        self._filepath = filepath
        filelist = filter(lambda f: isfile(join(self.filepath, 
                        f)), listdir(self.filepath))
        self._image_list = list(map(lambda p: normpath(join(self.filepath, p)),
                        filter((lambda f: ('*'+splitext(f)[1]) 
                            in cfg["IMAGE_EXTENSIONS"]), filelist)))

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        self._language = language
    
    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        self._orientation = orientation

    @property
    def ocr_model(self):
        return self._ocr_model

    @ocr_model.setter
    def ocr_model(self, ocr_model):
        self._ocr_model = ocr_model

    @property
    def write_mode(self):
        return self._write_mode

    @write_mode.setter
    def write_mode(self, write_mode):
        self._write_mode = write_mode
    
    def switch_write_mode(self):
        self._write_mode = not self._write_mode
        return self._write_mode

    def switch_ocr_mode(self):
        self._better_ocr = not self._better_ocr
        return self._better_ocr

class PImage(QPixmap):

    def __init__(self, filename=None):
        super(QPixmap, self).__init__(filename)

        # Current directory + filename
        self._filename = filename
        # Current directory
        self._filepath = None

    @property
    def filename(self):
        return self._filename
    
    @filename.setter
    def filename(self, filename):
        self._filename = filename

    def is_valid(self):
        return exists(self._filename) and isfile(self._filename)
    
