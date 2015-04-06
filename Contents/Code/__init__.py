# -*- coding: utf-8 -*-
import urlparse

TITLE  = u'ivoox'
PREFIX = '/music/ivoox'

IVOOX_ICON     = 'ivoox.png'
ICON           = 'default_icon.png'
ART            = 'background.jpg'
NEXT_ICON      = 'next.png'
SEARCH_ICON    = 'search.png'
FAVORITES_ICON = 'favorites.png'
AUDIOS_ICON    = 'audios.png'
PODCASTS_ICON  = 'podcasts.png'
COMMENTS_ICON  = 'comments.png'
FILTERS_ICON   = 'filters.png'
CATEGORY_ICON  = 'category.png'

IVOOX_BASE_URL     = 'http://www.ivoox.com'

IVOOX_AUDIOS_INI   = '%s/audios_sa_f_1.html?nogallery' % IVOOX_BASE_URL
IVOOX_PODCASTS_INI = '%s/audios_sc_f_1.html?nogallery' % IVOOX_BASE_URL
IVOOX_AUDIOS_QUE_GUSTAN = '%s/audios-recomendados_hy_1.html' % IVOOX_BASE_URL
IVOOX_AUDIOS_COMENTADOS = '%s/ultimos-audios-comentados_hx_1.html' % IVOOX_BASE_URL

IVOOX_AUDIOS_MENU = '%s/{0}?action=a&showCategories=1' % IVOOX_BASE_URL

IVOOX_AUDIOS_FILTRO = '%s/{0}?action=a&showCategories=1&showGender=1&showLanguage=1&showDaterange=1&showDuration=1' % IVOOX_BASE_URL
IVOOX_PODCASTS_FILTRO = '%s/{0}?action=c&showCategories=1&showGender=1' % IVOOX_BASE_URL
IVOOX_AUDIOS_PODCAST_FILTRO = '%s/{0}?action=q&o=all&showCategories=1&showGender=1&showDaterange=1&showDuration=1&showSection=1' % IVOOX_BASE_URL
IVOOX_BUSQUEDA_AUDIOS_FILTRO = '%s/{0}?action=b&showCategories=1&showGender=1&showLanguage=1&showDaterange=1&showDuration=1' % IVOOX_BASE_URL


IVOOX_SEARCH_AUDIOS_URL = '%s/{0}_sb_f_1.html?oa=1' % IVOOX_BASE_URL
IVOOX_SEARCH_PODCASTS_URL = '%s/{0}_sw_1_1.html' % IVOOX_BASE_URL

IVOOX_AUDIO = '%s/descargar-audio_mn_{0}_1.mp3' % IVOOX_BASE_URL

IVOOX_PAGE = Regex('_(\d+)\.html')

FILTROS = {
  'cat': {
    'class': 'interior_menu',
    'name': 'By Category'
  },
  'time': {
    'id': 'listaduracion',
    'name': 'By Length'
  },
  'date': {
    'id': 'listafecha',
    'name': 'By Publication Date'
  },
  'gender': {
    'id': 'listagenero',
    'name': 'By Gender'
  },
  'lang': {
    'id': 'listaidioma',
    'name': 'By Language'
  }
}

HTTP_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Connection': 'keep-alive',
  'Referer': IVOOX_BASE_URL
}

################################################################################
def Start():

  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')

  ObjectContainer.title1 = TITLE
  #ObjectContainer.view_group = 'List'
  ObjectContainer.art = R(ART)
  DirectoryObject.thumb = R(ICON)
  DirectoryObject.art = R(ART)

  HTTP.CacheTime = CACHE_1HOUR

################################################################################
@handler(PREFIX, TITLE, art=ART, thumb=IVOOX_ICON)
def ivoox_main_menu():

  oc = ObjectContainer()

  oc.add(DirectoryObject(
    key = Callback(
      ivoox_audios,
      type = 'audios',
      title = L('Audios'),
      url = IVOOX_AUDIOS_INI
    ),
    title = L('Audios'),
    summary = L('choose an audio you like and start listening'),
    thumb = R(AUDIOS_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback(
      ivoox_podcasts,
      type = 'podcasts',
      title = L('Podcasts'),
      url = IVOOX_PODCASTS_INI
    ),
    title = L('Podcasts'),
    summary = L('choose a podcast you like and start listening'),
    thumb = R(PODCASTS_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback(
      ivoox_gustan
    ),
    title = L('Top Audios'),
    summary = L('top rated audios in ivoox website'),
    thumb = R(FAVORITES_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback(
      ivoox_comentados,
      url = IVOOX_AUDIOS_COMENTADOS
    ),
    title = L('Last Commented Audios'),
    summary = L('last commented audios in ivoox website'),
    thumb = R(COMMENTS_ICON)
  ))

  if Client.Product != 'PlexConnect':
    oc.add(InputDirectoryObject(
      key = Callback(ivoox_search_audios),
      title = L('Search Audios'),
      prompt = L('Search for Audios'),
      summary = L('Search for Audios'),
      thumb = R(SEARCH_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/search', page = int)
def ivoox_search_audios(query, page = 1):

  audios_url = IVOOX_SEARCH_AUDIOS_URL.format(query.replace(' ', '-'))
  podcasts_url = IVOOX_SEARCH_PODCASTS_URL.format(query.replace(' ', '-'))

  oc = ObjectContainer( title2 = query )

  oc.add(DirectoryObject(
    key = Callback(
      ivoox_audios,
      type = 'busquedaaudios',
      title = L('Audios') + ' | ' + query,
      url = audios_url
    ),
    title = L('Search Audios'),
    summary = L('search audios about') + ': ' + query,
    thumb = R(AUDIOS_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback(
      ivoox_podcasts,
      type = 'busquedapodcasts',
      title = L('Podcasts') + ' | ' + query,
      url = podcasts_url
    ),
    title = L('Search Podcasts'),
    summary = L('search podcasts about') + ': ' + query,
    thumb = R(PODCASTS_ICON)
  ))

  return oc

################################################################################
@route(PREFIX+'/filtros', filtros = dict)
def ivoox_filtros(type, title, url, filtros):

  oc = ObjectContainer(
    title2 = title
  )

  urlmenu = url.split('?')[0]
  urlmenu = Regex('_sa_|_sc_|_sq_|_sb_').sub('_v1_', urlmenu)

  if type == 'audios':
    urlmenu = IVOOX_AUDIOS_FILTRO.format(urlmenu)
  if type == 'podcasts':
    urlmenu = IVOOX_PODCASTS_FILTRO.format(urlmenu)
  if type == 'audiospodcast':
    urlmenu = IVOOX_AUDIOS_PODCAST_FILTRO.format(urlmenu)
  if type == 'busquedaaudios':
    urlmenu = IVOOX_BUSQUEDA_AUDIOS_FILTRO.format(urlmenu)

  data = HTML.ElementFromURL(
    urlmenu,
    headers = HTTP_HEADERS
  )

  for key, filtro in FILTROS.iteritems():
    if key == 'cat' or len(data.xpath('//li[@id="' + filtro['id'] + '"]')) > 0:
      oc.add(DirectoryObject(
        key = Callback(
          ivoox_filtro,
          type = type,
          filtro = key,
          title = title,
          url = url,
          urlmenu = urlmenu,
          filtros = filtros
        ),
        title = L(filtro['name']),
        thumb = R(FILTERS_ICON)
      ))

  return oc

################################################################################
@route(PREFIX+'/filtro/{filtro}', filtros = dict)
def ivoox_filtro(type, filtro, title, url, urlmenu, filtros):

  oc = ObjectContainer(
    title2 = title + ' | ' + L(FILTROS[filtro]['name'])
  )

  data = HTML.ElementFromURL(
    urlmenu,
    headers = HTTP_HEADERS
  )

  if filtro == 'cat':
    lista_filtros = data.xpath('//li[@class="' + FILTROS[filtro]['class'] + '"]')[0]
    submenu_parent = data.xpath('//li[contains(@class, "submenu2")]')
    if len(submenu_parent) > 0:
      submenu_parent = submenu_parent[0].xpath('./preceding-sibling::li[not(contains(@class, "submenu2"))]/a/text()')[-1]
  else:
    lista_filtros = data.xpath('//li[@id="' + FILTROS[filtro]['id'] + '"]')[0]

  for filtroElement in lista_filtros.xpath('.//ul/li'):
    filtro_name = filtroElement.xpath('.//a/text()')[0]

    # Plex has no input so we don't want Otra fecha nor Filtrar options
    if filtro == "date" and any(x in filtro_name for x in ["Otra fecha", "Filtrar"]):
      continue

    # Categories can have subcategories
    if filtro == 'cat':
      is_submenu = filtroElement.xpath('./@class')
      is_submenu = len(is_submenu) > 0 and 'submenu2' in is_submenu[0]
      if is_submenu:
        filtro_name = submenu_parent + ' | ' + filtro_name

    filtro_url = filtroElement.xpath('.//a/@href')[0]

    # Add or remove the filter from filtros dict
    if any(x in filtro_name for x in ["Cualquier", "Cualquiera", "Todas", "Todos"]):
      if filtro in filtros:
        filtros.pop(filtro, None)
    else:
      filtros[filtro] = filtro_name

    callback = ivoox_audios if (type == 'audios' or type == 'audiospodcast' or type == 'busquedaaudios') else ivoox_podcasts

    oc.add(DirectoryObject(
      key = Callback(
        callback,
        type = type,
        title = title,
        url = filtro_url,
        filtros = filtros
      ),
      title = filtro_name,
      thumb = R(FILTERS_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/podcasts', filtros = dict, page = int)
def ivoox_podcasts(type, title, url, filtros = {}, page = 1):

  title2 = title
  for filtro in filtros:
    title2 = title2 + ' | ' + filtros[filtro]
  title2 = title2 + ' | ' + L('Page') + ' ' + str(page)

  oc = ObjectContainer(
    title2 = title2
  )

  if type != 'busquedapodcasts':
    oc.add(DirectoryObject(
      key = Callback(
        ivoox_filtros,
        type = type,
        title = title,
        url = url,
        filtros = filtros
      ),
      title = L('Filters') + '[+/-]',
      thumb = R(FILTERS_ICON)
    ))

  data = HTML.ElementFromURL(
    urlparse.urljoin(IVOOX_BASE_URL, url),
    headers = HTTP_HEADERS
  )

  for audioElement in data.xpath('//div[@class="audio_list_item" and (not(@id) or @id!="adsensem")]'):
    audio_title = audioElement.xpath('.//div[@class="content"]//a[@class="tituloPodcast"]/text()')[0]
    audio_url = audioElement.xpath('.//div[@class="content"]//a[@class="tituloPodcast"]/@href')[0]
    audio_thumb = audioElement.xpath('.//img[contains(@class, "thumb_item")]/@src')[0]
    audio_thumb = urlparse.urljoin(IVOOX_BASE_URL, audio_thumb)
    audio_summary = ' '.join([x.strip() for x in audioElement.xpath('.//div[@class="metadatos_list"]/preceding-sibling::*//text()')])
    oc.add(DirectoryObject(
      key = Callback(
        ivoox_audios,
        type = 'audiospodcast',
        title = audio_title,
        url = audio_url,
      ),
      title = audio_title,
      summary = audio_summary,
      thumb = Resource.ContentsOfURLWithFallback(audio_thumb)
    ))

  paginador = data.xpath('//div[@class="paginacion"]')
  
  if len(paginador) > 0:
    is_last = len(paginador[0].xpath('.//span[@class="selected"]/following-sibling::span[@class="off"]')) > 0
    if not is_last:
      next_page = page + 1
      next_url = IVOOX_PAGE.sub('_' + str(next_page) + '.html', url)
      oc.add(NextPageObject(
        key = Callback(
          ivoox_podcasts,
          type = type,
          title = title,
          url = next_url,
          filtros = filtros,
          page = next_page
        ),
        title = L('Next Page') + ' >>',
        thumb = R(NEXT_ICON)
      ))

  return oc

################################################################################
@route(PREFIX+'/gustan')
def ivoox_gustan():

  oc = ObjectContainer(
    title2 = L('Top Rated')
  )

  for audioElement in HTML.ElementFromURL(
    IVOOX_AUDIOS_QUE_GUSTAN,
    headers = HTTP_HEADERS
  ).xpath('//ul[@id="audios_sugeridos"]/li'):
    audio_id = audioElement.xpath('.//a[@class="titulo"]/@id')[0]
    audio_title = audioElement.xpath('.//a[@class="titulo"]/text()')[0]
    audio_url = audioElement.xpath('.//a[@class="titulo"]/@href')[0]
    audio_summary = ' ' + L('on') + ' '.join([x.strip() for x in audioElement.xpath('.//a[@class="titulo"]/following-sibling::*/u/text()')])
    oc.add(DirectoryObject(
      key = Callback(
        ivoox_audio,
        id = audio_id,
        title = audio_title,
        url = audio_url
      ),
      title = audio_title,
      summary = audio_summary,
      thumb = R(AUDIOS_ICON)
    ))
	
  return oc

################################################################################
@route(PREFIX+'/comentados', page = int)
def ivoox_comentados(url, page = 1):

  oc = ObjectContainer(
    title2 = L('Commented') + ' | ' + L('Page') + ' ' + str(page)
  )

  data = HTML.ElementFromURL(
    url,
    headers = HTTP_HEADERS
  )

  for audio in data.xpath('//ul[@id="audios_comentados"]/li'):
    audio_id = audio.xpath('.//a[@class="titulo"]/@id')[0]
    audio_title = audio.xpath('.//a[@class="titulo"]/text()')[0]
    audio_url = audio.xpath('.//a[@class="titulo"]/@href')[0]
    audio_metadata = " en ".join([x.strip() for x in audio.xpath('.//a[@class="titulo"]/following-sibling::*/u/text()|.//a[@class="titulo"]/following-sibling::a/text()')])
    audio_comentario = audio.xpath('.//div[@class="comentario"]/text()')[0]
    audio_summary = ' | ' + L('comment') + ': '.join([audio_metadata, audio_comentario])
    oc.add(DirectoryObject(
      key = Callback(
        ivoox_audio,
        id = audio_id,
        title = audio_title,
        url = audio_url
      ),
      title = audio_title,
      summary = audio_summary,
      thumb = R(AUDIOS_ICON)
    ))

  paginador = data.xpath('//div[@class="paginacion"]')

  # If there is a pager check if it is not last page
  if len(paginador) > 0:
    is_last = len(paginador[0].xpath('.//span[@class="selected"]/following-sibling::span[@class="off"]')) > 0
    if not is_last:
      next_page = page + 1
      next_url = IVOOX_PAGE.sub('_' + str(next_page) + '.html', url)
      oc.add(NextPageObject(
        key = Callback(
          ivoox_comentados,
          url = next_url,
          page = next_page
        ),
        title = L('Next Page') + ' >>',
        thumb = R(NEXT_ICON)
      ))

  return oc

################################################################################
@route(PREFIX+'/audios', filtros = dict, page = int)
def ivoox_audios(type, title, url, filtros = {}, page = 1):

  title2 = title
  for filtro in filtros:
    title2 = title2 + ' | ' + filtros[filtro]
  title2 = title2 + ' | ' + L('Page') + ' ' + str(page)

  oc = ObjectContainer(
    title2 = title2
  )

  oc.add(DirectoryObject(
    key = Callback(
      ivoox_filtros,
      type = type,
      title = title,
      url = url,
      filtros = filtros
    ),
    title = L('Filters') + '[+/-]',
    thumb = R(FILTERS_ICON)
  ))

  data = HTML.ElementFromURL(
    urlparse.urljoin(IVOOX_BASE_URL, url),
    headers = HTTP_HEADERS
  )

  for audioElement in data.xpath('//div[@class="audio_list_item" and (not(@id) or @id!="adsensem")]'):
    audio_id = audioElement.xpath('.//div[@class="content"]/a/@id')[0]
    audio_title = " ".join([x.strip() for x in audioElement.xpath('.//div[@class="content"]/a//text()')])
    audio_url = audioElement.xpath('.//div[@class="content"]/a/@href')[0]
    audio_thumb = audioElement.xpath('.//img[@class="thumb_item"]/@src')[0]
    audio_thumb = urlparse.urljoin(IVOOX_BASE_URL, audio_thumb)
    audio_summary = " ".join([x.strip() for x in audioElement.xpath('.//div[@class="metadatos_list"]/preceding-sibling::span//text()')])
    oc.add(DirectoryObject(
      key = Callback(
        ivoox_audio,
        id = audio_id,
        title = audio_title,
        url = audio_url
      ),
      title = audio_title,
      summary = audio_summary,
      thumb = Resource.ContentsOfURLWithFallback(audio_thumb)
    ))

  paginador = data.xpath('//div[@class="paginacion"]')

  # If there is a pager check if it is not last page
  if len(paginador) > 0:
    is_last = len(paginador[0].xpath('.//span[@class="selected"]/following-sibling::span[@class="off"]')) > 0
    if not is_last:
      next_page = page + 1
      next_url = IVOOX_PAGE.sub('_' + str(next_page) + '.html', url)
      oc.add(NextPageObject(
        key = Callback(
          ivoox_audios,
          type = type,
          title = title,
          url = next_url,
          filtros = filtros,
          page = next_page
        ),
        title = L('Next Page') + ' >>',
        thumb = R(NEXT_ICON)
      ))

  return oc

################################################################################
@route(PREFIX+'/audio/{id}')
def ivoox_audio(id, title, url):

  data = HTML.ElementFromURL(
    urlparse.urljoin(IVOOX_BASE_URL, url),
    headers = HTTP_HEADERS
  )

  thumb = data.xpath('//div[@class="masinfo_audio"]//img[@class="thumb_item"]/@src')[0]
  summary = data.xpath('//meta[@property="og:description"]/@content')[0]
  track = 'http://www.ivoox.com/descargar-audio_mn_{0}_1.mp3'.format(id)

  duration_string = data.xpath('//div[@class="duration"]/text()')[0]

  oc = ObjectContainer( title2 = title.decode() )

  oc.add(CreateTrackObject(
    url = track,
    title = title,
    summary = summary,
    thumb = thumb,
    duration = Datetime.MillisecondsFromString(duration_string)
  ))

  podcast_title = data.xpath('//img[@id="img_relacionados_podcast"]/following-sibling::h1/a/text()')[0]
  podcast_url = data.xpath('//img[@id="img_relacionados_podcast"]/following-sibling::h1/a/@href')[0]
  podcast_thumb = data.xpath('//img[@id="img_relacionados_podcast"]/@src')[0]
  oc.add(DirectoryObject(
    key = Callback(
      ivoox_audios,
      type = 'audiospodcast',
      title = podcast_title,
      url = podcast_url
    ),
    title = L('podcast') + ': ' + podcast_title,
    summary = L('this audio has been published on podcast') + ' ' + podcast_title,
    thumb = Resource.ContentsOfURLWithFallback(podcast_thumb)
  ))

  category_title = data.xpath('//h1[@id="titulo_relacionados_categoria"]/a/text()')[0]
  category_url = data.xpath('//h1[@id="titulo_relacionados_categoria"]/a/@href')[0]
  oc.add(DirectoryObject(
    key = Callback(
      ivoox_audios,
      type = 'audios',
      title = L('Audios'),
      url = category_url,
      filtros = {
        'cat': category_title
      }
    ),
    title = unicode('categoría: ' + category_title),
    summary = L('this audio has been published on category') + ' ' + category_title,
    thumb = R(CATEGORY_ICON)
  ))

  return oc

################################################################################
@route(PREFIX+'/track', duration = int, include_container = bool)
def CreateTrackObject(url, title, summary, thumb, duration, include_container=False):

  container = Container.MP3
  audio_codec = AudioCodec.MP3
  ext = 'mp3'

  track_object = TrackObject(
    key = Callback(
      CreateTrackObject,
      url = url,
      title = title,
      summary = summary,
      thumb = thumb,
      duration = duration,
      include_container = True
    ),
    rating_key = url,
    title = title,
    summary = summary,
    duration = duration,
    thumb = Resource.ContentsOfURLWithFallback(thumb),
    items = [
      MediaObject(
        parts = [
          PartObject(
            key = Callback(
              PlayAudio,
              url = url,
              ext = ext
            ),
            duration = duration,
            streams = [
              AudioStreamObject(
                #codec = audio_codec,
                channels = 2
              )
            ]
          )
        ],
        #container = container,
        #audio_codec = audio_codec,
        #bitrate = 192,
        duration = duration,
        audio_channels = 2
      )
    ]
  )

  if include_container:
    oc = ObjectContainer( title2 = title.decode() )
    oc.add(track_object)
    return oc
  else:
    return track_object

################################################################################
def PlayAudio(url):
  return Redirect(url)

################################################################################
def L(string):
  Request.Headers['X-Plex-Language'] = Prefs["language"].split("/")[1]
  local_string = Locale.LocalString(string)
  return str(local_string).decode()

################################################################################
try:
  any
except NameError:
  def any(s):
    for v in s:
      if v:
        return True
    return False