import network
import time
import machine

# Almost doxed myself last time leaving the wifi name and password in
class Wifi:
    def __init__(self, ssid, password, ap_mode=False):
        self.WIFI_SSID = ssid
        self.WIFI_PASSWORD = password
        self.WIFI_AP_MODE = ap_mode
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.led.off()

    def wait_wlan(self, wlan):
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('[WIFI] waiting for connection...')
            time.sleep(1)

        if wlan.status() != 3:
            print("[WIFI] Failed setting up wifi, will restart in 1 second")
            self.led.on()
            time.sleep(1)
            self.led.off()
            machine.reset()

    def is_connected(self, wlan):
        return wlan.isconnected()

    def setup_ap(self):
        wlan = network.WLAN(network.AP_IF)
        wlan.config(essid=self.WIFI_SSID, password=self.WIFI_PASSWORD)
        wlan.active(True)
        
        while not self.is_connected(wlan):
            print('[WIFI] Waiting for connection to access point...')
            time.sleep(1)

        print('Set up access point:', self.WIFI_SSID, 'with IP = ', wlan.ifconfig()[0])
        return wlan

    def connect_wlan(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        wlan.disconnect()

        wlan.active(True)
        self.led.on()  # Turn on LED when starting connection attempt
        wlan.connect(self.WIFI_SSID, self.WIFI_PASSWORD)

        while not self.is_connected(wlan):
            print('[WIFI] Connecting to Wi-Fi...')
            time.sleep(1)
            self.led.toggle()  # Flash the LED during the connection attempt

        self.led.on()  # Turn off LED once connected
        print('[WIFI] Connected to Wi-Fi:', self.WIFI_SSID, 'with IP = ', wlan.ifconfig()[0])
        return wlan

    def run(self):
        wlan = self.connect_wlan() if not self.WIFI_AP_MODE else self.setup_ap()
