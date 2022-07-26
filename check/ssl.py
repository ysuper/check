import socket
import ssl
import datetime


class SSL:

    @staticmethod
    def ssl_expire_date(hostname, port):  # 回傳憑證剩餘有效天數
        ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=hostname,
        )
        conn.settimeout(3.0)
        conn.connect((hostname, port))
        ssl_info = conn.getpeercert()
        expirationDate = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        now = datetime.datetime.now()
        delta = (expirationDate - now).days
        return delta


if __name__ == '__main__':
    print(SSL.ssl_expire_date('www.automodules.com', 443))
