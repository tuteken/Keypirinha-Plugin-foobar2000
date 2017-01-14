# Keypirinha: a fast launcher for Windows (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import os

class foobar2000(kp.Plugin):
    """
    Control and track selection of foobar2000.

    This plugin offers simple playback control of the currently running instance
    of foobar2000, if any (i.e.: Play, Pause, Stop, Previous, Next).
    """

    # Constants
    CONFIG_SECTION_MAIN = "main"
    DEFAULT_FILE_PATH = "C:\\Program Files (x86)\\foobar2000\\foobar2000.exe"
    ICON = "foobar2000.ico"
    PREFIX = "foobar2000"
    SIMPLE_COMMANDS = (
        { "target": "play",         "label": "Play",           "desc": "Requests foobar2000 to play the current track" },
        { "target": "pause",        "label": "Pause",          "desc": "Requests foobar2000 to pause the current track" },
        { "target": "playpause",    "label": "Play/Pause",     "desc": "Requests foobar2000 to play/plause the current track" },
        { "target": "prev",         "label": "Previous Track", "desc": "Requests foobar2000 to go to the previous track" },
        { "target": "next",         "label": "Next Track",     "desc": "Requests foobar2000 to go to the next track" },
        { "target": "rand",         "label": "Random Track",   "desc": "Requests foobar2000 to go to a random track"},
        { "target": "stop",         "label": "Stop",           "desc": "Requests foobar2000 to stop the current track" },
        { "target": "show",         "label": "Show Window",    "desc": "Requests foobar2000 to bring window to front"},
        { "target": "hide",         "label": "Hide Window",    "desc": "Requests foobar2000 to hide window away" })

    # Variables
    file_path = DEFAULT_FILE_PATH

    def __init__(self):
        super().__init__()
        self._debug = False
        self.dbg("CONSTRUCTOR")
        self.on_catalog()

    def on_start(self):
        self.dbg("On Start")
        self._read_config()

    def on_catalog(self):
        self.dbg("On Catalog")

        catalog = []
        for command in self.SIMPLE_COMMANDS:
            catalog.append(
                            self._create_keyword_item("{}: {}".format(self.PREFIX,
                            command['label']),
                            command['desc'],
                            command['target'],
                            self._load_resource_image(self.ICON))
                            )

        self.set_catalog(catalog)

    def on_suggest(self, user_input, items_chain):
        self.dbg('On Suggest "{}" (items_chain[{}])'.format(user_input, len(items_chain)))

    def on_execute(self, item, action):
        self.dbg("On execute (item {} : action {})".format(item, action))
        command = "\"{}\" /{}".format(self.file_path, item.target())
        self.dbg(command)
        os.system(command)

    def _read_config(self):
        self.dbg("Read Config")

        settings = self.load_settings()
        self.file_path = settings.get(
            "file_path",
            self.CONFIG_SECTION_MAIN,
            self.DEFAULT_FILE_PATH)
        self.dbg("Loaded file_path: {}".format(self.file_path))

    def _load_resource_image(self, image_name):
        return self.load_icon('res://{package}/{image}'.format(
            package=self.package_full_name(),
            image=image_name)
        )

    def _create_keyword_item(self, label, short_desc, target, icon):
        return self.create_item(
            category=kp.ItemCategory.KEYWORD,
            label=label,
            short_desc=short_desc,
            target=target,
            args_hint=kp.ItemArgsHint.FORBIDDEN,
            hit_hint=kp.ItemHitHint.NOARGS,
            icon_handle=icon)
