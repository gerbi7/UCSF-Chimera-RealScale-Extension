from math import sqrt
from Tkinter import StringVar
from RulerModel import RulerModel

import chimera
from chimera.baseDialog import ModelessDialog

import Tkinter
from CGLtk import Hybrid
from GridModel import GridModel

mm2infactor = 0.0393701 # ratio of in/mm
# -----------------------------------------------------------------------------
#
class Realscale_Dialog(ModelessDialog):

  lock_scale = disable_viewer_forcing = show_ruler = show_grid = 0
  scale_to_lock = 1.0
  hdpi = vdpi = 0
  ruler_grid_units = None

  ruler_model = grid_model = None
  
  title = 'Real Scale'
  name = 'Real Scale'
  buttons = ('Close',)
#   help = None
  
  def fillInUI(self, parent):

    self.model = None 

    self.toplevel_widget = parent.winfo_toplevel()
    self.toplevel_widget.withdraw()
    
    self.toplevel_widget.wm_resizable(0,0)
    
    row = 0

    mcf = Tkinter.Frame(parent)
    mcf.grid(row= row, column = 0, sticky = 'w')
    row += 1
    
    sb = Hybrid.Checkbutton(mcf, 'Lock Scale', 0)
    sb.button.grid(row = row, column = 0, sticky = 'w')
    self._lock_scale = sb.variable
    self._lock_scale.add_callback(self.settings_changed_cb)
    
    ob = Hybrid.Checkbutton(mcf, 'Disable viewer forcing', 0)
    ob.button.grid(row = row, column = 1, sticky = 'w')
    self._disable_viewer_forcing = ob.variable
    self._disable_viewer_forcing.add_callback(self.settings_changed_cb)


    # monitor frame (always visible part)
    mf = Tkinter.Frame(parent)
    mf.grid(row = row, column = 0, sticky = 'w')
    row +=1
    
    self.hdpi, self.vdpi = self.get_auto_monitor_dpi()
    
    
    #monitor dpi stringvar
    mdsv = Tkinter.StringVar()
    #monitor dpi
    md = Tkinter.Label(mf, textvariable = mdsv) 
    mdsv.set("Monitor DPI: " + str(self.hdpi) + "x" + str(self.vdpi) )
    md.grid(row = 0, column = 0, sticky = 'w')
    self.mdsv = mdsv
    
    #Manual scale check button    
    mscb = Hybrid.Checkbutton(mf, 'Manual Monitor Config', 0)
    mscb.button.grid(row = 0, column = 1, sticky = 'w')
    self._manual_monitor_conf = mscb.variable
    self._manual_monitor_conf.add_callback(self.monitor_scale_cb)
    
    
    #pop frame just used for making popup_frame work
    #monitor measurement popup frame
    mmpf =  Tkinter.Frame(parent)
    mscb.popup_frame(mmpf, row = row, column = 0, sticky = 'w')
    row += 1
    
    # screen [measurements] frame
    sf = Tkinter.Frame(mmpf)
    sf.grid(row = 0, column = 0, sticky = 'w')
    
    # equal axis check button
    eacb = Hybrid.Checkbutton(sf,"Non-equal horizontal and vertical DPI",0)
    eacb.button.grid(row = 0, column = 0, sticky = 'w')
    self._unequaldpi = eacb.variable
    self._unequaldpi.add_callback(self.monitor_scale_cb)
    
    #primary dimension frame
    pdf = Tkinter.Frame(sf)
    pdf.grid(row = 1, column = 0, sticky = 'w')
    
    #primary dimension measurement entry
    pdme = Hybrid.Entry(pdf, None, 5)
    pdme.frame.grid(row = 0, column = 0, sticky = 'w')
    pdme.entry.bind('<KeyPress-Return>', self.monitor_scale_cb)
    self.primary_dim_value = pdme.variable
    
    #primary unit menu
    pum = Hybrid.Option_Menu(pdf, None, 'in', 'cm', 'mm', 'dpi')
    pum.frame.grid(row = 0, column = 1, sticky = 'w')
    pum.add_callback(self.monitor_scale_cb)
    self.primary_dim_monitor_units = pum.variable
  
    #primary direction option menu
    pdom = Hybrid.Option_Menu(pdf, None, '','Diag.', 'Width', 'Height')
    pdom.frame.grid(row = 0, column = 2, sticky = 'w')
    pdom.add_callback(self.monitor_scale_cb)
    self.primary_monitor_direction = pdom.variable
    self.ui_pdom = pdom
    
    #secondary dimension popup frame
    sdpf = Tkinter.Frame(sf)
    eacb.popup_frame(sdpf, row = 2, column = 0, sticky = 'w')
    
    #secondary dimension frame
    sdf = Tkinter.Frame(sdpf)
    sdf.grid(row = 0, column = 0, sticky = 'w')
    
    #secondary dimension measurement entry
    sdme = Hybrid.Entry(sdf, None, 5)
    sdme.frame.grid(row = 0, column = 0, sticky = 'w')
    sdme.entry.bind('<KeyPress-Return>', self.monitor_scale_cb)
    self.secondary_dim_value = sdme.variable
    
    #secondary unit menu
    sum = Hybrid.Option_Menu(sdf, None, 'in', 'cm', 'mm', 'dpi')
    sum.frame.grid(row = 0, column = 1, sticky = 'w')
    sum.add_callback(self.monitor_scale_cb)
    self.secondary_dim_monitor_units = sum.variable
    
    #secondary direction option menu
    self.secondary_monitor_direction = Tkinter.StringVar()
    sdom = Tkinter.Label(sdf, textvariable = self.secondary_monitor_direction)
    sdom.grid(row = 0, column = 2, sticky = 'w')
    
    
    #ruler settings frame
    rf = Tkinter.Frame(parent)
    rf.grid(row = row, column = 0, sticky = 'w')
    row += 1
    
    #ruler on check button
    roncb = Hybrid.Checkbutton(rf,'Show Ruler', 0)
    roncb.button.grid(row = 0, column = 0, sticky = 'w')
    self._show_ruler = roncb.variable
    self._show_ruler.add_callback(self.settings_changed_cb)
    
    #grid on check button
    goncb = Hybrid.Checkbutton(rf,'Show Grid', 0)
    goncb.button.grid(row = 0, column = 1, sticky = 'w')
    self._show_grid = goncb.variable
    self._show_grid.add_callback(self.settings_changed_cb)
    
    #ruler/grid unit selection
    rgus = Hybrid.Option_Menu(rf, None, 'Metric', 'Imperial')
    rgus.frame.grid(row = 0, column = 2, sticky = 'w')
    rgus.add_callback(self.settings_changed_cb)
    self._ruler_grid_units = rgus.variable


    # Reset scale label
    rsl = Tkinter.Label(parent, text = 'Reset scale so Angstrom is equivalent to: ')
    rsl.grid(row = row, column = 0, sticky = 'w')
    row += 1
    
    # Reset Buttons 
    rbr = Hybrid.Button_Row(parent, '', 
                            (('inches', self.reset_inches_cb),
                             ('cm', self.reset_cm_cb),
                             ('mm', self.reset_mm_cb)) )
    rbr.frame.grid(row = row, column = 0, sticky = 'w')
    row += 1

    
    self.unequal_dpi = False
    
  def map(self):
    self._viewerhandler = chimera.triggers.addHandler(u'Viewer',self.viewer_changed_cb, None)

  def unmap(self):
    chimera.triggers.deleteHandler(u'Viewer', self._viewerhandler)
  
  def viewer_changed_cb(self, trigger, user_data, trig_data):
    if self.disable_viewer_forcing:
      return
    chimera.viewer.camera.ortho = True
    if self.lock_scale:
      chimera.viewer.setViewSizeAndScaleFactor(chimera.viewer.viewSize,self.scale_to_lock)
    if self.hdpi != 0:
      w,h = chimera.viewer.windowSize
#       print 'Inches wide: ',  float(w) / self.hdpi
#       chimera.viewer.viewSize = float(w) / self.hdpi
      chimera.viewer.setViewSizeAndScaleFactor(0.5 * w / self.hdpi, chimera.viewer.scaleFactor)
      
      
    
    
#     import SimpleSession
#     chimera.triggers.addHandler(SimpleSession.SAVE_SESSION,
# 				self.save_session_cb, None)
#     chimera.triggers.addHandler(chimera.CLOSE_SESSION,
# 				self.close_session_cb, None)
#     
#   # ---------------------------------------------------------------------------
#   #
#   def save_session_cb(self, trigger, x, file):
# 
#     import session  # @UnresolvedImport TODO fix this stupid import issue
#     session.save_scale_bar_state(self, file)
#       
#   # ---------------------------------------------------------------------------
#   #
#   def close_session_cb(self, trigger, a1, a2):
# 
#     self.show_scalebar.set(0)

  # ---------------------------------------------------------------------------
  #
  def settings_changed_cb(self, event = None, model_id = None):
#     print "Setting changed cb called!"
    if not self.lock_scale:
      self.scale_to_lock = chimera.viewer.scaleFactor
    self.lock_scale = self._lock_scale.get()
      
        
    self.disable_viewer_forcing = self._disable_viewer_forcing.get()
    self.show_ruler = self._show_ruler.get()
    self.show_grid = self._show_grid.get()
    
    rgu = self._ruler_grid_units.get()
    if rgu != self.ruler_grid_units:
      if self.ruler_model:
        self.ruler_model.setMajorChange()
      if self.grid_model:
        self.grid_model.setMajorChange()
    self.ruler_grid_units = rgu
    
    if not self.disable_viewer_forcing:
      chimera.viewer.camera.ortho = True
      
    if self.show_ruler:
      self.make_ruler()
      self.ruler_model.display = True
#       self.ruler_model.setMajorChange()
    elif self.ruler_model:
      self.ruler_model.display = False
    if self.show_grid:
      self.make_grid()
      self.grid_model.display = True
#       self.grid_model.setMajorChange()
    elif self.grid_model:
      self.grid_model.display = False    
    
  
  def monitor_scale_cb(self, event = None, model_id = None):
    manual = self._manual_monitor_conf.get()
    
    if not manual:
      self.hdpi, self.vdpi = self.get_auto_monitor_dpi()
    else:
      if self._unequaldpi.get():
        if not self.unequal_dpi:
          self.ui_pdom.remove_entry(0)
          self.ui_pdom.remove_entry(0)
        self.unequal_dpi = True
        
        if self.primary_monitor_direction.get() == 'Width':
          self.secondary_monitor_direction.set('Height')
          
          self.hdpi = self._get_dpi(self.primary_dim_value, self.primary_dim_monitor_units, self.primary_monitor_direction)
          self.vdpi = self._get_dpi(self.secondary_dim_value, self.secondary_dim_monitor_units, self.secondary_monitor_direction)
          
        elif self.primary_monitor_direction.get() == 'Height':
          self.secondary_monitor_direction.set('Width')
          
          self.vdpi = self._get_dpi(self.primary_dim_value, self.primary_dim_monitor_units, self.primary_monitor_direction)
          self.hdpi = self._get_dpi(self.secondary_dim_value, self.secondary_dim_monitor_units, self.secondary_monitor_direction)
          
        else: # should only really be this case when checking the box to show the secondary direction
          self.primary_monitor_direction.set('Width',0)
          self.secondary_monitor_direction.set('Height')
          
          
      # hdpi == vdpi
      else:
        if self.unequal_dpi:
          self.ui_pdom.insert_entry(0,'Diag.')
          self.ui_pdom.insert_entry(0, '')
        self.unequal_dpi = False
          
        self.hdpi = self.vdpi = self._get_dpi(self.primary_dim_value, self.primary_dim_monitor_units, self.primary_monitor_direction)
    
    
    self.mdsv.set("Monitor DPI: " + str(self.hdpi) + "x" + str(self.vdpi) )
    
    if self.ruler_model:
      self.ruler_model.setMajorChange()
    if self.grid_model:
      self.grid_model.setMajorChange()
  
  def _get_dpi(self, value, units, direction):
    if units.get() == 'dpi':
      if not self.unequal_dpi:
        direction.set('', 0)
      return int( float_variable_value(value, 0))
    else:    
      pixels = self._get_relevant_pixels(direction.get())
      inches = self._convert_to_inches(float_variable_value(value, 0), units.get())
      return int( pixels / inches ) if inches != 0 else 0
  
  def _get_relevant_pixels(self, direction =''):
    width, height = self.toplevel_widget.winfo_screenwidth(), self.toplevel_widget.winfo_screenheight()
    return {
      'Diag.': sqrt(width * width + height * height),
      'Width': width,
      'Height': height
    }.get(direction,0)
    
  def _convert_to_inches(self, value = 0, unit = ''):
    return {
      'in': value, 
      'cm': mm2infactor * 10 * value,
      'mm': mm2infactor * value
    }.get(unit,0)
  
  def get_auto_monitor_dpi(self):
    hdpi = int( round(self.toplevel_widget.winfo_screenwidth() / (self.toplevel_widget.winfo_screenmmwidth() * mm2infactor)) )
    vdpi = int( round(self.toplevel_widget.winfo_screenheight() / (self.toplevel_widget.winfo_screenmmheight() * mm2infactor)) )
    return hdpi, vdpi
  
  # ---------------------------------------------------------------------------
  #

  def reset_inches_cb(self):
    self.scale_to_lock = 1.0
    chimera.viewer.viewAll()
    chimera.viewer.setViewSizeAndScaleFactor(chimera.viewer.viewSize,self.scale_to_lock)
    
    
  def reset_cm_cb(self):
    self.scale_to_lock = 10.0 * mm2infactor
    chimera.viewer.viewAll()
    chimera.viewer.setViewSizeAndScaleFactor(chimera.viewer.viewSize,self.scale_to_lock)
    
  def reset_mm_cb(self):
    self.scale_to_lock = 1.0 * mm2infactor
    chimera.viewer.viewAll()
    chimera.viewer.setViewSizeAndScaleFactor(chimera.viewer.viewSize,self.scale_to_lock)
 
  def make_ruler(self):
    if not self.ruler_model:
      self.ruler_model = RulerModel(self)
      chimera.openModels.add([self.ruler_model], hidden = True)
      
  def make_grid(self):
    if not self.grid_model:
      self.grid_model = GridModel(self)
      chimera.openModels.add([self.grid_model], hidden = True)
 
# -----------------------------------------------------------------------------
#
def float_variable_value(v, default = None):

  try:
    return float(v.get())
  except:
    return default
  
# -----------------------------------------------------------------------------
#
def real_scale_dialog(create = 0):

  from chimera import dialogs
  return dialogs.find(Realscale_Dialog.name, create=create)
  
# -----------------------------------------------------------------------------
#
def show_dialog():

  from chimera import dialogs
  return dialogs.display(Realscale_Dialog.name)

# -----------------------------------------------------------------------------
#
from chimera import dialogs
dialogs.register(Realscale_Dialog.name, Realscale_Dialog, replace = 1)
