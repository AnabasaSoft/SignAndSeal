import sys
import os
import math
import socket
import threading
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
import email.parser
import email.policy

# --- LIBRERÍAS CRIPTOGRÁFICAS (Legal/eIDAS) ---
try:
    from pyhanko.sign import signers, fields, pdf_signer
    from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
    from pyhanko.pdf_utils import text, images
    from pyhanko_certvalidator import ValidationContext
    PYHANKO_AVAILABLE = True
except ImportError:
    PYHANKO_AVAILABLE = False

# Librerías gráficas y PDF
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
                             QGraphicsPixmapItem, QGraphicsTextItem, QFileDialog,
                             QToolBar, QVBoxLayout, QWidget, QMessageBox, QInputDialog,
                             QGraphicsItem, QLabel, QMenu, QSizePolicy, QComboBox,
                             QFontDialog, QColorDialog, QDialog, QPushButton, QVBoxLayout,
                             QHBoxLayout, QProgressBar, QLineEdit, QFormLayout)
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
        "window_title": "Sign & Seal - Firmador Legal eIDAS",
        "tools": "Herramientas",
        "open_pdf": "📂 Abrir PDF",
        "add_sign": "✒️ Firma Visual",
        "import_sign": "📱 Importar (WiFi)",
        "cert_sign": "🔐 Firma Digital (Legal)",
        "add_text": "T Texto",
        "save_pdf": "💾 Guardar",
        "help": "❓ Ayuda",
        "del_text": "🗑️ Borrar Texto",
        "del_sign": "🗑️ Borrar Firma",
        "change_font": "🔠 Fuente",
        "change_color": "🎨 Color",
        "rotate_menu": "🔄 Rotar",
        "edit_text_title": "Editar Texto",
        "edit_text_label": "Contenido:",
        "input_scale_title": "Cambiar Tamaño",
        "input_scale_label": "Porcentaje (%):",
        "default_text": "Texto aquí...",
        "select_sign": "Seleccionar Firma",
        "save_dialog": "Guardar PDF Firmado",
        "success": "Éxito",
        "saved_msg": "PDF firmado correctamente.",
        "error": "Error",
        "pyhanko_error": "Falta la librería 'pyhanko'. Instala: pip install 'pyhanko[crypto]'",
        "cert_dialog_title": "Seleccionar Certificado Digital",
        "cert_file_label": "Archivo P12/PFX:",
        "cert_pass_label": "Contraseña:",
        "cert_browse": "Buscar...",
        "cert_reason": "Razón (Opcional):",
        "cert_location": "Lugar (Opcional):",
        "cert_signing": "Firmando criptográficamente...",
        "import_title": "Crear Firma con el Móvil",
        "import_status_wait": "1. Escanea el QR.\n2. Haz foto a tu firma.\n3. Se limpiará el fondo.",
        "import_status_success": "¡Firma recibida! Procesando...",
        "processing_error": "Error procesando imagen.",
        "help_title": "Guía - Sign & Seal",
        "help_content": "..."
    },
    "en": {
        "window_title": "Sign & Seal - Legal PDF Signer",
        "tools": "Tools",
        "open_pdf": "📂 Open PDF",
        "add_sign": "✒️ Visual Sign",
        "import_sign": "📱 Import (WiFi)",
        "cert_sign": "🔐 Digital Sign (Legal)",
        "add_text": "T Text",
        "save_pdf": "💾 Save",
        "help": "❓ Help",
        "del_text": "🗑️ Delete Text",
        "del_sign": "🗑️ Delete Signature",
        "change_font": "🔠 Font",
        "change_color": "🎨 Color",
        "rotate_menu": "🔄 Rotate",
        "edit_text_title": "Edit Text",
        "edit_text_label": "Content:",
        "input_scale_title": "Resize",
        "input_scale_label": "Percentage (%):",
        "default_text": "Text here...",
        "select_sign": "Select Signature",
        "save_dialog": "Save Signed PDF",
        "success": "Success",
        "saved_msg": "PDF signed successfully.",
        "error": "Error",
        "pyhanko_error": "Missing 'pyhanko'. Install: pip install 'pyhanko[crypto]'",
        "cert_dialog_title": "Select Digital Certificate",
        "cert_file_label": "P12/PFX File:",
        "cert_pass_label": "Password:",
        "cert_browse": "Browse...",
        "cert_reason": "Reason (Optional):",
        "cert_location": "Location (Optional):",
        "cert_signing": "Cryptographic signing...",
        "import_title": "Create Mobile Signature",
        "import_status_wait": "1. Scan QR.\n2. Take photo.\n3. Background removed.",
        "import_status_success": "Received! Processing...",
        "processing_error": "Processing error.",
        "help_title": "Guide - Sign & Seal",
        "help_content": "..."
    },
    "eu": {
        "window_title": "Sign & Seal - Legezko PDF Sinatzailea",
        "tools": "Tresnak",
        "open_pdf": "📂 Ireki PDF",
        "add_sign": "✒️ Ikus-Sinadura",
        "import_sign": "📱 Inportatu (WiFi)",
        "cert_sign": "🔐 Sinadura Digitala",
        "add_text": "T Testua",
        "save_pdf": "💾 Gorde",
        "help": "❓ Laguntza",
        "del_text": "🗑️ Ezabatu Testua",
        "del_sign": "🗑️ Ezabatu Sinadura",
        "change_font": "🔠 Letra-tipoa",
        "change_color": "🎨 Kolorea",
        "rotate_menu": "🔄 Biratu",
        "edit_text_title": "Editatu Testua",
        "edit_text_label": "Edukia:",
        "input_scale_title": "Tamaina Aldatu",
        "input_scale_label": "Ehunekoa (%):",
        "default_text": "Testua hemen...",
        "select_sign": "Hautatu Sinadura",
        "save_dialog": "Gorde Sinatutako PDFa",
        "success": "Arrakasta",
        "saved_msg": "PDFa ondo sinatu da.",
        "error": "Errorea",
        "pyhanko_error": "'pyhanko' falta da. Instalatu: pip install 'pyhanko[crypto]'",
        "cert_dialog_title": "Hautatu Ziurtagiri Digitala",
        "cert_file_label": "P12/PFX Fitxategia:",
        "cert_pass_label": "Pasahitza:",
        "cert_browse": "Arakatu...",
        "cert_reason": "Arrazoia (Aukerakoa):",
        "cert_location": "Lekua (Aukerakoa):",
        "cert_signing": "Kriptografikoki sinatzen...",
        "import_title": "Sortu Sinadura Mugikorrarekin",
        "import_status_wait": "1. Eskaneatu QR.\n2. Egin argazkia.\n3. Garbitu.",
        "import_status_success": "Jaso da! Prozesatzen...",
        "processing_error": "Errorea prozesatzean.",
        "help_title": "Gida - Sign & Seal",
        "help_content": "..."
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

# --- CLASES PARA FIRMA DIGITAL LEGAL ---

class CertDialog(QDialog):
    """Diálogo para seleccionar certificado .p12 y poner contraseña."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("cert_dialog_title"))
        self.resize(400, 200)
        self.cert_path = None
        self.password = None
        self.reason = ""
        self.location = ""

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Archivo
        file_layout = QHBoxLayout()
        self.txt_file = QLineEdit()
        self.btn_browse = QPushButton(tr("cert_browse"))
        self.btn_browse.clicked.connect(self.browse_cert)
        file_layout.addWidget(self.txt_file)
        file_layout.addWidget(self.btn_browse)
        form.addRow(tr("cert_file_label"), file_layout)

        # Contraseña
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow(tr("cert_pass_label"), self.txt_pass)

        # Metadata (PAdES)
        self.txt_reason = QLineEdit("I approve this document")
        form.addRow(tr("cert_reason"), self.txt_reason)
        self.txt_location = QLineEdit("Linux Desktop")
        form.addRow(tr("cert_location"), self.txt_location)

        layout.addLayout(form)

        # Botones
        btn_box = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept_data)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(btn_cancel)
        btn_box.addWidget(btn_ok)
        layout.addLayout(btn_box)

    def browse_cert(self):
        home_dir = os.path.expanduser("~")
        path, _ = QFileDialog.getOpenFileName(self, "Certificado", home_dir, "Certificates (*.p12 *.pfx)")
        if path:
            self.txt_file.setText(path)

    def accept_data(self):
        self.cert_path = self.txt_file.text()
        self.password = self.txt_pass.text()
        self.reason = self.txt_reason.text()
        self.location = self.txt_location.text()
        if self.cert_path and os.path.exists(self.cert_path):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid file")

class DigitalSigner:
    """Clase encargada de aplicar PAdES usando pyHanko."""
    @staticmethod
    def sign_pdf(input_pdf_path, output_pdf_path, p12_path, password, reason, location):
        if not PYHANKO_AVAILABLE:
            raise ImportError(tr("pyhanko_error"))

        try:
            # 1. Cargar la identidad del firmante desde el archivo P12/PFX
            signer = signers.P12Signer(
                entry_fname=p12_path,
                entry_cert_pass=password.encode('utf-8')
            )

            # 2. Configurar metadatos de la firma (PAdES básico)
            # Esto inserta la firma visible e invisible
            with open(input_pdf_path, 'rb') as inf:
                w = IncrementalPdfFileWriter(inf)

                # Crear campo de firma
                fields.append_signature_field(
                    w, sig_field_spec=fields.SigFieldSpec(
                        sig_field_name='Signature1'
                    )
                )

                # Configurar metadatos de firma
                meta = signers.PdfSignatureMetadata(
                    field_name='Signature1',
                    reason=reason,
                    location=location,
                    validation_context=None, # Para PAdES-LTA se necesitaría contexto OCSP/CRL
                    embed_validation_info=True
                )

                # 3. Escribir el PDF firmado
                with open(output_pdf_path, 'wb') as outf:
                    pdf_signer.sign_pdf(
                        w, meta, signer=signer, output=outf,
                    )
            return True
        except Exception as e:
            print(f"Signing Error: {e}")
            raise e

# --- LÓGICA DE SERVIDOR Y PROCESAMIENTO (Igual que v4.3) ---

class ImageProcessor:
    @staticmethod
    def remove_background(image_data):
        try:
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None: return None
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY_INV, 21, 10)
            result = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
            result[:, :, 0] = 0
            result[:, :, 1] = 0
            result[:, :, 2] = 0
            result[:, :, 3] = thresh
            height, width, channel = result.shape
            bytes_per_line = 4 * width
            qimg = QImage(result.data, width, height, bytes_per_line, QImage.Format.Format_RGBA8888)
            return QPixmap.fromImage(qimg)
        except Exception as e:
            return None

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = """
        <!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>body{font-family:sans-serif;text-align:center;padding:20px;background:#f0f0f0}
        .btn{background:#2196F3;color:white;padding:15px;border-radius:5px;display:block;margin:20px auto;width:80%}
        .box{background:white;padding:20px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}
        input{display:none} label{display:block;width:100%;height:100%;cursor:pointer}
        </style></head><body><div class="box"><h2>Sign & Seal</h2>
        <form method="POST" enctype="multipart/form-data">
        <label class="btn">📷 FOTO / PHOTO <input type="file" name="file" accept="image/*" onchange="this.form.submit()"></label>
        </form></div></body></html>"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            headers_str = ""
            for key, value in self.headers.items():
                headers_str += f"{key}: {value}\r\n"
            full_msg = headers_str.encode('utf-8') + b"\r\n" + body
            msg = email.parser.BytesParser(policy=email.policy.default).parsebytes(full_msg)
            file_data = None
            if msg.is_multipart():
                for part in msg.iter_parts():
                    if part.get_content_disposition() == 'form-data' and part.get_param('name', header='content-disposition') == 'file':
                        file_data = part.get_content()
                        break
            if file_data:
                self.server.received_data = file_data
                self.server.event_received.set()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"<h1>OK!</h1><script>setTimeout(function(){window.close()}, 2000);</script>")
            else: self.send_error(400)
        except: self.send_error(500)

class ImportServerThread(QThread):
    image_received = pyqtSignal(bytes)
    def __init__(self):
        super().__init__()
        self.server = None
        self.port = 8000
        self.ip = self.get_local_ip()
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]; s.close(); return ip
        except: return "127.0.0.1"
    def run(self):
        try:
            while True:
                try:
                    self.server = HTTPServer(('0.0.0.0', self.port), SimpleHTTPRequestHandler)
                    self.server.event_received = threading.Event()
                    self.server.received_data = None
                    break
                except OSError: self.port += 1
            while not self.isInterruptionRequested():
                self.server.handle_request()
                if self.server.event_received.is_set():
                    self.image_received.emit(self.server.received_data)
                    break
        except: pass
    def stop(self):
        self.requestInterruption()
        if self.server: self.server.server_close()

class ImportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("import_title"))
        self.setFixedSize(400, 500)
        self.uploaded_pixmap = None
        layout = QVBoxLayout(self)
        self.lbl_status = QLabel(tr("import_status_wait"))
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)
        self.lbl_qr = QLabel()
        self.lbl_qr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_qr.setFixedSize(380, 380)
        layout.addWidget(self.lbl_qr)
        self.progress = QProgressBar(); self.progress.hide(); layout.addWidget(self.progress)
        self.server_thread = ImportServerThread()
        self.server_thread.image_received.connect(self.on_image_received)
        self.server_thread.start()
        url = f"http://{self.server_thread.ip}:{self.server_thread.port}"
        self.generate_qr(url)
    def generate_qr(self, data):
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        im_data = img.convert("RGBA").tobytes("raw", "RGBA")
        qim = QImage(im_data, img.size[0], img.size[1], QImage.Format.Format_RGBA8888)
        self.lbl_qr.setPixmap(QPixmap.fromImage(qim).scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio))
    def on_image_received(self, data):
        self.lbl_status.setText(tr("import_status_success"))
        self.progress.show(); self.lbl_qr.hide()
        pixmap = ImageProcessor.remove_background(data)
        if pixmap:
            self.uploaded_pixmap = pixmap
            self.accept()
        else: self.lbl_status.setText(tr("processing_error")); self.progress.hide()
    def closeEvent(self, event):
        self.server_thread.stop()
        super().closeEvent(event)

# --- CLASES GRÁFICAS ---

class DraggableTextItem(QGraphicsTextItem):
    def __init__(self, text="Texto aquí", parent=None):
        super().__init__(text, parent)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setDefaultTextColor(QColor("black"))
        self.setFont(QFont("Arial", 12))
    def mouseDoubleClickEvent(self, event):
        text, ok = QInputDialog.getMultiLineText(None, tr("edit_text_title"), tr("edit_text_label"), self.toPlainText())
        if ok: self.setPlainText(text)
        super().mouseDoubleClickEvent(event)
    def contextMenuEvent(self, event):
        menu = QMenu()
        action_font = menu.addAction(tr("change_font"))
        action_color = menu.addAction(tr("change_color"))
        menu.addSeparator()
        action_del = menu.addAction(tr("del_text"))
        action = menu.exec(event.screenPos())
        if action == action_del: self.scene().removeItem(self)
        elif action == action_font:
            f, ok = QFontDialog.getFont(self.font(), None, tr("change_font"))
            if ok: self.setFont(f)
        elif action == action_color:
            c = QColorDialog.getColor(self.defaultTextColor(), None, tr("change_color"))
            if c.isValid(): self.setDefaultTextColor(c)

class DraggableImageItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, parent=None):
        super().__init__(pixmap, parent)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        rect = pixmap.rect()
        self.setTransformOriginPoint(rect.width()/2, rect.height()/2)
        self.handle_size = 12; self.handle_offset = 25; self.is_rotating = False
    def boundingRect(self): return super().boundingRect().adjusted(0, -self.handle_offset - self.handle_size, 0, 0)
    def shape(self):
        path = QPainterPath(); rect = self.pixmap().rect(); path.addRect(QRectF(rect))
        if self.isSelected():
            cx = rect.width()/2; hc = QPointF(cx, -self.handle_offset)
            path.addEllipse(hc, self.handle_size/1.5, self.handle_size/1.5)
        return path
    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.save(); rect = self.pixmap().rect()
            pen = QPen(QColor("#2196F3")); pen.setStyle(Qt.PenStyle.DashLine); pen.setWidth(2)
            painter.setPen(pen); painter.setBrush(Qt.BrushStyle.NoBrush); painter.drawRect(rect)
            cx = rect.width()/2; hc = QPointF(cx, -self.handle_offset)
            pen.setStyle(Qt.PenStyle.SolidLine); painter.setPen(pen)
            painter.drawLine(QPointF(cx, 0), hc)
            painter.setBrush(QColor("white")); painter.drawEllipse(hc, self.handle_size/2, self.handle_size/2)
            painter.restore()
    def wheelEvent(self, event):
        if self.isSelected():
            delta = event.delta(); step = 1.1
            ns = self.scale() * step if delta > 0 else self.scale() / step
            if 0.05 < ns < 5.0: self.setScale(ns)
            event.accept()
        else: super().wheelEvent(event)
    def mousePressEvent(self, event):
        if self.isSelected():
            pos = event.pos(); rect = self.pixmap().rect()
            hc = QPointF(rect.width()/2, -self.handle_offset)
            if (pos - hc).manhattanLength() < self.handle_size * 1.5:
                self.is_rotating = True; event.accept(); return
        self.is_rotating = False; super().mousePressEvent(event)
    def mouseMoveEvent(self, event):
        if self.is_rotating:
            ip = self.mapToScene(self.transformOriginPoint()); cp = event.scenePos()
            ang = math.degrees(math.atan2(cp.y()-ip.y(), cp.x()-ip.x())) + 90
            self.setRotation(ang)
        else: super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event): self.is_rotating = False; super().mouseReleaseEvent(event)
    def contextMenuEvent(self, event):
        menu = QMenu(); act = menu.addAction(tr("del_sign"))
        if menu.exec(event.screenPos()) == act: self.scene().removeItem(self)

class PDFCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setBackgroundBrush(QColor("#e0e0e0"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_path = get_resource_path("sign_and_seal_icon.png")
        if os.path.exists(icon_path): self.setWindowIcon(QIcon(icon_path))
        self.resize(1200, 850)
        self.doc = None; self.current_page_num = 0; self.zoom_level = 1.5; self.pdf_item = None
        self.init_ui(); self.update_texts()

    def init_ui(self):
        main_widget = QWidget(); layout = QVBoxLayout(main_widget)
        self.canvas = PDFCanvas(); layout.addWidget(self.canvas)
        self.setCentralWidget(main_widget)

        self.toolbar = QToolBar(); self.toolbar.setMovable(False); self.addToolBar(self.toolbar)

        # Acciones
        self.btn_open = QAction(self); self.btn_open.triggered.connect(self.open_pdf); self.toolbar.addAction(self.btn_open)
        self.toolbar.addSeparator()
        self.btn_sign = QAction(self); self.btn_sign.triggered.connect(self.add_signature); self.toolbar.addAction(self.btn_sign)
        self.btn_import = QAction(self); self.btn_import.triggered.connect(self.import_signature); self.toolbar.addAction(self.btn_import)
        self.btn_text = QAction(self); self.btn_text.triggered.connect(self.add_text); self.toolbar.addAction(self.btn_text)
        self.toolbar.addSeparator()

        # --- NUEVO BOTÓN: Certificado Digital ---
        self.btn_cert = QAction(self); self.btn_cert.triggered.connect(self.sign_digitally);
        # Ponemos un color o icono distintivo si quieres, por ahora texto
        self.toolbar.addAction(self.btn_cert)
        self.toolbar.addSeparator()

        self.btn_prev = QAction(self); self.btn_prev.triggered.connect(self.prev_page); self.toolbar.addAction(self.btn_prev)
        self.lbl_page = QLabel(" 0 / 0 "); self.toolbar.addWidget(self.lbl_page)
        self.btn_next = QAction(self); self.btn_next.triggered.connect(self.next_page); self.toolbar.addAction(self.btn_next)
        self.toolbar.addSeparator()

        self.btn_save = QAction(self); self.btn_save.triggered.connect(self.save_pdf); self.toolbar.addAction(self.btn_save)

        empty = QWidget(); empty.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred); self.toolbar.addWidget(empty)
        self.combo_lang = QComboBox(); self.combo_lang.addItems(["Español", "English", "Euskera"])
        self.combo_lang.currentIndexChanged.connect(self.change_language); self.toolbar.addWidget(self.combo_lang)
        spacer_label = QLabel("  "); self.toolbar.addWidget(spacer_label)
        self.btn_help = QAction(self); self.btn_help.triggered.connect(self.show_help); self.toolbar.addAction(self.btn_help)

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
        self.btn_import.setText(tr("import_sign"))
        self.btn_cert.setText(tr("cert_sign")) # Texto del botón legal
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
        if not self.doc: QMessageBox.warning(self, tr("error"), tr("open_pdf")); return
        dialog = ImportDialog(self)
        if dialog.exec():
            pixmap = dialog.uploaded_pixmap
            if pixmap: self.place_signature(pixmap)

    def place_signature(self, pixmap):
        if pixmap.height() > 200: pixmap = pixmap.scaledToHeight(200, Qt.TransformationMode.SmoothTransformation)
        item = DraggableImageItem(pixmap)
        center = self.canvas.mapToScene(self.canvas.viewport().rect().center())
        item.setPos(center)
        self.canvas.scene.addItem(item)

    def prev_page(self):
        if self.doc and self.current_page_num > 0: self.current_page_num -= 1; self.render_page()

    def next_page(self):
        if self.doc and self.current_page_num < len(self.doc) - 1: self.current_page_num += 1; self.render_page()

    # --- FUNCIÓN UNIFICADA PARA GUARDAR ---
    def generate_visual_pdf(self):
        """Genera el PDF visual (con imágenes/texto) en un archivo temporal."""
        try:
            # Crear copia en memoria del doc actual para no romperlo
            temp_doc = fitz.open()
            temp_doc.insert_pdf(self.doc)

            # Aplicar cambios a la página actual (solo soporta 1 página editada en MVP)
            page = temp_doc[self.current_page_num]

            for item in self.canvas.scene.items():
                if item == self.pdf_item: continue
                if isinstance(item, DraggableTextItem):
                    pos = item.scenePos(); x = pos.x() / self.zoom_level; y = pos.y() / self.zoom_level
                    text = item.toPlainText()
                    qcolor = item.defaultTextColor()
                    pdf_color = (qcolor.redF(), qcolor.greenF(), qcolor.blueF())
                    font_size = item.font().pointSize()
                    point = fitz.Point(x, y + font_size)
                    page.insert_text(point, text, fontsize=font_size, fontname="helv", color=pdf_color)
                elif isinstance(item, DraggableImageItem):
                    from PyQt6.QtCore import QBuffer, QByteArray
                    ba = QByteArray(); buf = QBuffer(ba); buf.open(QBuffer.OpenModeFlag.WriteOnly)
                    item.pixmap().save(buf, "PNG")
                    scale = item.scale()
                    rotation = int(item.rotation()) % 360
                    orig_w = item.pixmap().width(); orig_h = item.pixmap().height()
                    scaled_w = orig_w * scale; scaled_h = orig_h * scale
                    scene_center = item.sceneBoundingRect().center()
                    pdf_center_x = scene_center.x() / self.zoom_level
                    pdf_center_y = scene_center.y() / self.zoom_level
                    final_w = scaled_w / self.zoom_level
                    final_h = scaled_h / self.zoom_level
                    rect = fitz.Rect(pdf_center_x - final_w/2, pdf_center_y - final_h/2,
                                     pdf_center_x + final_w/2, pdf_center_y + final_h/2)
                    page.insert_image(rect, stream=ba.data(), rotate=rotation)

            # Guardar en archivo temporal
            fd, temp_path = tempfile.mkstemp(suffix=".pdf")
            os.close(fd)
            temp_doc.save(temp_path)
            temp_doc.close()
            return temp_path
        except Exception as e:
            print(f"Error generating visual PDF: {e}")
            return None

    def save_pdf(self):
        """Guardado visual simple (sin certificado)."""
        if not self.doc: return
        home_dir = os.path.expanduser("~")
        out_path, _ = QFileDialog.getSaveFileName(self, tr("save_dialog"), home_dir, "PDF Files (*.pdf)")
        if not out_path: return

        temp_pdf = self.generate_visual_pdf()
        if temp_pdf:
            shutil.move(temp_pdf, out_path)
            QMessageBox.information(self, tr("success"), tr("saved_msg"))

    def sign_digitally(self):
        """Flujo completo: Guardar visual + Firma Criptográfica (PAdES)."""
        if not self.doc: return

        # 1. Pedir Certificado
        dialog = CertDialog(self)
        if not dialog.exec(): return

        p12_path = dialog.cert_path
        password = dialog.password
        reason = dialog.reason
        location = dialog.location

        # 2. Pedir dónde guardar
        home_dir = os.path.expanduser("~")
        out_path, _ = QFileDialog.getSaveFileName(self, tr("save_dialog"), home_dir, "PDF Files (*.pdf)")
        if not out_path: return

        # 3. Generar PDF Visual Temporal
        temp_pdf = self.generate_visual_pdf()
        if not temp_pdf:
            QMessageBox.critical(self, tr("error"), "Error generating visual layer.")
            return

        # 4. Aplicar Firma Digital (PAdES)
        try:
            DigitalSigner.sign_pdf(temp_pdf, out_path, p12_path, password, reason, location)
            QMessageBox.information(self, tr("success"), tr("saved_msg") + "\n(PAdES Compliance)")
        except Exception as e:
            QMessageBox.critical(self, tr("error"), str(e))
        finally:
            if os.path.exists(temp_pdf): os.remove(temp_pdf)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    icon_path = get_resource_path("sign_and_seal_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
