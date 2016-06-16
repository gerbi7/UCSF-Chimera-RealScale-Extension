'''
Created on Jun 13, 2016

@author: snorris
'''

from PythonModel.PythonModel import PythonModel
from OpenGL.GL import *  # @UnusedWildImport
from math import log, floor, pow

import chimera

mm2infactor = 0.0393701 # ratio of in/mm
 
class GridModel(PythonModel):
    '''
    Implements a ruler overlay for the RealScale Extention
    '''
    def __init__(self, RSDialog):
      PythonModel.__init__(self)
      
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
        hdpu, vdpu = hdpi * 10 * mm2infactor, vdpi * 10 * mm2infactor
      elif units == 'Imperial':
        hdpu, vdpu = hdpi, vdpi
      else:
        return
      
      glColor3f(1.0,1.0,1.0)
      glBegin(GL_LINES)
        
      xPos = 0
      while xPos < w:
        glVertex2f(xPos, 0)
        glVertex2f(xPos,h)
        xPos += hdpu
      
      yPos = 0
      while yPos < h:
        glVertex2f(0, yPos)
        glVertex2f(w, yPos)
        yPos += vdpu
      
      glEnd()
