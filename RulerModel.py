'''
Created on Jun 13, 2016

@author: snorris
'''

from PythonModel.PythonModel import PythonModel
from OpenGL.GL import *  # @UnusedWildImport
from math import log, floor, pow

import chimera

mm2infactor = 0.0393701 # ratio of in/mm
 
class RulerModel(PythonModel):
    '''
    Implements a ruler overlay for the RealScale Extention
    '''
    def __init__(self, RSDialog):
      PythonModel.__init__(self)
      
      self.metric = False
      
      # Do something with triggers?
      self.RSDialog = RSDialog
      
    def destroy(self, *args):
      PythonModel.destroy()
    
    def computeBounds(self, sphere, bbox):
      return False
    
    def validXform(self):
      return False
    
    def draw(self, lens, viewer, passType):
      if passType != chimera.LensViewer.Overlay2d:
          return
      
      MIN_TICK_PIXEL_SEP = 5
      
      w, h = viewer.windowSize
      hdpi, vdpi = self.RSDialog.hdpi, self.RSDialog.vdpi
      if hdpi == 0 or vdpi == 0:
        return
      
      
      glLineWidth(1.0)
      glDisable(GL_LINE_SMOOTH)
      
      units = self.RSDialog.ruler_grid_units
      
#       glEnable(GL_BLEND)
#       glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
      if units == 'Metric':
        hdpmm, vdpcm = hdpi * mm2infactor, vdpi * 10 * mm2infactor
        
        glColor3f(1.0,1.0,1.0)
        glBegin(GL_LINES)
        
        xPos = 0
        while xPos * hdpmm < w:
          glVertex2f(xPos * hdpmm, 0)
          glVertex2f(xPos * hdpmm, vdpcm * (1 if xPos % 10 == 0 else .75))
          xPos += 1
          
        glEnd()
        
      elif units == 'Imperial':
        divLevels = floor( log(hdpi/MIN_TICK_PIXEL_SEP,2))
        maxSubDiv = int( pow(  divLevels, 2) ) 
        def _drawTick(xPos, currentLevel):
          
          glVertex2f(xPos,0)
          glVertex2f(xPos,vdpi * (1 + divLevels + log(1.0 / currentLevel, 2)) / (divLevels + 1)  )
          if currentLevel < maxSubDiv:
            _drawTick(xPos + hdpi / (currentLevel * 2), currentLevel * 2)
            if currentLevel == 1:
              if xPos + hdpi < w:
                _drawTick(xPos + hdpi, 1)
            else:
              _drawTick(xPos - hdpi / (currentLevel * 2), currentLevel * 2)
        
        glColor3f(1.0,1.0,1.0)
        glBegin(GL_LINES)
        
        _drawTick(0,1)
          
        glEnd()
