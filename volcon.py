# coding: utf-8
from objc_util import *
import ui


#e.g.:
# precision = 1 -> '10-00'
# precision = 2 -> '100-000'
# precision = 3 -> '1000-0000'
# precision = 4 -> '10000-00000'
precision = 4


vs = None
volman = None


class VolumeManager:
	def __init__(self, _val, _prec, _lvol, _pos):
		if _val < 0 or _prec < 0 or _pos <= 0:
			raise ValueError()
		elif None in {_val, _prec, _lvol, _pos}:
			raise ValueError()

		self.val  = _val * pow(10, _prec)
		self.prec = _prec
		self.lvol = _lvol		
		self.pos  = _pos
	def call(self, _com):
		{
			'up'   : self.inc,
			'down' : self.dec,
			'left' : self.lshift,
			'right': self.rshift,
		}[_com]()
	def rshift(self):
		self.pos += 1
		if self.pos > self.prec:
			self.pos = 1
	def lshift(self):
		self.pos -= 1
		if self.pos < 1:
			self.pos = self.prec
	def inc(self):
		self.val += pow(10, self.prec - self.pos)
		if self.val > pow(10, self.prec):
			self.val = pow(10, self.prec)
	def dec(self):
		self.val -= pow(10, self.prec - self.pos)
		if self.val < 0:
			self.val = 0
	def updateLabelText(self):
		tmp = ObjCClass('NSMutableAttributedString').alloc().initWithString_((
			'%%0%dd' % (self.prec + 1)
		) % self.val).autorelease()
		tmp.setAttributes_range_(
			{'NSColor': ObjCClass('UIColor').redColor()},
			NSRange(self.pos, 1)
		)
		ObjCInstance(self.lvol).setAttributedText_(tmp)
	def updateVolume(self):
		vs.setValue_(float(self.val / pow(10, self.prec)))


def btn_down(sender):
	btn = sender.name
	volman.call(btn)
	volman.updateLabelText()
	if btn in {'up', 'down'}:
		volman.updateVolume()


def main():
	mv = ui.load_view('volcon')
	mv.name = 'Volume Controller'
	
	mpvs = ObjCClass('MPVolumeView').alloc().initWithFrame(CGRect(CGPoint(20, 30), CGSize(280, 34))).autorelease()
	mpvs.setShowsRouteButton_(False)
	
	global vs
	vs = mpvs.volumeSlider()
	
	tmp = None
	for i in mv.subviews:
		if i.name == 'volume':
			tmp = i
	
	global volman
	volman = VolumeManager(
		_val  = vs.value(),
		_prec = precision,
		_lvol = tmp,
		_pos  = 1
	)
	
	volman.updateLabelText()
	
	ObjCInstance(mv).addSubview_(mpvs)
	mv.present(orientations = ['portrait'])


if __name__=='__main__':
	main()

