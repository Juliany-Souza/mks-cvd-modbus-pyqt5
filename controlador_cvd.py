from pyModbusTCP.client import ModbusClient
from pymodbus.client import ModbusTcpClient 
from pyModbusTCP.utils import encode_ieee
import struct
import time
import asyncio
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import (QTextEdit, QApplication,QDoubleSpinBox,QLabel, QFileDialog, QWidget, QToolTip, QPushButton, QMainWindow,QHBoxLayout,QVBoxLayout, QToolBar, QAction, QStatusBar, QComboBox, QLineEdit, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


# classe para colocar uma cor de fundo na interface:
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
        
# classe principal, contem interface grafica e funçoes        
class controladorCVD(QMainWindow):
    def __init__(self):
        super(controladorCVD, self).__init__()
        
        self.setWindowTitle("Controladores de Fluxo - CVD")
        self.setMinimumSize(QSize(1400,800))
        #define o cliente, ou seja, possui o endereço de ip do controlador, usando a biblioteca pyModbusTCP
        self.client_controlador1 = ModbusClient('192.168.2.155', port=502, auto_open=False)
        
        layout_geral=QVBoxLayout()
        layout_principal=QHBoxLayout()
        layout_conecta_desconecta=QVBoxLayout()
        layout_controlador1=QVBoxLayout()
        layout_controlador2=QVBoxLayout()
        layout_grafico_controlador1 = QVBoxLayout()
        layout_grafico_controlador2 = QVBoxLayout()
        
        
        topo_widget = QWidget()
        topo_layout = QHBoxLayout()
        topo_widget.setLayout(topo_layout)
        topo_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        topo_layout.setContentsMargins(20, 10, 20, 10)
        
        # Novo layout para agrupar titulo + logo
        box_titulo_logo = QWidget()
        box_layout = QHBoxLayout()
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.setSpacing(15)  # espaco entre titulo e logo
        box_titulo_logo.setLayout(box_layout)
        
        titulo = QLabel("Laboratório de Síntese e Caracterização de Nanomaterias")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")
        titulo.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        logo = QLabel()
        imagem = QPixmap("logo.png")
        imagem = imagem.scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Redimensiona a logo
        logo.setPixmap(imagem)
        logo.setAlignment(Qt.AlignCenter)
        
        box_layout.addWidget(titulo)
        box_layout.addWidget(logo)
        
        topo_layout.addStretch()
        topo_layout.addWidget(box_titulo_logo)
        topo_layout.addStretch()
        
        layout_geral.addWidget(topo_widget)
        layout_geral.addLayout(layout_principal)
        
        # Criar widgets para cada layout verticar, para definir bordas
        widget_conecta_desconecta = QWidget()
        widget_conecta_desconecta.setLayout(layout_conecta_desconecta)
        widget_conecta_desconecta.setStyleSheet("""
            QWidget {
                border: 1.2px solid black;
                border-radius: 5px;
                padding: 5px;
                margin: 5px;
            }
        """)

        widget_controlador1 = QWidget()
        widget_controlador1.setLayout(layout_controlador1)
        widget_controlador1.setStyleSheet("""
            QWidget {
                border: 1.2px solid black;
                border-radius: 5px;
                padding: 5px;
                margin: 5px;
            }
        """)

        widget_controlador2 = QWidget()
        widget_controlador2.setLayout(layout_controlador2)
        widget_controlador2.setStyleSheet("""
            QWidget {
                border: 1.2px solid black;
                border-radius: 5px;
                padding: 5px;
                margin: 5px;
            }
        """)
        
        layout_principal.addWidget(widget_conecta_desconecta)
        layout_principal.addWidget(widget_controlador1)
        layout_principal.addWidget(widget_controlador2)
        
        layout_conecta_desconecta_linha1=QHBoxLayout()
        layout_conecta_desconecta_linha2=QHBoxLayout()
        layout_conecta_desconecta_linha3=QHBoxLayout()
        
        layout_controlador1_linha0=QHBoxLayout()
        layout_controlador1_linha1=QHBoxLayout()
        layout_controlador1_linha2=QHBoxLayout()
        layout_controlador1_linha3=QHBoxLayout()
        layout_controlador1_linha4=QHBoxLayout()
        layout_controlador1_linha5=QHBoxLayout()
        layout_controlador1_linha6=QHBoxLayout()
        
        layout_controlador2_linha0=QHBoxLayout()
        layout_controlador2_linha1=QHBoxLayout()
        layout_controlador2_linha2=QHBoxLayout()
        layout_controlador2_linha3=QHBoxLayout()
        layout_controlador2_linha4=QHBoxLayout()
        layout_controlador2_linha5=QHBoxLayout()
        layout_controlador2_linha6=QHBoxLayout()
        
        layout_conecta_desconecta.addLayout(layout_conecta_desconecta_linha1)
        layout_conecta_desconecta.addLayout(layout_conecta_desconecta_linha2)
        layout_conecta_desconecta.addLayout(layout_conecta_desconecta_linha3)
        
        layout_controlador1.addLayout(layout_controlador1_linha0)
        layout_controlador1.addLayout(layout_controlador1_linha1)
        layout_controlador1.addLayout(layout_controlador1_linha2)
        layout_controlador1.addLayout(layout_controlador1_linha3)
        layout_controlador1.addLayout(layout_controlador1_linha4)
        layout_controlador1.addLayout(layout_controlador1_linha5)
        layout_controlador1.addLayout(layout_controlador1_linha6)
        
        layout_controlador2.addLayout(layout_controlador2_linha0)
        layout_controlador2.addLayout(layout_controlador2_linha1)
        layout_controlador2.addLayout(layout_controlador2_linha2)
        layout_controlador2.addLayout(layout_controlador2_linha3)
        layout_controlador2.addLayout(layout_controlador2_linha4)
        layout_controlador2.addLayout(layout_controlador2_linha5)
        layout_controlador2.addLayout(layout_controlador2_linha6)
        
        widget = Color('gray')
        widget.setLayout(layout_geral)
        
        self.setCentralWidget(widget)
        
#-------------------------------------------------------------------------------------------------------------------------------------
#                                          COMPONENTES DA INTERFACE
#--------------------------------------------------------------------------------------------------------------------------------------        
#                               BOTAO CONECTAR/DESCONECTA
        
        self.btn_conectar = QPushButton("Conectar")
        self.btn_conectar.clicked.connect(self.acao_conectar)    #chama a funcao ação_conectar
        self.btn_conectar.setFixedSize(150,150)
        self.btn_conectar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightgray;
            }
        """)
        layout_conecta_desconecta_linha1.addWidget(self.btn_conectar)
        
        self.btn_desconectar = QPushButton("Desconectado")
        self.btn_desconectar.setEnabled(False)  # começa desativado
        self.btn_desconectar.clicked.connect(self.acao_desconectar)  #chama a funcao ação_desconectar
        self.btn_desconectar.setFixedSize(150,150)
        self.btn_desconectar.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        layout_conecta_desconecta_linha2.addWidget(self.btn_desconectar)

#---------------------------------------------------------------------------------------------------------------------------------------
#                               VISOR CONECTAR/DESCONECTAR     

        self.visor_conectar = QTextEdit()
        self.visor_conectar.setReadOnly(True)  #usuario nao pode digitar, so visualizar
        self.visor_conectar.setStyleSheet("background-color: white; color: black;")
        self.visor_conectar.setFixedSize(150,150)
        layout_conecta_desconecta_linha3.addWidget(self.visor_conectar)
        
#---------------------------------------------------------------------------------------------------------------------
        #Controlador 1
        label_controlador_controlador1 = QLabel("Controlador 1:")
        font = label_controlador_controlador1.font()
        font.setPointSize(10)
        label_controlador_controlador1.setFont(font)
        label_controlador_controlador1.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        layout_controlador1_linha0.addWidget(label_controlador_controlador1)
        
        #Controlador 2
        label_controlador_controlador2 = QLabel("Controlador 2:")
        font = label_controlador_controlador2.font()
        font.setPointSize(10)
        label_controlador_controlador2 .setFont(font)
        label_controlador_controlador2 .setAlignment(Qt.AlignCenter | Qt.AlignTop)
        layout_controlador2_linha0.addWidget(label_controlador_controlador2)
    
#----------------------------------------------------------------------------------------------------------------------        
#                        LABEL, INPUT E BOTAO (PARA DEFINIR FLUXO)
        #Controlador 1
        label_setpoint_controlador1 = QLabel("Definir Fluxo:")
        font = label_setpoint_controlador1.font()
        font.setPointSize(10)
        label_setpoint_controlador1 .setFont(font)
        label_setpoint_controlador1 .setAlignment(Qt.AlignCenter | Qt.AlignTop)
              
        self.input_setpoint_controlador1 = QDoubleSpinBox()
        self.input_setpoint_controlador1.setRange(0.00, 100.00)        # define o intervalo permitido
        self.input_setpoint_controlador1.setDecimals(2)                # número de casas decimais
        self.input_setpoint_controlador1.setSingleStep(0.1)            # passo ao clicar nas setas
        self.input_setpoint_controlador1.setFixedSize(250,40)          # largura do campo
        self.input_setpoint_controlador1.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.input_setpoint_controlador1.setStyleSheet("font-size: 18px;")
        
        # Botao para enviar valor
        self.btn_enviar_setpoint1 = QPushButton("Enviar")
        self.btn_enviar_setpoint1.setFixedSize(100, 40)
        self.btn_enviar_setpoint1.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.btn_enviar_setpoint1.clicked.connect(self.definir_setpoint_controlador1)     #chama a funcao definir_setpoint_controlador1
        self.btn_enviar_setpoint1.setAutoDefault(False)
        self.btn_enviar_setpoint1.setDefault(False)
        
        # Layout auxiliar horizontal para agrupar o label e o input
        layout_label_input_controlador1 = QHBoxLayout()
        layout_label_input_controlador1.setSpacing(10)  # espaço entre o label e o input
        layout_label_input_controlador1.addWidget(label_setpoint_controlador1)
        layout_label_input_controlador1.addWidget(self.input_setpoint_controlador1)
        layout_label_input_controlador1.addWidget(self.btn_enviar_setpoint1)

        # Layout auxiliar para centralizar horizontalmente o grupo
        layout_centralizado_controlador1 = QHBoxLayout()
        layout_centralizado_controlador1.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout_centralizado_controlador1.addLayout(layout_label_input_controlador1)
        layout_centralizado_controlador1.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        layout_controlador1_linha1.addLayout(layout_centralizado_controlador1)

#------------Controlador 2-------------------------------------------------------------------------------------------------------
        label_setpoint_controlador2 = QLabel("Definir Fluxo:")
        font = label_setpoint_controlador2 .font()
        font.setPointSize(10)
        label_setpoint_controlador2 .setFont(font)
        label_setpoint_controlador2 .setAlignment(Qt.AlignCenter | Qt.AlignTop)
        
        self.input_setpoint_controlador2 = QDoubleSpinBox()
        self.input_setpoint_controlador2.setRange(0.00, 100.00)        # define o intervalo permitido
        self.input_setpoint_controlador2.setDecimals(2)                # número de casas decimais
        self.input_setpoint_controlador2.setSingleStep(0.1)            # passo ao clicar nas setas
        self.input_setpoint_controlador2.setFixedSize(250,40)          # largura do campo
        self.input_setpoint_controlador2.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.input_setpoint_controlador2.setStyleSheet("font-size: 18px;")
        
        # Botão para enviar valor
        self.btn_enviar_setpoint2 = QPushButton("Enviar")
        self.btn_enviar_setpoint2.setFixedSize(100, 40)
        self.btn_enviar_setpoint2.setStyleSheet("font-size: 16px; font-weight: bold;")
       #self.btn_enviar_setpoint2.clicked.connect(self.definir_setpoint_controlador2)
        self.btn_enviar_setpoint1.setAutoDefault(False)
        self.btn_enviar_setpoint1.setDefault(False)
        
        # Layout auxiliar horizontal para agrupar o label e o input
        layout_label_input_controlador_2 = QHBoxLayout()
        layout_label_input_controlador_2.setSpacing(10)  # espaço entre o label e o input
        layout_label_input_controlador_2.addWidget(label_setpoint_controlador2)
        layout_label_input_controlador_2.addWidget(self.input_setpoint_controlador2)
        layout_label_input_controlador_2.addWidget(self.btn_enviar_setpoint2)


        # Layout auxiliar para centralizar horizontalmente o grupo
        layout_centralizado_controlador_2 = QHBoxLayout()
        layout_centralizado_controlador_2.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout_centralizado_controlador_2.addLayout(layout_label_input_controlador_2)
        layout_centralizado_controlador_2.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        layout_controlador2_linha1.addLayout(layout_centralizado_controlador_2)

#-----------------------------------------------------------------------------------------------------------------
        #Controlador 1
        label_controlar_fluxo_controlador1 = QLabel("Monitorar Fluxo e Temperatura:")
        font = label_controlar_fluxo_controlador1 .font()
        font.setPointSize(10)
        label_controlar_fluxo_controlador1 .setFont(font)
        label_controlar_fluxo_controlador1 .setAlignment(Qt.AlignCenter | Qt.AlignTop)
        layout_controlador1_linha2.addWidget(label_controlar_fluxo_controlador1 )
        
        #Controlador 2
        label_controlar_fluxo_controlador2 = QLabel("Monitorar Fluxo e Temperatura:")
        font = label_controlar_fluxo_controlador2 .font()
        font.setPointSize(10)
        label_controlar_fluxo_controlador2 .setFont(font)
        label_controlar_fluxo_controlador2 .setAlignment(Qt.AlignCenter | Qt.AlignTop)
        layout_controlador2_linha2.addWidget(label_controlar_fluxo_controlador2 )
    
#-------------------------------------------------------------------------------------------------------------------    
#                    BOTAO INICIAR MONITORAMENTO, VISOR E BOTAO PARAR MONITORAMENTO

        #Controlador 1     
        self.btn_monitoramento_fluxo_controlador1 = QPushButton("on")
        self.btn_monitoramento_fluxo_controlador1.clicked.connect(self.acao_monitoramento_fluxo_controlador1)   # chama a funcao acao_monitoramento_fluxo_controlador1
        self.btn_monitoramento_fluxo_controlador1.setFixedSize(120,80)
        self.btn_monitoramento_fluxo_controlador1.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightgray;
            }
        """)
        layout_controlador1_linha3.addWidget(self.btn_monitoramento_fluxo_controlador1)
        
        self.visor_monitoramento_fluxo_controlador1 = QTextEdit()
        self.visor_monitoramento_fluxo_controlador1.setReadOnly(True)  #usuario nao pode digitar, so visualizar
        self.visor_monitoramento_fluxo_controlador1.setStyleSheet("background-color: white; color: black;")
        self.visor_monitoramento_fluxo_controlador1.setFixedSize(250,80)
        layout_controlador1_linha3.addWidget(self.visor_monitoramento_fluxo_controlador1)
        
        self.btn_parar_monitoramento_fluxo_controlador1 = QPushButton("off")
        self.btn_parar_monitoramento_fluxo_controlador1.clicked.connect(self.acao_parar_monitoramento_fluxo_controlador1)  ## chama a funcao acao_parar_monitoramento_fluxo_controlador1
        self.btn_parar_monitoramento_fluxo_controlador1.setFixedSize(120,80)
        self.btn_parar_monitoramento_fluxo_controlador1.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        layout_controlador1_linha3.addWidget(self.btn_parar_monitoramento_fluxo_controlador1)
        
#---------Controlador 2-------------------------------------------------------------------------------------------------------------------------------------------------------
        self.btn_monitoramento_fluxo_controlador2 = QPushButton("on")
        self.btn_monitoramento_fluxo_controlador2.clicked.connect(self.acao_monitoramento_fluxo_controlador2)
        self.btn_monitoramento_fluxo_controlador2.setFixedSize(120,80)
        self.btn_monitoramento_fluxo_controlador2.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightgray;
            }
        """)
        layout_controlador2_linha3.addWidget(self.btn_monitoramento_fluxo_controlador2)
        
        self.visor_monitoramento_fluxo_controlador2 = QTextEdit()
        self.visor_monitoramento_fluxo_controlador2.setReadOnly(True)  #usuario nao pode digitar, so visualizar
        self.visor_monitoramento_fluxo_controlador2.setStyleSheet("background-color: white; color: black;")
        self.visor_monitoramento_fluxo_controlador2.setFixedSize(250,80)
        layout_controlador2_linha3.addWidget(self.visor_monitoramento_fluxo_controlador2)
        
        self.btn_parar_monitoramento_fluxo_controlador2 = QPushButton("off")
        self.btn_parar_monitoramento_fluxo_controlador2.clicked.connect(self.acao_parar_monitoramento_fluxo_controlador2)
        self.btn_parar_monitoramento_fluxo_controlador2.setFixedSize(120,80)
        self.btn_parar_monitoramento_fluxo_controlador2.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        layout_controlador2_linha3.addWidget(self.btn_parar_monitoramento_fluxo_controlador2)

#---------------------------------------------------------------------------------------------------------------------------------
#                              GRAFICOS
        #Controlador 1        
        self.fig_monitoramento_fluxo_controlador1 = Figure(figsize=(5, 4), constrained_layout=True)
        self.ax_monitoramento_fluxo_controlador1 = self.fig_monitoramento_fluxo_controlador1.add_subplot(111)
        self.ax_monitoramento_fluxo_controlador1.set_xlabel("Tempo (s)")
        self.ax_monitoramento_fluxo_controlador1.set_ylabel("Fluxo (sccm)")
        self.ax_monitoramento_fluxo_controlador1.grid(True)
         #Cria um segundo eixo Y compartilhando o mesmo eixo X
        self.ax_temperatura_controlador1 = self.ax_monitoramento_fluxo_controlador1.twinx()
        self.ax_temperatura_controlador1.set_ylabel("Temperatura (°C)", color='red')
        self.ax_temperatura_controlador1.tick_params(axis='y', labelcolor='red')
        
        # Listas para armazenar dados
        self.tempo_monitoramento_controlador1 = []
        self.fluxo_monitoramento_controlador1 = []
        self.temperatura_monitoramento_controlador1 = []
        self.tempo_inicial_controlador1 = time.time()         # Marca o instante inicial da medicao

        # curvas no grafico
        self.linha_fluxo_controlador1, = self.ax_monitoramento_fluxo_controlador1.plot([], [], 'b-', label="Fluxo (sccm)")
        self.linha_temperatura_controlador1, = self.ax_temperatura_controlador1.plot([], [], 'r-', label="Temperatura (°C)")

        # Legendas
        self.ax_monitoramento_fluxo_controlador1.legend(loc="upper left")
        self.ax_temperatura_controlador1.legend(loc="upper right")
        
        # Cria o canvas (area grafica) e adiciona ao layout da interface
        self.canvas_monitoramento_fluxo_controlador1 = FigureCanvas(self.fig_monitoramento_fluxo_controlador1)
        layout_grafico_controlador1.addWidget(self.canvas_monitoramento_fluxo_controlador1)
        
        # Barra de ferramentas interativa
        self.toolbar_monitoramento_fluxo_controlador1 = NavigationToolbar(self.canvas_monitoramento_fluxo_controlador1, self)
        layout_grafico_controlador1.addWidget(self.toolbar_monitoramento_fluxo_controlador1)
        layout_controlador1_linha6.addLayout(layout_grafico_controlador1)
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        #Controlador 2
        self.fig_monitoramento_fluxo_controlador2 = Figure(figsize=(5, 4), constrained_layout=True)
        self.ax_monitoramento_fluxo_controlador2 = self.fig_monitoramento_fluxo_controlador2.add_subplot(111)
        self.ax_monitoramento_fluxo_controlador2.set_xlabel("Tempo (s)")
        self.ax_monitoramento_fluxo_controlador2.set_ylabel("Fluxo (sccm)")
        self.ax_monitoramento_fluxo_controlador2.grid(True)
        self.ax_temperatura_controlador2 = self.ax_monitoramento_fluxo_controlador2.twinx()
        self.ax_temperatura_controlador2.set_ylabel("Temperatura (°C)", color='red')
        self.ax_temperatura_controlador2.tick_params(axis='y', labelcolor='red')
        
        # Listas para armazenar dados
        self.tempo_monitoramento_controlador2 = []
        self.fluxo_monitoramento_controlador2 = []
        self.temperatura_monitoramento_controlador2 = []
        self.tempo_inicial_controlador2 = time.time()       # Marca o instante inicial da medicao

        # curvas no grafico
        self.linha_fluxo_controlador2, = self.ax_monitoramento_fluxo_controlador2.plot([], [], 'b-', label="Fluxo (sccm)")
        self.linha_temperatura_controlador2, = self.ax_temperatura_controlador2.plot([], [], 'r-', label="Temperatura (°C)")

        # Legendas
        self.ax_monitoramento_fluxo_controlador2.legend(loc="upper left")
        self.ax_temperatura_controlador2.legend(loc="upper right")
        
        # Cria o canvas (area grafica) e adiciona ao layout da interface
        self.canvas_monitoramento_fluxo_controlador2 = FigureCanvas(self.fig_monitoramento_fluxo_controlador2)
        layout_grafico_controlador2.addWidget(self.canvas_monitoramento_fluxo_controlador2)
        
        # Barra de ferramentas interativa
        self.toolbar_monitoramento_fluxo_controlador2 = NavigationToolbar(self.canvas_monitoramento_fluxo_controlador2, self)
        layout_grafico_controlador2.addWidget(self.toolbar_monitoramento_fluxo_controlador2)
        
        layout_controlador2_linha6.addLayout(layout_grafico_controlador2)
        
#---------------------------------------------------------------------------------------------------------------------------------------------
#                                                               EVENTOS
#---------------------------------------------------------------------------------------------------------------------------------------------
    def acao_conectar(self):
        if self.abrir_conexao():
            self.btn_conectar.setText("Conectado")
            self.btn_conectar.setEnabled(False)       #botao fica inativo
            self.btn_conectar.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    color: black;
                    font-weight: bold;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: darkgreen;
                }
            """)
            self.btn_desconectar.setEnabled(True)     #botao fica ativo
            self.btn_desconectar.setText("Desconectar")
            self.btn_desconectar.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: black;
                    font-weight: bold;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: lightgray;
                }
            """)
            self.visor_conectar.setText("Controlador 1\nconectado")
        
    def acao_desconectar(self):
        self.fechar_conexao()
        self.btn_conectar.setEnabled(True)           #botao fica ativo
        self.btn_desconectar.setText("Desconectado")
        self.btn_desconectar.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.btn_desconectar.setEnabled(False)     #botao inativo
        self.btn_conectar.setText("Conectar")
        self.btn_conectar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightgray;
            }
        """)
        self.visor_conectar.setText("Controlador 1\ndesconectado.")
        
    def acao_monitoramento_fluxo_controlador1(self):
        #limpa o grafico quando comeca a monitorar
        self.tempo_monitoramento_controlador1.clear()
        self.fluxo_monitoramento_controlador1.clear()
        self.temperatura_monitoramento_controlador1.clear()
        self.tempo_inicial_controlador1 = time.time()            # Registra o tempo inicial do monitoramento

        self.linha_fluxo_controlador1.set_data([], [])           # Reseta a linha do grafico de fluxo
        self.linha_temperatura_controlador1.set_data([], [])     # Reseta a linha do grafico de temperatura
        self.canvas_monitoramento_fluxo_controlador1.draw()      # Atualiza o canvas do grafico (grafico vazio)
        
        self.btn_monitoramento_fluxo_controlador1.setText("on")
        self.btn_monitoramento_fluxo_controlador1.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: darkgreen;
            }
        """)
        self.btn_parar_monitoramento_fluxo_controlador1.setText("off")
        self.btn_parar_monitoramento_fluxo_controlador1.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightgray;
            }
        """)
        self.btn_monitoramento_fluxo_controlador1.setEnabled(False)           #botao desativado
        self.btn_parar_monitoramento_fluxo_controlador1.setEnabled(True)      #botao ativado
        
        # Inicia thread de monitoramento
        self.thread_monitoramento = MonitoramentoThread(self.client_controlador1)                          #client_controlador1-contem o IP do servidor
        self.thread_monitoramento.dados_lidos.connect(self.atualizar_visor_controlador1)                   # Conecta o sinal 'dados_lidos' da thread a funcao que atualiza os valores (atualizar_visor_controlador1)
        self.thread_monitoramento.dados_lidos.connect(self.atualizar_grafico_monitoramento_controlador1)   # Conecta o mesmo sinal 'dados_lidos' a funcao que atualiza o grafico de monitoramento.
        self.thread_monitoramento.start()          # Inicia a execucao da thread de monitoramento.                     
    
    def acao_parar_monitoramento_fluxo_controlador1(self):
        self.btn_parar_monitoramento_fluxo_controlador1.setText("off")
        self.btn_parar_monitoramento_fluxo_controlador1.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.btn_monitoramento_fluxo_controlador1.setEnabled(True)             #botao ativado
        self.btn_parar_monitoramento_fluxo_controlador1.setEnabled(False)      #botao desativado
        self.btn_monitoramento_fluxo_controlador1.setText("on")
        self.btn_monitoramento_fluxo_controlador1.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightgray;
            }
        """)
        
        # Para thread
        if hasattr(self, 'thread_monitoramento'):    # Verifica se a thread de monitoramento ja existe
            self.thread_monitoramento.stop()         # Solicita a thread que pare sua execucao de forma segura
            self.thread_monitoramento.wait()         # Aguarda a thread finalizar completamente antes de prosseguir
            
    def atualizar_visor_controlador1(self, temperatura, fluxo):
        #O visor mostrara a temperatura e o fluxo mais recentes lidos pela thread
        self.visor_monitoramento_fluxo_controlador1.setText(
            f"Temperatura atual: {temperatura:.2f} °C\nFluxo atual: {fluxo:.4f} sccm"
        )

#------------Controlador 2--------------------------------------------------------------------------------------------------------------------        
    def acao_monitoramento_fluxo_controlador2(self):
        self.btn_monitoramento_fluxo_controlador2.setText("on")
        self.btn_monitoramento_fluxo_controlador2.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: darkgreen;
            }
        """)
        self.btn_parar_monitoramento_fluxo_controlador2.setText("off")
        self.btn_parar_monitoramento_fluxo_controlador2.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightgray;
            }
        """)
        self.btn_monitoramento_fluxo_controlador2.setEnabled(False)            #botao desativado
        self.btn_parar_monitoramento_fluxo_controlador2.setEnabled(True)       #botao ativado
    
    def acao_parar_monitoramento_fluxo_controlador2(self):
        self.btn_parar_monitoramento_fluxo_controlador2.setText("off")
        self.btn_parar_monitoramento_fluxo_controlador2.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.btn_monitoramento_fluxo_controlador2.setEnabled(True)             #botao ativado
        self.btn_parar_monitoramento_fluxo_controlador2.setEnabled(False)      #botao desativado
        self.btn_monitoramento_fluxo_controlador2.setText("on")
        self.btn_monitoramento_fluxo_controlador2.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightgray;
            }
        """)
    
  
#-----------------------------------------------------------------------------------------------------------------------------------------
#                                                                 ABRIR/FECHAR CONEXAO
#----------------------------------------------------------------------------------------------------------------------------------------

    def abrir_conexao(self):
        if not self.client_controlador1.is_open:        #verifica se nao estiver conectado
            if self.client_controlador1.open():         #conecta
                print("Conexão aberta com sucesso.")
                return True
            else:
                print("Falha ao abrir conexão.")
                return False
        else:                                          #se ja estiver conectado
            print("Conexão já está aberta.")
            return True


    def fechar_conexao(self):
        if self.client_controlador1.is_open:           #verifica se está conectado
            self.client_controlador1.close()           #desconecta
            print("Conexão fechada.")
        else:                                          
            print("Conexão já está fechada.")


#----------------------------------------------------------------------------------------------------------------------------------------
#                                                                DEFINIR SETPOINT
#-----------------------------------------------------------------------------------------------------------------------------------------

    def definir_setpoint_controlador1(self):
        #Le o valor atual do input de setpoint, O valor é retornado como float
        valor_float = self.input_setpoint_controlador1.value()
        # Chama a funcao assincrona que envia o setpoint para o controlador
        # Usa asyncio.run() para executar a coroutine de forma sincrona neste contexto
        asyncio.run(self.definir_setpoint_async(valor_float))
    
    async def definir_setpoint_async(self,valor_float):
        self.btn_enviar_setpoint1.setEnabled(False)  # Desabilita botao
        if not self.client_controlador1.is_open:
            print("Equipamento não conectado.")
            self.btn_enviar_setpoint1.setEnabled(True)
            return None
        #         converte float em int32 no formato IEEE (biblioteca pyModbusTCP)
        valor_int32 = encode_ieee(valor_float)
        #         dividir o int32 em dois registradores de 16 bits
        bytes_ = valor_int32.to_bytes(4, byteorder='big')
        registrador1 = int.from_bytes(bytes_[:2], 'big')     # bytes 0 e 1 (parte alta)
        registrador2 = int.from_bytes(bytes_[2:], 'big')     # bytes 2 e 3 (parte baixa)

        # Endereço do registrador de setpoint (0xA000 = 40960 decimal) funçao para definir o fluxo
        sucesso = self.client_controlador1.write_multiple_registers(40960, [registrador1, registrador2])
        if sucesso:
            print(f"Setpoint definido para {valor_float} sccm.")
        else:
            print("Falha ao definir setpoint.")
        self.btn_enviar_setpoint1.setEnabled(True) # Reabilita botao
        return sucesso
    
#-----------------------------------------------------------------------------------------------------------------------------------------
#                                                              ATUALIZAR GRAFICO
#-----------------------------------------------------------------------------------------------------------------------------------------

    def atualizar_grafico_monitoramento_controlador1(self, temperatura, fluxo):
        tempo_decorrido = time.time() - self.tempo_inicial_controlador1          # Calcula o tempo decorrido desde o inicio do monitoramento

        # Guarda os dados
        self.tempo_monitoramento_controlador1.append(tempo_decorrido)
        self.fluxo_monitoramento_controlador1.append(fluxo)
        self.temperatura_monitoramento_controlador1.append(temperatura)

        # Atualiza as curvas
        self.linha_fluxo_controlador1.set_data(self.tempo_monitoramento_controlador1, self.fluxo_monitoramento_controlador1)
        self.linha_temperatura_controlador1.set_data(self.tempo_monitoramento_controlador1, self.temperatura_monitoramento_controlador1)

        # Ajusta limites
        self.ax_monitoramento_fluxo_controlador1.set_xlim(0, max(10, tempo_decorrido))  #mostrar pelo menos 10 seg ou ate o tempo decorrido atual
        #ajusta os limites do eixo Y do grafico de fluxo
        #define minimo e maximo com uma margem de 1 unidade para melhor visualização
        self.ax_monitoramento_fluxo_controlador1.set_ylim(
            min(self.fluxo_monitoramento_controlador1) - 1,
            max(self.fluxo_monitoramento_controlador1) + 1
        )
        self.ax_temperatura_controlador1.set_ylim(
            min(self.temperatura_monitoramento_controlador1) - 1,
            max(self.temperatura_monitoramento_controlador1) + 1
        )

        # Redesenha
        self.canvas_monitoramento_fluxo_controlador1.draw()

#---------------------------------------------------------------------------------------------------------------------------------------
#                           CLASSE DE MONITORAMENTO

            
class MonitoramentoThread(QThread):
    dados_lidos = pyqtSignal(float, float)  # temperatura, fluxo
    
    
    def __init__(self, client, parent=None):
        super().__init__(parent)
        #Armazena o objeto client (controlado) para que possa ser usado dentro da classe
        self.client = client
        #Define a flag interna _running como True. Essa flag é usada para controlar o loop da thread (manter rodando ou parar)
        self._running = True

#---------------------------------------------------------------------------------------------------------------------------------------
#                                                       FUNCAO PARA LER O FLUXO ATUAL
#---------------------------------------------------------------------------------------------------------------------------------------
    async def ler_fluxo_atual(self,):
        if not self.client.is_open:
            print("Equipamento não conectado.")
            return None
    # Endereco do registrador do fluxo atual (0x4000 = 16384 decimal)
        regs = self.client.read_input_registers(16384, 2)
        if regs:
        # Combina os dois registradores (16 bits cada) em float32 IEEE754
            bytes_ = struct.pack('>HH', regs[0], regs[1])
            fluxo = struct.unpack('>f', bytes_)[0]
            print(f"Fluxo atual: {fluxo:.4f} sccm")      #.4f >> 4 casas decimais
            return fluxo
        else:
            print("Falha ao ler o fluxo.")
            return None

#--------------------------------------------------------------------------------------------------------------------
#                                                 LER O VALOR DA TEMPERATURA
#--------------------------------------------------------------------------------------------------------------------
    # Function Code 4 = Read Input Registers, nao holding registers = function Code 3
    async def ler_temperatura(self):
        if not self.client.is_open:
            print("Equipamento não conectado.")
            return None
        # Registro 0x4002 = 16386 decimal  
        regs = self.client.read_input_registers(16386, 2)
        if regs:
            bytes_ = struct.pack('>HH', regs[0], regs[1])
            temperatura = struct.unpack('>f', bytes_)[0]
            print(f"Temperatura atual: {temperatura:.2f} °C")
            return temperatura
        else:
            print("Falha ao ler a temperatura.")
            return None
#--------------------------------------------------------------------------------------------------------------------
#                                        FUNCAO DE MONITORAMENTO (FLUXO E TEMPERATURA)
#--------------------------------------------------------------------------------------------------------------------   
    async def monitorar_ambos(self):
        #Loop principal da thread assincrona de monitoramento. Enquanto a flag _running for True, o loop continua
        while self._running:
            temp = await self.ler_temperatura()
            fluxo = await self.ler_fluxo_atual()
            #Emite os dados lidos para visor_monitoramento_fluxo_controlador1 e grafico (sinais do PyQt). Se algum valor for None, envia 0 como padrão
            self.dados_lidos.emit(temp if temp else 0, fluxo if fluxo else 0)
            await asyncio.sleep(1)

#--------------------------------------------------------------------------------------------------------------------
#                                                 FUNCAO PARA INICIAR/PARAR A THREAD
#--------------------------------------------------------------------------------------------------------------------
    #funcao esponsável por iniciar o monitoramento em background
    def run(self):
        loop = asyncio.new_event_loop()                    # cria um novo event loop independente
        asyncio.set_event_loop(loop)                       # define ele como o loop atual na thread
        loop.run_until_complete(self.monitorar_ambos())    # executa a corrotina até acabar (quando _running = False)
    #interrompe a thread
    def stop(self):
        self._running = False
            
               

#app = QApplication(sys.argv)
#janela = controladorCVD()
#janela.show()
#sys.exit(app.exec_())


#------------------------------------------------------------------------------------------------------------------------------------
#                                FUNCAO EXTRA   verifica se o modo Full Modbus Control está ativo no controlador               
#------------------------------------------------------------------------------------------------------------------------------------

def verificar_modbus_control(ip="192.168.2.155"):
    client = ModbusTcpClient(host=ip, port=502)
    client.connect()

    result = client.read_holding_registers(address=0xA006, count=2)

    if result.isError():
        print("Erro ao ler registro.")
    else:
        valor = result.registers[1]  # LSB está no segundo registrador
        print(f"Full Modbus Control: {valor}")

    client.close()

# verificar_modbus_control()
#pode verificar no site fornecido pela mks 


