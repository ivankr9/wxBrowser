#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
import os, sys, subprocess
import getpass
from wx.lib.wordwrap import wordwrap
import wx.lib.agw.ultimatelistctrl as ULC
import unicodedata
import datetime, time
import shutil
import random
import socket
import re
from PIL import ImageDraw,Image

def p(input):
	print('<<<'+str(input)+'>>>')

def Lin_Win_and_sep(): #return 0 is linux return 1 is windows
	if sys.platform == "linux" or sys.platform == "linux2":
		return 0, '/'
	elif sys.platform == "darwin":
		return 2, '/'
	elif sys.platform == "win32" or sys.platform == "win64":
		return 1, '\\'

def toggleConvertPath(inp=''):
	if inp == '':
		#line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
		text_data = wx.TextDataObject()
		if wx.TheClipboard.Open():
			success = wx.TheClipboard.GetData(text_data)
			wx.TheClipboard.Close()
		else:
			return None
		if success:
			line = text_data.GetText()
		pass
	else: 
	   line = inp
	if '/' in line: #confert to win \
		newline = '\\'.join(line.split('/'))
	else: #confert to unix 
		newline = '/'.join(line.split('\\'))
	if inp == '':
		#QtGui.QApplication.clipboard().setText(newline)
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(newline))
			wx.TheClipboard.Close()
		else:
			return None
	return newline

def reColorMarker(path,color): # make new color marker to .preview.jpg
	filepic = path[1:][:-1] + '/.preview.jpg'
	if not os.path.isfile(filepic):
		img = Image.new('RGB', (256,256), color='black')
		img.save(filepic)
	#file generated
	im = Image.open(filepic)
	width,height = im.size
	if width != 256:
		im.thumbnail((256,256),Image.ANTIALIAS)
	draw = ImageDraw.Draw(im)
	r = 35
	ry = 1900
	center = 256
	splcolor = color[1:][:-1].split(',')
	c = (int(splcolor[0]),int(splcolor[1]),int(splcolor[2]),255)
	draw.ellipse((center-r, center-ry, center+r, center+ry), fill=c)
	im.save(filepic)
	return None

def makeBakup(filepath_to_bak): # make Bakup given file to folder ./backup
	os.umask(0000)
	userPC = getpass.getuser()
	name = os.path.basename(filepath_to_bak)
	dir = os.path.dirname(filepath_to_bak)
	bakupdir = dir + '/backup'
	ts = timeStamp().replace(' ','_').replace(':','_')
	if not os.path.isdir(bakupdir):
		os.mkdir(bakupdir)
	bakuppath = bakupdir + '/' + ts[:6] +'_'+ ts[6:] + '_' + name + '_backup_' + userPC
	shutil.copyfile(filepath_to_bak,bakuppath)

def transliterate(string): # transliterals
	capital_letters = {u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G',u'Д': u'D',u'Е': u'E',u'Ё': u'E',u'З': u'Z',u'И': u'I',u'Й': u'Y',u'К': u'K',u'Л': u'L',u'М': u'M',u'Н': u'N',u'О': u'O',u'П': u'P',u'Р': u'R',u'С': u'S',u'Т': u'T',u'У': u'U',u'Ф': u'F',u'Х': u'H',u'Ъ': u'',u'Ы': u'Y',u'Ь': u'',u'Э': u'E',}
	capital_letters_transliterated_to_multiple_letters = {u'Ж': u'Zh',u'Ц': u'Ts',u'Ч': u'Ch',u'Ш': u'Sh',u'Щ': u'Sch',u'Ю': u'Yu',u'Я': u'Ya',}
	lower_case_letters = {u'а': u'a',u'б': u'b',u'в': u'v',u'г': u'g',u'д': u'd',u'е': u'e',u'ё': u'e',u'ж': u'zh',u'з': u'z',u'и': u'i',u'й': u'y',u'к': u'k',u'л': u'l',u'м': u'm',u'н': u'n',u'о': u'o',u'п': u'p',u'р': u'r',u'с': u's',u'т': u't',u'у': u'u',u'ф': u'f',u'х': u'h',u'ц': u'ts',u'ч': u'ch',u'ш': u'sh',u'щ': u'sch',u'ъ': u'',u'ы': u'y',u'ь': u'',u'э': u'e',u'ю': u'yu',u'я': u'ya',}
	for cyrillic_string, latin_string in iter(capital_letters_transliterated_to_multiple_letters.items()):
		string = re.sub(r'%s([а-я])' %cyrillic_string, r'%s\1' %latin_string, string)
	for dictionary in (capital_letters, lower_case_letters):
		for cyrillic_string, latin_string in iter(dictionary.items()):
			string = string.replace(cyrillic_string, latin_string)
	for cyrillic_string, latin_string in iter(capital_letters_transliterated_to_multiple_letters.items()):
		string = string.replace(cyrillic_string, latin_string.upper())
	return string

def writeutf8(file,line): # write UTF8 Files
	with open(file , 'w',encoding='utf-8') as f:
		f.write(line)

def readutf8_returnlistlines(file):
	lines = []
	if PLATFORM == 1:
		with open(file , 'r', encoding='utf-8') as f:
			lines = f.readlines() 
	else:
		with open(file , 'r') as f:
			lines = f.readlines() 
	return lines

def wxToClip(text):
	clipdata = wx.TextDataObject()
	clipdata.SetText(text)
	wx.TheClipboard.Open()
	wx.TheClipboard.SetData(clipdata)
	wx.TheClipboard.Close()

def selPatternToCurrentPath(selitem):
	# return currnt path from_sel pattern
	#selitem - "C:/Users/ivank"|"C:/Users/ivank"
	c = ''
	if '|' in selitem:
		items = selitem.split('|')
		for i in items:
			if i[0] == '"':
				c = i[1:][:-1]
				c = '/'.join(c.split('/')[:-1])
				break
			else:
				c = i
	else:

		if selitem[0] == '"':
			crop = selitem[1:]
			c = crop[:-1]
			c = '/'.join(c.split('/')[:-1])
		else:
			c = selitem
	c = c.split('+')
	return c[0]

def timeStamp(read=1): # generate timestamp 
	ts = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d%H%M%S')
	TS = str(ts[4:6])+' '+str(ts[2:4])+' 20'+str(ts[0:2])+' ' + str(ts[6:8]) +':'+ str(ts[8:10])
	if read == 1:
		return TS
	else:
		return ts

def linear_date_to_readible(date=''): # format 200105_194535_43.utf8 string input date
	dt = date.split('_')
	d = dt[0]
	t = dt[1]
	return d[4:6] +'.'+d[2:4]+'.20'+d[0:2]+'\n  '+t[0:2]+':'+t[2:4]+':'+t[4:6]

def getFileItemsFromPath(path,self): #return list of texts and list bitmaps
	#ls = os.listdir(path)
	sort_by_date=False
	sort_by_tags=False
	if self.SORT_MODE == 1:
		sort_by_date=True
		sort_by_tags=False
	if self.SORT_MODE == 2:
		sort_by_date=False
		sort_by_tags=True
	enbQuickLetter = False
	if self.ALET != '':
		enbQuickLetter = True

	filterLabel = ''
	if self.ENB_FILLTER == True:
		filterLabel = self.search_byLabel_tx.GetValue()
	if not os.path.isdir(path):
		path = HOMEPATH
	ls = [unicodedata.normalize('NFC', f) for f in os.listdir(path)]
	ls = sorted(ls)
	defaulticopathasset = APPFOLDER+'/icons/nopreview.jpg'
	defaulticopathfolder = APPFOLDER+'/icons/folder.jpg'
	defaulticopathfile = APPFOLDER+'/icons/file.jpg'
	assets = []
	dirs = []
	files = []
	for item in ls: # Base filter hidet files and folders and sort
		if enbQuickLetter:
			if item[0].lower() != self.ALET:
				continue
		if os.path.isdir(path+'/'+item):
			if os.path.isfile(path+'/'+item+'/.preview.jpg') or os.path.isdir(path+'/'+item+'/.infolabel'):
				assets.append((path+'/'+item,item))
			else:
				if item[0] != '.': #isnot hided dir make append
					dirs.append((path,item))
		else:
			if item[0] != '.': #isnot hided file (description) make append
				files.append((path,item))
	tassets = []
	n=0
	for ai in assets:
		a = ai[0]
		i = ai[1]  # name asset
		#get label get last info prewie int far sorting and store to tuples
		icopath = defaulticopathasset
		lbl = ' - no tags'
		lastinfo = ' - no info'
		aint = 0
		dsum = ''
		
		if os.path.isfile(a+'/.preview.jpg'):
			icopath = a+'/.preview.jpg'
		if os.path.isdir(a+'/.infolabel'):
			listinfos = os.listdir(a+'/.infolabel')
			listinfos = sorted(listinfos)
			lblfile = '000000_000000.utf8'
			if lblfile in listinfos:
				listinfos.remove(lblfile)
				lbl = ''
				lines = readutf8_returnlistlines(a+'/.infolabel/'+lblfile)
				lbl = ' '.join(lines)
				#with open(a+'/.infolabel/'+lblfile,'r') as f:
				#	lbl = ' '.join(f.readlines())
				if sort_by_tags:
					for s in lbl.split():
						if s.isdigit(): dsum += s
					if dsum != '': aint = 1000-int(dsum)
					else: aint = 100-n
			else: lbl = ' - no tags'
			if filterLabel != '':
				if not ' ' in filterLabel:
					if filterLabel.lower() in lbl.lower(): pass
					else: continue
				else:
					fls = filterLabel.split(' ')
					cont = 0
					for fs in fls:
						if fs.lower() in lbl.lower():
							cont += 1
					if cont == 0:
						continue
							
			if len(listinfos) > 0:
				lastinfofile = listinfos[-1]
				if lastinfofile != '000000_000000.utf8':
					lastinfo = ''
					lines = readutf8_returnlistlines(a+'/.infolabel/'+lastinfofile)
					lastinfo = ' '.join(lines)
					#with open(a+'/.infolabel/'+lastinfofile,'r') as f:
					#	lastinfo = ' '.join(f.readlines())
					if lastinfofile != '000000_000000.utf8':
						s = lastinfofile.split('.')[0].replace('_','')
						if sort_by_tags: pass
						else:
							aint = int(s)
		
		i = i
		n+=1
		if self.ENB_FILLTER:
			if lbl != ' - no tags':
				tassets.append((aint,i,icopath,lbl,lastinfo))
		else:
			tassets.append((aint,i,icopath,lbl,lastinfo))
	tfld = []
	tfile = []
	i = 0
	for wherei in dirs:
		if filterLabel != '':
			if not ' ' in filterLabel:
				if filterLabel.lower() in wherei[1].lower(): pass
				else: continue
			else:
				fls = filterLabel.split(' ')
				l = len(fls)
				for fl in fls:
					if fl.lower() in wherei[1].lower():
						l -= 1
				if l != 0: continue
		where = wherei[0]
		name = wherei[1]
		dname = '.'+name
		icopath = defaulticopathfolder
		lbl = ' - '
		lastinfo = ' - '
		aint = 0
		if os.path.isfile(where+'/'+dname):
			lines = readutf8_returnlistlines(where+'/'+dname)
			lastinfo = ' '.join(lines)
			#with open(where+'/'+dname,'r',encoding='utf-8') as f:
			#	lastinfo = ' '.join(f.readlines())
		tfld.append((-1-i,name,icopath,lbl,lastinfo))
		i+=1
	
	i = 0
	for wherei in files:
		if filterLabel != '':
			if not ' ' in filterLabel:
				if filterLabel.lower() in wherei[1].lower(): pass
				else: continue
			else:
				fls = filterLabel.split(' ')
				l = len(fls)
				for fl in fls:
					if fl.lower() in wherei[1].lower():
						l -= 1
				if l != 0: continue
		where = wherei[0]
		name = wherei[1]
		dname = '.'+name
		icopath = defaulticopathfile
		lbl = ' - '
		lastinfo = ' - '
		aint = 0
		size = os.path.getsize(where+'/'+name)
		sec = os.path.getmtime(where+'/'+name)
		mt = time.strftime('%Y-%m-%d %H:%M',time.localtime(sec))
		i = int(time.strftime('%Y%m%d%H%M',time.localtime(sec)))
		if sort_by_tags:
			i = int(size)
		kb = str(size/1000) + ' kb'
		mb = str(size/1000000) + ' mb'
		if size > 999999:
			size = mb
		else:
			size = kb
		lbl = str(mt) + '	                     size: ' + size
		# if description
		if os.path.isfile(where+'/'+dname):
			lines = readutf8_returnlistlines(where+'/'+dname)
			lastinfo = ' '.join(lines)
			#with open(where+'/'+dname,'r') as f:
			#	lastinfo = ' '.join(f.readlines())
		tfile.append((-1000-i,name,icopath,lbl,lastinfo))
		i+=1

	elements = tassets+tfld+tfile
	if sort_by_date or sort_by_tags: # resort elements by first intager
		elements = sorted(elements, key=lambda tup: tup[0])
		elements = elements[::-1]
	return elements #sorted list of tupels (name,icofile,row1,row2)

def getInfoLinesFromPath(path): # path to asset folder info lines from folder when Select
	tinfo = []
	if os.path.isdir(path+'/.infolabel'):
		ls = [unicodedata.normalize('NFC', f) for f in os.listdir(path+'/.infolabel')]
		#ls = os.listdir(path+'/.infolabel')
		ls = sorted(ls)
		for item in ls:
			if item != '000000_000000.utf8':
				dt = linear_date_to_readible(item)
				lines = readutf8_returnlistlines(path+'/.infolabel/'+item)
				read = ' '.join(lines)
				#with open(path+'/.infolabel/'+item,'r') as f:
				#	read = ''.join(f.readlines())
				autor = '\n'.join(read.split('\n')[:2])
				comms = read.replace(autor+'\n','')
				tinfo.append((dt,autor,comms))
	return tinfo[::-1]

def update_toggle_colors(btn , bool=None):
	if bool == None:
		btn.SetForegroundColour(wx.Colour(0,0,0))
		if btn.GetValue():
			btn.SetBackgroundColour(wx.Colour(25,235,45)) # enable color
		else:
			btn.SetBackgroundColour(wx.Colour(85,85,85))
	else:
		if bool:
			btn.SetBackgroundColour(wx.Colour(25,235,45 )) # enable color
		else:
			btn.SetBackgroundColour(wx.Colour(85,85,85))

def redrawToolPallete(self, CurrentPallete): # !!!!!!!!!!!!!!!!!!!  TOOOL PALLETE REDAW !!!!!!!!!!
	curcat = CurrentPallete+1
	for t in self.toolList:
		t.Destroy()
	self.toolList = []
	self.toolsizer.Layout()
	#p = self.toolsizer.GetChildren()
	listTools = []
	for t in TOOLS:
		command_buttonpref_tooltip = t.split('|||') #command and notes
		lable_cat_color = command_buttonpref_tooltip[1].split(' ')
		cat = lable_cat_color[1]
		if str(curcat) in cat:
			listTools.append(t)
	self.toolsizer.SetCols(len(listTools))
	for t in listTools:
		command_buttonpref_tooltip = t.split('|||')
		lable_cat_color = command_buttonpref_tooltip[1].split(' ')
		command = command_buttonpref_tooltip[0]
		lable = lable_cat_color[0]
		color_list = lable_cat_color[2].split('_')
		toolbtn = wx.Button(self, label=lable, style=wx.NO_BORDER,size=(100,20))
		toolbtn.SetBackgroundColour(wx.Colour(int(color_list[0]), int(color_list[1]), int(color_list[2])))
		toolbtn.SetFont(self.font_to_read)
		toolbtn.SetForegroundColour(wx.Colour(0,0,0))
		tooltip_text = command + '\n\n' + command_buttonpref_tooltip[2]
		toolbtn.SetToolTip(tooltip_text)
		toolbtn.Bind(wx.EVT_BUTTON,self.run_tool)
		self.toolsizer.Add(toolbtn,flag=wx.EXPAND,border=15) #, 
		self.toolList.append(toolbtn)
	self.toolsizer.Layout()

class FileDrop(wx.FileDropTarget): # file DROP to send text setVARIABLE
	def __init__(self, textctrl, preclean=False):
		wx.FileDropTarget.__init__(self)
		self.textctrl = textctrl
		self.preclean = preclean

	def OnDropFiles(self, x, y, filenames):
		text = ''
		for name in filenames:
			text += '"' + name + '"'
			for e in ENVS:
				if e != '':
					ee = e.split('=')
					if ee[1] in text:
						text = text.replace(ee[1],ee[0])
		self.textctrl.WriteText((text))
		return False


class MyTextDropTarget(wx.TextDropTarget): # kuda drop texta
	#----------------------------------------------------------------------
	def __init__(self, textctrl, parent, preclean=False):
		wx.TextDropTarget.__init__(self)
		self.textctrl = textctrl
		self.preclean = preclean
		self.parent = parent
	#----------------------------------------------------------------------
	def OnDropText(self, x, y, text):
		if self.preclean:
			self.textctrl.SetValue('')
		if '"' in text and ' ' in text:
			text = text.split(' ')[1]
		self.textctrl.WriteText((text.replace('\n','').replace(' ','')))
		self.parent.SetListAndSelectionFromLocation_path_tx()
		return False
	#----------------------------------------------------------------------
	def OnDragOver(self, x, y, d):
		return wx.DragCopy

class myList(ULC.UltimateListCtrl): # LIST ITEMS or INFO COMMENTS  UltimateListCtrl
	def __init__(self,*args, **kw):
		super(myList, self).__init__( *args,agwStyle=ULC.ULC_NO_HIGHLIGHT|ULC.ULC_REPORT|ULC.ULC_HAS_VARIABLE_ROW_HEIGHT|ULC.ULC_NO_HEADER ,**kw)
		backcol = wx.Colour(15,15,15)
		col_text = wx.Colour(225,225,225)
		self.SetBackgroundColour(backcol)
		self.SetTextColour(col_text)
		#font_to_read = wx.Font(8, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		font_to_read = wx.Font( wx.FontInfo(8))
		self.SetFont(font_to_read)
		self.col = wx.Colour(30,30,30)
		self.col2 = wx.Colour(40,40,40)
		#self.col3 = wx.Colour(180, 51,0)
		self.col3 = wx.Colour(1,85,1)
		self.MAXFILEFOLDERS = int(START_MAXFILEFOLDERS)
		self.MAXINFOLINES = int(START_MAXINFOLINES)

	def setOtherMaxFoldersNums(self, maxnum):
		self.MAXFILEFOLDERS = maxnum

	def setOtherMaxInfoNums(self, maxnum):
		self.MAXINFOLINES = maxnum

	def getMax(self):
		return self.MAXFILEFOLDERS, self.MAXINFOLINES
	
	def setMyList(self,asFilesTorInfosF=True,items=[], selectedItems=[]):
		self.ClearAll()
		sel_index = -1
		if asFilesTorInfosF:
			#create columns with preview
			imgscale = 52
			defaultImages = wx.ImageList(imgscale, imgscale)
			self.SetImageList(defaultImages, wx.IMAGE_LIST_SMALL)
			ico_paths = [APPFOLDER+'/icons/folder.jpg',APPFOLDER+'/icons/file.jpg',APPFOLDER+'/icons/nopreview.jpg']
			fi = None
			foi = None
			npi = None
			for ip in ico_paths:
				img = wx.Image(ip, wx.BITMAP_TYPE_ANY)
				bmp = img.Rescale(imgscale,imgscale,wx.IMAGE_QUALITY_HIGH)
				if ico_paths.index(ip) == 0:
					foi = defaultImages.Add(wx.Bitmap(bmp))
				if ico_paths.index(ip) == 1:
					fi = defaultImages.Add(wx.Bitmap(bmp))
				if ico_paths.index(ip) == 2:
					npi = defaultImages.Add(wx.Bitmap(bmp))
			
			colWidth = 488
			self.InsertColumn(0, "", width=colWidth)
			index = 0
			maxitems = self.MAXFILEFOLDERS
			m = False
			if items == []:
				#self.InsertColumn(0, "", width=200)
				self.InsertStringItem(0,'Not items to display!\nFolder empty or Filter enabled')
				return None
			if len(items) < maxitems:
				maxitems = len(items)
			else: m = True
			for i in items[:maxitems]:
				name = i[1]
				icopath = i[2]
				label = i[3]
				label = label.replace('\r',' ').replace('\n',' ')
				lastinfo = i[4]
				
				if '\n' in lastinfo:
					spl = lastinfo.split('\n')
					author = spl[0] + '\n' + spl[1][1:]
					if author in PCNAMEUSERkeyAndViewNameDICT:
						author = PCNAMEUSERkeyAndViewNameDICT[author]
					lastinfo = author+':'+' '.join(spl[2:])
				cut_lastinfo = lastinfo[:68]
				if lastinfo != cut_lastinfo:
					lastinfo = cut_lastinfo + '..'
				lastinfo = lastinfo.replace('\r',' ').replace('\n',' ')
				endname = ''
				length = 50
				lname = len(name)
				length -= lname
				if icopath == APPFOLDER+'/icons/file.jpg':
					#extension = name.split('.',1)[-1]
					fc = name.split('.')
					ec = []
					imax = 2
					i=0
					for c in fc[::-1]:
						if imax == 0:
							break
						if i != 0:
							if c[-1].isdigit():
								break
						if c == fc[0]:
							break
						ec.append(c)
						imax -= 1
						i+=1
					extension = '.'.join(ec[::-1])
					endname = ('  '*length)+extension.upper()
				elif icopath == APPFOLDER+'/icons/folder.jpg':
					endname = ('  '*length)+'FOLDER'
				else:
					pass#endname = (' '*length)+'  -'*10
				#u' diffuse_house.rstexbin \n	 label: - \n	 lastinfo: - ',

				#print lastinfo
				#print name,infoline
				fdisplay_u = '     '+name+'  '+endname+u' \n '+label+u' \n '+lastinfo
				#fdisplay_u = '		 '+name.replace('\n',' ')+endname.replace('\n',' ')+'  '+'  '+lastinfo.replace('\n',' ') #label.replace('\n',' ')
				item = wordwrap(fdisplay_u, colWidth, wx.ClientDC(self),breakLongWords=False)
				#print item
				self.InsertStringItem(index, item)
				if selectedItems != []:
					for sel_path in selectedItems:
						basename = sel_path.replace('"','').split('/')[-1]
						if name == basename:
							self.Select(index)
							sel_index = index
				if icopath == APPFOLDER+'/icons/file.jpg':
					self.SetItemImage(index, fi)
				elif icopath == APPFOLDER+'/icons/folder.jpg':
					self.SetItemImage(index, foi)
				elif icopath == APPFOLDER+'/icons/nopreview.jpg':
					self.SetItemImage(index, npi)
				else:
					img = wx.Image(icopath, wx.BITMAP_TYPE_ANY)
					bmp = img.Rescale(imgscale,imgscale,wx.IMAGE_QUALITY_HIGH)
					preview_im = defaultImages.Add(wx.Bitmap(bmp))
					self.SetItemImage(index, preview_im)
				index+=1
			if m:
				self.InsertStringItem(index+1, 'Max Items limmited: '+ str(maxitems))
			else:
				self.Bind( wx.EVT_LIST_ITEM_RIGHT_CLICK, self.RightClickItems ) # ---------------- ADD MENU

		else: #create columns date autor info  !!!!!!!!!!!!!!!!!!!!!!***********************************************************
			textcolwidth = 570
			self.InsertColumn(0, "", width=80)
			self.InsertColumn(1, "", width=80)
			self.InsertColumn(2, "", width=textcolwidth)
			row = 0
			maxitems = int(self.MAXINFOLINES)
			if len(items) < maxitems:
				maxitems = len(items)
			for i in items[:maxitems]:
				date = i[0].replace('\r',' ')
				autor = i[1].replace('\r',' ')#
				if autor in PCNAMEUSERkeyAndViewNameDICT:
					autor = PCNAMEUSERkeyAndViewNameDICT[autor]
				text = i[2].replace('\r',' ')
				if text[-1] == '\n':
					text = text[:-1]
				item = wordwrap(text, textcolwidth, wx.ClientDC(self),breakLongWords=False)
				self.InsertStringItem(row,date)
				self.SetStringItem(row,1, autor)
				self.SetStringItem(row,2, item)
			#self.Bind( wx.EVT_LIST_ITEM_RIGHT_CLICK, self.RightClickInfo )# ---------------- ADD MENU
		return sel_index

	def RightClickInfo( self, event ):
		#row = event.GetIndex()
		#col = 2
		#item = self.GetItem(itemOrId=row, col=col)
		#text = item.GetText()
		#parse message
		self.menu = wx.Menu()
		for i in [3,5,7,8]:
			self.menu.Append( i, str(i)+'fsdfsdfsdf' )
			self.menu.Bind( wx.EVT_MENU, self.menuSelect_evnt )
		self.PopupMenu( self.menu, event.GetPoint() )
		#print self

	def RightClickItems_old( self, event ):
		print('right clk Items')
		text = event.GetText().split('\n')[0][9:]
		ts = text.split('  ')
		end = ts[-1]
		begin = ts[0]
		sel = ''
		asset_dir_file = 0
		if end == ' ': #this Asset
			sel = text
		elif end.replace(' ','') == 'FOLDER': #this folder
			sel = begin
			asset_dir_file = 1
		else:
			sel = begin
			asset_dir_file = 2
		self.selpath = self.GetParent().CurrentPath + '/' + sel
		check = False
		#if '|' in self.selpath:
		#f	fifile = self.selpath.split('|',)
		if asset_dir_file == 0 or asset_dir_file== 1:
			if os.path.isdir(self.selpath):
				#folder menu
				check = True
				print('folder')
		else:
			if os.path.isfile(self.selpath):
				#file menu
				check = True
				print('file')
		if check:
			menuitems = ['Go Up', 'Reveal in location' ,'Open with preferred Application']
			#add Menu Copy Lin win Relative Lin relative Win
			#partial(self.option_chosen, 1),menu_item_1)
			self.menu = wx.Menu()
			i = 0
			for mi in menuitems:
				self.menu.Append( i, mi)
				i+=1
			splselpath = self.selpath.split('/')
			rslice = int(-(len(splselpath)/2))
			self.relL = '/'.join(splselpath[rslice:])
			self.menu.Append( 3, 'Copy linux path') #+ self.selpath)
			#self.menu.Append( 4, '	or relative :\t../' + self.relL)
			self.menu.Append( 5, 'Copy win path') #+ self.selpath.replace('/','\\'))
			#self.menu.Append( 6, '	or relative:\t..\\' + self.relL.replace('/','\\'))
			self.menu.Append( 7, 'Flip Clipboard Path')
			self.menu.Bind( wx.EVT_MENU, self.menuSelect_evnt )
			self.PopupMenu( self.menu, event.GetPoint() )
		#parse message


	def RightClickItems( self, event ):
		print('RightClickItems()')
		text = event.GetText()
		text = text.split('\n')[0][5:]
		if text[-3:] == '   ': #this asset or file without extension
			if text[-9:] == '         ':
				asset_dir_file = 2
				self.selpath = self.GetParent().CurrentPath + '/' + text.replace(' ', '')
			else:
				asset_dir_file = 0
				self.selpath = self.GetParent().CurrentPath + '/' + text.replace(' ', '')
		elif text[-7:] == 'FOLDER ':
			asset_dir_file = 1
			self.selpath = self.GetParent().CurrentPath + '/' + text.replace('FOLDER ', '').replace(' ','')
		else:
			asset_dir_file = 2
			self.selpath = self.GetParent().CurrentPath + '/' + text.split('   ')[0].replace(' ', '')
		#p(self.selpath)
		#p(asset_dir_file)

		#self.selpath = self.GetParent().CurrentPath + '/' + sel
		check = False

		#if '|' in self.selpath:
		#f	fifile = self.selpath.split('|',)
		if asset_dir_file == 0 or asset_dir_file== 1:
			if os.path.isdir(self.selpath):
				#folder menu
				check = True
				print('folder')
		else:
			if os.path.isfile(self.selpath):
				#file menu
				check = True
				print('file')
		if check:
			menuitems = ['Go Up', 'Reveal in location' ,'Open with preferred Application']
			#add Menu Copy Lin win Relative Lin relative Win
			#partial(self.option_chosen, 1),menu_item_1)
			self.menu = wx.Menu()
			i = 0
			for mi in menuitems:
				self.menu.Append( i, mi)
				i+=1
			splselpath = self.selpath.split('/')
			rslice = int(-(len(splselpath)/2))
			self.relL = '/'.join(splselpath[rslice:])
			self.menu.Append( 3, 'Copy linux path') #+ self.selpath)
			#self.menu.Append( 4, '	or relative :\t../' + self.relL)
			self.menu.Append( 5, 'Copy win path') #+ self.selpath.replace('/','\\'))
			#self.menu.Append( 6, '	or relative:\t..\\' + self.relL.replace('/','\\'))
			self.menu.Append( 7, 'Flip Clipboard Path')
			self.menu.Bind( wx.EVT_MENU, self.menuSelect_evnt )
			self.PopupMenu( self.menu, event.GetPoint() )
		#parse message


	def menuSelect_evnt( self, event):
		id_selected = event.GetId()

		path = self.selpath
		rpath = self.relL
		if id_selected == 0: #GO UP
			#si = self.GetFirstSelected()
			#self.Select(si,False)
			self.GetParent().toUpFolder(None)
		elif id_selected == 2:
			try:
				os_sep = Lin_Win_and_sep()
				pp = path.replace('/',os_sep[1])
				if os_sep[0] == 0: #Linux Mac
					subprocess.Popen(["xdg-open", pp],shell=False)
				else: #WINDa
					os.startfile(pp)
			except:
				print('Application not prefered for this file: \n	' + pp)
		elif  id_selected == 1:
			cmds = r'explorer /select,"'+ path.replace('/','\\') + '"'
			os_sep = Lin_Win_and_sep()
			path = '/'.join(path.split('/')[:-1])
			pp = path.replace('/',os_sep[1])
			if os_sep[0] == 0:
				subprocess.Popen(["xdg-open", pp], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			else:
				subprocess.Popen(cmds, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		elif id_selected == 7:
			toggleConvertPath()
		elif  id_selected > 2:
			if id_selected == 3 or id_selected == 5 :
				if id_selected == 3:
					#linus
					print('clipboard:', path)
					if ' ' in path:
						path = path.replace(' ', '')
					if path[0] == '/':
						if path[0] != path[1]:
							path = '/' + path
					wxToClip(path)
				else:
					#wind
					print( 'clipboard', path.replace('/','\\'))
					if ' ' in path:
						path = path.replace(' ', '')
					#if path[0] == '/':
					#	if path[0] != path[1]:
					#		path = '/' + path
					wxToClip(path.replace('/','\\'))
			else:
				if id_selected == 4:
					print( 'clipboard', rpath)
					if rpath[-1] == ' ':
						rpath = rpath[:-1]
					wxToClip('../'+rpath)
				else:
					print( 'clipboard', rpath.replace('/','\\'))
					if rpath[-1] == ' ': rpath = rpath[:-1]
					wxToClip('..\\'+rpath.replace('/','\\'))

	def reDrawBackground(self):
		bc = 0
		item = -1
		while 1:
			item = self.GetNextItem(item, ULC.ULC_NEXT_ALL)
			if item == -1:
				break
			if bc == 0:
				bc = 1
				self.SetItemBackgroundColour(item, self.col)
			else:
				bc = 0
				self.SetItemBackgroundColour(item, self.col2)
		pass

	def reDrawSelBackground(self):
		item = -1
		while 1:
			item = self.GetNextItem(item, ULC.ULC_NEXT_ALL, ULC.ULC_STATE_SELECTED)
			if item == -1:
				break
			self.SetItemBackgroundColour(item, self.col3)
		pass

	def setNotFoundDir(self):
		self.InsertColumn(0, "", width=200)
		self.InsertStringItem(0,'not Found directory')

class Example(wx.Frame): # MAIN OBJECT FRAME 
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
		s = (795, 962)
		self.SetSize(s)
		self.SetMaxSize(s)
		self.SetMinSize(s)
		self.SetBackgroundColour(wx.Colour(100,100,100))
		self.LISTSPACES = LISTSPACES
		self.ASPACE = int(STARTSPACE)
		self.AFILT = ''
		self.ALET = ''
		self.AMODEFILT = '0 0 0'
		self.SORT_MODE = 0
		self.SORT_DATE = 0
		self.SORT_TAGS = 0
		self.ENB_FILLTER = 0
		self.CurrentPath = HOMEPATH
		self.SelectionPattern = HOMEPATH
		self.reSetupLISTSPACES(chSpaceTo=self.ASPACE) # set Active Space
		#8, wx.SWISS, wx.NORMAL,wx.NORMAL, False, u'Courier')
		#self.font_to_all = wx.Font(6, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Arial')
		#self.font_to_read = wx.Font(9, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Arial')
		self.font_to_all = wx.Font( wx.FontInfo(6))
		self.font_to_read = wx.Font( wx.FontInfo(9))
		#ico_path = 'nopreview.jpg'
		#img = wx.Image(ico_path, wx.BITMAP_TYPE_ANY)
		#bmp = img.Rescale(16,16,wx.IMAGE_QUALITY_HIGH)
		#self.SetIcon(bmp)
		self.setTitleState()
		self.InitUI()
		self.Centre()
		self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

	def OnCloseFrame(self,evn): # evt to close Window for
		self.saveState()
		self.Destroy()

	def setTitleState(self):
		#0~"C:/Users/ivank"+i+asf sfs~C:/Users/ivank+f+sfsf fsf~C:/Users/ivank++sfse~C:/Users/ivank++fsdf~
		s = self.ASPACE
		#s = 10
		ws = ''
		t = '--'
		for f in range(1,13):
			if f > 9:
				t = '---'
			if f == s+1:
				ws += ''+t+'|'
			else:
				ws += 'F'+str(f)+'|'
		pp = self.CurrentPath
		plus = ''
		if self.ALET != '':
			plus = ' + ' + self.ALET 
		#self.SetTitle(ws+'  '+pp+'+'+self.ALET)
		if len(pp) > 40:
			pp = pp[:15] +'.../'+ pp.split('/')[-2]+'/'+pp.split('/')[-1]
		self.SetTitle(ws+'  '+pp+plus)

	def reSetupLISTSPACES(self,chSpaceTo=-1, #F1 - F12 0-11
								chCurrentPatternTo='', #"C:/Users/ivank"+i
								chCurrentFilterTo='None', # fsfa fsf
								chCurrentQLetterTo='None', #"C:/Users/ivank"+i - i
								chCurrentSortFiltModeTo='None'): # SORT_MODE ENB_FILTER
		if chSpaceTo != -1:
			cs = self.LISTSPACES[chSpaceTo]
			cs_spl = cs.split('|||')
			self.AFILT = cs_spl[1]
			self.ALET = cs_spl[-1].split('+')[-1]
			self.AMODEFILT = cs_spl[2]
			self.SelectionPattern = cs_spl[-1].split('+')[0]
			self.CurrentPath = selPatternToCurrentPath(self.SelectionPattern)
			spl = self.AMODEFILT.split(' ')
			self.SORT_DATE = 0
			self.SORT_TAGS = 0
			self.ENB_FILLTER = 0
			if spl[0] == '1':
				self.SORT_DATE = 1
				self.SORT_TAGS = 0
			if spl[1] == '1':
				self.SORT_TAGS = 1
				self.SORT_DATE = 0
			if spl[2] == '1':
				self.ENB_FILLTER = 1
			new_space = '|||'+self.AFILT+'|||'+self.AMODEFILT+'|||'+self.SelectionPattern+'+'+self.ALET
			self.ASPACE = chSpaceTo
			self.LISTSPACES[chSpaceTo] = new_space

		if chCurrentPatternTo != '': # change Current path "C:/Users/ivank"|"C:/Users/ivank"
			s = self.ASPACE
			self.CurrentPath = selPatternToCurrentPath(chCurrentPatternTo)
			self.SelectionPattern = chCurrentPatternTo
			new_space = '|||'+self.AFILT+'|||'+self.AMODEFILT+'|||'+self.SelectionPattern+'+'+self.ALET
			self.LISTSPACES[s] = new_space # Only active list space item set new element

		if chCurrentFilterTo != 'None':
			s = self.ASPACE
			self.AFILT = chCurrentFilterTo
			new_space = '|||'+self.AFILT+'|||'+self.AMODEFILT+'|||'+self.SelectionPattern+'+'+self.ALET
			self.LISTSPACES[s] = new_space

		if chCurrentQLetterTo != 'None':
			s = self.ASPACE
			self.ALET = chCurrentQLetterTo
			new_space = '|||'+self.AFILT+'|||'+self.AMODEFILT+'|||'+self.SelectionPattern+'+'+self.ALET
			self.LISTSPACES[s] = new_space

		if chCurrentSortFiltModeTo != 'None': # date change to date  tags or fillter TOGGLES
			s = self.ASPACE
			ef = str(self.ENB_FILLTER)
			tg = self.sorted_by_tags.GetValue()
			dt = self.sorted_by_date.GetValue()
			filt = ''
			if chCurrentSortFiltModeTo == 'date':
				if dt != 0:
					filt =  '1 0 ' + ef
					dt = 1
					tg = 0
					self.SORT_MODE = 1
				else:
					filt =  '0 0 ' + ef
					dt = 0
					tg = 0
					self.SORT_MODE = 0

			if chCurrentSortFiltModeTo == 'tags':
				if tg != 0:
					filt =  '0 1 ' + ef
					tg = 1
					dt = 0
					self.SORT_MODE = 2
				else:
					filt =  '0 0 ' + ef
					tg = 0
					dt = 0
					self.SORT_MODE = 0
			if chCurrentSortFiltModeTo == 'eflt':
				if self.ENB_FILLTER == 0:
					filt =  str(int(dt)) + ' ' +str(int(tg)) + ' 1'
					self.ENB_FILLTER = 1
				else:
					filt =  str(int(dt)) + ' ' +str(int(tg)) + ' 0'
					self.ENB_FILLTER = 0

			self.AMODEFILT = filt
			new_space = '|||'+self.AFILT+'|||'+self.AMODEFILT+'|||'+self.SelectionPattern+'+'+self.ALET
			self.LISTSPACES[s] = new_space
			ts = timeStamp(1)[-5:]
			if chCurrentSortFiltModeTo == 'eflt':
				print(ts + ' Filter/Search: ', self.ENB_FILLTER)
			else:
				print(ts+' Sort Mode: ',self.SORT_MODE)

			update_toggle_colors(self.sorted_by_date, bool(int(filt.split(' ')[0])))
			self.sorted_by_date.SetValue(dt)
			update_toggle_colors(self.sorted_by_tags, bool(int(filt.split(' ')[1])))
			self.sorted_by_tags.SetValue(tg)
			update_toggle_colors(self.filter_toggle , self.ENB_FILLTER)
			self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
			self.list_files_assets.setMyList(True,self.listitemsTuple)
			self.list_files_assets.reDrawBackground()
		pass
		 # from current space set current Path Selection pattern

	def currentTabsLocationQuickLetterActiveTAB(self,activeTab_tPATHs='',changeQuickletter='',changeActiveTab=''): # set Current Path and Quickletter
		#0~"C:/Users/ivank"+i+asf sfs~C:/Users/ivank+f+sfsf fsf~C:/Users/ivank++sfse~C:/Users/ivank++fsdf~
		print('tablocations:', activeTab_tPATHs)
		if activeTab_tPATHs != '':
			spl_activeTab_tPATHs = activeTab_tPATHs.split('~')
			active = int(spl_activeTab_tPATHs[0])
			apath = ''
			i = 0
			for ap in spl_activeTab_tPATHs[1:]:
				if i == active:
					apath = ap
				else: pass
				i+=1
			path_letter = apath.split('+')
			self.activeTab = active
			cp = selPatternToCurrentPath(path_letter[0])
			self.CurrentPath = cp
			self.CurrentSpaces = activeTab_tPATHs
			self.quickLetter = path_letter[1]
	
	def saveState(self): #  Save State to User file 
		mf = START_MAXFILEFOLDERS
		mil = START_MAXINFOLINES
		cat = self.CUR_COLLECTION
		spaces = ''
		for ws in self.LISTSPACES:
			try:
				dws = ws
			except:
				dws = ws
			if dws[-1] != '\n':
				spaces += dws+'\n'
			else:
				spaces += dws
		fline = str(mf)+'|||'+str(mil)+'|||'+str(cat)+'|||'+str(self.ASPACE)+'\n'
		notes = self.notes_book.GetValue()
		writeutf8(history_notes_filepath,fline+spaces+notes)
		ts = timeStamp(1)[-5:]
		print('Saved State to '+ history_notes_filepath)
		print(ts + ' Quit...')
		return None
	
	def InitUI(self): # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!	init MAIN Layout  !!!!!!!!!
		self.NotUpdate = 0
		vbox = wx.BoxSizer(wx.VERTICAL)
		#st = wx.StaticText(self,label="  OPEN WITH apps/utils (from $APPPATH/app_launchers):")
		#vbox.Add(st, flag=wx.EXPAND, border=40)
		gs = wx.GridSizer(1, len(COLLECTIONS), 2, 2) #neeed dynamic fill Apps from config
		self.CUR_COLLECTION = int(START_CATEGORY)
		self.catbtns = []
		indx = 0
		for col in COLLECTIONS:
			scol = col.split('_')
			self.catbtn = wx.Button(self, label=scol[1].replace('\n',''),style=wx.NO_BORDER,size=(100,20))
			#tooltip = al[2] +'\n'+ al[1] + ' {%listSel}'
			#btn.SetToolTip(wx.ToolTip(tooltip))
			self.catbtn.Bind(wx.EVT_BUTTON,self.set_collection_evnt)
			self.catbtn.SetFont(self.font_to_all)
			self.catbtn.SetForegroundColour(wx.Colour(0,0,0))
			self.catbtn.SetBackgroundColour(wx.Colour(100, 100, 100))
			if indx == self.CUR_COLLECTION:
				self.catbtn.SetForegroundColour(wx.Colour(255,255,75))
			self.catbtns.append(self.catbtn)
			gs.Add(self.catbtn,flag=wx.EXPAND)
			indx += 1
		vbox.Add(gs, proportion=0,flag=wx.EXPAND,  border=7) #flag=wx.EXPAND,
		# sizer init with 5 elements
		#SHELFA INIT
		self.toolsizer = wx.GridSizer(1, 5, 2, 2)
		self.toolList = []
		redrawToolPallete(self,self.CUR_COLLECTION)
		vbox.Add(self.toolsizer, proportion=0,flag=wx.EXPAND,  border=7) #flag=wx.EXPAND,		

		st = wx.StaticText(self,label="  CURRENT LOCATION: (selected items)  /  Sort  /  Filter" ) #+ "——"*23
		st.SetFont(self.font_to_all)
		st.SetForegroundColour(wx.Colour(0,0,0))
		vbox.Add(st, flag=wx.EXPAND, border=40)
		
		#gt = wx.GridBagSizer(1, 8)
		b = 5
		s = (28,28)
		gt = wx.BoxSizer(wx.HORIZONTAL)
		gt.AddSpacer(2)
		upb = wx.Button(self, label='go\nup',style=wx.NO_BORDER,size=s)
		upb.SetForegroundColour(wx.Colour(0,0,0))
		#upb.SetBackgroundColour((251,242,160))
		upb.SetBackgroundColour(wx.Colour(253,235,184))
		upb.SetFont(self.font_to_all)
		upb.Bind(wx.EVT_BUTTON,self.toUpFolder)
		
		gt.Add(upb, border=b) #pos=(0, 0)
		gt.AddSpacer(2)
		self.location_path_tx = wx.TextCtrl(self,size=(573,28),style=wx.TE_PROCESS_ENTER) #style = wx.TE_MULTILINE style=wx.TE_RIGHT style=wx.TE_LEFT
		self.location_path_tx.SetValue(self.SelectionPattern)
		self.location_path_tx.SetFont(self.font_to_read)
		self.location_path_tx.SetBackgroundColour(wx.Colour(255,255,255))
		self.location_path_tx.SetForegroundColour(wx.Colour(0,0,0))
		self.location_path_tx.SetInsertionPoint(len(self.CurrentPath))
		
		location_text_dt = MyTextDropTarget(self.location_path_tx, self,preclean=True)
		self.location_path_tx.SetDropTarget(location_text_dt)
		
		self.location_path_tx.Bind(wx.EVT_TEXT_ENTER, self.OnKeyENTER) #_ENTER
		

		gt.Add(self.location_path_tx, border=b) #pos=(0, 1), span=(1, 31), 
		gt.AddSpacer(2)
		self.sorted_by_date = wx.ToggleButton(self, label='info\ndate',style=wx.NO_BORDER,size=s)
		self.sorted_by_date.SetFont(self.font_to_all)
		self.sorted_by_date.SetForegroundColour(wx.Colour(0,0,0))
		self.sorted_by_date.Bind(wx.EVT_TOGGLEBUTTON, self.sorted_by_date_evnt)
		self.sorted_by_date.SetValue(self.SORT_DATE)
		self.sorted_by_tags = wx.ToggleButton(self, label='tags\nsize',style=wx.NO_BORDER,size=s)
		self.sorted_by_tags.SetFont(self.font_to_all)
		self.sorted_by_tags.SetForegroundColour(wx.Colour(0,0,0))
		self.sorted_by_tags.Bind(wx.EVT_TOGGLEBUTTON, self.sorted_by_tags_evnt)
		self.sorted_by_tags.SetValue(self.SORT_TAGS)
		update_toggle_colors(self.sorted_by_tags)
		update_toggle_colors(self.sorted_by_date)

		gt.Add(self.sorted_by_date, border=b) #pos=(0, 32),
		gt.AddSpacer(2)
		gt.Add(self.sorted_by_tags, border=b) #pos=(0, 33),
		gt.AddSpacer(2)
		
		self.search_byLabel_tx = wx.TextCtrl(self,style=wx.TE_CENTRE,size=(80,28))
		filter_text_dt = MyTextDropTarget(self.search_byLabel_tx, self, preclean=True)
		self.search_byLabel_tx.SetDropTarget(filter_text_dt)
		self.search_byLabel_tx.SetFont(self.font_to_read)
		self.search_byLabel_tx.SetBackgroundColour(wx.Colour(255,255,255))
		self.search_byLabel_tx.SetForegroundColour(wx.Colour(0,0,0))
		self.search_byLabel_tx.Bind(wx.EVT_TEXT,self.text_filter_changed)

		if self.AFILT != '':
			self.search_byLabel_tx.SetValue(self.AFILT)

		gt.Add(self.search_byLabel_tx, border=b) #pos=(0, 34), span=(1, 0), flag=wx.EXPAND,
		gt.AddSpacer(2)

		self.filter_toggle = wx.ToggleButton(self, style=wx.NO_BORDER, label='filter', size=s)
		self.filter_toggle.SetFont(self.font_to_all)
		self.filter_toggle.SetForegroundColour(wx.Colour(0,0,0))
		self.filter_toggle.Bind(wx.EVT_TOGGLEBUTTON, self.enb_filter_evnt)
		self.filter_toggle.SetValue(self.ENB_FILLTER)

		gt.Add(self.filter_toggle, border=b) #pos=(0, 35), flag=wx.EXPAND,
		
		vbox.Add(gt, border=2) #flag=wx.EXPAND,

		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
		self.list_files_assets = myList(self, size=(488, 605))
		self.list_files_assets.setMyList(True, self.listitemsTuple)
		#self.list_files_assets.SetSingleStyle(wx.LC_SINGLE_SEL)		
		self.list_files_assets.SetSize((488, 606))
		self.list_files_assets.reDrawBackground()
		self.list_files_assets.reDrawSelBackground()
		self.list_files_assets.Bind(wx.EVT_LIST_ITEM_SELECTED, self.SetLocation_path_txFromListAndSelection)
		self.list_files_assets.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.SetLocation_path_txFromListAndSelection)
		self.list_files_assets.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.SetLocationNewListDouble)
		self.list_files_assets.Bind(wx.EVT_LIST_BEGIN_DRAG, self.Begin_drag_From_List)
		self.list_files_assets.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

		update_toggle_colors(self.filter_toggle, self.ENB_FILLTER)

		st = wx.StaticText(self, label="  LIST: (assets/folders/files)  /  NOTES:   ")#+"——"*24
		vbox.Add(st, flag=wx.EXPAND, border=1)
		st.SetFont(self.font_to_all)
		st.SetForegroundColour(wx.Colour(0,0,0))

		ln = wx.BoxSizer(wx.HORIZONTAL) 
		ln.AddSpacer(2)
		ln.Add(self.list_files_assets) #,flag=wx.EXPAND
		ln.AddSpacer(2)

		self.notes_book = wx.TextCtrl(self,style = wx.TE_MULTILINE,size=(286,606)) #|wx.TE_DONTWRAP
		self.notes_book.SetFont(self.font_to_read)
		self.notes_book.SetBackgroundColour ((40,41,38))
		self.notes_book.SetForegroundColour(wx.Colour(130,130,120))
		self.notes_book.Bind(wx.EVT_MIDDLE_DOWN,self.onDragFromNotes)

		text_dt = MyTextDropTarget(self.notes_book,self)
		self.notes_book.SetDropTarget(text_dt)


		self.notes_book.SetValue(STARTNOTES)
		#ln.Add(location_path_tx, pos=(0, 0), span=(34, 33),flag=wx.EXPAND ,border=40)
		ln.Add(self.notes_book,flag=wx.EXPAND)

		vbox.Add(ln, flag=wx.EXPAND, border=7)

		st = wx.StaticText(self,label="  WORK INFO:  / Create New Folder /  Create or Edit Tags  / Set Color / Add Info") #+"——"*22
		st.SetFont(self.font_to_all)
		st.SetForegroundColour(wx.Colour(0,0,0))
		vbox.Add(st, flag=wx.EXPAND, border=40)

		info_sizer = wx.BoxSizer(wx.HORIZONTAL)
		vbox.Add(info_sizer, flag=wx.EXPAND, border=40)
		
		


		button_info_sizer = wx.BoxSizer(wx.VERTICAL)
		info_sizer.AddSpacer(2)
		size_colors = (32, 17)

		button_info_sizer.AddSpacer(2)
		colors = [(255, 73, 73), (255, 142, 2), (0, 154, 218), (140, 214, 233),
					(136, 105, 184), (50, 114, 80), (208, 251, 199), (253, 228, 167)]
		colorsSizer = wx.GridSizer(rows=8, cols=1,hgap=2, vgap=2)
		i = 1
		for c in colors:
			l = str(i)
			capture_icon_btn = wx.Button(self, label=l, style=wx.NO_BORDER, size=size_colors)
			capture_icon_btn.SetFont(self.font_to_all)
			capture_icon_btn.SetForegroundColour(wx.Colour(5,5,5))
			capture_icon_btn.SetBackgroundColour(wx.Colour(c))
			capture_icon_btn.SetToolTip(str(c))
			capture_icon_btn.Bind(wx.EVT_BUTTON,self.setColorToSelected)
			colorsSizer.Add(capture_icon_btn,border=10)
			i += 1

		button_info_sizer.Add(colorsSizer,border=4)
		info_sizer.Add(button_info_sizer, border=40)
		info_sizer.AddSpacer(4)
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		self.MAXINFOLINES = START_MAXINFOLINES
		self.path_comments = self.location_path_tx.GetValue()
		self.info_lines_txt = myList(self, size=(740,160))
		self.info_lines_txt.SetSize((740,160))
		self.info_lines_txt.reDrawBackground()
		self.info_lines_txt.Bind(wx.EVT_LIST_BEGIN_DRAG, self.Begin_drag_From_Info)

		self.OnKeyENTER(None)

		info_sizer.Add(self.info_lines_txt, border=40)
		vbox.AddSpacer(2)

		send_panel = wx.BoxSizer(wx.HORIZONTAL)
		send_panel.AddSpacer(2)

		size2 = (38, 25)
		file_dir_operations_sizer = wx.GridSizer(rows=2, cols=4,hgap=1, vgap=1)
		#fileops = ['newFld','eTags','copy..','rename','move..','backup','..TO','delete']
		# del bc rn nf co mo to et
		fileops = ['delete','backup','rename','newFld','copy..','move..','..TO','eTags']
		tooltips = ['-DL Delete File or Folder commad, then press CONFIRM',
					'-BC Duplicate File or Folder to backup Folder command, then press CONFIRM',
					'-RN Select Item(s) in list for Rename, set new name for file or folder, then press CONFIRM',
					'-NF New Folder command, set name for new forder, then press CONFIRM',
					'-CP Select Item(s) in list for Copy, press this button for copy command, them select item Folder or File to Replace and press [..to], then press CONFIRM',
					'-MV Select Item(s) in list for Move, press this button for move command, them select item Folder or File to Replace and press [..to], then press CONFIRM',
					'-TO Set destination File or Folder Copy or Move command',
					'-ET Edit Tags command, edit tags, then press CONFIRM'				
					]
					

		colors_filops = [	(75, 5, 75), # del
							(5, 75, 5), # bc
							(15, 25, 15), # rn
							(15, 75, 15),  # NF
							(55, 5, 5),  # co
							(55, 5, 5),  # mo
							(55, 5, 5), # to
							(15, 15, 75)  # ET
											]
		i=0
		for fileop in fileops:
			filop_btn = wx.Button(self, label=fileop, style=wx.NO_BORDER, size=size2)
			filop_btn.SetFont(self.font_to_all)
			filop_btn.SetForegroundColour(wx.Colour(200,200,200))
			filop_btn.SetBackgroundColour(colors_filops[i])
			filop_btn.SetForegroundColour(wx.Colour(255, 255, 255))
			filop_btn.SetToolTip(tooltips[i])
			filop_btn.Bind(wx.EVT_BUTTON, self.file_operation_evnt)

			file_dir_operations_sizer.Add(filop_btn, border=3)
			i+=1

		send_panel.Add(file_dir_operations_sizer,border=1)

		send_panel.AddSpacer(2)


		vbox.Add(send_panel, flag=wx.EXPAND, border=40)

		self.send_txt = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(546, 47))
		self.send_txt.Bind(wx.EVT_TEXT, self.Ctrl_ENTER_SEND_TEXT_evnt)
		#send_txt_dt = MyTextDropTarget(self.send_txt, preclean=False)
		#self.send_txt.SetDropTarget(send_txt_dt)
		self.send_txt.SetBackgroundColour(wx.Colour(255,255,255))
		self.send_txt.SetForegroundColour(wx.Colour(0,0,0))
		self.send_txt.SetFont(self.font_to_read)
		send_file_dt = FileDrop(self.send_txt, preclean=False)
		self.send_txt.SetDropTarget(send_file_dt)


		send_panel.Add(self.send_txt, flag=wx.EXPAND, border=7)
		send_panel.AddSpacer(2)

		add_info_line_btn = wx.Button(self, label='ADD INFO /\n..CONFIRM', style=wx.NO_BORDER, size=(69,40))
		add_info_line_btn.SetBackgroundColour(wx.Colour(2, 2, 2))
		add_info_line_btn.SetForegroundColour(wx.Colour(255, 255, 255))
		add_info_line_btn.SetFont(self.font_to_read)
		add_info_line_btn.Bind(wx.EVT_BUTTON, self.Add_INFO_CONFIRM_evnt)
		send_panel.Add(add_info_line_btn, flag=wx.EXPAND, border=7)
		self.SetSizer(vbox)

	def onKeyPress(self,event):
		keycode = event.GetKeyCode()
		#i = self.list_files_assets.GetFocusedItem()
		
		fkeys = {340:0, 341:1, 342:2, 343:3, 344:4, 345:5, 346:6, 347:7, 348:8, 349:9, 350:10, 351:11}
		if keycode in fkeys:
			to_space = fkeys[keycode]
			print('SWITCH FSPACE:', to_space)
			self.reSetupLISTSPACES(chSpaceTo=to_space)
			self.sorted_by_tags.SetValue(self.SORT_TAGS)
			self.sorted_by_date.SetValue(self.SORT_DATE)
			update_toggle_colors(self.sorted_by_tags,self.SORT_TAGS)
			update_toggle_colors(self.sorted_by_date,self.SORT_DATE)
			
			self.location_path_tx.SetValue(self.SelectionPattern)
			self.location_path_tx.SetInsertionPoint(len(self.SelectionPattern))
			
			self.filter_toggle.SetValue(0)
			self.search_byLabel_tx.SetValue(self.AFILT)
			update_toggle_colors(self.filter_toggle, self.ENB_FILLTER)
			self.SetListAndSelectionFromLocation_path_tx()
		
		qkeys = {49:'1', 50:'2', 51:'3', 52:'4', 53:'5', 54:'6', 55:'7', 56:'8', 57:'9', 48:'0',
					81:'q', 87:'w', 69:'e', 82:'r', 84:'t', 89:'y', 85:'u', 73:'i', 79:'o', 80:'p',
					65:'a', 83:'s', 68:'d', 70:'f', 71:'g', 72:'h', 74:'j', 75:'k', 76:'l',
					90:'z', 88:'x', 67:'c', 86:'v', 66:'b', 78:'n', 77:'m'}
		if keycode in qkeys:
			quick = qkeys[keycode]
			print('QUICK KEY:', quick)
			if self.ALET != quick:
				self.reSetupLISTSPACES(chCurrentQLetterTo=quick)
				self.SetListAndSelectionFromLocation_path_tx()
				self.list_files_assets.Focus(0)
				self.list_files_assets.Update()
			else:
				self.reSetupLISTSPACES(chCurrentQLetterTo='')
				self.SetListAndSelectionFromLocation_path_tx()


		if keycode == 27:
			print('DISABLE QUICK KEY')
			self.reSetupLISTSPACES(chCurrentQLetterTo='')
			self.SetListAndSelectionFromLocation_path_tx()


		if keycode == 349:
			print('LOCK F10 Key!!!')
		if event.AltDown() and keycode == 315:
			print('atl up')
			self.toUpFolder(event, IFKEY=True)
		if keycode == 8:
			print('backspace')
			self.toUpFolder(event, IFKEY=False)

	def setColorToSelected(self, evt): # set color to selected items
		paths = self.location_path_tx.GetValue()
		btn = evt.GetEventObject()
		tt = btn.GetToolTip().GetTip()
		spl = [paths]
		if '|' in paths:
			spl = paths.split('|')
		if paths[0] == '"':
			if '|' in paths:
				sp = paths.split('|')
				for p in sp:
					reColorMarker(p,tt)
			else:
				reColorMarker(paths,tt)
		ts = timeStamp(1)[-5:]
		print(ts + ' New Color to item(s)...')
		#self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
		#self.list_files_assets.setMyList(True,self.listitemsTuple)
		#self.list_files_assets.Focus(l)
		#self.list_files_assets.SetSize((488,606))
		#self.list_files_assets.reDrawBackground()
		#self.list_files_assets.reDrawSelBackground()
		#self.list_files_assets.Update()
		self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
		l = self.list_files_assets.setMyList(True,self.listitemsTuple,selectedItems=spl)
		try:
			self.list_files_assets.Focus(l)
		except:pass
		self.list_files_assets.SetSize((488,606))
		self.list_files_assets.reDrawBackground()
		self.list_files_assets.reDrawSelBackground()
		self.list_files_assets.Update()
		#self.UpdateInfoList()

		#self.list_files_assets.setMyList(True,self.listitemsTuple)
		#self.SetListAndSelectionFromLocation_path_tx()
		pass

	def set_collection_evnt(self, evt): # Redraw Pallete
		indx = 0
		for catbtn in self.catbtns:
			if evt.Id != catbtn.Id:
				catbtn.SetForegroundColour(wx.Colour(0,0,0))
			else:
				catbtn.SetForegroundColour(wx.Colour(255,255,75))
				self.CUR_COLLECTION = indx
			indx +=1
		ts = timeStamp(1)[-5:]
		print(ts + ' TOOL COLLECTION to: ',self.CUR_COLLECTION)
		redrawToolPallete(self,self.CUR_COLLECTION)
	
	def run_tool(self,event): # Run Tool with Args
		args = self.location_path_tx.GetValue()
		if '|' in self.location_path_tx.GetValue():
			args = self.location_path_tx.GetValue().replace('|', ' ')
		btn = event.GetEventObject()
		tt = btn.GetToolTip().GetTip()
		cmds = tt.split('\n\n')[0].replace('<SEL_ITEMS>',args.replace('"',''))
		ts = timeStamp(1)[-5:]
		print(ts+' RUN TOOL',cmds)
		#subprocess.call(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		outfile = open(HOMEPATH+'/wxBro.log', 'a+') #same with "w" or "a" as opening mode
		outfile.write('\n----\n'+ts+' RUN TOOL: '+cmds+'->\n')
		print(cmds)
		subprocess.Popen(cmds.split(' '), stdout=outfile,stderr=outfile)
		return None
		with open(HOMEPATH+'/wxBro.log', 'a+') as f:
			f.write(cmds)  # replace 'w' with 'wb' for Python 3
			process = subprocess.Popen(cmds, stdout=subprocess.PIPE)
			for c in iter(lambda: process.stdout.read(1), ''):  # replace '' with b'' for Python 3
				f.write(c)
		return None

	def UpdateInfoList(self): # when focu item setMyList RedrawBackground
		focus_index = self.list_files_assets.GetFocusedItem()
		#t = self.list_files_assets.GetItem(focus_index).Get #DeleteItem
		#self.list_files_assets.DeleteItem(c-1)
		if focus_index == -1:
			focus_name = ''
		else:
			focus_name = self.listitemsTuple[focus_index][1]
		self.path_comments = self.CurrentPath +'/'+ focus_name

		if os.path.isdir(self.path_comments):
			item_comments = getInfoLinesFromPath(self.path_comments)
			self.info_lines_txt.setMyList(False,item_comments)
			self.info_lines_txt.reDrawBackground()
			count = self.info_lines_txt.GetItemCount()
			if count > 1 :
				self.info_lines_txt.Focus(count-1)
				self.info_lines_txt.Update()
		else:
			self.info_lines_txt.ClearAll()

	def Add_INFO_CONFIRM_evnt(self, evt):  # Add folder Add Tags Add Info
		ts = timeStamp(1)[-5:]
		print(ts+' Parse Add Info/CONFIRM..')
		info_or_command = self.send_txt.GetValue()
		fileops = ['-NF', '-ET', '-CP', '-RN', '-MV', '-BC', '-DL','-FI','-FF']
		if info_or_command != '':
			if info_or_command[-1] == '\n':
				if info_or_command[-2] == '\t':
					info_or_command = info_or_command[:-2]
			if info_or_command[:3] in fileops:
				if info_or_command[:3] == '-NF':
					folderto = info_or_command.split('(')[1].split(')')[0]
					oldfoldername = info_or_command.split(' ',1)[1].replace('\t\n','').replace('\n(corrected!)','').replace('\n(already exist!)','')
					newfoldername = transliterate(oldfoldername)
					nonsy = 'qwertyuiopasdfghjklzxcvbnm_QWERTYUIOPASDFGHJKLZXCVBNM1234567890'
					res = ''
					er = 0
					for char in newfoldername:
						if not char in nonsy:
							char = '_'
							er = 1
						res +=char.lower()
					if ' ' in res or er == 1:
						#make Correct Folder Name need disable kirirlicy
						# check name in folder alredy
						res = res.replace(' ', '_')
						#nf = transliterate(newfoldername)
						newtexe = info_or_command.split(' ',1)[0] + ' ' + res + '\n(corrected!)'
						self.send_txt.SetValue(newtexe)
						return None
					if os.path.isdir(folderto+res):
						existfolder_cmd = info_or_command.replace(oldfoldername,res)
						self.send_txt.SetValue(existfolder_cmd+'\n(already exist!)')
						return None
					if os.path.isdir(folderto):
						os.umask(0000)
						os.mkdir(folderto+res)
						self.send_txt.SetValue('')
						self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
						l = self.list_files_assets.setMyList(True,self.listitemsTuple,selectedItems=[res])
						try:
							self.list_files_assets.Focus(l)
						except:pass
						self.list_files_assets.SetSize((488,606))
						self.list_files_assets.reDrawBackground()
						self.list_files_assets.reDrawSelBackground()
						self.list_files_assets.Update()
						self.UpdateInfoList()
						return None
					else:
						print('folder_to_not_dir')
						return None
				elif info_or_command[:3] == '-ET':
					tagsto = info_or_command.split('(')[1].split(')')[0]
					newtags = info_or_command.split(' ',1)[-1].replace('\t\n','')
					filetags = tagsto+'/.infolabel/000000_000000.utf8'
					if os.path.isdir(tagsto+'/.infolabel'):
						if os.path.isfile(filetags):
							writeutf8(filetags,newtags)
						else:
							writeutf8(filetags,newtags)
					else:
						os.mkdir(tagsto+'/.infolabel')
						writeutf8(filetags,newtags)
					self.send_txt.SetValue('')
					self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
					l = self.list_files_assets.setMyList(True,self.listitemsTuple,selectedItems=[tagsto])
					self.list_files_assets.Focus(l)
					self.list_files_assets.SetSize((488,606))
					self.list_files_assets.reDrawBackground()
					self.list_files_assets.reDrawSelBackground()
					self.list_files_assets.Update()
					self.UpdateInfoList()
				
				elif info_or_command[:3] == '-FI':
					print('Full Info Command: -FI')
					self.info_lines_txt.setOtherMaxInfoNums(5000)
					self.UpdateInfoList()
					self.info_lines_txt.setOtherMaxInfoNums(15)
					self.send_txt.SetValue('')

				elif info_or_command[:3] == '-FF':
					print('Full Files Command: -FF')
					self.list_files_assets.setOtherMaxFoldersNums(10000)
					self.list_files_assets.setMyList(True,self.listitemsTuple)
					self.list_files_assets.reDrawBackground()
					self.list_files_assets.reDrawSelBackground()
					self.list_files_assets.setOtherMaxFoldersNums(80)
					self.send_txt.SetValue('')
				elif info_or_command[:3] == '-CP':
					print('COPY_COMMAND_CONFIRM')
					#-CP(//dataserver/Project/MALYSH/person_files/Kirilovskih_I/test_project_aftica/asset2) (//dataserver/Project/MALYSH/person_files/Kirilovskih_I/test_project_aftica/gogogogogog_porusski_sukableat//) REPLACE!?!?!? press CONFIRM
					#-CP(//dataserver/Project/MALYSH/person_files/Kirilovskih_I/test_project_aftica/to_copy_file.txt) (//dataserver/Project/MALYSH/person_files/Kirilovskih_I/test_project_aftica/lin_new_test/) press CONFIRM to Copy Or Replace
					cp_cmd_short = info_or_command.replace('-CP(', '').replace(') (','->').replace(') press CONFIRM to Copy Or Replace File/Folder','')
					print(cp_cmd_short)
					spl_cp_cmd_short = cp_cmd_short.split('->')
					src = spl_cp_cmd_short[0]
					name = os.path.basename(src)
					dst_folder = spl_cp_cmd_short[1]
					if os.path.isfile(src):
						shutil.copyfile(src,dst_folder+'/'+name)
					else:
						shutil.copytree(src,dst_folder+'/'+name)
					self.send_txt.SetValue('')
					self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
					l = self.list_files_assets.setMyList(True,self.listitemsTuple,selectedItems=[name])
					try:
						self.list_files_assets.Focus(l)
					except:pass
					self.list_files_assets.SetSize((488,606))
					self.list_files_assets.reDrawBackground()
					self.list_files_assets.reDrawSelBackground()
					self.list_files_assets.Update()

				elif info_or_command[:3] == '-MV':
					print('MOVE_COMMAND_CONFIRM')
					cp_cmd_short = info_or_command.replace('-MV(', '').replace(') (','->').replace(') press CONFIRM to Copy Or Replace File/Folder','')
					print(cp_cmd_short)
					spl_cp_cmd_short = cp_cmd_short.split('->')
					src = spl_cp_cmd_short[0]
					name = os.path.basename(src)
					dst_folder = spl_cp_cmd_short[1]
					shutil.move(src,dst_folder+'/'+name)
					self.send_txt.SetValue('')
					self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
					l = self.list_files_assets.setMyList(True,self.listitemsTuple,selectedItems=[name])
					try:
						self.list_files_assets.Focus(l)
					except:pass
					self.list_files_assets.SetSize((488,606))
					self.list_files_assets.reDrawBackground()
					self.list_files_assets.reDrawSelBackground()
					self.list_files_assets.Update()
				elif info_or_command[:3] == '-DL':
					print('DELETE_COMMAND_CONFIRM')
					#-DL(//dataserver/Project/MALYSH/person_files/Kirilovskih_I/test_project_aftica/readme_zdgy.txt) pressCONFIRM to Delete File
					file = info_or_command.replace('-DL(', '').replace(') pressCONFIRM to Delete File','')
					if os.path.isfile(file):
						os.remove(file)
						print('Removed file: '+file)
						self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
						self.list_files_assets.setMyList(True,self.listitemsTuple,selectedItems=[])
						self.list_files_assets.SetSize((488,606))
						self.list_files_assets.reDrawBackground()
						self.list_files_assets.reDrawSelBackground()
						self.list_files_assets.Update()
						self.send_txt.SetValue('')
					else:
						print('Delete Not Worked With Folders')

				elif info_or_command[:3] == '-RN':
					print('RENAME_COMMAND_CONFIRM')
					#-RN(//dataserver/Project/MALYSH/person_files/Kirilovskih_I/test_project_aftica/nava_umask) new_rename
					from_to = info_or_command.split(' ',1)
					src = from_to[0].replace('-RN(','').replace(')','')
					name = src.split('/')[-1]
					new_name = from_to[1].replace(' ','_').lower()
					if new_name == 'setNEWnameANDpressCONFIRM'.lower():
						print('Set New Name for Item')
						return None
					new_name = transliterate(new_name)
					dst = from_to[0].replace('-RN(','').replace(name+')',new_name)
					os.rename(src,dst)
					print(dst)
					self.send_txt.SetValue('')
					self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
					l = self.list_files_assets.setMyList(True,self.listitemsTuple,selectedItems=[new_name])
					try:
						self.list_files_assets.Focus(l)
					except:pass
					self.list_files_assets.SetSize((488,606))
					self.list_files_assets.reDrawBackground()
					self.list_files_assets.reDrawSelBackground()
					self.list_files_assets.Update()

				elif info_or_command[:3] == '-BC':
					print('BACKUP_COMMAND_CONFIRM')
					#-BC(//dataserver/Project/MALYSH/person_files/Kirilovskih_I/test_project_aftica/o_russki_pishemi) pressCONFIRM to MAKE Backup file or directory
					file = info_or_command.replace('-BC(', '').replace(') pressCONFIRM to MAKE Backup file or directory','')
					if os.path.isfile(file):
						makeBakup(file)
						print('BACKUP Created to folder named <backup>')
						self.send_txt.SetValue('')
						self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
						l = self.list_files_assets.setMyList(True,self.listitemsTuple,selectedItems=['backup'])
						try:
							self.list_files_assets.Focus(l)
						except:pass
						self.list_files_assets.SetSize((488,606))
						self.list_files_assets.reDrawBackground()
						self.list_files_assets.reDrawSelBackground()
						self.list_files_assets.Update()
					else:
						print('Backup For Directory not work!')
						return None
			else:
				user = HOSTNAME+u'\n'+USERNAME # need get_user_pass
				ts = timeStamp(0)
				randint99 =  str(random.randrange(10,99))
				text = info_or_command
				#text = text.replace('\t','\n')
				if text != '':
					path_label_info  = self.path_comments + '/.infolabel'
					if os.path.isdir(self.path_comments):
						if not os.path.isdir(path_label_info):
							os.mkdir(path_label_info)
						new_file_comment = ts[:6] + '_' + ts[6:] + '_' + randint99 + '.utf8'
						new_file_path =path_label_info + '/' + new_file_comment
						writeutf8(new_file_path,user+'\n'+text)
						self.send_txt.SetValue('')
						self.UpdateInfoList()
					else:
						basename = os.path.basename(self.path_comments)
						dirname = os.path.dirname(self.path_comments)
						commentfile = dirname + '/.'+ basename
						writeutf8(commentfile,user+'\n'+text)
						self.send_txt.SetValue('')
						self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
						self.list_files_assets.setMyList(True,self.listitemsTuple)
						self.list_files_assets.SetSize((488,606))
						self.list_files_assets.reDrawBackground()
						self.list_files_assets.reDrawSelBackground()
						self.list_files_assets.Update()
						#self.UpdateInfoList()
	
	def Ctrl_ENTER_SEND_TEXT_evnt(self,event): # Event when send text Changed
		if self.send_txt.GetValue()[-2:] == '\t\n': # TAB -> ENTER for SEND
			self.Add_INFO_CONFIRM_evnt(None)
		if self.send_txt.GetValue()[:2] == '\t\n':
			self.send_txt.SetValue(self.send_txt.GetValue().replace('\t\n',''))
			self.Add_INFO_CONFIRM_evnt(None)

	def newFolder_evnt(self,event): # event Button NewFolder
		#where Folder
		# -newFolderTo(D:/test_project_wx/c001_collection — копия (13)) _writeNameAndConfirm_
		wf = self.CurrentPath+'/'
		self.send_txt.SetValue('-newFolderTo('+wf+') writeNAMEandCONFIRM')
		ts = timeStamp(1)[-5:]
		print(ts +' New Folder press CONFIRM')
		pass

	def file_operation_evnt(self,event): # event Button Edit Tags
		#where Folder
		# -editTagsFor("D:/test_project_wx/c001_collection/asset02_c001") _writeNewTagsAndConfirm_
		btn = event.GetEventObject()
		tt = btn.GetToolTip().GetTip()
		fileops = ['-NF', '-ET', '-CP', '-RN', '-MV', '-BC', '-TO', '-DL']
		fileop = tt[:3]
		snames = ['writeNAMEnewFOLDER', 'writeTAGSwithSPACESandCONFIRM',
					'Select Destination And Press ..TO, then CONFIRM',
					'writeNEWname','Select Destination And Press ..TO, then CONFIRM', 
					'Press CONFIRM to make Backup', 'press CONFIRM to apply',
					 'Delete This File???']
		if fileop in fileops:
			i = fileops.index(fileop)
			cp = self.CurrentPath+'/'
			fe = self.list_files_assets.GetFocusedItem()
			info = ''
			name = ''
			info = self.list_files_assets.GetItemText(fe)
			info=info[5:]
			name = info.split(' ',1)[0]
			sname = snames[i]
			if fileop != '-TO':
				if fileop == '-ET':
					tags = 'writeTAGSwithSPACESandCONFIRM'
					if fe != -1:
						if os.path.isdir(cp+name+'/.infolabel'):
							filetags = cp+name+'/.infolabel/000000_000000.utf8'
							if os.path.isfile(filetags):
								lines = readutf8_returnlistlines(filetags)
								tags = ' '.join(lines)
								#with open(filetags , 'r') as f:
								#	tags = f.read()
					self.send_txt.SetValue('-ET('+cp+name+') '+tags)
					ts = timeStamp(1)[-5:]
					print(ts+' '+sname)
				elif fileop == '-NF':
					wf = self.CurrentPath+'/'
					self.send_txt.SetValue('-NF('+wf+') '+sname)
					ts = timeStamp(1)[-5:]
					print(ts +' New Folder press CONFIRM')
				elif fileop == '-CP':
					if fe != -1:
						if os.path.isfile(cp+name) or os.path.isdir(cp+name):
							self.send_txt.SetValue('-CP('+cp+name+') ')
						else:
							print('')
				elif fileop == '-MV':
					if fe != -1:
						if os.path.isfile(cp+name) or os.path.isdir(cp+name):
							self.send_txt.SetValue('-MV('+cp+name+') ')
						else:
							print('Move only file (not Folders) !!! Select File')
				elif fileop == '-RN':
					if fe != -1:
						if os.path.isfile(cp+name) or os.path.isdir(cp+name):
							self.send_txt.SetValue('-RN('+cp+name+') '+ name)
						else:
							print('not to rename')
				elif fileop == '-BC':
					if fe != -1:
						if os.path.isfile(cp+name) or os.path.isdir(cp+name):
							self.send_txt.SetValue('-BC('+cp+name+') pressCONFIRM to MAKE Backup file or directory')
						else:
							print('not to backup')
				elif fileop == '-DL':
					if fe != -1:
						if os.path.isfile(cp+name):
							self.send_txt.SetValue('-DL('+cp+name+') pressCONFIRM to Delete File')
						else:
							print('Delete only file (not Folders) !!! Select File')
			else: # if pressed TO
				if fe != -1:
					print(cp)
					if os.path.isfile(cp) or os.path.isdir(cp):
						if os.path.isdir(cp):
							withname = cp
						else:
							withname = cp
						g = self.send_txt.GetValue()
						if g[:3] == '-CP' or g[:3] == '-MV':
							if not ') (' in g:
								g += '('+withname+') press CONFIRM to Copy Or Replace File/Folder'
								self.send_txt.SetValue(g)
						else:
							print('Select source File press copy or move then select destination press TO')
					else:
						print('Copy only files (not Folders) !!! Select File')
				pass
		pass

	def editTags_evnt(self,event): # event Button Edit Tags
		#where Folder
		# -editTagsFor("D:/test_project_wx/c001_collection/asset02_c001") _writeNewTagsAndConfirm_
		cp = self.CurrentPath+'/'
		fe = self.list_files_assets.GetFocusedItem()
		info = ''
		name = ''
		tags = 'writeTAGSandCONFIRM'
		if fe != -1:
			info = self.list_files_assets.GetItemText(fe)
			info=info[9:]
			name = info.split(' ',1)[0]
			if os.path.isdir(cp+name+'/.infolabel'):
				filetags = cp+name+'/.infolabel/000000_000000.utf8'
				if os.path.isfile(filetags):
					lines = readutf8_returnlistlines(filetags)
					tags = ' '.join(lines)
					#with open(filetags , 'r',encoding='utf-8') as f:
					#	tags = f.read()
		self.send_txt.SetValue('-editTagsFor('+cp+name+u') '+tags)
		ts = timeStamp(1)[-5:]
		print(ts+' Edit Tags press CONFIRM')
		pass

	def enb_filter_evnt(self, evt): # Button Filter tags 
		self.reSetupLISTSPACES(chCurrentQLetterTo='')
		self.reSetupLISTSPACES(chCurrentSortFiltModeTo='eflt')
		
	def sorted_by_date_evnt(self, evt): # button Sort by DATE
		self.reSetupLISTSPACES(chCurrentSortFiltModeTo='date')


	def sorted_by_tags_evnt(self, evt): # button Sort by TAGS
		self.reSetupLISTSPACES(chCurrentSortFiltModeTo='tags')

	def Begin_drag_From_List(self, evt): # Drop to App File not _use
		text = self.location_path_tx.GetValue()
		obj = evt.GetEventObject()
		data = wx.FileDataObject()
		if not '|' in text:
			fullpath = text.replace('"','')
			data.AddFile(fullpath)
		else:
			fullpaths = text.replace('"','').split('|')
			for file in fullpaths:
				data.AddFile(file)
		dropSource = wx.DropSource(obj)
		dropSource.SetData(data)
		dropSource.DoDragDrop()

	def Begin_drag_From_Info(self, evt): # Drop to App File not _use
		obj = evt.GetEventObject()
		inx_focus = obj.GetFocusedItem()
		item = obj.GetItem(inx_focus,2)
		text = item.GetText()
		print(text)
		my_data = wx.TextDataObject(text)
		dropSource = wx.DropSource(obj)
		dropSource.SetData(my_data)
		dropSource.DoDragDrop()

	def onDragFromNotes(self, evt):
		obj = evt.GetEventObject()
		selText = obj.GetStringSelection()
		my_data = wx.TextDataObject(selText)
		dropSource = wx.DropSource(obj)
		dropSource.SetData(my_data)
		dropSource.DoDragDrop()

	def OnKeyENTER(self, event): # when in list kye Enter
		self.reSetupLISTSPACES(chCurrentQLetterTo='')
		self.SetListAndSelectionFromLocation_path_tx()

	def text_filter_changed(self, event): #when changed Filter text
		t = event.GetEventObject().GetValue()
		self.reSetupLISTSPACES(chCurrentFilterTo=t)
		if self.ENB_FILLTER == 1:
			self.reSetupLISTSPACES(chCurrentQLetterTo='')
			self.SetListAndSelectionFromLocation_path_tx()
		else: pass


	def SetListAndSelectionFromLocation_path_tx(self): # When Paste selection text or path 
		location_to_parse = self.location_path_tx.GetValue()
		if '\\' in location_to_parse:
			location_to_parse = location_to_parse.replace('\\','/')
		if location_to_parse == '':
			self.list_files_assets.ClearAll()
			return None
		location_to_parse = location_to_parse.replace('\n','')
		if location_to_parse[-1] == ' ':
			location_to_parse=location_to_parse[:-1]
		if location_to_parse[0] == '"':
			if location_to_parse[-1] != '|':
				location_to_parse += '|'
		items = location_to_parse.split('|')
		if len(items) != 1:
			if items[0][0] == '"':
				path = items[0].replace('"','')
				dirpath = os.path.dirname(path)
				if os.path.isdir(dirpath):
					if dirpath[-1] != '/':
						dirpath = dirpath + '/'
						if '"' in dirpath:
							dirpath = dirpath.replace('"','')
					#self.CurrentPath = dirpath
					self.reSetupLISTSPACES(chCurrentPatternTo=dirpath)
					self.setTitleState()
					ts = timeStamp(1)[-5:]
					print(ts+' Set Current Location: ',self.CurrentPath)
					self.listitemsTuple = getFileItemsFromPath(dirpath,self)
					last_selectedindex = self.list_files_assets.setMyList(True,self.listitemsTuple,selectedItems=items)
					try: 
						self.list_files_assets.Focus(last_selectedindex)
						#self.list_files_assets.Selected(last_selectedindex)
					except: pass
					self.list_files_assets.reDrawBackground()
					self.list_files_assets.reDrawSelBackground()
					self.list_files_assets.Update()


				else: self.list_files_assets.ClearAll()
		else:
			if os.path.isdir(location_to_parse):
				if location_to_parse[-1] != '/':
					location_to_parse = location_to_parse + '/'
				#set List Location
				#self.CurrentPath = location_to_parse
				self.reSetupLISTSPACES(chCurrentPatternTo=location_to_parse)
				self.reSetupLISTSPACES(chCurrentQLetterTo='')
				self.setTitleState()
				print('set Current Location: ',self.CurrentPath)
				self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
				last_selectedindex = self.list_files_assets.setMyList(True,self.listitemsTuple)
				#self.list_files_assets.Focus(last_selectedindex)
				self.list_files_assets.reDrawBackground()
				self.list_files_assets.reDrawSelBackground()
				#self.list_files_assets.Update()
			else: self.list_files_assets.ClearAll();self.list_files_assets.setNotFoundDir()
		self.UpdateInfoList()
		pass

	def SetLocation_path_txFromListAndSelection(self,event): # get focus on list and open new location
		#focus = self.list_files_assets.GetFocusedItem()
		list_sel = []
		item = -1
		while 1:
			item = self.list_files_assets.GetNextItem(item, ULC.ULC_NEXT_ALL, ULC.ULC_STATE_SELECTED)
			if item == -1:
				break
			list_sel.append(item)
		string_to_current = ''
		for list_item in list_sel:
			try:
				selitem = self.listitemsTuple[list_item]
			except:
				return None
			sep = ''
			if len(self.CurrentPath) < 2: # this KOREN
				sep = self.CurrentPath[0]
			elif self.CurrentPath[-1] != '/':
				sep = '/'
			string_to_current += '|"'+self.CurrentPath+sep+selitem[1]+'"'
			pass
		if string_to_current != '':
			if string_to_current[0] == '|':
				string_to_current = string_to_current[1:]
		if list_sel == []:
			return None
			#if len(list_sel) == 1:
			#	string_to_current = string_to_current.replace('"','')
		self.reSetupLISTSPACES(chCurrentPatternTo=string_to_current) # SORT_MODE ENB_FILTER
		self.location_path_tx.SetValue(string_to_current)
		self.location_path_tx.SetInsertionPoint(len(string_to_current))
		self.list_files_assets.reDrawBackground()
		self.list_files_assets.reDrawSelBackground()
		if self.NotUpdate == 0:
			self.UpdateInfoList()
		pass

	def SetLocationNewListDouble(self,event): #event Double click on list items
		print('SetLocationNewListDouble')
		cp = self.CurrentPath
		sep = ''
		if cp[-1] != '/':
			sep = '/'
		cp += sep
		focused = None
		item = -1
		while 1:
			item = self.list_files_assets.GetNextItem(item, ULC.ULC_NEXT_ALL, ULC.ULC_STATE_FOCUSED)
			if item == -1:
				break
			focused = item
		selitem = self.listitemsTuple[focused]
		new_cp = cp+selitem[1]
		if os.path.isdir(new_cp):
			self.reSetupLISTSPACES(chCurrentPatternTo=new_cp)
			self.reSetupLISTSPACES(chCurrentQLetterTo='')
			self.setTitleState()
			ts = timeStamp(1)[-5:]
			print(ts + ' ENTER: ',self.CurrentPath)
			if self.CurrentPath[-1] != '/':
				self.CurrentPath += '/'
			self.reSetupLISTSPACES(chCurrentQLetterTo='')
			self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
			self.list_files_assets.setMyList(True,self.listitemsTuple)
			self.list_files_assets.Focus(0)
			self.list_files_assets.Select(0)
			self.list_files_assets.reDrawBackground()
		# c = self.list_files_assets.GetItemCount()
		# if c == 1:
		#	 self.list_files_assets.Append(' ')
		#	 self.list_files_assets.Append(' ')
			

	def toUpFolder(self,event,IFKEY=False): # button GO UP
		cp = self.CurrentPath
		if cp[-1] == '/':
			cp = cp[:-1]
		dirpath = os.path.dirname(cp)
		name = os.path.basename(cp)
		if os.path.isdir(dirpath):
			if dirpath[-1] != '/':
				dirpath += '/'
			self.NotUpdate = 1
			#self.CurrentPath = dirpath
			self.reSetupLISTSPACES(chCurrentQLetterTo='')
			self.reSetupLISTSPACES(chCurrentPatternTo=dirpath)
			self.setTitleState()
			ts = timeStamp(1)[-5:]
			print(ts + ' GO UP: ',self.CurrentPath)
			self.listitemsTuple = getFileItemsFromPath(self.CurrentPath,self)
			self.location_path_tx.SetValue(self.CurrentPath)
			last_selectedindex = self.list_files_assets.setMyList(True,self.listitemsTuple,selectedItems=[name])
			#self.list_files_assets.Append('a')

			#last_selectedindex = 0
			#self.list_files_assets.SetScrollPos(orientation=wx.VERTICAL,pos=last_selectedindex*3,refresh=False) # 
			self.list_files_assets.reDrawBackground()
			self.list_files_assets.reDrawSelBackground()
			try:
				if IFKEY:
					self.list_files_assets.Focus(last_selectedindex+1)
					self.list_files_assets.Select(last_selectedindex+1)
				else:
					self.list_files_assets.Focus(last_selectedindex)
			except:pass
			
			self.list_files_assets.Update()
			self.path_comments = dirpath + self.listitemsTuple[last_selectedindex][1]
			self.NotUpdate = 0
			fi = self.list_files_assets.GetFocusedItem()
			if fi == -1:
				self.list_files_assets.Focus(last_selectedindex)
				self.list_files_assets.Select(last_selectedindex)
			if fi == 0:
				self.list_files_assets.Focus(0)
				self.list_files_assets.Select(0)

			self.UpdateInfoList()
		pass


#TEST_FUNCTUINS
def makelist():
	current_path = 'D:/test_project_wx'
	print('-------------------------------',current_path)
	g = getFileItemsFromPath(current_path,None)
	for i in g:
		print(i[3])

def makeinfolist():
	current_path = 'D:/test_project_wx/c001_collection'
	print('-------------------------------',current_path)
	g = getInfoLinesFromPath(current_path)
	print(g)
def makedatereadible():
	g = linear_date_to_readible('200105_194535.utf8')
	print(g)

#STARTUP APP
def main():
	app = wx.App()
	ex = Example(None, title='wxBro.1.0')
	ex.Show()
	app.MainLoop()

if __name__ == '__main__':
	print('init MAIN -------------------')
	if getattr( sys, 'frozen', False ) :
	# running in a bundle
		filepy = sys.executable
	else :
	# running live
		filepy = sys.argv[0]
	
	INTERPRETATOR = sys.executable
	print('SYSVER:\n', sys.version)
	print('SYSEXEC:\n',INTERPRETATOR)
	print('WXVER:\n' , wx.version())
	print('MAIN:\n' , filepy)

	#print('LOCALS:\n')
	#localsstr = str(locals())
	#for l in localsstr.split(','):
	#	print('	'+l)

	HOSTNAME = socket.gethostname()
	HOMEPATH = os.path.expanduser('~')
	PLATFORM,SEP = Lin_Win_and_sep()
	USERNAME = getpass.getuser()#os.path.basename(HOMEPATH)
	fullpath = os.path.abspath(filepy)
	dirpath = os.path.dirname(fullpath)
	conf_path = dirpath+os.sep+'config.utf8'
	#font_path = dirpath+os.sep+'FallingSkyBoldplusOblique-yxmV.otf'
	print('CONF:\n' , conf_path)

	APPFOLDER = dirpath

	history_notes_filepath = HOMEPATH+os.sep+'.wxBrowserHistory.utf8'
	#history_notes_filepath = HOMEPATH+os.sep+'.notes_asset_browser.utf8'
	print('PREF:\n' , history_notes_filepath)
	collections = ''
	tools = ''
	users = ''
	envs = ''
	e = 0
	if os.path.isfile(conf_path):
		with open(conf_path,'r',encoding='utf-8') as f:
			fl = f.readlines()
			for l in fl:
				if l[:3] == '-c ': collections += l[3:].replace('\n','')
				if l[:3] == '-e ': envs += l[3:]
				o = Lin_Win_and_sep()[0]
				if o == 1:
					if l[:4] == '-tw ': tools += l[4:]
				elif o == 0:
					if l[:4] == '-tl ': tools += l[4:]
				elif o == 2:
					if l[:4] == '-tm ': tools += l[4:]
				if l[:3] == '-u ': users += l[3:]
					
		COLLECTIONS = collections.split(' ')
		#COLLECTIONS.append('ch_help')
		TOOLS = tools.split('\n')
		USERS = users.split('\n')
		ENVS = envs.split('\n')
	else:
		print('Conf file not found')
		e = 1
	TOOLS_envs = []
	for t in TOOLS:
		toolE = t
		for env in ENVS:
			if env != '':
				ee = env.split('=')
				toolE = toolE.replace(ee[0],ee[1]).replace('<APP_PATH>',APPFOLDER).replace('<PYTHON_INTERP>',INTERPRETATOR)
		if toolE != '':
			TOOLS_envs.append(toolE)
	TOOLS = TOOLS_envs
	startprefs = ''
	STARTNOTES = ''
	PCNAMEUSERkeyAndViewNameDICT = {}
	for u in USERS:
		if u != '':
			su = u.split('|||')
			compNuser = su[1].replace('__','\n')
			nameNlast = su[0].replace('__','\n')
			PCNAMEUSERkeyAndViewNameDICT[compNuser] = nameNlast
	LISTSPACES = []

	if os.path.isfile(history_notes_filepath):
		fl = readutf8_returnlistlines(history_notes_filepath)
		
		#with open(history_notes_filepath, 'r') as f:
		#	fl = f.readlines()
		if fl != []:
			startprefs = fl[0]
			for l in fl[1:]:
				if l[0:3] == '|||':
					LISTSPACES.append(l)
				else:
					STARTNOTES += l
			START_PREFS  = startprefs.split('|||')
		else:
			START_PREFS = None
	else:
		START_PREFS = None

	STARTSPACE = '0'
	START_MAXFILEFOLDERS = '80'
	START_MAXINFOLINES = '15'
	START_CATEGORY = '0'
	if LISTSPACES == []:
		STARTSPACE = '0'
		dpath = '||||||0 0 0|||"'+'/'.join(HOMEPATH.split('\\'))+'"+'
		LISTSPACES = [dpath,dpath,dpath,dpath,dpath,dpath,dpath,dpath,dpath,dpath,dpath,dpath]
		
	if START_PREFS != None:
		START_MAXFILEFOLDERS = START_PREFS[0]
		START_MAXINFOLINES = START_PREFS[1]
		START_CATEGORY = START_PREFS[2]
		STARTSPACE = START_PREFS[3]
	print('init UI -------------------')
	if e == 0:
		main()
		pass
