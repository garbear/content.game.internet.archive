import os
import re
import xbmcaddon
import xbmcvfs
from descriptionparserfactory import DescriptionParserFactory

#
# CONSTANTS AND GLOBALS #
#

iarl_plugin_name = 'content.game.internet.archive'

__addon__ = xbmcaddon.Addon(id=iarl_plugin_name)

html_unescape_table = {
		"&amp;" : "&",
		"&quot;" : '"' ,
		"&apos;" : "'",
		"&gt;" : ">",
		"&lt;" : "<",
		"&nbsp;" : " ",
		"&#x26;" : "&",
		"&#x27;" : "\'",
		"&#xB2;" : "2",
		"&#xB3;" : "3",		
		}

def html_unescape(text):
	for key in html_unescape_table.keys():
		text = text.replace(key, html_unescape_table[key])

	return text

html_escape_table = {
		"&" : "%26",
		" " : "%20" ,
		"'" : "%27",
		">" : "%3E",
		"<" : "%3C",		
		}

def html_escape(text):
	for key in html_escape_table.keys():
		text = text.replace(key, html_escape_table[key])

	return text

#
# METHODS #
#

def getDATFilePath():
	return os.path.join(getAddonInstallPath(), 'resources/data/dat_files')

#Parses all the xml dat files in the folder and returns them to create the proper directories
def scape_xml_headers():
	dat_path = getDATFilePath()
	subfolders, files = xbmcvfs.listdir(dat_path)
	#debug("Contents of %r:\nSubfolders: %r\nFiles: %r" % (dat_path, subfolders, files))
	emu_location = list()
	emu_name = list()
	emu_parser = list()
	emu_description = list()
	emu_category = list()
	emu_version = list()
	emu_date = list()
	emu_author = list()
	emu_homepage = list()
	emu_baseurl = list()
	emu_downloadpath = list()
	emu_postdlaction = list()
	emu_comment = list()
	emu_thumb = list()
	emu_banner = list()
	emu_fanart = list()
	emu_logo = list()
	emu_trailer = list()
	for ffile in files:
		total_lines = 500  #Read up to this many lines looking for the header
		f=open(os.path.join(dat_path,ffile),'rU')
		f.seek(0)
		header_end=0
		line_num=0
		header_text = ''
		while header_end < 1:
			line=f.readline()    
			header_text+=str(line)
			line_num = line_num+1
			if '</header>' in header_text: #Found the header
				header_end = 1
				header_text = header_text.split('<header>')[1].split('</header>')[0]
				emu_name.append(header_text.split('<emu_name>')[1].split('</emu_name>')[0])
				emu_parser.append(header_text.split('<emu_parser>')[1].split('</emu_parser>')[0])
				emu_location.append(os.path.join(dat_path,ffile))
				emu_description.append(header_text.split('<emu_description>')[1].split('</emu_description>')[0])
				emu_category.append(header_text.split('<emu_category>')[1].split('</emu_category>')[0])
				emu_version.append(header_text.split('<emu_version>')[1].split('</emu_version>')[0])
				emu_date.append(header_text.split('<emu_date>')[1].split('</emu_date>')[0])
				emu_author.append(header_text.split('<emu_author>')[1].split('</emu_author>')[0])
				emu_homepage.append(header_text.split('<emu_homepage>')[1].split('</emu_homepage>')[0])
				emu_baseurl.append(header_text.split('<emu_baseurl>')[1].split('</emu_baseurl>')[0])
				emu_downloadpath.append(header_text.split('<emu_downloadpath>')[1].split('</emu_downloadpath>')[0])
				emu_postdlaction.append(header_text.split('<emu_postdlaction>')[1].split('</emu_postdlaction>')[0])
				emu_comment.append(header_text.split('<emu_comment>')[1].split('</emu_comment>')[0])
				emu_thumb.append(header_text.split('<emu_thumb>')[1].split('</emu_thumb>')[0])
				emu_banner.append(header_text.split('<emu_banner>')[1].split('</emu_banner>')[0])
				emu_fanart.append(header_text.split('<emu_fanart>')[1].split('</emu_fanart>')[0])
				emu_logo.append(header_text.split('<emu_logo>')[1].split('</emu_logo>')[0])
				emu_trailer.append(header_text.split('<emu_trailer>')[1].split('</emu_trailer>')[0])
				f.close()

			if line_num == total_lines:  #Couldn't find the header
				header_end = 1
				f.close()
				print 'IARL Error:  Unable to parse header in xml file'

	dat_file_table = {
		'emu_name' : emu_name,
		'emu_parser' : emu_parser,
		'emu_location' : emu_location,
		'emu_description' : emu_description,
		'emu_category' : emu_category,
		'emu_version' : emu_version,
		'emu_date' : emu_date,
		'emu_author' : emu_author,
		'emu_homepage' : emu_homepage,
		'emu_baseurl' : emu_baseurl,
		'emu_downloadpath' : emu_downloadpath,
		'emu_postdlaction' : emu_postdlaction,
		'emu_comment' : emu_comment,
		'emu_thumb' : emu_thumb,
		'emu_banner' : emu_banner,
		'emu_fanart' : emu_fanart,
		'emu_logo': emu_logo,
		'emu_trailer': emu_trailer
	}
	#print dat_file_table
	return dat_file_table

def get_xml_header_paths(xmlfilename):
	total_lines = 500  #Read up to this many lines looking for the header
	f=open(xmlfilename,'rU')
	f.seek(0)
	header_end=0
	line_num=0
	header_text = ''
	emu_name = list()
	emu_logo = list()
	emu_fanart = list()
	emu_baseurl = list()
	emu_downloadpath = list()
	emu_postdlaction = list()
	emu_launcher = list()
	emu_ext_launch_cmd = list()

	while header_end < 1:
		line=f.readline()    
		header_text+=str(line)
		line_num = line_num+1
		if '</header>' in header_text: #Found the header
			header_end = 1
			header_text = header_text.split('<header>')[1].split('</header>')[0]
			emu_name.append(header_text.split('<emu_name>')[1].split('</emu_name>')[0])
			emu_logo.append(header_text.split('<emu_logo>')[1].split('</emu_logo>')[0])
			emu_fanart.append(header_text.split('<emu_fanart>')[1].split('</emu_fanart>')[0])
			emu_baseurl.append(header_text.split('<emu_baseurl>')[1].split('</emu_baseurl>')[0])
			emu_downloadpath.append(header_text.split('<emu_downloadpath>')[1].split('</emu_downloadpath>')[0])
			emu_postdlaction.append(header_text.split('<emu_postdlaction>')[1].split('</emu_postdlaction>')[0])
			emu_launcher.append(header_text.split('<emu_launcher>')[1].split('</emu_launcher>')[0])
			emu_ext_launch_cmd.append(header_text.split('<emu_ext_launch_cmd>')[1].split('</emu_ext_launch_cmd>')[0])
			f.close()
		if line_num == total_lines:  #Couldn't find the header
			header_end = 1
			f.close()
			print 'IARL Error:  Unable to parse header in xml file'

	dat_file_table = {
		'emu_name' : emu_name,
		'emu_logo': emu_logo,
		'emu_fanart': emu_fanart,
		'emu_baseurl' : emu_baseurl,
		'emu_downloadpath' : emu_downloadpath,
		'emu_postdlaction' : emu_postdlaction,
		'emu_launcher' : emu_launcher,
		'emu_ext_launch_cmd' : emu_ext_launch_cmd,
	}

	return dat_file_table

def getParserFilePath(xmlname):
	return os.path.join(getAddonInstallPath(), 'resources/data/' + xmlname)

def getAddonInstallPath():
	return __addon__.getAddonInfo('path')

def getYouTubePluginurl(videoid):
	return 'plugin://plugin.video.youtube/play/?video_id=' + videoid

def parse_xml_romfile(xmlfilename, parserfile, cleanlist, plugin):

	#Get basic xml path info
	xml_header_info = get_xml_header_paths(xmlfilename)

	#Define the Parser
	descParser = DescriptionParserFactory.getParser(parserfile)
	#Get Results
	results = descParser.parseDescription(xmlfilename, 'xml')

	items = []
	current_item = []
	idx = 0
	total_arts = 10
	for entries in results:
		idx += 1

		current_name = []
		if entries['rom_name']:
			current_name = entries['rom_name'][0]
			if cleanlist:
				current_name = re.sub(r'\([^)]*\)', '', current_name)
		else:
			current_name = None

		current_fname = []
		if entries['rom_filename']:
			current_fname = xml_header_info['emu_baseurl'][0]+str(entries['rom_filename'][0])
			current_fname = html_unescape(current_fname)
		else:
			current_fname = None

		current_save_fname = []
		if entries['rom_filename']:
			current_save_fname = str(entries['rom_filename'][0])
			current_save_fname = html_unescape(current_save_fname)
		else:
			current_save_fname = None

		current_emu_name = []
		if xml_header_info['emu_name']:
			current_emu_name = xml_header_info['emu_name'][0]
		else:
			current_emu_name = None

		current_emu_logo = []
		if xml_header_info['emu_logo']:
			current_emu_logo = xml_header_info['emu_logo'][0]
		else:
			current_emu_logo = None

		current_emu_fanart = []
		if xml_header_info['emu_fanart']:
			current_emu_fanart = xml_header_info['emu_fanart'][0]
		else:
			current_emu_fanart = None

		current_emu_downloadpath = []
		if xml_header_info['emu_downloadpath']:
			current_emu_downloadpath = xml_header_info['emu_downloadpath'][0]
		else:
			current_emu_downloadpath = None

		current_emu_postdlaction = []
		if xml_header_info['emu_postdlaction']:
			current_emu_postdlaction = xml_header_info['emu_postdlaction'][0]
		else:
			current_emu_postdlaction = None

		current_emu_launcher = []
		if xml_header_info['emu_launcher']:
			current_emu_launcher = xml_header_info['emu_launcher'][0]
		else:
			current_emu_launcher = None

		current_emu_ext_launch_cmd = []
		if xml_header_info['emu_ext_launch_cmd']:
			current_emu_ext_launch_cmd = xml_header_info['emu_ext_launch_cmd'][0]
		else:
			current_emu_ext_launch_cmd = None

		current_sfname = []
		if entries['rom_supporting_file']:
			current_sfname = xml_header_info['emu_baseurl'][0]+str(entries['rom_supporting_file'][0])
			current_sfname = html_unescape(current_sfname)
		else:
			current_sfname = None

		current_save_sfname = []
		if entries['rom_supporting_file']:
			current_save_sfname = str(entries['rom_supporting_file'][0])
			current_save_sfname = html_unescape(current_save_sfname)
		else:
			current_save_sfname = None

		current_icon = list()
		for ii in range(0,total_arts):
			if entries['rom_clearlogo'+str(ii+1)]:
				current_icon.append(html_unescape(entries['rom_clearlogo'+str(ii+1)][0]))
			else:
				current_icon.append(None)

		current_icon2 = filter(bool, current_icon)

		if current_icon2:
			current_icon2 = current_icon2[0]

		current_snapshot = list()
		for ii in range(0,total_arts):
			if entries['rom_snapshot'+str(ii+1)]:
				current_snapshot.append(html_unescape(entries['rom_snapshot'+str(ii+1)][0]))
			else:
				current_snapshot.append(None)

		current_thumbnail = list()
		for ii in range(0,total_arts):
			if entries['rom_boxart'+str(ii+1)]:
				current_thumbnail.append(html_unescape(entries['rom_boxart'+str(ii+1)][0]))
				# print html_unescape(entries['rom_boxart'+str(ii+1)][0])
			else:
				current_thumbnail.append(None)

		current_thumbnail2 = filter(bool, current_thumbnail)

		if current_thumbnail2:
			current_thumbnail2 = current_thumbnail2[0]

		if entries['rom_category']:
			current_genre = entries['rom_category'][0]
		else:
			current_genre = None

		if entries['rom_author']:
			current_credits = entries['rom_author'][0]
		else:
			current_credits = None

		if entries['rom_year']:
			current_date = '01-01-%s' % entries['rom_year'][0]
		else:
			current_date = None

		if entries['rom_plot']:
			current_plot = entries['rom_plot'][0]
		else:
			current_plot = None

		if entries['rom_players']:
			current_nplayers = entries['rom_players'][0]
		else:
			current_nplayers = None

		if entries['rom_videoid']:
			current_trailer = getYouTubePluginurl(entries['rom_videoid'][0]) #Return youtube plugin URL
		else:
			current_trailer = None

		if entries['rom_emu_command']:
			current_rom_emu_command = entries['rom_emu_command'][0]
		else:
			current_rom_emu_command = None

		current_fanart = list()
		for ii in range(0,total_arts):
			if entries['rom_fanart'+str(ii+1)]:
				current_fanart.append(html_unescape(entries['rom_fanart'+str(ii+1)][0]))
			else:
				current_fanart.append(None)

		current_banner = list()
		for ii in range(0,total_arts):
			if entries['rom_banner'+str(ii+1)]:
				current_banner.append(html_unescape(entries['rom_banner'+str(ii+1)][0]))
			else:
				current_banner.append(None)

		current_clearlogo = list()
		for ii in range(0,total_arts):
			if entries['rom_clearlogo'+str(ii+1)]:
				current_clearlogo.append(html_unescape(entries['rom_clearlogo'+str(ii+1)][0]))
			else:
				current_clearlogo.append(None)

		if current_emu_name == 'MAME - Multiple Arcade Machine Emulator':  #MAME xml filenames dont include the extension
			if current_fname:
				current_fname = current_fname+'.zip'
			if current_sfname:
				current_sfname = current_sfname+'.zip'
			if current_save_fname:
				current_save_fname = current_save_fname+'.zip'
			if current_save_sfname:
				current_save_sfname = current_save_sfname+'.zip'

		current_item = []
		current_item = { 
			'label' : current_name, 'icon': current_icon2,
			'thumbnail' : current_thumbnail2,
			'path' : plugin.url_for('get_selected_rom', romname=entries['rom_name'][0]),
			'info' : {'genre': current_genre, 'studio': current_credits, 'date': current_date, 'plot': current_plot, 'trailer': current_trailer},
			'properties' : {'fanart_image' : current_fanart[0], 'banner' : current_banner[0], 'clearlogo': current_clearlogo[0], 'poster': current_thumbnail[1],
			'fanart1': current_fanart[0], 'fanart2': current_fanart[1], 'fanart3': current_fanart[2], 'fanart4': current_fanart[3], 'fanart5': current_fanart[4], 'fanart6': current_fanart[5], 'fanart7': current_fanart[6], 'fanart8': current_fanart[7], 'fanart9': current_fanart[8], 'fanart10': current_fanart[9],
			'banner1': current_banner[0], 'banner2': current_banner[1], 'banner3': current_banner[2], 'banner4': current_banner[3], 'banner5': current_banner[4], 'banner6': current_banner[5], 'banner7': current_banner[6], 'banner8': current_banner[7], 'banner9': current_banner[8], 'banner10': current_banner[9],
			'snapshot1': current_snapshot[0], 'snapshot2': current_snapshot[1], 'snapshot3': current_snapshot[2], 'snapshot4': current_snapshot[3], 'snapshot5': current_snapshot[4], 'snapshot6': current_snapshot[5], 'snapshot7': current_snapshot[6], 'snapshot8': current_snapshot[7], 'snapshot9': current_snapshot[8], 'snapshot10': current_snapshot[9],
			'boxart1': current_thumbnail[0], 'boxart2': current_thumbnail[1], 'boxart3': current_thumbnail[2], 'boxart4': current_thumbnail[3], 'boxart5': current_thumbnail[4], 'boxart6': current_thumbnail[5], 'boxart7': current_thumbnail[6], 'boxart8': current_thumbnail[7], 'boxart9': current_thumbnail[8], 'boxart10': current_thumbnail[9],
			'nplayers': current_nplayers, 'emu_logo': current_emu_logo, 'emu_fanart': current_emu_fanart, 'emu_name': current_emu_name, 'rom_fname': current_fname, 'rom_sfname': current_sfname, 'rom_save_fname': current_save_fname, 'rom_save_sfname': current_save_sfname,
			'emu_downloadpath': current_emu_downloadpath, 'emu_postdlaction': current_emu_postdlaction, 'emu_launcher': current_emu_launcher, 'emu_ext_launch_cmd': current_emu_ext_launch_cmd, 'rom_emu_command': current_rom_emu_command}
		}
		items.append(current_item)

	return items
