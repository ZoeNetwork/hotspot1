
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests
from requests.auth import HTTPBasicAuth

PISTAR_IP = "http://192.168.178.34"
USERNAME = "pi-star"
PASSWORD = "raspberry"

class ControlPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.status_label = Label(text="MMDVM Hotspot Control")
        self.add_widget(self.status_label)

        modes = ["DMR", "YSF", "D-Star", "P25", "NXDN", "M17"]
        for mode in modes:
            btn = Button(text="Enable " + mode)
            btn.bind(on_press=self.enable_mode)
            self.add_widget(btn)

        reboot_btn = Button(text="Reboot Hotspot")
        reboot_btn.bind(on_press=self.reboot_hotspot)
        self.add_widget(reboot_btn)

    def enable_mode(self, instance):
        mode = instance.text.split()[1].lower()
        url = f"{PISTAR_IP}/admin/expert/enable_{mode}.php"
        try:
            r = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
            self.status_label.text = f"{mode.upper()} enabled" if r.ok else f"Failed to enable {mode.upper()}"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def reboot_hotspot(self, instance):
        url = f"{PISTAR_IP}/admin/power.php?cmd=reboot"
        try:
            r = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
            self.status_label.text = "Reboot command sent" if r.ok else "Failed to reboot"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

class MMDVMApp(App):
    def build(self):
        return ControlPanel()

if __name__ == "__main__":
    MMDVMApp().run()
