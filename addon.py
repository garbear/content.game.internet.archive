from xbmcswift2 import Plugin
import xbmcplugin
from resources.lib.util import scape_xml_headers
from resources.lib.util import getParserFilePath
from resources.lib.util import parse_xml_romfile
from resources.lib.util import getYouTubePluginurl

plugin = Plugin()

iarl_setting_clean_list = plugin.get_setting('iarl_setting_clean_list', bool)

@plugin.route('/') #Start Page
def index():
    items = []
    emu_info = scape_xml_headers() #Find all xml dat files and get the header info

    for ii in range(0,len(emu_info['emu_name'])):
        
        items.append({ 
            'label' : emu_info['emu_name'][ii], 'path': plugin.url_for('get_rom_page', category_id=emu_info['emu_name'][ii],page_id='1',parser_id=emu_info['emu_parser'][ii],xml_id=emu_info['emu_location'][ii]), 'icon': emu_info['emu_logo'][ii],
            'thumbnail' : emu_info['emu_thumb'][ii],
            'info' : {'genre': emu_info['emu_category'][ii], 'credits': emu_info['emu_author'][ii], 'date': emu_info['emu_date'][ii], 'plot': emu_info['emu_comment'][ii], 'trailer': getYouTubePluginurl(emu_info['emu_trailer'][ii]), 'FolderPath': emu_info['emu_baseurl'][ii]},
            'properties' : {'fanart_image' : emu_info['emu_fanart'][ii], 'banner' : emu_info['emu_banner'][ii], 'clearlogo': emu_info['emu_logo'][ii]},
        })
    
    return plugin.finish(items, sort_methods=[xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE, xbmcplugin.SORT_METHOD_GENRE])

@plugin.route('/Emulator/<category_id>')
def get_rom_page(category_id):
    
    #Define Parser
    args_in = plugin.request.args
    try:
        parserpath = args_in['parser_id'][0]
    except:
        parserpath = None

    try:
        xmlpath = args_in['xml_id'][0]
    except:
        xmlpath = None

    try:
        rom_list = get_rom_list(xmlpath, parserpath)
    except:
        rom_list = None

    return plugin.finish(rom_list, sort_methods=[xbmcplugin.SORT_METHOD_NONE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE, xbmcplugin.SORT_METHOD_DATE, xbmcplugin.SORT_METHOD_GENRE, xbmcplugin.SORT_METHOD_STUDIO_IGNORE_THE])

@plugin.cached(TTL=24*60*30)
def get_rom_list(xmlpath, parserpath):
    parserpath = getParserFilePath(parserpath)
    rom_list = parse_xml_romfile(xmlpath, parserpath, iarl_setting_clean_list, plugin) #List doesn't exist, so get the romlist
    return rom_list

if __name__ == '__main__':
    plugin.run()
