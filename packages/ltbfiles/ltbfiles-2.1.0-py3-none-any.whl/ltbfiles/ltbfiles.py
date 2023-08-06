"""
This module contains functions designed for reading file formats used by LTB spectrometers.

LICENSE
  Copyright (C) 2022 Dr. Sven Merk

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
    
  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
import tempfile
import zipfile
import os
import numpy as np
import struct
import configparser
import json


def _load_file(filename: str):
    _,ext = os.path.splitext(filename)
    if ".ary" == ext.lower():
        return read_ltb_ary(filename)
    elif  ".aryx" == ext.lower():
        return read_ltb_aryx(filename)
    else:
        raise Exception(f"{ext} is not a supported file type")


def load_files(filelist: list[str]) -> tuple[np.array, np.array, list[dict]]:
    assert len(filelist) > 0, "At least one file must be passed"
    y, wl, _, h = _load_file(filelist[0])
    Y = np.full((len(y), len(filelist)), np.nan)
    Y[:,0] = y
    head = [h]
    if len(filelist) > 1:
        for i,file in enumerate(filelist[1:], start=1):
            y,x,_,h = _load_file(file)
            assert np.all(x == wl), "Can only merge spectra with identical wavelength axis"
            Y[:,i] = y
            head.append(h)
    return Y, wl, head


def read_ltb_ary(filename: str, sort_wl: bool=True) -> tuple[np.array, np.array, np.array, dict]:
    """
    This function reads data from binary *.ary files for LTB spectrometers.
     
    Syntax
    ------
        >>> y,x,o,head = read_ltb_ary(filename, sort_wl)
    
    Inputs
    ------
       filename : str
           Name of the *.ary file to be read. May be a relative path or full filename.               
       sortWL : bool
           OPTIONAL flag, if spectra should be sorted by their wavelength after reading. default: true
    Outputs
    -------
       x : float array
           Wavelengths    
       o : float array
           Spectral order of the current pixel    
       y : float array
           Intensity    
       head : dict
           additional file header (list)
    
    Caution! Due to order overlap, it may happen that two pixels have the
    same wavelength. If this causes problems in later data treatment, such
    pixels should be removed using 
    
        >>> x, ind = numpy.unique(x, True)
        >>> o=o[ind]
        >>> y=y[ind]
    """
    x = None
    y = None
    sort_order = None
    order_info = None
    head = {'filename': filename}
    with tempfile.TemporaryDirectory(prefix='ary_') as extract_folder:
        with zipfile.ZipFile(filename) as zf:
            file_list = zf.namelist()
            zf.extractall(extract_folder)

        for iFile in file_list:

            if iFile.endswith('~tmp'):
                spec_file_full = os.path.join(extract_folder, iFile)
                with open(spec_file_full, 'rb') as sf:
                    dt = np.dtype([('int', np.float32), ('wl', np.float32)])
                    values = np.fromfile(sf, dtype=dt)
                if sort_wl:
                    sort_order = np.argsort(values['wl'])
                    x = values['wl'][sort_order]
                    y = values['int'][sort_order]
                else:
                    sort_order = np.arange(0, len(values['wl']))
                    x = values['wl']
                    y = values['int']

            elif iFile.endswith('~aif'):
                add_file_full = os.path.join(extract_folder, iFile)
                with open(add_file_full, 'rb') as af:
                    dt = np.dtype([('indLow', np.int32),
                                   ('indHigh', np.int32),
                                   ('order', np.int16),
                                   ('lowPix', np.int16),
                                   ('highPix', np.int16),
                                   ('foo', np.int16),
                                   ('lowWave', np.float32),
                                   ('highWave', np.float32)])
                    order_info = np.fromfile(af, dt)

            elif iFile.endswith('~rep'):
                rep_file_full = os.path.join(extract_folder, iFile)
                with open(rep_file_full, 'r') as rf:
                    for iLine in rf:
                        stripped_line = str.strip(iLine)
                        if '[end of file]' == str.strip(stripped_line):
                            break
                        new_entry = stripped_line.split('=')
                        head[new_entry[0].replace(' ', '_')] = new_entry[1]

        if (sort_order is not None) and (order_info is not None):
            o = np.empty(len(x))
            o[:] = np.NAN
            for iCurrOrder in order_info:
                o[iCurrOrder['indLow']:iCurrOrder['indHigh'] + 1] = iCurrOrder['order']
            o = o[sort_order]
        else:
            o = np.ones(len(x))

    return y, x, o, head


def read_ltb_aryx(filename: str, sort_wl:bool=True) -> tuple[np.array, np.array, np.array, dict]:
    """
    This function reads data from binary *.aryx files for LTB spectrometers.
     
    Syntax
    ------
        >>> y,x,o,head = read_ltb_aryx(filename, sort_wl)
    
    Inputs
    ------
       filename : str
           Name of the *.aryx file to be read. May be a relative path or full filename.               
       sortWL : bool
           OPTIONAL flag, if spectra should be sorted by their wavelength after reading. default: true
    Outputs
    -------
       x : float array
           Wavelengths    
       o : float array
           Spectral order of the current pixel    
       y : float array
           Intensity    
       head : dict
           additional file header (list)
    
    Caution! Due to order overlap, it may happen that two pixels have the
    same wavelength. If this causes problems in later data treatment, such
    pixels should be removed using 
    
        >>> x, ind = numpy.unique(x, True)
        >>> o=o[ind]
        >>> y=y[ind]
    """
    x = None
    y = None
    sort_order = None
    order_info = None
    head = {}
    with tempfile.TemporaryDirectory(prefix='aryx_') as extract_folder:
        with zipfile.ZipFile(filename) as zf:
            file_list = zf.namelist()
            zf.extractall(extract_folder)

        for iFile in file_list:

            if iFile.endswith('~tmp'):
                spec_file_full = os.path.join(extract_folder, iFile)
                with open(spec_file_full, 'rb') as sf:
                    dt = np.dtype([('int', np.double), ('wl', np.double)])
                    values = np.fromfile(sf, dtype=dt)
                if sort_wl:
                    sort_order = np.argsort(values['wl'])
                    x = values['wl'][sort_order]
                    y = values['int'][sort_order]
                else:
                    sort_order = np.arange(0, len(values['wl']))
                    x = values['wl']
                    y = values['int']

            elif iFile.endswith('~aif'):
                add_file_full = os.path.join(extract_folder, iFile)
                with open(add_file_full, 'rb') as af:
                    dt = np.dtype([('indLow', np.int32),
                                   ('indHigh', np.int32),
                                   ('order', np.int16),
                                   ('lowPix', np.int16),
                                   ('highPix', np.int16),
                                   ('foo', np.int16),
                                   ('lowWave', np.double),
                                   ('highWave', np.double)])
                    order_info = np.fromfile(af, dt)

            elif iFile.endswith('~json'):
                rep_file_full = os.path.join(extract_folder, iFile)
                with open(rep_file_full, 'r') as rf:
                   head = json.load(rf)

        if (sort_order is not None) and (order_info is not None):
            o = np.empty(len(x))
            o[:] = np.NAN
            for iCurrOrder in order_info:
                o[iCurrOrder['indLow']:iCurrOrder['indHigh'] + 1] = iCurrOrder['order']
            o = o[sort_order]
        else:
            o = np.ones(len(x))

    head['filename'] = filename
    return y, x, o, head


def _make_header_from_array(data):
    head = {'ChipWidth': data[0],
            'ChipHeight': data[1],
            'PixelSize': data[2],
            'HorBinning': data[3],
            'VerBinning': data[4],
            'BottomOffset': data[5],
            'LeftOffset': data[6],
            'ImgHeight': data[7],
            'ImgWidth': data[8]
            }
    return head
    

def read_ltb_raw(filename: str) -> tuple[np.array, dict]:
    """
    This function reads *.raw image files created with LTB spectrometers.
    Input
    -----
    filename : str
    
    Outputs
    -------
    image : np.array of image shape
    head : dict containing image properties
    """
    data = np.loadtxt(filename)
    head = _make_header_from_array(data[0:9])
    image = np.reshape(data[9:], (head['ImgHeight'], head['ImgWidth']))
    return image, head


def read_ltb_rawb(filename: str) -> tuple[np.array, dict]:
    """
    This function reads *.rawb image files created with LTB spectrometers.
    Input
    -----
    filename : str
    
    Outputs
    -------
    image : np.array of image shape
    head : dict containtng image properties
    """
    struct_fmt = '=iidiiiiii'
    struct_len = struct.calcsize(struct_fmt)
    struct_unp = struct.Struct(struct_fmt).unpack_from
    
    with open(filename,'rb') as f:
        metadata = f.read(struct_len)       
        im_stream = np.fromfile(f, dtype=np.int32)
        s = struct_unp(metadata)
        head = _make_header_from_array(s)
        image = np.reshape(im_stream, (head['ImgHeight'], head['ImgWidth']))
    return image, head


def read_ltb_rawx(filename:str) -> tuple[np.array, dict]:
    """
    This function reads *.rawx image files created with LTB spectrometers.
    Input
    -----
    filename : str
    
    Outputs
    -------
    image : np.array of image shape
    head : dict containtng all measurement and spectrometer parameters
    """
    with tempfile.TemporaryDirectory(prefix='rawx_') as extract_folder:
        with zipfile.ZipFile(filename) as zf:
            file_list = zf.namelist()
            zf.extractall(extract_folder)
        
        image = None
        sophi_head = configparser.ConfigParser()
        aryelle_head = configparser.ConfigParser()
        for iFile in file_list:
            if iFile.endswith('rawdata'):
                img_file_full = os.path.join(extract_folder, iFile)
                image = np.loadtxt(img_file_full)
            elif iFile.lower() == 'aryelle.ini':
                aryelle_file_full = os.path.join(extract_folder, iFile)
                aryelle_head.read(aryelle_file_full)
            elif iFile.lower() == 'sophi.ini':
                sophi_file_full = os.path.join(extract_folder, iFile)
                sophi_head.read(sophi_file_full)            
        width = int(aryelle_head['CCD']['width']) // int(sophi_head['Echelle 1']['vertical binning'])
        height = int(aryelle_head['CCD']['height']) // int(sophi_head['Echelle 1']['horizontal binning'])
        head = {'sophi_ini': sophi_head,
                'aryelle_ini': aryelle_head}
        image = image.reshape((width, height))

    return image, head