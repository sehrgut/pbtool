#!/usr/bin/python

import sys
import unicodedata
import argparse

from AppKit import (NSPasteboard,
	NSGeneralPboard, NSDragPboard, NSFindPboard, NSFontPboard, NSRulerPboard,
	NSPasteboardItem, NSArray,
	NSPasteboardTypePDF, NSPasteboardTypePNG, NSPasteboardTypeTIFF, NSPostScriptPboardType,
	NSURLPboardType, NSPasteboardTypeColor, NSFileContentsPboardType, NSFilesPromisePboardType,
	NSFindPanelSearchOptionsPboardType, NSPasteboardTypeFont,
	NSPasteboardTypeHTML, NSInkTextPboardType, NSPasteboardTypeMultipleTextSelection,
	NSPasteboardTypeRTF, NSPasteboardTypeRTFD, NSPasteboardTypeRuler, NSPasteboardTypeSound,
	NSPasteboardTypeString, NSPasteboardTypeTabularText, NSPasteboardTypeTextFinderOptions,
	NSVCardPboardType)

verbosity = 0

text_types = [NSPasteboardTypeHTML, NSPasteboardTypeString, NSPasteboardTypeTabularText]
image_types = [NSPasteboardTypePDF, NSPasteboardTypePNG, NSPasteboardTypeTIFF, NSPostScriptPboardType]

def log(msg):
	if verbosity > 0:
		print >> sys.stderr, msg

def unicode_clean(string):
#https://gist.github.com/Jonty/6705090
	"""Cleans a string based on a whitelist of printable unicode categories
	You can find a full list of categories here:
	http://www.fileformat.info/info/unicode/category/index.htm
	"""
	letters     = ('LC', 'Ll', 'Lm', 'Lo', 'Lt', 'Lu')
	numbers     = ('Nd', 'Nl', 'No')
	marks       = ('Mc', 'Me', 'Mn')
	punctuation = ('Pc', 'Pd', 'Pe', 'Pf', 'Pi', 'Po', 'Ps')
	symbol      = ('Sc', 'Sk', 'Sm', 'So')
	space       = ('Zs',)

	allowed_categories = letters + numbers + marks + punctuation + symbol + space
	allowed_exceptions = [u'\u000a', u'\u000d']

	return u''.join([ c for c in string if
		c in allowed_exceptions
		or unicodedata.category(c) in allowed_categories ])	
	

def info():
	global verbosity # todo STAHP THAT!

	verbosity += 1

	for n in [NSGeneralPboard, NSDragPboard, NSFindPboard, NSFontPboard, NSRulerPboard]:
		pb = NSPasteboard.pasteboardWithName_(n)
		log(pb.name())

		items = pb.pasteboardItems()
		if len(items):
			log('Found items:')
			for i in items:
				log(i)
				log(i.types())
				log(i.dataForType_(NSPasteboardTypeString))
		else:
			log('Pasteboard empty')
		
		log('')

	verbosity -= 1


def zap():
	log('Scrubbing non-printing character data from pasteboard')
	pb = NSPasteboard.generalPasteboard()
	items = pb.pasteboardItems()
	
	if len(items):
		log('Found items:')
		for i in items:
			log(i)
			log(i.types())
			log(i.dataForType_(NSPasteboardTypeString))

	olditem = pb.pasteboardItems()[0]
	newitem = NSPasteboardItem.alloc().init()

	for t in olditem.types():
		if t in text_types: # TODO validate against string, tabular, and html
			s = olditem.stringForType_(t)
			x = ":".join("{:04x}".format(ord(c)) for c in s)
			log(t)
			log('old: ' + x)
			s = unicode_clean(s)
			x = ":".join("{:04x}".format(ord(c)) for c in s)
			log('new: ' + x)
			s = bytearray(s, encoding='utf-8')
			newitem.setData_forType_(s, t)
		else:
			d = olditem.dataForType_(t)
			log(t + ': copying')
			newitem.setData_forType_(olditem.dataForType_(t), t)

	pb.clearContents()
	pb.writeObjects_([newitem])

	log('New clipboard state:')
	items = pb.pasteboardItems()
	if len(items):
		log('Found items:')
		for i in items:
			log(i)
			log(i.types())
			log(i.dataForType_(NSPasteboardTypeString))


def image():
	log('Scrubbing non-image data from pasteboard')
	pb = NSPasteboard.generalPasteboard()
	items = pb.pasteboardItems()
	
	if len(items):
		log('Found items:')
		for i in items:
			log(i)
			log(i.types())


		#TODO: multi-item pasteboards?
		olditem = pb.pasteboardItems()[0]
		newitem = NSPasteboardItem.alloc().init()

		for t in olditem.types():
			if t in image_types:
				newitem.setData_forType_(olditem.dataForType_(t), t)

		pb.clearContents()
		pb.writeObjects_([newitem])

		log('New clipboard state:')
		log(pb.pasteboardItems())
		log(pb.types())
	else:
		log('Pasteboard empty')

parser = argparse.ArgumentParser(description='manipulate the MacOS pasteboard')
parser.add_argument('-V', '--version', action='version', version='pbtool/0.1a')
parser.add_argument('-I', '--info', action='store_const', dest='mode', const='info',
	help='show info about pasteboard contents, but do not modify them (default)'),
parser.add_argument('-i', '--image', action='store_const', dest='mode', const='image',
	help='remove non-image data from pasteboard')
parser.add_argument('-z', '--zap-gremlins', action='store_const', dest='mode', const='zap',
	help='remove nonprintable characters from text data in pasteboard')
parser.add_argument('-v', '--verbose', action='count', default=0,
	help='increase verbosity level')

parser.set_defaults(mode='info')
args = parser.parse_args()

verbosity = args.verbose
log(args)

modes = {
	'image': image,
	'zap': zap,
	'info': info
}

modes[args.mode]()