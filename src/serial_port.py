import glob
import serial
import sys


class PortaSerial():
    def __init__(self):
        self.readAvailable = True
        self.porta = serial.Serial()

    def config_port(self, baudrate=115200, portName='COM1', timeout=1):
        self.porta.baudrate = int(baudrate)
        self.porta.port = str(portName)
        self.porta.timeout = timeout      # Timeout 1s

    def open_port(self):
        self.porta.open()
        print("Porta serial " + str(self.porta.name) + " aberta")
    # Lista as portas seriais disponiveis. Retorna uma lista com os nomes das portas
    def list_ports(self):
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    # Le buffer da porta serial
    def read_buffer(self, delimiters, tam):
        if not self.porta.timeout:
            raise TypeError('Port needs to have a timeout set!')
        read_buffer = b''
        while (self.porta.inWaiting() == 0):
            pass
        cnt = 0
        firstCarac = self.porta.read().decode()
        while firstCarac not in delimiters:
            firstCarac = self.porta.read().decode()
            cnt = cnt+1
            if cnt > 300:
                print('300 Bytes sem delimitador')
                return 'erro'

        delimiter = firstCarac

        # Depois de ler os bytes de inicio, le o resto do buffer
        while True:
            # Read in chunks. Each chunk will wait as long as specified by
            # timeout.
            byte_chunk = self.porta.read()
            if (byte_chunk.decode() == '\r'):
                break
            read_buffer += byte_chunk
            # Se leu exatamente o numero de bytes correspondente ao tamanho do buffer esperado
            # if len(byte_chunk) == tam:
            #     if byte_chunk[-1].decode() == '\r':
            #         break
            # else:
            #     print('erro')
            #     print(byte_chunk.decode())
            #     print(len(byte_chunk))
            #     break

        return read_buffer, delimiter
