# ============================================================
# arduino_control.py — Arduino & ESP32 Communication Module
# ============================================================
# This module communicates with Arduino and ESP32 boards via:
#   1. Serial (USB cable) — using pyserial
#   2. Bluetooth — using serial Bluetooth COM port
#   3. WiFi (ESP32) — using HTTP requests
#
# HOW IT WORKS:
#   - Serial/Bluetooth: Open COM port, send text commands, read responses
#   - WiFi (ESP32): Send HTTP GET/POST requests to ESP32's IP address
#
# HOW TO CUSTOMIZE:
#   - Change COM port in config.json "arduino_port" (e.g., "COM3", "COM5")
#   - Change baud rate in config.json "arduino_baud_rate" (default: 9600)
#   - Change ESP32 IP in config.json "esp32_ip" (e.g., "192.168.1.100")
#
# ARDUINO SKETCH EXAMPLE:
#   Your Arduino should read serial input and act on it:
#   
#   void setup() {
#     Serial.begin(9600);
#     pinMode(13, OUTPUT);
#   }
#   void loop() {
#     if (Serial.available()) {
#       String cmd = Serial.readStringUntil('\n');
#       cmd.trim();
#       if (cmd == "LED_ON") {
#         digitalWrite(13, HIGH);
#         Serial.println("LED is ON");
#       } else if (cmd == "LED_OFF") {
#         digitalWrite(13, LOW);
#         Serial.println("LED is OFF");
#       }
#     }
#   }
# ============================================================

import time
import threading

# --- Serial communication ---
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False

# --- WiFi (HTTP) communication ---
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class ArduinoController:
    """
    Manages connections to Arduino and ESP32 boards.
    
    Supports three connection types:
        - Serial USB (cable connection)
        - Bluetooth (serial over BT COM port)
        - WiFi (HTTP requests to ESP32)
    
    Usage:
        controller = ArduinoController(config)
        controller.connect_serial()          # Connect via USB
        controller.send_serial("LED_ON")     # Send command
        controller.disconnect_serial()       # Disconnect
    """
    
    def __init__(self, config: dict):
        """
        Initialize the Arduino controller with settings from config.
        
        Args:
            config (dict): Configuration dictionary from config.json
        """
        # --- Serial (USB / Bluetooth) settings ---
        self.serial_port = config.get('arduino_port', 'COM3')
        self.baud_rate = config.get('arduino_baud_rate', 9600)
        self.serial_connection = None  # Will hold the serial.Serial object
        
        # --- WiFi (ESP32) settings ---
        self.esp32_ip = config.get('esp32_ip', '192.168.1.100')
        self.esp32_port = config.get('esp32_port', 80)
        
        # --- Status tracking ---
        self.is_serial_connected = False
        self.is_wifi_connected = False
        self.last_response = ""
    
    # ========================================================
    # SERIAL (USB / Bluetooth) METHODS
    # ========================================================
    
    def list_ports(self) -> str:
        """
        List all available COM ports on this PC.
        Useful for finding your Arduino's port.
        
        Returns:
            str: Formatted list of available COM ports
        """
        if not SERIAL_AVAILABLE:
            return "❌ pyserial is not installed. Run: pip install pyserial"
        
        ports = serial.tools.list_ports.comports()
        if not ports:
            return "🔌 No COM ports found. Make sure your device is connected."
        
        result = "🔌 Available COM ports:\n"
        for port in ports:
            result += f"  → {port.device}: {port.description}\n"
        return result.strip()
    
    def connect_serial(self, port: str = None) -> str:
        """
        Connect to Arduino/ESP32 via Serial (USB cable or Bluetooth).
        
        Args:
            port (str, optional): COM port to use. Defaults to config setting.
        
        Returns:
            str: Connection status message
        """
        if not SERIAL_AVAILABLE:
            return "❌ pyserial is not installed. Run: pip install pyserial"
        
        if self.is_serial_connected:
            return f"✅ Already connected to {self.serial_port}"
        
        use_port = port if port else self.serial_port
        
        try:
            self.serial_connection = serial.Serial(
                port=use_port,
                baudrate=self.baud_rate,
                timeout=2  # 2 second read timeout
            )
            time.sleep(2)  # Wait for Arduino to reset after connection
            self.is_serial_connected = True
            self.serial_port = use_port
            return f"✅ Connected to {use_port} at {self.baud_rate} baud"
        except serial.SerialException as e:
            return f"❌ Could not connect to {use_port}: {e}"
        except Exception as e:
            return f"❌ Connection error: {e}"
    
    def disconnect_serial(self) -> str:
        """
        Disconnect from the serial port.
        
        Returns:
            str: Disconnection status message
        """
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.close()
                self.is_serial_connected = False
                return "✅ Serial connection closed."
            except Exception as e:
                return f"❌ Error closing connection: {e}"
        return "ℹ️ No active serial connection."
    
    def send_serial(self, command: str) -> str:
        """
        Send a text command to Arduino via Serial and read the response.
        
        The command is sent as a string followed by a newline character.
        Arduino should use Serial.readStringUntil('\\n') to read it.
        
        Args:
            command (str): Command to send (e.g., "LED_ON", "MOTOR_START")
        
        Returns:
            str: Response from Arduino, or error message
        """
        if not self.is_serial_connected or not self.serial_connection:
            return "❌ Not connected. Use 'connect arduino' first."
        
        try:
            # --- Send command with newline terminator ---
            self.serial_connection.write(f"{command}\n".encode('utf-8'))
            time.sleep(0.5)  # Small delay for Arduino to process
            
            # --- Read response ---
            response = ""
            while self.serial_connection.in_waiting > 0:
                response += self.serial_connection.readline().decode('utf-8').strip()
            
            self.last_response = response
            
            if response:
                return f"📡 Arduino response: {response}"
            else:
                return f"📡 Sent '{command}' to Arduino (no response received)"
        except Exception as e:
            self.is_serial_connected = False
            return f"❌ Serial communication error: {e}"
    
    def read_serial(self) -> str:
        """
        Read any available data from the serial port.
        
        Returns:
            str: Data from Arduino, or status message
        """
        if not self.is_serial_connected or not self.serial_connection:
            return "❌ Not connected. Use 'connect arduino' first."
        
        try:
            if self.serial_connection.in_waiting > 0:
                data = self.serial_connection.readline().decode('utf-8').strip()
                self.last_response = data
                return f"📡 Arduino says: {data}"
            else:
                return "📡 No data available from Arduino."
        except Exception as e:
            return f"❌ Read error: {e}"
    
    # ========================================================
    # WIFI (ESP32) METHODS
    # ========================================================
    
    def send_wifi(self, command: str) -> str:
        """
        Send a command to ESP32 via WiFi (HTTP GET request).
        
        The command is sent as a URL parameter:
            http://<esp32_ip>/command?cmd=<command>
        
        Your ESP32 should run a web server that reads this parameter.
        
        ESP32 SKETCH EXAMPLE (Arduino framework):
            #include <WiFi.h>
            #include <WebServer.h>
            
            WebServer server(80);
            
            void handleCommand() {
                String cmd = server.arg("cmd");
                if (cmd == "LED_ON") {
                    digitalWrite(2, HIGH);
                    server.send(200, "text/plain", "LED is ON");
                } else {
                    server.send(200, "text/plain", "Unknown command");
                }
            }
            
            void setup() {
                WiFi.begin("your_ssid", "your_password");
                server.on("/command", handleCommand);
                server.begin();
            }
            
            void loop() { server.handleClient(); }
        
        Args:
            command (str): Command to send (e.g., "LED_ON")
        
        Returns:
            str: ESP32's response or error message
        """
        if not REQUESTS_AVAILABLE:
            return "❌ 'requests' library not installed. Run: pip install requests"
        
        try:
            url = f"http://{self.esp32_ip}:{self.esp32_port}/command?cmd={command}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                self.is_wifi_connected = True
                return f"📡 ESP32 response: {response.text}"
            else:
                return f"❌ ESP32 returned status {response.status_code}"
        except requests.exceptions.ConnectionError:
            self.is_wifi_connected = False
            return f"❌ Cannot reach ESP32 at {self.esp32_ip}. Check WiFi connection."
        except requests.exceptions.Timeout:
            return f"❌ ESP32 connection timed out. Check if it's running."
        except Exception as e:
            return f"❌ WiFi communication error: {e}"
    
    def check_esp32_status(self) -> str:
        """
        Check if ESP32 is reachable over WiFi.
        
        Returns:
            str: Connection status message
        """
        if not REQUESTS_AVAILABLE:
            return "❌ 'requests' library not installed."
        
        try:
            url = f"http://{self.esp32_ip}:{self.esp32_port}/"
            response = requests.get(url, timeout=3)
            self.is_wifi_connected = True
            return f"✅ ESP32 is online at {self.esp32_ip}"
        except Exception:
            self.is_wifi_connected = False
            return f"❌ ESP32 not reachable at {self.esp32_ip}"
    
    # ========================================================
    # STATUS & UTILITY METHODS
    # ========================================================
    
    def get_status(self) -> str:
        """
        Get the current connection status of all interfaces.
        
        Returns:
            str: Formatted status of Serial and WiFi connections
        """
        serial_status = f"✅ Connected ({self.serial_port})" if self.is_serial_connected else "❌ Not connected"
        wifi_status = f"✅ Connected ({self.esp32_ip})" if self.is_wifi_connected else "❌ Not connected"
        
        return f"""🔌 Arduino/ESP32 Status:
  USB/Bluetooth: {serial_status}
  WiFi (ESP32):  {wifi_status}"""
    
    def cleanup(self) -> None:
        """
        Clean up all connections. Call this when the app exits.
        """
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.close()
            except:
                pass
        self.is_serial_connected = False
        self.is_wifi_connected = False
