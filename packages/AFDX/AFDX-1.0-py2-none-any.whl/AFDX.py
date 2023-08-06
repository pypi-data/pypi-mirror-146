
import os
from spherea.utest.ICDManager import ICDManager
from spherea.utest.ICDManager import Channel, Data, Container

current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)


def test():
    print('the wheels has been installed successly')
    
class ChannelA664(Channel):
    """Class for A664 channel"""
    def __init__(self, device, name, **kwargs):
        """create a channel A664
        @param device:name of device
        @param name : name of create object
        @param **kwargs：you can set 
        """
        Channel.__init__(self, device, name,
            **dict(templateName="ChannelAFDX",
                    channelType="AFDX",
                    **kwargs))
    def createVL(self ,name):
        '''create a VL in current channelA664 channel
        @type name: str
        @para name: name of object
        @return create VL
        '''
        return VL(name,self.path,self.icdManager)
    def createSamplingPort(self,name):
        '''create a sampling port in current VL
        @param name:the sampling port name
        @para type: str
        @return create sampling port
        '''
        return samplingport(name, self.path, self.icdManager)

class VL(Container):
    '''class for AFDX VL container'''

    def __init__(self, name, path, icd_manager, **kwargs):
        Container.__init__(self, name, path, icd_manager,
                        templateName="VL", **kwargs)

    def createSamplingPort(self,name):
        '''create a sampling port in current VL
        @param name:the sampling port name
        @para type: str
        @return create sampling port
        '''
        return samplingport(name, self.path, self.icdManager)



class samplingport(Container):
    '''Class for VL sampling port container
    @
    @
    '''
    def __init__(self, name, path, icd_manager, **kwargs):
        Container.__init__(self, name, path, icd_manager,
                        templateName="Sampling Port", **kwargs)
