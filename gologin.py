import json
import math
import os
import pathlib
import random
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import time
import zipfile

import psutil
import requests

from db import db_fingerprint
from extensionsManager import ExtensionsManager

# profile_str = '{"name":"daomannaha312312","role":"owner","id":"6524c8569ecf5b0505bff894","notes":"","browserType":"chrome","lockEnabled":false,"timezone":{"enabled":true,"fillBasedOnIp":true},"navigator":{"hardwareConcurrency":8,"doNotTrack":false,"deviceMemory":8,"userAgent":"Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/116.0.5845.106Safari/537.36","resolution":"1440x960","language":"en-US,en;q=0.9","platform":"Win32","maxTouchPoints":0},"geolocation":{"mode":"prompt","enabled":true,"customize":true,"fillBasedOnIp":true,"latitude":0,"longitude":0,"accuracy":10},"debugMode":false,"os":"win","proxy":{"mode":"none","port":80,"autoProxyRegion":"us","torProxyRegion":"us","host":"","username":"","password":"","changeIpUrl":null},"folders":[],"createdAt":"2023-10-10T03:43:18.640Z","updatedAt":"2023-10-10T03:43:18.640Z","chromeExtensions":[],"userChromeExtensions":[],"tags":[],"proxyEnabled":false,"isBookmarksSynced":true,"autoLang":true,"webGLMetadata":{"mode":"off","vendor":"GoogleInc.(Intel)","renderer":"ANGLE(Intel,Intel(R)Iris(R)XeGraphicsDirect3D11vs_5_0ps_5_0,D3D11)"},"fonts":{"enableMasking":true,"enableDomRect":true,"families":["AIGDT","AMGDT","Arial","ArialBaltic","ArialBlack","ArialCE","ArialCyr","ArialGreek","ArialHebrew","ArialMT","ArialNarrow","ArialRoundedMTBold","ArialTUR","ArialUnicodeMS","Calibri","CalibriLight","Cambria","CambriaMath","Candara","ComicSansMS","Consolas","Constantia","Corbel","Courier","CourierNew","CourierNewBaltic","CourierNewCE","CourierNewCyr","CourierNewGreek","CourierNewTUR","David","DavidLibre","DejaVuSans","DejaVuSansCondensed","DejaVuSansLight","DejaVuSansMono","DejaVuSerif","DejaVuSerifCondensed","Ebrima","FrankRuehl","FrankRuehlLibre","FrankRuehlLibreBlack","FrankRuehlLibreLight","FranklinGothicBook","FranklinGothicDemi","FranklinGothicDemiCond","FranklinGothicHeavy","FranklinGothicMedium","Gabriola","Gadugi","Georgia","GillSans","GillSansMT","GillSansMTCondensed","GillSansMTExtCondensedBold","GillSansUltraBold","GillSansUltraBoldCondensed","Impact","KacstBook","KacstLetter","KacstNaskh","KacstTitlel","Leelawadee","LiberationMono","LiberationSansNarrow","LucidaBright","LucidaCalligraphy","LucidaConsole","LucidaSansUnicode","MSGothic","MSLineDraw","MSMincho","MSOutlook","MSPGothic","MSPMincho","MSReferenceSansSerif","MSReferenceSpecialty","MSSansSerif","MSSerif","MSUIGothic","MVBoli","MalgunGothic","Marlett","MicrosoftHimalaya","MicrosoftJhengHei","MicrosoftJhengHeiUI","MicrosoftNewTaiLue","MicrosoftPhagsPa","MicrosoftSansSerif","MicrosoftTaiLe","MicrosoftUighur","MicrosoftYaHei","MicrosoftYaHeiUI","MicrosoftYiBaiti","MingLiU","MingLiU-ExtB","MingLiU_HKSCS","MingLiU_HKSCS-ExtB","Miriam","MiriamFixed","MiriamLibre","MongolianBaiti","NSimSun","NirmalaUI","NotoMono","NotoSansCJKHK","NotoSansCJKJP","NotoSansCJKKR","NotoSansCJKSC","NotoSansCJKTC","NotoSansLisu","NotoSansMonoCJKHK","NotoSansMonoCJKJP","NotoSansMonoCJKKR","NotoSansMonoCJKSC","NotoSansMonoCJKTC","NotoSerif","NotoSerifCJKJP","NotoSerifCJKKR","NotoSerifCJKSC","NotoSerifCJKTC","NotoSerifGeorgian","NotoSerifHebrew","NotoSerifItalic","NotoSerifLao","OpenSymbol","Oswald","PMingLiU","PMingLiU-ExtB","Palatino","PalatinoLinotype","Roboto","RobotoBlack","RobotoLight","RobotoMedium","RobotoThin","SegoePrint","SegoeScript","SegoeUI","SegoeUILight","SegoeUISemibold","SegoeUISemilight","SegoeUISymbol","SimSun","SimSun-ExtB","Sylfaen","Symbol","Tahoma","TimesNewRoman","TimesNewRomanBaltic","TimesNewRomanGreek","TimesNewRomanTUR","TrebuchetMS","Verdana","Webdings","Wingdings","Wingdings3","YuGothic","YuGothicUI","ZapfDingbats"]}}'
fingerprint_str = '{"navigator":{"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.106 Safari/537.36","resolution":"1366x768","language":"en-US,en;q=0.9","platform":"Win32","hardwareConcurrency":4,"deviceMemory":8,"maxTouchPoints":0},"canvas":{"mode":"off"},"mediaDevices":{"videoInputs":1,"audioInputs":1,"audioOutputs":1},"webRTC":{"localIps":[]},"webGLMetadata":{"mode":"noise","vendor":"Google Inc. (Intel)","renderer":"ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)"},"webglParams":{"glCanvas":"webgl2","supportedFunctions":[{"name":"beginQuery","supported":true},{"name":"beginTransformFeedback","supported":true},{"name":"bindBufferBase","supported":true},{"name":"bindBufferRange","supported":true},{"name":"bindSampler","supported":true},{"name":"bindTransformFeedback","supported":true},{"name":"bindVertexArray","supported":true},{"name":"blitFramebuffer","supported":true},{"name":"clearBufferfi","supported":true},{"name":"clearBufferfv","supported":true},{"name":"clearBufferiv","supported":true},{"name":"clearBufferuiv","supported":true},{"name":"clientWaitSync","supported":true},{"name":"compressedTexImage3D","supported":true},{"name":"compressedTexSubImage3D","supported":true},{"name":"copyBufferSubData","supported":true},{"name":"copyTexSubImage3D","supported":true},{"name":"createQuery","supported":true},{"name":"createSampler","supported":true},{"name":"createTransformFeedback","supported":true},{"name":"createVertexArray","supported":true},{"name":"deleteQuery","supported":true},{"name":"deleteSampler","supported":true},{"name":"deleteSync","supported":true},{"name":"deleteTransformFeedback","supported":true},{"name":"deleteVertexArray","supported":true},{"name":"drawArraysInstanced","supported":true},{"name":"drawBuffers","supported":true},{"name":"drawElementsInstanced","supported":true},{"name":"drawRangeElements","supported":true},{"name":"endQuery","supported":true},{"name":"endTransformFeedback","supported":true},{"name":"fenceSync","supported":true},{"name":"framebufferTextureLayer","supported":true},{"name":"getActiveUniformBlockName","supported":true},{"name":"getActiveUniformBlockParameter","supported":true},{"name":"getActiveUniforms","supported":true},{"name":"getBufferSubData","supported":true},{"name":"getFragDataLocation","supported":true},{"name":"getIndexedParameter","supported":true},{"name":"getInternalformatParameter","supported":true},{"name":"getQuery","supported":true},{"name":"getQueryParameter","supported":true},{"name":"getSamplerParameter","supported":true},{"name":"getSyncParameter","supported":true},{"name":"getTransformFeedbackVarying","supported":true},{"name":"getUniformBlockIndex","supported":true},{"name":"getUniformIndices","supported":true},{"name":"invalidateFramebuffer","supported":true},{"name":"invalidateSubFramebuffer","supported":true},{"name":"isQuery","supported":true},{"name":"isSampler","supported":true},{"name":"isSync","supported":true},{"name":"isTransformFeedback","supported":true},{"name":"isVertexArray","supported":true},{"name":"pauseTransformFeedback","supported":true},{"name":"readBuffer","supported":true},{"name":"renderbufferStorageMultisample","supported":true},{"name":"resumeTransformFeedback","supported":true},{"name":"samplerParameterf","supported":true},{"name":"samplerParameteri","supported":true},{"name":"texImage3D","supported":true},{"name":"texStorage2D","supported":true},{"name":"texStorage3D","supported":true},{"name":"texSubImage3D","supported":true},{"name":"transformFeedbackVaryings","supported":true},{"name":"uniform1ui","supported":true},{"name":"uniform1uiv","supported":true},{"name":"uniform2ui","supported":true},{"name":"uniform2uiv","supported":true},{"name":"uniform3ui","supported":true},{"name":"uniform3uiv","supported":true},{"name":"uniform4ui","supported":true},{"name":"uniform4uiv","supported":true},{"name":"uniformBlockBinding","supported":true},{"name":"uniformMatrix2x3fv","supported":true},{"name":"uniformMatrix2x4fv","supported":true},{"name":"uniformMatrix3x2fv","supported":true},{"name":"uniformMatrix3x4fv","supported":true},{"name":"uniformMatrix4x2fv","supported":true},{"name":"uniformMatrix4x3fv","supported":true},{"name":"vertexAttribDivisor","supported":true},{"name":"vertexAttribI4i","supported":true},{"name":"vertexAttribI4iv","supported":true},{"name":"vertexAttribI4ui","supported":true},{"name":"vertexAttribI4uiv","supported":true},{"name":"vertexAttribIPointer","supported":true},{"name":"waitSync","supported":true}],"glParamValues":[{"name":"ALIASED_LINE_WIDTH_RANGE","value":{"0":1,"1":1}},{"name":"ALIASED_POINT_SIZE_RANGE","value":{"0":1,"1":1024}},{"name":["DEPTH_BITS","STENCIL_BITS"],"value":"n/a"},{"name":"MAX_3D_TEXTURE_SIZE","value":2048},{"name":"MAX_ARRAY_TEXTURE_LAYERS","value":2048},{"name":"MAX_COLOR_ATTACHMENTS","value":8},{"name":"MAX_COMBINED_FRAGMENT_UNIFORM_COMPONENTS","value":200704},{"name":"MAX_COMBINED_TEXTURE_IMAGE_UNITS","value":32},{"name":"MAX_COMBINED_UNIFORM_BLOCKS","value":24},{"name":"MAX_COMBINED_VERTEX_UNIFORM_COMPONENTS","value":212992},{"name":"MAX_CUBE_MAP_TEXTURE_SIZE","value":16384},{"name":"MAX_DRAW_BUFFERS","value":8},{"name":"MAX_FRAGMENT_INPUT_COMPONENTS","value":120},{"name":"MAX_FRAGMENT_UNIFORM_BLOCKS","value":12},{"name":"MAX_FRAGMENT_UNIFORM_COMPONENTS","value":4096},{"name":"MAX_FRAGMENT_UNIFORM_VECTORS","value":1024},{"name":"MAX_PROGRAM_TEXEL_OFFSET","value":7},{"name":"MAX_RENDERBUFFER_SIZE","value":16384},{"name":"MAX_SAMPLES","value":16},{"name":"MAX_TEXTURE_IMAGE_UNITS","value":16},{"name":"MAX_TEXTURE_LOD_BIAS","value":2},{"name":"MAX_TEXTURE_SIZE","value":16384},{"name":"MAX_TRANSFORM_FEEDBACK_INTERLEAVED_COMPONENTS","value":120},{"name":"MAX_TRANSFORM_FEEDBACK_SEPARATE_ATTRIBS","value":4},{"name":"MAX_TRANSFORM_FEEDBACK_SEPARATE_COMPONENTS","value":4},{"name":"MAX_UNIFORM_BLOCK_SIZE","value":65536},{"name":"MAX_UNIFORM_BUFFER_BINDINGS","value":24},{"name":"MAX_VARYING_COMPONENTS","value":120},{"name":"MAX_VARYING_VECTORS","value":30},{"name":"MAX_VERTEX_ATTRIBS","value":16},{"name":"MAX_VERTEX_OUTPUT_COMPONENTS","value":120},{"name":"MAX_VERTEX_TEXTURE_IMAGE_UNITS","value":16},{"name":"MAX_VERTEX_UNIFORM_BLOCKS","value":12},{"name":"MAX_VERTEX_UNIFORM_COMPONENTS","value":16384},{"name":"MAX_VERTEX_UNIFORM_VECTORS","value":4096},{"name":"MAX_VIEWPORT_DIMS","value":{"0":32767,"1":32767}},{"name":"MIN_PROGRAM_TEXEL_OFFSET","value":-8},{"name":["RED_BITS","GREEN_BITS","BLUE_BITS","ALPHA_BITS"],"value":"n/a"},{"name":"RENDERER","value":"WebKit WebGL"},{"name":"SHADING_LANGUAGE_VERSION","value":"WebGL GLSL ES 3.00 (OpenGL ES GLSL ES 3.0 Chromium)"},{"name":"UNIFORM_BUFFER_OFFSET_ALIGNMENT","value":256},{"name":"VENDOR","value":"WebKit"},{"name":"VERSION","value":"WebGL 2.0 (OpenGL ES 3.0 Chromium)"}],"antialiasing":true,"textureMaxAnisotropyExt":16,"shaiderPrecisionFormat":"highp/highp","extensions":["EXT_color_buffer_float","EXT_color_buffer_half_float","EXT_disjoint_timer_query_webgl2","EXT_float_blend","EXT_texture_compression_bptc","EXT_texture_compression_rgtc","EXT_texture_filter_anisotropic","EXT_texture_norm16","KHR_parallel_shader_compile","OES_draw_buffers_indexed","OES_texture_float_linear","OVR_multiview2","WEBGL_compressed_texture_s3tc","WEBGL_compressed_texture_s3tc_srgb","WEBGL_debug_renderer_info","WEBGL_debug_shaders","WEBGL_lose_context","WEBGL_multi_draw","WEBGL_provoking_vertex"]},"webGL":{"mode":"off"},"clientRects":{"mode":"off"},"os":"win","devicePixelRatio":1,"fonts":["AIGDT","AMGDT","Arial","Arial Black","Arial CE","Arial Cyr","Arial Greek","Arial Hebrew","Arial MT","Arial Narrow","Arial Rounded MT Bold","Arial TUR","Arial Unicode MS","Calibri","Calibri Light","Cambria","Cambria Math","Candara","Comic Sans MS","Consolas","Constantia","Corbel","Courier","Courier New","Courier New Baltic","Courier New CE","Courier New Cyr","Courier New Greek","Courier New TUR","David","David Libre","DejaVu Sans","DejaVu Sans Condensed","DejaVu Sans Light","DejaVu Sans Mono","DejaVu Serif","DejaVu Serif Condensed","Ebrima","Frank Ruehl","Frank Ruehl Libre","Frank Ruehl Libre Black","Frank Ruehl Libre Light","Franklin Gothic Book","Franklin Gothic Demi","Franklin Gothic Demi Cond","Franklin Gothic Heavy","Franklin Gothic Medium","Franklin Gothic Medium Cond","Gadugi","Gill Sans","Gill Sans MT","Gill Sans MT Condensed","Gill Sans MT Ext Condensed Bold","Gill Sans Ultra Bold","Impact","KacstLetter","KacstNaskh","KacstOffice","KacstTitlel","Leelawadee","Liberation Mono","Liberation Sans","Liberation Serif","Lucida Bright","Lucida Calligraphy","MS LineDraw","MS PGothic","MS PMincho","MS Reference Sans Serif","MS Sans Serif","MS Serif","MS UI Gothic","MV Boli","Malgun Gothic","Microsoft Himalaya","Microsoft JhengHei","Microsoft JhengHei UI","Microsoft New Tai Lue","Microsoft PhagsPa","Microsoft Tai Le","Microsoft Uighur","Microsoft YaHei","Microsoft Yi Baiti","MingLiU","MingLiU_HKSCS","MingLiU_HKSCS-ExtB","Miriam Fixed","Miriam Libre","Mongolian Baiti","NSimSun","Nirmala UI","Noto Mono","Noto Sans","Noto Sans Arabic UI","Noto Sans CJK HK","Noto Sans CJK JP","Noto Sans CJK KR","Noto Sans CJK TC","Noto Sans Lisu","Noto Sans Mono CJK HK","Noto Sans Mono CJK KR","Noto Sans Mono CJK TC","Noto Serif","Noto Serif CJK SC","Noto Serif CJK TC","Noto Serif Georgian","Noto Serif Hebrew","Noto Serif Italic","Noto Serif Lao","OpenSymbol","Oswald","PMingLiU","PMingLiU-ExtB","Palatino","Palatino Linotype","Roboto","Roboto Black","Roboto Light","Roboto Medium","Roboto Thin","Segoe Print","Segoe Script","Segoe UI","Segoe UI Light","Segoe UI Semibold","Segoe UI Semilight","Segoe UI Symbol","SimSun","SimSun-ExtB","Sylfaen","Symbol","Tahoma","Times New Roman","Times New Roman CE","Times New Roman Cyr","Times New Roman Greek","Trebuchet MS","Verdana","Webdings","Wingdings","Wingdings 2","Yu Gothic","Yu Gothic UI","Zapf Dingbats"],"extensionsToNewProfiles":[],"userExtensionsToNewProfiles":[],"autoLang":true}'
zip_path = r'C:\Users\daoma\PycharmProjects\pygologin\gologin_zeroprofile.zip'


class GoLogin(object):
    def __init__(self, options):
        self.profile_path = options.get('profile_path')
        if os.path.exists(self.profile_path):
            pref_file = os.path.join(self.profile_path, 'Default', 'Preferences')
            with open(pref_file, 'r', encoding="utf-8") as pfile:
                preferences = json.load(pfile)
            self.profile = preferences.get('gologin')
        else:
            self.profile = None
        self.tmpdir = options.get('tmpdir', tempfile.gettempdir())
        self.address = options.get('address', '127.0.0.1')
        self.extra_params = options.get('extra_params', [])
        self.port = options.get('port', 3500)
        self.local = options.get('local', True)
        self.spawn_browser = options.get('spawn_browser', True)
        self.credentials_enable_service = options.get('credentials_enable_service')
        self.cleaningLocalCookies = options.get('cleaningLocalCookies', False)
        self.executablePath = options.get('executable_path')
        self.is_new_cloud_browser = options.get('is_new_cloud_browser', False)
        # self.profile = json.loads(profile_str)
        self.profile_zip_path = zip_path

        if self.extra_params:
            print('extra_params', self.extra_params)
        self.setProfileId(options.get('profile_id'))
        self.preferences = {}
        self.pid = int()

    def setProfileId(self, profile_id):
        self.profile_id = profile_id
        if self.profile_id == None:
            return

    def loadExtensions(self):
        profile = self.profile
        chromeExtensions = profile.get('chromeExtensions')
        extensionsManagerInst = ExtensionsManager()
        pathToExt = ''
        profileExtensionsCheck = []
        for ext in chromeExtensions:
            ver = extensionsManagerInst.downloadExt(ext)
            pathToExt += os.path.join(pathlib.Path.home(), '.gologin', 'extensions', 'chrome-extensions',
                                      ext + '@' + ver + ',')
            profileExtensionsCheck.append(
                os.path.join(pathlib.Path.home(), '.gologin', 'extensions', 'chrome-extensions', ext + '@' + ver))

        pref_file = os.path.join(self.profile_path, 'Default', 'Preferences')
        with open(pref_file, 'r', encoding="utf-8") as pfile:
            preferences = json.load(pfile)

        noteExtExist = ExtensionsManager().extensionIsAlreadyExisted(preferences, profileExtensionsCheck)

        if noteExtExist:
            return
        else:
            return pathToExt

    def spawnBrowser(self):
        proxy = self.proxy
        proxy_host = ''
        if proxy:
            if proxy.get('mode') == None or proxy.get('mode') == 'geolocation':
                proxy['mode'] = 'http'
            proxy_host = proxy.get('host')
            proxy = self.formatProxyUrl(proxy)

        tz = self.tz.get('timezone')

        params = [
            self.executablePath,
            '--remote-debugging-port=' + str(self.port),
            '--user-data-dir=' + self.profile_path,
            '--password-store=basic',
            '--tz=' + tz,
            '--gologin-profile=' + self.profile_name,
            '--lang=en-US',
        ]

        chromeExtensions = self.profile.get('chromeExtensions')
        if chromeExtensions and len(chromeExtensions) > 0:
            paths = self.loadExtensions()
            if paths is not None:
                extToParams = '--load-extension=' + paths
                params.append(extToParams)

        if proxy:
            hr_rules = '"MAP * 0.0.0.0 , EXCLUDE %s"' % (proxy_host)
            params.append('--proxy-server=' + proxy)
            params.append('--host-resolver-rules=' + hr_rules)

        for param in self.extra_params:
            params.append(param)

        if sys.platform == "darwin":
            open_browser = subprocess.Popen(params)
            self.pid = open_browser.pid
        else:
            open_browser = subprocess.Popen(params, start_new_session=True)
            self.pid = open_browser.pid

        try_count = 1
        url = str(self.address) + ':' + str(self.port)
        while try_count < 100:
            try:
                data = requests.get('http://' + url + '/json').content
                break
            except:
                try_count += 1
                time.sleep(1)
        return url

    def start(self):
        profile_path = self.createStartup()
        if self.spawn_browser == True:
            return self.spawnBrowser()
        return profile_path

    def zipdir(self, path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                path = os.path.join(root, file)
                if not os.path.exists(path):
                    continue
                if stat.S_ISSOCK(os.stat(path).st_mode):
                    continue
                try:
                    ziph.write(path, path.replace(self.profile_path, ''))
                except:
                    continue

    def waitUntilProfileUsing(self, try_count=0):
        if try_count > 10:
            return
        time.sleep(1)
        profile_path = self.profile_path
        if os.path.exists(profile_path):
            try:
                os.rename(profile_path, profile_path)
            except OSError as e:
                print("waiting chrome termination")
                self.waitUntilProfileUsing(try_count + 1)

    def stop(self):
        for proc in psutil.process_iter(['pid']):
            if proc.info.get('pid') == self.pid:
                proc.kill()
        self.waitUntilProfileUsing()
        self.sanitizeProfile()
        if self.local == False:
            self.commitProfile()
            os.remove(self.profile_zip_path_upload)
            shutil.rmtree(self.profile_path)

    def sanitizeProfile(self):
        if (self.cleaningLocalCookies):
            path_to_coockies = os.path.join(self.profile_path, 'Default', 'Network', 'Cookies')
            os.remove(path_to_coockies)

        remove_dirs = [
            'Default/Cache',
            'Default/Service Worker/CacheStorage',
            'Default/Code Cache',
            'Default/GPUCache',
            'GrShaderCache',
            'ShaderCache',
            'biahpgbdmdkfgndcmfiipgcebobojjkp',
            'afalakplffnnnlkncjhbmahjfjhmlkal',
            'cffkpbalmllkdoenhmdmpbkajipdjfam',
            'Dictionaries',
            'enkheaiicpeffbfgjiklngbpkilnbkoi',
            'oofiananboodjbbmdelgdommihjbkfag',
            'SafetyTips',
            'fonts',
        ];

        for d in remove_dirs:
            fpath = os.path.join(self.profile_path, d)
            if os.path.exists(fpath):
                try:
                    shutil.rmtree(fpath)
                except:
                    continue

    def formatProxyUrl(self, proxy):
        return proxy.get('mode', 'http') + '://' + proxy.get('host', '') + ':' + str(proxy.get('port', 80))

    def formatProxyUrlPassword(self, proxy):
        mode = "socks5h" if proxy.get("mode") == "socks5" else proxy.get("mode", "http")
        if proxy.get('username', '') == '':
            return mode + '://' + proxy.get('host', '') + ':' + str(proxy.get('port', 80))
        else:
            return proxy.get('mode', 'http') + '://' + proxy.get('username', '') + ':' + proxy.get(
                'password') + '@' + proxy.get('host', '') + ':' + str(proxy.get('port', 80))

    def getTimeZone(self):
        proxy = self.proxy
        if proxy:
            proxies = {
                'http': self.formatProxyUrlPassword(proxy),
                'https': self.formatProxyUrlPassword(proxy)
            }
            data = requests.get('https://time.gologin.com', proxies=proxies)
        else:
            data = requests.get('https://time.gologin.com')
        return json.loads(data.content.decode('utf-8'))

    def getProfile(self, ):
        # profile = self.profile_id if profile_id == None else profile_id
        # headers = {
        #     'Authorization': 'Bearer ' + self.access_token,
        #     'User-Agent': 'Selenium-API'
        # }
        # data = json.loads(requests.get(API_URL + '/browser/' + profile, headers=headers).content.decode('utf-8'))
        # if data.get("statusCode") == 404:
        #     raise Exception(data.get("error") + ": " + data.get("message"))
        return self.profile

    def getGeolocationParams(self, profileGeolocationParams, tzGeolocationParams):
        if profileGeolocationParams.get('fillBasedOnIp'):
            return {
                'mode': profileGeolocationParams['mode'],
                'latitude': float(tzGeolocationParams['latitude']),
                'longitude': float(tzGeolocationParams['longitude']),
                'accuracy': float(tzGeolocationParams['accuracy']),
            }

        return {
            'mode': profileGeolocationParams['mode'],
            'latitude': profileGeolocationParams['latitude'],
            'longitude': profileGeolocationParams['longitude'],
            'accuracy': profileGeolocationParams['accuracy'],
        }

    def convertPreferences(self, preferences):
        resolution = preferences.get('resolution', '1920x1080')
        preferences['screenWidth'] = int(resolution.split('x')[0])
        preferences['screenHeight'] = int(resolution.split('x')[1])
        self.preferences = preferences
        self.tz = self.getTimeZone()
        # print('tz=', self.tz)
        tzGeoLocation = {
            'latitude': self.tz.get('ll', [0, 0])[0],
            'longitude': self.tz.get('ll', [0, 0])[1],
            'accuracy': self.tz.get('accuracy', 0),
        }

        preferences['geoLocation'] = self.getGeolocationParams(preferences['geolocation'], tzGeoLocation)

        preferences['webRtc'] = {
            'mode': 'public' if preferences.get('webRTC', {}).get('mode') == 'alerted' else preferences.get('webRTC',
                                                                                                            {}).get(
                'mode'),
            'publicIP': self.tz['ip'] if preferences.get('webRTC', {}).get('fillBasedOnIp') else preferences.get(
                'webRTC', {}).get('publicIp'),
            'localIps': preferences.get('webRTC', {}).get('localIps', [])
        }

        preferences['timezone'] = {
            'id': self.tz.get('timezone')
        }

        preferences['' \
                    ''] = preferences.get('webGL', {}).get('noise')
        preferences['get_client_rects_noise'] = preferences.get('webGL', {}).get('getClientRectsNoise')
        preferences['canvasMode'] = preferences.get('canvas', {}).get('mode')
        preferences['canvasNoise'] = preferences.get('canvas', {}).get('noise')
        if preferences.get('clientRects', {}).get('mode') == 'noise':
            preferences['client_rects_noise_enable'] = True
        preferences['audioContextMode'] = preferences.get('audioContext', {}).get('mode')
        preferences['audioContext'] = {
            'enable': preferences.get('audioContextMode') != 'off',
            'noiseValue': preferences.get('audioContext', {}).get('noise'),
        }

        preferences['webgl'] = {
            'metadata': {
                'vendor': preferences.get('webGLMetadata', {}).get('vendor'),
                'renderer': preferences.get('webGLMetadata', {}).get('renderer'),
                'mode': preferences.get('webGLMetadata', {}).get('mode') == 'mask',
            }
        }

        if preferences.get('navigator', {}).get('userAgent'):
            preferences['userAgent'] = preferences.get('navigator', {}).get('userAgent')

        if preferences.get('navigator', {}).get('doNotTrack'):
            preferences['doNotTrack'] = preferences.get('navigator', {}).get('doNotTrack')

        if preferences.get('navigator', {}).get('hardwareConcurrency'):
            preferences['hardwareConcurrency'] = preferences.get('navigator', {}).get('hardwareConcurrency')

        if preferences.get('navigator', {}).get('language'):
            preferences['languages'] = preferences.get('navigator', {}).get('language')

        if preferences.get('isM1', False):
            preferences["is_m1"] = preferences.get('isM1', False)

        if preferences.get('os') == "android":
            devicePixelRatio = preferences.get("devicePixelRatio");
            deviceScaleFactorCeil = math.ceil(devicePixelRatio or 3.5);
            deviceScaleFactor = devicePixelRatio;
            if deviceScaleFactorCeil == devicePixelRatio:
                deviceScaleFactor += 0.00000001;

            preferences["mobile"] = {
                "enable": True,
                "width": preferences['screenWidth'],
                "height": preferences['screenHeight'],
                "device_scale_factor": deviceScaleFactor,
            }

        return preferences

    def updatePreferences(self):
        pref_file = os.path.join(self.profile_path, 'Default', 'Preferences')
        with open(pref_file, 'r', encoding="utf-8") as pfile:
            preferences = json.load(pfile)
        profile = self.profile
        proxy = self.profile.get('proxy')
        # print('proxy=', proxy)
        if proxy and (proxy.get('mode') == 'gologin' or proxy.get('mode') == 'tor'):
            autoProxyServer = profile.get('autoProxyServer')
            splittedAutoProxyServer = autoProxyServer.split('://')
            splittedProxyAddress = splittedAutoProxyServer[1].split(':')
            port = splittedProxyAddress[1]

            proxy = {
                'mode': 'http',
                'host': splittedProxyAddress[0],
                'port': port,
                'username': profile.get('autoProxyUsername'),
                'password': profile.get('autoProxyPassword'),
                'timezone': profile.get('autoProxyTimezone', 'us'),
            }

            profile['proxy']['username'] = profile.get('autoProxyUsername')
            profile['proxy']['password'] = profile.get('autoProxyPassword')

        if not proxy or proxy.get('mode') == 'none':
            print('no proxy')
            proxy = None

        if proxy and proxy.get('mode') == 'geolocation':
            proxy['mode'] = 'http'

        if proxy and proxy.get('mode') == None:
            proxy['mode'] = 'http'

        self.proxy = proxy
        self.profile_name = profile.get('name')
        if self.profile_name == None:
            print('empty profile name')
            print('profile=', profile)
            exit()

        gologin = self.convertPreferences(profile)
        if self.credentials_enable_service != None:
            preferences['credentials_enable_service'] = self.credentials_enable_service
        preferences['gologin'] = gologin
        pfile = open(pref_file, 'w')
        json.dump(preferences, pfile)

    def createStartup(self):

        self.profile = self.getProfile()

        self.updatePreferences()

        return self.profile_path

    def update(self, options):
        for k, v in options.items():
            self.profile[k] = v

    def getRandomFingerprint(self):
        # os_type = options.get('os', 'lin')
        return db_fingerprint.get_random_fingerprint().data

    def create(self, options={}):
        profile_options = self.getRandomFingerprint()
        navigator = options.get('navigator')
        if options.get('navigator'):
            resolution = navigator.get('resolution')
            userAgent = navigator.get('userAgent')
            language = navigator.get('language')
            hardwareConcurrency = navigator.get('hardwareConcurrency')
            deviceMemory = navigator.get('deviceMemory')

            if resolution == 'random' or userAgent == 'random':
                options.pop('navigator')
            if resolution != 'random' and userAgent != 'random':
                options.pop('navigator')
            if resolution == 'random' and userAgent != 'random':
                profile_options['navigator']['userAgent'] = userAgent
            if userAgent == 'random' and resolution != 'random':
                profile_options['navigator']['resolution'] = resolution
            if resolution != 'random' and userAgent != 'random':
                profile_options['navigator']['userAgent'] = userAgent
                profile_options['navigator']['resolution'] = resolution
            if hardwareConcurrency != 'random' and userAgent != 'random' and hardwareConcurrency != None:
                profile_options['navigator']['hardwareConcurrency'] = hardwareConcurrency
            if deviceMemory != 'random' and userAgent != 'random' and deviceMemory != None:
                profile_options['navigator']['deviceMemory'] = deviceMemory

            profile_options['navigator']['language'] = language

        profile = {
            "name": "default_name",
            "notes": "auto generated",
            "browserType": "chrome",
            "os": "win",
            "googleServicesEnabled": True,
            "lockEnabled": False,
            "audioContext": {
                "mode": "noise"
            },
            "canvas": {
                "mode": "noise"
            },
            "webRTC": {
                "mode": "disabled",
                "enabled": False,
                "customize": True,
                "fillBasedOnIp": True
            },
            "fonts": {
                "families": profile_options.get('fonts')
            },
            "navigator": profile_options.get('navigator', {}),
            "profile": json.dumps(profile_options),
            "geolocation": {
                    "mode": "allow",
                    "enabled": True,
                    "customize": True,
                    "fillBasedOnIp": False,
                    "isCustomCoordinates": False,
                    "latitude": 24.76176411847304,
                    "longitude": 90.39498007665587,
                    "accuracy": 10
                }
        }

        if options.get('storage'):
            profile['storage'] = options.get('storage')

        for k, v in options.items():
            profile[k] = v

        self.profile = profile
        self.extractProfileZip()

        # self.updatePreferences()
        print('profile: ' + json.dumps(profile))
        self.profile = profile

        # response = json.loads(
        #     requests.post(API_URL + '/browser/', headers=self.headers(), json=profile).content.decode('utf-8'))
        return profile

    def extractProfileZip(self):
        with zipfile.ZipFile(self.profile_zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.profile_path)
        # os.remove(self.profile_zip_path)

    # def update(self, options):
    #     self.profile_id = options.get('id')
    #     profile = self.getProfile()
    #     # print("profile", profile)
    #     for k, v in options.items():
    #         profile[k] = v
    #     resp = requests.put(API_URL + '/browser/' + self.profile_id, headers=self.headers(),
    #                         json=profile).content.decode('utf-8')
    #     # print("update", resp)
    #     # return json.loads(resp)

    def waitDebuggingUrl(self, delay_s, remote_orbita_url, try_count=3):
        url = remote_orbita_url + '/json/version'
        wsUrl = ''
        try_number = 1
        while wsUrl == '':
            time.sleep(delay_s)
            try:
                response = json.loads(requests.get(url).content)
                wsUrl = response.get('webSocketDebuggerUrl', '')
            except:
                pass
            if try_number >= try_count:
                return {'status': 'failure', 'wsUrl': wsUrl}
            try_number += 1

        remote_orbita_url_without_protocol = remote_orbita_url.replace('https://', '')
        wsUrl = wsUrl.replace('ws://', 'wss://').replace('127.0.0.1', remote_orbita_url_without_protocol)

        return {'status': 'success', 'wsUrl': wsUrl}

    # def startRemote(self, delay_s=3):
    #     responseJson = requests.post(
    #         API_URL + '/browser/' + self.profile_id + '/web',
    #         headers=self.headers(),
    #         json={'isNewCloudBrowser': self.is_new_cloud_browser}
    #     ).content.decode('utf-8')
    #     response = json.loads(responseJson)
    #     print('profileResponse', response)
    #
    #     remote_orbita_url = 'https://' + self.profile_id + '.orbita.gologin.com'
    #     if self.is_new_cloud_browser:
    #         if not response['remoteOrbitaUrl']:
    #             raise Exception('Couldn\' start the remote browser')
    #         remote_orbita_url = response['remoteOrbitaUrl']
    #
    #     return self.waitDebuggingUrl(delay_s, remote_orbita_url=remote_orbita_url)
    #
    # def stopRemote(self):
    #     response = requests.delete(
    #         API_URL + '/browser/' + self.profile_id + '/web',
    #         headers=self.headers(),
    #         params={'isNewCloudBrowser': self.is_new_cloud_browser}
    #     )
    #
    # def clearCookies(self, profile_id=None):
    #     self.cleaningLocalCookies = True
    #
    #     profile = self.profile_id if profile_id == None else profile_id
    #     resp = requests.post(API_URL + '/browser/' + profile + '/cookies?cleanCookies=true', headers=self.headers(),
    #                          json=[])
    #
    #     if resp.status_code == 204:
    #         return {'status': 'success'}
    #     else:
    #         return {'status': 'failure'}

    async def normalizePageView(self, page):
        if self.preferences.get("screenWidth") == None:
            self.profile = self.getProfile()
            self.preferences['screenWidth'] = int(self.profile.get("navigator").get("resolution").split('x')[0])
            self.preferences['screenHeight'] = int(self.profile.get("navigator").get("resolution").split('x')[1])
        width = self.preferences.get("screenWidth")
        height = self.preferences.get("screenHeight")
        await page.setViewport({"width": width, "height": height});


def getRandomPort():
    while True:
        port = random.randint(1000, 35000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            continue
        else:
            return port
        sock.close()
