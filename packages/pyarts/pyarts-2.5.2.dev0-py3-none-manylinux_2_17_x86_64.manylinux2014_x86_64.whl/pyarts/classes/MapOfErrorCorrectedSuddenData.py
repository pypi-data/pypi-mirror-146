import ctypes as c
from pyarts.workspace.api import arts_api as lib

from pyarts.classes.io import correct_save_arguments, correct_read_arguments
from pyarts.classes.quantum import QuantumIdentifier
from pyarts.classes.LineShapeModelParameters import LineShapeModelParameters
from pyarts.classes.BasicTypes import Numeric
from pyarts.classes.SpeciesIsotopeRecord import Species


class SpeciesErrorCorrectedSuddenData:
    """ ARTS SpeciesErrorCorrectedSuddenData data

    Properties:
        spec:
            Species
        
        scaling:
            Constant 1
        
        beta:
            Constant 2
        
        lambda_value:
            Constant 3
        
        collisional_distance:
            Constant 4
        
        mass:
            Constant 5
    """
    def __init__(self, data=None):
        if isinstance(data, c.c_void_p):
            self.__delete__ = False
            self.__data__ = data
        else:
            self.__delete__ = True
            self.__data__ = c.c_void_p(lib.createSpeciesErrorCorrectedSuddenData())
            assert data is None, "Fail initialize properly"

    def print(self):
        """ Print to cout the ARTS representation of the class """
        lib.printSpeciesErrorCorrectedSuddenData(self.__data__)

    def __del__(self):
        if self.__delete__:
            lib.deleteSpeciesErrorCorrectedSuddenData(self.__data__)

    def set(self, _):
        """ Sets this class according to another python instance of itself """
        raise RuntimeError("Cannot be set from another copy")

    def __repr__(self):
        return f"{self.spec} {self.scaling} {self.beta} {self.lambda_value} {self.collisional_distance} {self.mass}"

    def __eq__(self, other):
        return self.spec == other.spec and \
        self.a == other.a and \
        self.b == other.b and \
        self.gamma == other.gamma and \
        self.dc == other.dc and \
        self.mass == other.mass
        
    @property
    def spec(self):
        return Species(c.c_void_p(lib.getspecSpeciesErrorCorrectedSuddenData(self.__data__)))
    
    @spec.setter
    def spec(self, val):
        self.spec.set(val)
        
    @property
    def scaling(self):
        return LineShapeModelParameters(c.c_void_p(lib.getscalingSpeciesErrorCorrectedSuddenData(self.__data__)))
    
    @scaling.setter
    def scaling(self, val):
        self.scaling.set(val)
        
    @property
    def lambda_value(self):
        return LineShapeModelParameters(c.c_void_p(lib.getlambdaSpeciesErrorCorrectedSuddenData(self.__data__)))
    
    @lambda_value.setter
    def lambda_value(self, val):
        self.lambda_value.set(val)
        
    @property
    def beta(self):
        return LineShapeModelParameters(c.c_void_p(lib.getbetaSpeciesErrorCorrectedSuddenData(self.__data__)))
    
    @beta.setter
    def beta(self, val):
        self.beta.set(val)
        
    @property
    def collisional_distance(self):
        return LineShapeModelParameters(c.c_void_p(lib.getcollisional_distanceSpeciesErrorCorrectedSuddenData(self.__data__)))
    
    @collisional_distance.setter
    def collisional_distance(self, val):
        self.collisional_distance.set(val)
        
    @property
    def mass(self):
        return Numeric(c.c_void_p(lib.getmassSpeciesErrorCorrectedSuddenData(self.__data__)))
        
    @mass.setter
    def mass(self, val):
        self.mass.set(val)

lib.createSpeciesErrorCorrectedSuddenData.restype = c.c_void_p
lib.createSpeciesErrorCorrectedSuddenData.argtypes = []

lib.deleteSpeciesErrorCorrectedSuddenData.restype = None
lib.deleteSpeciesErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.printSpeciesErrorCorrectedSuddenData.restype = None
lib.printSpeciesErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.getspecSpeciesErrorCorrectedSuddenData.restype = c.c_void_p
lib.getspecSpeciesErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.getscalingSpeciesErrorCorrectedSuddenData.restype = c.c_void_p
lib.getscalingSpeciesErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.getlambdaSpeciesErrorCorrectedSuddenData.restype = c.c_void_p
lib.getlambdaSpeciesErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.getbetaSpeciesErrorCorrectedSuddenData.restype = c.c_void_p
lib.getbetaSpeciesErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.getcollisional_distanceSpeciesErrorCorrectedSuddenData.restype = c.c_void_p
lib.getcollisional_distanceSpeciesErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.getmassSpeciesErrorCorrectedSuddenData.restype = c.c_void_p
lib.getmassSpeciesErrorCorrectedSuddenData.argtypes = [c.c_void_p]


class ErrorCorrectedSuddenData:
    """ ARTS ErrorCorrectedSuddenData data

    Properties:
        id:
            Identity of the band/species/isotopologue
        
        Access operator with Species
    """
    def __init__(self, data=None):
        if isinstance(data, c.c_void_p):
            self.__delete__ = False
            self.__data__ = data
        else:
            self.__delete__ = True
            self.__data__ = c.c_void_p(lib.createErrorCorrectedSuddenData())
            assert data is None, "Fail initialize properly"

    def print(self):
        """ Print to cout the ARTS representation of the class """
        lib.printErrorCorrectedSuddenData(self.__data__)

    def __del__(self):
        if self.__delete__:
            lib.deleteErrorCorrectedSuddenData(self.__data__)

    def set(self, other):
        """ Sets this class according to another python instance of itself """
        raise RuntimeError("Cannot be set from another copy")

    def __repr__(self):
        x = ""
        x += f"{self.id}\n"
        for i in range(lib.getnelemErrorCorrectedSuddenData(self.__data__)):
            ptr = lib.getSpeciesErrorCorrectedSuddenDataAtErrorCorrectedSuddenData(self.__data__, i)
            x += f"\t{SpeciesErrorCorrectedSuddenData(c.c_void_p(ptr))}\n"
        return x

    def __eq__(self, other):
        n1 = lib.getnelemErrorCorrectedSuddenData(self.__data__)
        n2 = lib.getnelemErrorCorrectedSuddenData(other.__data__)
        if n1 != n2:
            return False
        
        for i in range(n1):
            ptr1 = lib.getSpeciesErrorCorrectedSuddenDataAtErrorCorrectedSuddenData(self.__data__, i)
            ptr2 = lib.getSpeciesErrorCorrectedSuddenDataAtErrorCorrectedSuddenData(other.__data__, i)
            if not (SpeciesErrorCorrectedSuddenData(c.c_void_p(ptr1)) == SpeciesErrorCorrectedSuddenData(c.c_void_p(ptr2))):
                return False
        return True
        
    @property
    def id(self):
        return QuantumIdentifier(c.c_void_p(lib.getidErrorCorrectedSuddenData(self.__data__)))
        
    @id.setter
    def id(self, val):
        self.id.set(val)
        
    def __getitem__(self, key):
        if not isinstance(key, Species):
            key = Species(key)
        return SpeciesErrorCorrectedSuddenData(c.c_void_p(
            lib.getErrorCorrectedSuddenData(self.__data__, key.__data__)))
        
    def __setitem__(self, key, val):
        self[key].set(val)

lib.createErrorCorrectedSuddenData.restype = c.c_void_p
lib.createErrorCorrectedSuddenData.argtypes = []

lib.deleteErrorCorrectedSuddenData.restype = None
lib.deleteErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.printErrorCorrectedSuddenData.restype = None
lib.printErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.getidErrorCorrectedSuddenData.restype = c.c_void_p
lib.getidErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.getErrorCorrectedSuddenData.restype = c.c_void_p
lib.getErrorCorrectedSuddenData.argtypes = [c.c_void_p, c.c_void_p]

lib.getnelemErrorCorrectedSuddenData.restype = c.c_long
lib.getnelemErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.getSpeciesErrorCorrectedSuddenDataAtErrorCorrectedSuddenData.restype = c.c_void_p
lib.getSpeciesErrorCorrectedSuddenDataAtErrorCorrectedSuddenData.argtypes = [c.c_void_p, c.c_long]


class MapOfErrorCorrectedSuddenData:
    """ ARTS MapOfErrorCorrectedSuddenData data

    Properties:
        Access operator with QuantumIdentifier
    """
    def __init__(self, data=None):
        if isinstance(data, c.c_void_p):
            self.__delete__ = False
            self.__data__ = data
        else:
            self.__delete__ = True
            self.__data__ = c.c_void_p(lib.createMapOfErrorCorrectedSuddenData())
            assert data is None, "Fail initialize properly"

    def print(self):
        """ Print to cout the ARTS representation of the class """
        lib.printMapOfErrorCorrectedSuddenData(self.__data__)

    def __del__(self):
        if self.__delete__:
            lib.deleteMapOfErrorCorrectedSuddenData(self.__data__)

    def set(self, other):
        """ Sets this class according to another python instance of itself """
        raise RuntimeError("Cannot be set from another copy")

    @staticmethod
    def name():
        return "MapOfErrorCorrectedSuddenData"

    def readxml(self, file):
        """ Reads the XML file

        Input:
            file:
                Filename to valid class-file (str)
        """
        if lib.xmlreadMapOfErrorCorrectedSuddenData(self.__data__, correct_read_arguments(file)):
            raise OSError("Cannot read {}".format(file))

    def savexml(self, file, type="ascii", clobber=True):
        """ Saves the class to XML file

        Input:
            file:
                Filename to writable file (str)

            type:
                Filetype (str)

            clobber:
                Allow clobbering files? (any boolean)
        """
        if lib.xmlsaveMapOfErrorCorrectedSuddenData(self.__data__, *correct_save_arguments(file, type, clobber)):
            raise OSError("Cannot save {}".format(file))

    def __eq__(self, other):
        n1 = lib.getnelemMapOfErrorCorrectedSuddenData(self.__data__)
        n2 = lib.getnelemMapOfErrorCorrectedSuddenData(other.__data__)
        if n1 != n2:
            return False
        
        for i in range(n1):
            ptr1 = lib.getErrorCorrectedSuddenDataAtMapOfErrorCorrectedSuddenData(self.__data__, i)
            ptr2 = lib.getErrorCorrectedSuddenDataAtMapOfErrorCorrectedSuddenData(other.__data__, i)
            if not (ErrorCorrectedSuddenData(c.c_void_p(ptr1)) == ErrorCorrectedSuddenData(c.c_void_p(ptr2))):
                return False
        return True
        
    def __getitem__(self, key):
        if not isinstance(key, QuantumIdentifier):
            key = QuantumIdentifier(key)
        return ErrorCorrectedSuddenData(c.c_void_p(
            lib.getMapOfErrorCorrectedSuddenData(self.__data__, key.__data__)))
        
    def __setitem__(self, key, val):
        self[key].set(val)

    def __repr__(self):
        x = ""
        for i in range(lib.getnelemMapOfErrorCorrectedSuddenData(self.__data__)):
            ptr = lib.getErrorCorrectedSuddenDataAtMapOfErrorCorrectedSuddenData(self.__data__, i)
            x += f"{ErrorCorrectedSuddenData(c.c_void_p(ptr))}\n"
        return x

lib.createMapOfErrorCorrectedSuddenData.restype = c.c_void_p
lib.createMapOfErrorCorrectedSuddenData.argtypes = []

lib.deleteMapOfErrorCorrectedSuddenData.restype = None
lib.deleteMapOfErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.printMapOfErrorCorrectedSuddenData.restype = None
lib.printMapOfErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.xmlreadMapOfErrorCorrectedSuddenData.restype = c.c_long
lib.xmlreadMapOfErrorCorrectedSuddenData.argtypes = [c.c_void_p, c.c_char_p]

lib.xmlsaveMapOfErrorCorrectedSuddenData.restype = c.c_long
lib.xmlsaveMapOfErrorCorrectedSuddenData.argtypes = [c.c_void_p, c.c_char_p, c.c_long, c.c_long]

lib.getMapOfErrorCorrectedSuddenData.restype = c.c_void_p
lib.getMapOfErrorCorrectedSuddenData.argtypes = [c.c_void_p, c.c_void_p]

lib.getnelemMapOfErrorCorrectedSuddenData.restype = c.c_long
lib.getnelemMapOfErrorCorrectedSuddenData.argtypes = [c.c_void_p]

lib.getErrorCorrectedSuddenDataAtMapOfErrorCorrectedSuddenData.restype = c.c_void_p
lib.getErrorCorrectedSuddenDataAtMapOfErrorCorrectedSuddenData.argtypes = [c.c_void_p, c.c_long]
