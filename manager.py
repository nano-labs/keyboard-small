#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8

import wx
import json
import subprocess
import os

# import wx.lib.agw.flatnotebook as fnb
import wx.lib.agw.labelbook as LB
import wx.lib.buttons as buttons

CONFIG_FILE = "/Users/fabio/projects/keyboard-small/config.json"


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        kwargs["style"] = (
            kwargs.get("style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.SYSTEM_MENU | wx.CLOSE_BOX
        )
        super(MainFrame, self).__init__(*args, **kwargs)
        self.SetBackgroundColour(wx.Colour(24, 25, 21))

        pnl = wx.Panel(self)

        self.nb = LB.LabelBook(
            pnl,
            wx.ID_ANY,
            pos=wx.Point(5, 5),
            size=wx.Size(557, 400),
            agwStyle=LB.INB_SHOW_ONLY_TEXT | LB.INB_LEFT | LB.INB_NO_RESIZE | LB.INB_FIT_LABELTEXT,
        )
        self.nb.SetColour(LB.INB_TAB_AREA_BACKGROUND_COLOUR, wx.Colour(24, 25, 21))
        self.nb.SetColour(LB.INB_TEXT_COLOUR, wx.Colour(191, 191, 189))
        self.nb.SetColour(LB.INB_ACTIVE_TAB_COLOUR, wx.Colour(40, 41, 35))
        self.nb.SetColour(LB.INB_ACTIVE_TEXT_COLOUR, wx.Colour(191, 191, 189))
        self.nb.SetColour(LB.INB_HILITE_TAB_COLOUR, wx.Colour(40, 41, 35))

        imagelist = wx.ImageList(1, 1)
        imagelist.Add(
            wx.Bitmap("/Users/fabio/projects/keyboard-small/my_bitmap.png", wx.BITMAP_TYPE_PNG)
        )
        self.nb.AssignImageList(imagelist)

        self.texts = {}
        for i in range(1, 7):
            panel = wx.Panel(self.nb, wx.ID_ANY)
            text_area = wx.TextCtrl(
                parent=panel,
                id=wx.ID_ANY,
                value="",
                pos=wx.Point(5, 5),
                size=wx.Size(450, 370),
                style=wx.TE_MULTILINE,
            )
            text_area.SetForegroundColour(wx.Colour(248, 248, 248))
            text_area.SetDefaultStyle(wx.TextAttr(wx.Colour(248, 248, 248), wx.Colour(40, 41, 35)))
            text_area.SetBackgroundColour(wx.Colour(40, 41, 35))
            text_area.OSXDisableAllSmartSubstitutions()

            text_area.SetFont(
                wx.Font(
                    14,
                    wx.FONTFAMILY_TELETYPE,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD,
                    0,
                    "Courier New",
                )
            )
            self.nb.AddPage(panel, "Key {}".format(i))
            self.texts["key{}".format(i)] = text_area

        self.load_config()
        self.nb.ResizeTabArea()

        self.save_button = buttons.GenButton(pnl, -1, "Save", pos=(5, 315), size=wx.Size(100, 30))
        self.save_button.SetBackgroundColour(wx.Colour(40, 41, 35))
        self.save_button.SetForegroundColour(wx.Colour(191, 191, 189))

        self.push_button = buttons.GenButton(pnl, -1, "Push", pos=(5, 350), size=wx.Size(100, 30))
        self.push_button.SetBackgroundColour(wx.Colour(40, 41, 35))
        self.push_button.SetForegroundColour(wx.Colour(191, 191, 189))

        self.make_menu_bar()

        self.CreateStatusBar()
        self.SetStatusText("Nano-labs!")

    @property
    def serial_port(self):
        for p in os.listdir("/dev/"):
            if p.startswith("cu.usb"):
                return "/dev/{}".format(p)

    def load_config(self):
        base_config = {
            "key1": "// KEY 1\n",
            "key2": "// KEY 2\n",
            "key3": "// KEY 3\n",
            "key4": "// KEY 4\n",
            "key5": "// KEY 5\n",
            "key6": "// KEY 6\n",
        }
        try:
            config_file = open(CONFIG_FILE, "r")
        except IOError:
            config_file = open(CONFIG_FILE, "w")
            json.dump(base_config, config_file, indent=4, sort_keys=True)
            config_file.close()

        try:
            config_file = open(CONFIG_FILE, "r")
            config = json.load(config_file)
        except ValueError:
            config = base_config
        finally:
            config_file.close()

        for k, v in self.texts.items():
            v.write(config[k])
        return config

    def save_config(self):
        self.SetStatusText("Saving...")

        config = {}
        for k, v in self.texts.items():
            config[k] = "\n".join([v.GetLineText(l) for l in range(v.GetNumberOfLines())])
        with open(CONFIG_FILE, "w") as config_file:
            json.dump(config, config_file, indent=4, sort_keys=True)
        self.SetStatusText("Saved to {}".format(CONFIG_FILE))
        return config

    def make_menu_bar(self):
        fileMenu = wx.Menu()
        save_item = fileMenu.Append(-1, "&Save")
        push_item = fileMenu.Append(-1, "&Push")
        fileMenu.AppendSeparator()

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.on_save, save_item)
        self.Bind(wx.EVT_BUTTON, self.on_save, self.save_button)
        self.Bind(wx.EVT_MENU, self.on_push, push_item)
        self.Bind(wx.EVT_BUTTON, self.on_push, self.push_button)

    def OnExit(self, event):
        self.Close(True)

    def on_save(self, event):
        self.save_config()
        # wx.MessageBox("Saved")

    def process_helpers(self, key_config):
        def process_char(char):
            char = char.strip()
            if len(char) == 1 and char in (
                """abcdefghijklmnopqrstuvwxyz"""
                """ABCDEFGHIJKLMNOPQRSTUVWXY"""
                """Z1234567890"""
                """!@£$%^&*()_+-={}[]:;"'|<>,.?/`~"""
            ):
                return ord(char)
            return char

        def process_line(line):
            result = []
            if line.startswith("push"):
                params = line.split("(")[1].split(")")[0].split(",")
                for p in params:
                    result.append("Keyboard.press({});".format(process_char(p)))
                for p in params:
                    result.append("Keyboard.release({});".format(process_char(p)))
            elif line.startswith("hold"):
                params = line.split("(")[1].split(")")[0].split(",")
                for p in params:
                    result.append("Keyboard.press({});".format(process_char(p)))
            elif line.startswith("release"):
                params = line.split("(")[1].split(")")[0].split(",")
                for p in params:
                    result.append("Keyboard.release({});".format(process_char(p)))
            elif line.startswith("write"):
                params = line.split("(")[1].split(")")[0]
                result.append("Keyboard.print({});".format(params))
            else:
                result.append(line)
            return result

        lines = []
        for line in key_config.split("\n"):
            lines += process_line(line)
        return "\n".join(lines)

    def render(self, config):
        with open(
            "/Users/fabio/projects/keyboard-small/src/src.ino.template", "r"
        ) as template_file:
            template = template_file.read()
        template = template.replace("//<<KEY1>>", self.process_helpers(config["key1"]))
        template = template.replace("//<<KEY2>>", self.process_helpers(config["key2"]))
        template = template.replace("//<<KEY3>>", self.process_helpers(config["key3"]))
        template = template.replace("//<<KEY4>>", self.process_helpers(config["key4"]))
        template = template.replace("//<<KEY5>>", self.process_helpers(config["key5"]))
        template = template.replace("//<<KEY6>>", self.process_helpers(config["key6"]))
        return template

    def on_push(self, event):
        self.SetStatusText("Compiling binary and pushing to keyboard...")
        config = self.save_config()
        src = self.render(config)
        with open("/Users/fabio/projects/keyboard-small/src/src.ino", "w") as ino_file:
            ino_file.write(src)

        command_params = [
            "arduino-cli",
            "compile",
            "-b",
            "arduino:samd:nano_33_iot",
            os.path.abspath("/Users/fabio/projects/keyboard-small/src/"),
        ]
        print(" ".join(command_params))
        command = subprocess.Popen(
            command_params,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        )
        output = command.stdout.read()
        print(output)

        command_params = [
            "arduino-cli",
            "upload",
            "-b",
            "arduino:samd:nano_33_iot",
            "-p",
            self.serial_port,
            os.path.abspath("/Users/fabio/projects/keyboard-small/src/"),
        ]
        print(" ".join(command_params))
        command = subprocess.Popen(
            command_params,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        )
        output = command.stdout.read()
        print(output)
        if command.returncode != 0:
            self.SetStatusText(output.replace("\n", " ").decode())
        else:
            self.SetStatusText("Pushed!")


if __name__ == '__main__':
    app = wx.App()
    frm = MainFrame(None, title='Keyboard config', size=wx.Size(570, 440))
    frm.Show()
    app.MainLoop()
