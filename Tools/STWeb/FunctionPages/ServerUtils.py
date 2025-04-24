from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import ipaddress
import os
import threading
import time
import socket

class ServerControl():
    @staticmethod
    def get_local_ip():
        """动态获取本机IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            return "localhost"

    @staticmethod
    def start_report_server(report_path):
        """启动报告服务器并返回访问URL"""
        try:
            os.chdir(report_path)
            server = ThreadingHTTPServer(
                ('0.0.0.0', 8000),
                ServerControl.ZJUHTTPHandler
            )
            
            # 启动超时监控
            threading.Thread(
                target=ServerControl.server_monitor, 
                args=(server,),
                daemon=True
            ).start()
            
            threading.Thread(
                target=server.serve_forever,
                daemon=True
            ).start()
            
            return ServerControl.get_url()
        except Exception as e:
            raise Exception(f"服务器启动失败: {str(e)}")
    @staticmethod
    def get_url():
        """获取报告URL"""
        local_ip = ServerControl.get_local_ip()
        return f"http://{local_ip}:8000/topmsv/index.html"
    @staticmethod
    def server_monitor(server):
        """60分钟无操作自动关闭"""
        start_time = time.time()
        while time.time() - start_time < 3600:
            time.sleep(10)
        server.shutdown()

    class ZJUHTTPHandler(SimpleHTTPRequestHandler):
        """浙大内网访问控制器"""
        zju_networks = [
            ipaddress.ip_network('10.0.0.0/8'),
            ipaddress.ip_network('210.32.0.0/15'),
            ipaddress.ip_network('222.205.0.0/16'),
            ipaddress.ip_network('2001:da8::/32'),
            ipaddress.ip_network('2001:da8:8000::/48')
        ]
        
        def is_zju_client(self):
            try:
                client_ip = ipaddress.ip_address(self.client_address[0].split('%')[0])
                return any(client_ip in net for net in self.zju_networks)
            except:
                return False

        def do_GET(self):
            if not self.is_zju_client():
                self.send_error(403, "Forbidden", "仅限浙江大学内网访问")
                return
            super().do_GET()