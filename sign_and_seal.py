import sys
import os
import math
import socket
import threading
import io
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer
import email.parser
import email.policy

# Librerías gráficas y PDF
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
                             QGraphicsPixmapItem, QGraphicsTextItem, QFileDialog,
                             QToolBar, QVBoxLayout, QWidget, QMessageBox, QInputDialog,
                             QGraphicsItem, QLabel, QMenu, QSizePolicy, QComboBox,
                             QFontDialog, QColorDialog, QDialog, QPushButton, QVBoxLayout,
                             QHBoxLayout, QProgressBar)
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal, QThread, QByteArray, QBuffer
from PyQt6.QtGui import (QPixmap, QImage, QColor, QFont, QAction, QIcon, QPainter,
                         QTransform, QPen, QPainterPath)

# Librerías para procesamiento de imagen y QR
import cv2
import numpy as np
import qrcode

# --- CONFIGURACIÓN GLOBAL ---
CURRENT_LANG = "es"

# --- DICCIONARIO DE TRADUCCIONES ---
TRANSLATIONS = {
    "es": {
        "window_title": "Sign & Seal - Firmador PDF Linux",
        "tools": "Herramientas",
        "open_pdf": "📂 Abrir PDF",
        "add_sign": "✒️ Añadir Firma",
        "import_sign": "📱 Crear Firma (WiFi)",
        "add_text": "T Añadir Texto",
        "save_pdf": "💾 Guardar PDF",
        "help": "❓ Ayuda",
        "del_text": "🗑️ Borrar Texto",
        "del_sign": "🗑️ Borrar Firma",
        "change_font": "🔠 Cambiar Fuente",
        "change_color": "🎨 Cambiar Color",
        "rotate_menu": "🔄 Rotar",
        "edit_text_title": "Editar Texto",
        "edit_text_label": "Contenido:",
        "input_scale_title": "Cambiar Tamaño",
        "input_scale_label": "Porcentaje (%):",
        "default_text": "Texto aquí...",
        "select_sign": "Seleccionar Firma",
        "save_dialog": "Guardar PDF Firmado",
        "success": "Éxito",
        "saved_msg": "PDF guardado correctamente.",
        "import_title": "Crear Firma con el Móvil",
        "import_status_wait": "1. Escanea el QR con tu móvil.\n2. Haz una foto a tu firma en un papel blanco.\n3. Se limpiará el fondo automáticamente.",
        "import_status_success": "¡Firma recibida! Procesando...",
        "processing_error": "Error al procesar la imagen.",
        "server_error": "Error al iniciar servidor.",
        "help_title": "Guía de Usuario - Sign & Seal",
        "help_content": """
        <h3>Bienvenido a Sign & Seal</h3>
        <p>La forma más rápida de firmar documentos PDF en Linux.</p>

        <h4>🛠️ Herramientas Principales</h4>
        <ul>
            <li><b>📂 Abrir PDF:</b> Carga el documento que necesitas firmar.</li>
            <li><b>✒️ Añadir Firma (Archivo):</b> Carga una imagen (PNG/JPG) que ya tengas en tu PC.</li>
            <li><b>📱 Crear Firma (WiFi):</b> Convierte tu móvil en un escáner. Escanea el QR, firma en un papel, hazle una foto y aparecerá en tu pantalla sin fondo.</li>
            <li><b>T Añadir Texto:</b> Inserta cajas de texto para rellenar nombres, fechas o formularios.</li>
        </ul>

        <h4>🖱️ Cómo editar (Ratón y Teclado)</h4>
        <ul>
            <li><b>Mover:</b> Haz clic y arrastra cualquier elemento (firma o texto) para colocarlo.</li>
            <li><b>🔄 Rotar:</b> Selecciona una firma. Verás un <b>círculo azul</b> encima de ella. Arrástralo para girar la firma libremente.</li>
            <li><b>🔍 Redimensionar:</b> Selecciona una firma y usa la <b>Rueda del Ratón</b> para agrandarla o reducirla.</li>
            <li><b>✏️ Editar Texto:</b> Haz <b>doble clic</b> sobre un texto para modificar su contenido.</li>
            <li><b>🎨 Estilo y Borrado:</b> Haz <b>clic derecho</b> sobre cualquier elemento para cambiar su fuente, color o borrarlo.</li>
        </ul>

        <h4>💾 Finalizar</h4>
        <ul>
            <li><b>Guardar PDF:</b> Crea un nuevo archivo PDF con todos tus cambios integrados. El documento original no se modifica.</li>
        </ul>

        <hr>
        <b>Desarrollado por:</b> Daniel Serrano Armenta (AnabasaSoft)<br>
        📧 <a href='mailto:anabasasoft@gmail.com'>anabasasoft@gmail.com</a><br>
        🐙 <a href='https://github.com/anabasasoft'>github.com/anabasasoft</a>
        """
    },
    "en": {
        "window_title": "Sign & Seal - Linux PDF Signer",
        "tools": "Tools",
        "open_pdf": "📂 Open PDF",
        "add_sign": "✒️ Add Signature",
        "import_sign": "📱 Create Signature (WiFi)",
        "add_text": "T Add Text",
        "save_pdf": "💾 Save PDF",
        "help": "❓ Help",
        "del_text": "🗑️ Delete Text",
        "del_sign": "🗑️ Delete Signature",
        "change_font": "🔠 Change Font",
        "change_color": "🎨 Change Color",
        "rotate_menu": "🔄 Rotate",
        "edit_text_title": "Edit Text",
        "edit_text_label": "Content:",
        "input_scale_title": "Resize",
        "input_scale_label": "Percentage (%):",
        "default_text": "Text here...",
        "select_sign": "Select Signature",
        "save_dialog": "Save Signed PDF",
        "success": "Success",
        "saved_msg": "PDF saved successfully.",
        "import_title": "Create Signature with Mobile",
        "import_status_wait": "1. Scan QR with your phone.\n2. Take a photo of your signature on white paper.\n3. Background will be removed automatically.",
        "import_status_success": "Signature received! Processing...",
        "processing_error": "Error processing image.",
        "server_error": "Error starting server.",
        "help_title": "User Guide - Sign & Seal",
        "help_content": """
        <h3>Welcome to Sign & Seal</h3>
        <p>The fastest way to sign PDF documents on Linux.</p>

        <h4>🛠️ Main Tools</h4>
        <ul>
            <li><b>📂 Open PDF:</b> Load the document you need to sign.</li>
            <li><b>✒️ Add Signature (File):</b> Load an image (PNG/JPG) from your PC.</li>
            <li><b>📱 Create Signature (WiFi):</b> Turn your phone into a scanner. Scan the QR, sign on paper, take a photo, and it appears on your screen background-free.</li>
            <li><b>T Add Text:</b> Insert text boxes to fill names, dates, or forms.</li>
        </ul>

        <h4>🖱️ How to Edit (Mouse & Keyboard)</h4>
        <ul>
            <li><b>Move:</b> Click and drag any element (signature or text) to position it.</li>
            <li><b>🔄 Rotate:</b> Select a signature. You will see a <b>blue circle</b> above it. Drag it to rotate freely.</li>
            <li><b>🔍 Resize:</b> Select a signature and use the <b>Mouse Wheel</b> to scale it up or down.</li>
            <li><b>✏️ Edit Text:</b> Double-click on any text to modify its content.</li>
            <li><b>🎨 Style & Delete:</b> Right-click on any element to change font, color, or delete it.</li>
        </ul>

        <h4>💾 Finish</h4>
        <ul>
            <li><b>Save PDF:</b> Creates a new PDF file with all your changes embedded. The original file remains untouched.</li>
        </ul>

        <hr>
        <b>Developed by:</b> Daniel Serrano Armenta (AnabasaSoft)<br>
        📧 <a href='mailto:anabasasoft@gmail.com'>anabasasoft@gmail.com</a><br>
        🐙 <a href='https://github.com/anabasasoft'>github.com/anabasasoft</a>
        """
    },
    "eu": {
        "window_title": "Sign & Seal - Linux PDF Sinatzailea",
        "tools": "Tresnak",
        "open_pdf": "📂 Ireki PDF",
        "add_sign": "✒️ Gehitu Sinadura",
        "import_sign": "📱 Sortu Sinadura (WiFi)",
        "add_text": "T Gehitu Testua",
        "save_pdf": "💾 Gorde PDF",
        "help": "❓ Laguntza",
        "del_text": "🗑️ Ezabatu Testua",
        "del_sign": "🗑️ Ezabatu Sinadura",
        "change_font": "🔠 Aldatu Letra-tipoa",
        "change_color": "🎨 Aldatu Kolorea",
        "rotate_menu": "🔄 Biratu",
        "edit_text_title": "Editatu Testua",
        "edit_text_label": "Edukia:",
        "input_scale_title": "Tamaina Aldatu",
        "input_scale_label": "Ehunekoa (%):",
        "default_text": "Testua hemen...",
        "select_sign": "Hautatu Sinadura",
        "save_dialog": "Gorde Sinatutako PDFa",
        "success": "Arrakasta",
        "saved_msg": "PDFa ondo gorde da.",
        "import_title": "Sortu Sinadura Mugikorrarekin",
        "import_status_wait": "1. Eskaneatu QR kodea mugikorrarekin.\n2. Egin argazkia sinadurari paper zurian.\n3. Atzeko planoa automatikoki garbituko da.",
        "import_status_success": "Sinadura jaso da! Prozesatzen...",
        "processing_error": "Errorea irudia prozesatzean.",
        "server_error": "Errorea zerbitzaria abiaraztean.",
        "help_title": "Erabiltzaile Gida - Sign & Seal",
        "help_content": """
        <h3>Ongi etorri Sign & Seal-era</h3>
        <p>Linux-en PDF dokumentuak sinatzeko modurik azkarrena.</p>

        <h4>🛠️ Tresna Nagusiak</h4>
        <ul>
            <li><b>📂 Ireki PDF:</b> Kargatu sinatu behar duzun dokumentua.</li>
            <li><b>✒️ Gehitu Sinadura (Fitxategia):</b> Kargatu ordenagailuan duzun irudi bat (PNG/JPG).</li>
            <li><b>📱 Sortu Sinadura (WiFi):</b> Bihurtu mugikorra eskaner. Eskaneatu QR-a, sinatu paper batean, atera argazkia eta pantailan agertuko da atzeko planorik gabe.</li>
            <li><b>T Gehitu Testua:</b> Txertatu testu-koadroak izenak, datak edo inprimakiak betetzeko.</li>
        </ul>

        <h4>🖱️ Nola Editatu (Sagua eta Teklatua)</h4>
        <ul>
            <li><b>Mugitu:</b> Egin klik eta arrastatu edozein elementu (sinadura edo testua) kokatzeko.</li>
            <li><b>🔄 Biratu:</b> Hautatu sinadura bat. <b>Zirkulu urdin</b> bat ikusiko duzu gainean. Arrastatu aske biratzeko.</li>
            <li><b>🔍 Tamaina Aldatu:</b> Hautatu sinadura bat eta erabili <b>Saguaren Gurpila</b> handitzeko edo txikitzeko.</li>
            <li><b>✏️ Editatu Testua:</b> Egin klik bikoitza testu batean edukia aldatzeko.</li>
            <li><b>🎨 Estiloa eta Ezabatu:</b> Egin klik eskuineko botoiarekin edozein elementutan letra-tipoa, kolorea aldatzeko edo ezabatzeko.</li>
        </ul>

        <h4>💾 Amaitu</h4>
        <ul>
            <li><b>Gorde PDF:</b> PDF fitxategi berri bat sortzen du aldaketa guztiekin. Jatorrizko fitxategia ez da aldatzen.</li>
        </ul>

        <hr>
        <b>Garatzailea:</b> Daniel Serrano Armenta (AnabasaSoft)<br>
        📧 <a href='mailto:anabasasoft@gmail.com'>anabasasoft@gmail.com</a><br>
        🐙 <a href='https://github.com/anabasasoft'>github.com/anabasasoft</a>
        """
    }
}

def tr(key):
    return TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["es"]).get(key, key)

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- LÓGICA DE SERVIDOR Y PROCESAMIENTO ---

class ImageProcessor:
    @staticmethod
    def remove_background(image_data):
        """
        Recibe bytes de imagen, elimina fondo usando OpenCV y devuelve QPixmap.
        Usa umbralización adaptativa para separar tinta del papel.
        """
        try:
            # 1. Convertir bytes a array numpy
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None: return None

            # 2. Convertir a escala de grises
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 3. Aplicar desenfoque gaussiano para reducir ruido del papel
            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            # 4. Umbralización adaptativa (Mágica para sombras)
            # Detecta bordes locales en lugar de un corte global
            thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY_INV, 21, 10)

            # 5. Crear canal Alpha
            # thresh es blanco (255) donde hay tinta, negro (0) donde es papel (gracias al INV)
            # Usamos 'thresh' directamente como máscara alpha.

            # 6. Colorear la tinta (puedes cambiar el color base aquí, ahora es negro)
            b, g, r = cv2.split(img)
            # Forzamos que la tinta sea negra o azul oscuro, ignorando el color original de la foto
            # O mejor, mantenemos el color original pero oscurecido

            # Estrategia "Clean Scan": Tinta negra, fondo transparente
            result = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
            result[:, :, 0] = 0 # Blue
            result[:, :, 1] = 0 # Green
            result[:, :, 2] = 0 # Red
            result[:, :, 3] = thresh # Alpha

            # 7. Convertir de vuelta a formato Qt
            height, width, channel = result.shape
            bytes_per_line = 4 * width
            qimg = QImage(result.data, width, height, bytes_per_line, QImage.Format.Format_RGBA8888)

            return QPixmap.fromImage(qimg)

        except Exception as e:
            print(f"Error procesando imagen: {e}")
            return None

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Manejador HTTP simple para recibir el archivo."""

    def do_GET(self):
        # HTML simple para subir archivo
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sign & Seal Upload</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding: 20px; background: #f0f0f0; }
                .btn { background: #2196F3; color: white; padding: 15px 30px; border: none;
                       border-radius: 5px; font-size: 18px; cursor: pointer; display: inline-block; margin-top: 20px;}
                .upload-box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                input[type="file"] { display: none; }
                label { background: #eee; padding: 10px 20px; border-radius: 5px; cursor: pointer; border: 1px solid #ccc;}
            </style>
        </head>
        <body>
            <div class="upload-box">
                <h2>Sign & Seal</h2>
                <p>Sube una foto de tu firma</p>
                <form method="POST" enctype="multipart/form-data">
                    <label for="file">📷 Seleccionar / Hacer Foto</label>
                    <input type="file" name="file" id="file" accept="image/*" onchange="this.form.submit()">
                </form>
            </div>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def do_POST(self):
        # FIX PYTHON 3.13: Usar 'email' en lugar de 'cgi' para parsear multipart
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            # Reconstruir las cabeceras y el cuerpo como un mensaje de email para el parser
            headers_str = ""
            for key, value in self.headers.items():
                headers_str += f"{key}: {value}\r\n"

            full_msg = headers_str.encode('utf-8') + b"\r\n" + body

            # Parsear el mensaje completo
            msg = email.parser.BytesParser(policy=email.policy.default).parsebytes(full_msg)

            file_data = None

            # Buscar la parte que corresponde al archivo subido
            if msg.is_multipart():
                for part in msg.iter_parts():
                    # El campo del formulario se llama 'file'
                    if part.get_content_disposition() == 'form-data' and part.get_param('name', header='content-disposition') == 'file':
                        file_data = part.get_content() # Devuelve bytes para imágenes
                        break

            if file_data:
                # Enviar señal al hilo principal
                self.server.received_data = file_data
                self.server.event_received.set()

                # Respuesta de éxito
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<h1>OK! Revisa tu PC.</h1><script>setTimeout(function(){window.close()}, 2000);</script>")
            else:
                self.send_error(400, "No file found")

        except Exception as e:
            print(f"Error en POST: {e}")
            self.send_error(500, f"Server Error: {e}")

class ImportServerThread(QThread):
    image_received = pyqtSignal(bytes)

    def __init__(self):
        super().__init__()
        self.server = None
        self.port = 8000
        self.ip = self.get_local_ip()

    def get_local_ip(self):
        try:
            # Truco para obtener la IP real que sale a internet
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def run(self):
        try:
            # Intentar puerto 8000, si falla, probar otro
            while True:
                try:
                    self.server = HTTPServer(('0.0.0.0', self.port), SimpleHTTPRequestHandler)
                    self.server.event_received = threading.Event()
                    self.server.received_data = None
                    break
                except OSError:
                    self.port += 1

            # Loop esperando conexión
            while not self.isInterruptionRequested():
                self.server.handle_request()
                if self.server.event_received.is_set():
                    self.image_received.emit(self.server.received_data)
                    break

        except Exception as e:
            print(f"Server error: {e}")

    def stop(self):
        self.requestInterruption()
        if self.server:
            self.server.server_close()

class ImportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("import_title"))
        self.setFixedSize(400, 500)
        self.uploaded_pixmap = None

        layout = QVBoxLayout(self)

        # 1. Instrucciones
        self.lbl_status = QLabel(tr("import_status_wait"))
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        # 2. QR Code
        self.lbl_qr = QLabel()
        self.lbl_qr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_qr.setFixedSize(380, 380)
        layout.addWidget(self.lbl_qr)

        # 3. Barra de progreso (oculta al inicio)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0) # Indeterminado
        self.progress.hide()
        layout.addWidget(self.progress)

        # Iniciar Servidor
        self.server_thread = ImportServerThread()
        self.server_thread.image_received.connect(self.on_image_received)
        self.server_thread.start()

        # Generar QR
        url = f"http://{self.server_thread.ip}:{self.server_thread.port}"
        self.generate_qr(url)

    def generate_qr(self, data):
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convertir PIL a QPixmap
        im_data = img.convert("RGBA").tobytes("raw", "RGBA")
        qim = QImage(im_data, img.size[0], img.size[1], QImage.Format.Format_RGBA8888)
        self.lbl_qr.setPixmap(QPixmap.fromImage(qim).scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio))

    def on_image_received(self, data):
        self.lbl_status.setText(tr("import_status_success"))
        self.progress.show()
        self.lbl_qr.hide()

        # Procesar en segundo plano para no congelar (aunque es rápido)
        pixmap = ImageProcessor.remove_background(data)

        if pixmap:
            self.uploaded_pixmap = pixmap
            self.accept() # Cerrar diálogo con éxito
        else:
            self.lbl_status.setText(tr("processing_error"))
            self.progress.hide()

    def closeEvent(self, event):
        self.server_thread.stop()
        super().closeEvent(event)

# --- CLASES GRÁFICAS (Iguales que v3.5) ---

class DraggableTextItem(QGraphicsTextItem):
    def __init__(self, text="Texto aquí", parent=None):
        super().__init__(text, parent)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
                      QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
                      QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setDefaultTextColor(QColor("black"))
        font = QFont("Arial", 12)
        self.setFont(font)

    def mouseDoubleClickEvent(self, event):
        text, ok = QInputDialog.getMultiLineText(
            None, tr("edit_text_title"), tr("edit_text_label"), self.toPlainText()
        )
        if ok:
            self.setPlainText(text)
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu()
        action_font = menu.addAction(tr("change_font"))
        action_color = menu.addAction(tr("change_color"))
        menu.addSeparator()
        action_delete = menu.addAction(tr("del_text"))

        action = menu.exec(event.screenPos())

        if action == action_delete:
            self.scene().removeItem(self)
        elif action == action_font:
            self.change_font()
        elif action == action_color:
            self.change_color()

    def change_font(self):
        font, ok = QFontDialog.getFont(self.font(), None, tr("change_font"))
        if ok:
            self.setFont(font)

    def change_color(self):
        color = QColorDialog.getColor(self.defaultTextColor(), None, tr("change_color"))
        if color.isValid():
            self.setDefaultTextColor(color)

class DraggableImageItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, parent=None):
        super().__init__(pixmap, parent)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
                      QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        rect = pixmap.rect()
        self.setTransformOriginPoint(rect.width() / 2, rect.height() / 2)
        self.handle_size = 12
        self.handle_offset = 25
        self.is_rotating = False

    def boundingRect(self):
        rect = super().boundingRect()
        return rect.adjusted(0, -self.handle_offset - self.handle_size, 0, 0)

    def shape(self):
        path = QPainterPath()
        rect = self.pixmap().rect()
        path.addRect(QRectF(rect))
        if self.isSelected():
            center_x = rect.width() / 2
            handle_center = QPointF(center_x, -self.handle_offset)
            hit_radius = self.handle_size / 1.5
            path.addEllipse(handle_center, hit_radius, hit_radius)
        return path

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.save()
            rect = self.pixmap().rect()
            pen = QPen(QColor("#2196F3"))
            pen.setStyle(Qt.PenStyle.DashLine)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(rect)
            center_x = rect.width() / 2
            handle_center = QPointF(center_x, -self.handle_offset)
            pen.setStyle(Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.drawLine(QPointF(center_x, 0), handle_center)
            painter.setBrush(QColor("white"))
            painter.drawEllipse(handle_center, self.handle_size/2, self.handle_size/2)
            painter.restore()

    def wheelEvent(self, event):
        if self.isSelected():
            delta = event.delta()
            step = 1.1
            if delta > 0: new_scale = self.scale() * step
            else: new_scale = self.scale() / step
            if 0.05 < new_scale < 5.0: self.setScale(new_scale)
            event.accept()
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):
        if self.isSelected():
            pos = event.pos()
            rect = self.pixmap().rect()
            center_x = rect.width() / 2
            handle_center = QPointF(center_x, -self.handle_offset)
            diff = pos - handle_center
            if diff.manhattanLength() < self.handle_size * 1.5:
                self.is_rotating = True
                event.accept()
                return
        self.is_rotating = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_rotating:
            item_pos = self.mapToScene(self.transformOriginPoint())
            cursor_pos = event.scenePos()
            angle_rad = math.atan2(cursor_pos.y() - item_pos.y(), cursor_pos.x() - item_pos.x())
            angle_deg = math.degrees(angle_rad) + 90
            self.setRotation(angle_deg)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.is_rotating = False
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu()
        action_delete = menu.addAction(tr("del_sign"))
        action = menu.exec(event.screenPos())
        if action == action_delete:
            self.scene().removeItem(self)

class PDFCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setBackgroundBrush(QColor("#e0e0e0"))

# --- MAIN WINDOW ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_path = get_resource_path("sign_and_seal_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.resize(1000, 800)
        self.doc = None
        self.current_page_num = 0
        self.zoom_level = 1.5
        self.pdf_item = None
        self.init_ui()
        self.update_texts()

    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        self.canvas = PDFCanvas()
        layout.addWidget(self.canvas)
        self.setCentralWidget(main_widget)

        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.btn_open = QAction(self)
        self.btn_open.triggered.connect(self.open_pdf)
        self.toolbar.addAction(self.btn_open)

        self.btn_sign = QAction(self)
        self.btn_sign.triggered.connect(self.add_signature)
        self.toolbar.addAction(self.btn_sign)

        # NUEVO BOTÓN: Importar WiFi
        self.btn_import = QAction(self)
        self.btn_import.triggered.connect(self.import_signature)
        self.toolbar.addAction(self.btn_import)

        self.btn_text = QAction(self)
        self.btn_text.triggered.connect(self.add_text)
        self.toolbar.addAction(self.btn_text)

        self.toolbar.addSeparator()

        self.btn_prev = QAction(self)
        self.btn_prev.triggered.connect(self.prev_page)
        self.toolbar.addAction(self.btn_prev)
        self.lbl_page = QLabel(" 0 / 0 ")
        self.toolbar.addWidget(self.lbl_page)
        self.btn_next = QAction(self)
        self.btn_next.triggered.connect(self.next_page)
        self.toolbar.addAction(self.btn_next)

        self.toolbar.addSeparator()
        self.btn_save = QAction(self)
        self.btn_save.triggered.connect(self.save_pdf)
        self.toolbar.addAction(self.btn_save)

        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(empty)
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(["Español", "English", "Euskera"])
        self.combo_lang.currentIndexChanged.connect(self.change_language)
        self.toolbar.addWidget(self.combo_lang)
        spacer_label = QLabel("  ")
        self.toolbar.addWidget(spacer_label)
        self.btn_help = QAction(self)
        self.btn_help.triggered.connect(self.show_help)
        self.toolbar.addAction(self.btn_help)

    def change_language(self, index):
        global CURRENT_LANG
        if index == 0: CURRENT_LANG = "es"
        elif index == 1: CURRENT_LANG = "en"
        elif index == 2: CURRENT_LANG = "eu"
        self.update_texts()

    def update_texts(self):
        self.setWindowTitle(tr("window_title"))
        self.toolbar.setWindowTitle(tr("tools"))
        self.btn_open.setText(tr("open_pdf"))
        self.btn_sign.setText(tr("add_sign"))
        self.btn_import.setText(tr("import_sign")) # Texto del nuevo botón
        self.btn_text.setText(tr("add_text"))
        self.btn_prev.setText(tr("prev"))
        self.btn_next.setText(tr("next"))
        self.btn_save.setText(tr("save_pdf"))
        self.btn_help.setText(tr("help"))

    def show_help(self):
        QMessageBox.about(self, tr("help_title"), tr("help_content"))

    def open_pdf(self):
        home_dir = os.path.expanduser("~")
        path, _ = QFileDialog.getOpenFileName(self, tr("open_pdf"), home_dir, "PDF Files (*.pdf)")
        if path:
            self.doc = fitz.open(path)
            self.current_page_num = 0
            self.render_page()

    def render_page(self):
        if not self.doc: return
        self.canvas.scene.clear()
        page = self.doc.load_page(self.current_page_num)
        mat = fitz.Matrix(self.zoom_level, self.zoom_level)
        pix = page.get_pixmap(matrix=mat)
        img_format = QImage.Format.Format_RGBA8888 if pix.alpha else QImage.Format.Format_RGB888
        qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, img_format)
        pixmap = QPixmap.fromImage(qimg)
        self.pdf_item = self.canvas.scene.addPixmap(pixmap)
        self.pdf_item.setZValue(-1)
        self.pdf_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.pdf_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.canvas.setSceneRect(QRectF(pixmap.rect()))
        self.lbl_page.setText(f" {self.current_page_num + 1} / {len(self.doc)} ")

    def add_text(self):
        if not self.doc: return
        item = DraggableTextItem(tr("default_text"))
        center = self.canvas.mapToScene(self.canvas.viewport().rect().center())
        item.setPos(center)
        self.canvas.scene.addItem(item)
        item.setFocus()

    def add_signature(self):
        if not self.doc: return
        home_dir = os.path.expanduser("~")
        path, _ = QFileDialog.getOpenFileName(self, tr("select_sign"), home_dir, "Images (*.png *.jpg *.jpeg)")
        if path:
            pixmap = QPixmap(path)
            self.place_signature(pixmap)

    def import_signature(self):
        if not self.doc:
            QMessageBox.warning(self, tr("error"), tr("open_pdf"))
            return

        dialog = ImportDialog(self)
        if dialog.exec():
            # Si el usuario subió algo y se procesó bien
            pixmap = dialog.uploaded_pixmap
            if pixmap:
                self.place_signature(pixmap)

    def place_signature(self, pixmap):
        if pixmap.height() > 200:
            pixmap = pixmap.scaledToHeight(200, Qt.TransformationMode.SmoothTransformation)
        item = DraggableImageItem(pixmap)
        center = self.canvas.mapToScene(self.canvas.viewport().rect().center())
        item.setPos(center)
        self.canvas.scene.addItem(item)

    def prev_page(self):
        if self.doc and self.current_page_num > 0:
            self.current_page_num -= 1
            self.render_page()

    def next_page(self):
        if self.doc and self.current_page_num < len(self.doc) - 1:
            self.current_page_num += 1
            self.render_page()

    def save_pdf(self):
        if not self.doc: return
        home_dir = os.path.expanduser("~")
        out_path, _ = QFileDialog.getSaveFileName(self, tr("save_dialog"), home_dir, "PDF Files (*.pdf)")
        if not out_path: return
        try:
            page = self.doc[self.current_page_num]
            for item in self.canvas.scene.items():
                if item == self.pdf_item: continue
                if isinstance(item, DraggableTextItem):
                    pos = item.scenePos()
                    x = pos.x() / self.zoom_level
                    y = pos.y() / self.zoom_level
                    text = item.toPlainText()
                    qcolor = item.defaultTextColor()
                    pdf_color = (qcolor.redF(), qcolor.greenF(), qcolor.blueF())
                    font_size = item.font().pointSize()
                    point = fitz.Point(x, y + font_size)
                    page.insert_text(point, text, fontsize=font_size, fontname="helv", color=pdf_color)
                elif isinstance(item, DraggableImageItem):
                    from PyQt6.QtCore import QBuffer, QByteArray
                    ba = QByteArray()
                    buf = QBuffer(ba)
                    buf.open(QBuffer.OpenModeFlag.WriteOnly)
                    item.pixmap().save(buf, "PNG")
                    scale = item.scale()
                    rotation = int(item.rotation()) % 360
                    orig_w = item.pixmap().width()
                    orig_h = item.pixmap().height()
                    scaled_w = orig_w * scale
                    scaled_h = orig_h * scale
                    scene_center = item.sceneBoundingRect().center()
                    pdf_center_x = scene_center.x() / self.zoom_level
                    pdf_center_y = scene_center.y() / self.zoom_level
                    final_w = scaled_w / self.zoom_level
                    final_h = scaled_h / self.zoom_level
                    rect = fitz.Rect(pdf_center_x - final_w/2, pdf_center_y - final_h/2,
                                     pdf_center_x + final_w/2, pdf_center_y + final_h/2)
                    page.insert_image(rect, stream=ba.data(), rotate=rotation)
            self.doc.save(out_path)
            QMessageBox.information(self, tr("success"), tr("saved_msg"))
        except Exception as e:
            QMessageBox.critical(self, tr("error"), str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    icon_path = get_resource_path("sign_and_seal_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
