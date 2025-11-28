import sys
import os
import math  # Necesario para calcular ángulos
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
                             QGraphicsPixmapItem, QGraphicsTextItem, QFileDialog,
                             QToolBar, QVBoxLayout, QWidget, QMessageBox, QInputDialog,
                             QGraphicsItem, QLabel, QMenu, QSizePolicy, QComboBox,
                             QFontDialog, QColorDialog)
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (QPixmap, QImage, QColor, QFont, QAction, QIcon, QPainter,
                         QTransform, QPen, QPainterPath)

# --- CONFIGURACIÓN GLOBAL ---
CURRENT_LANG = "es"

# --- DICCIONARIO DE TRADUCCIONES ---
TRANSLATIONS = {
    "es": {
        "window_title": "Sign & Seal - Firmador PDF Linux",
        "tools": "Herramientas",
        "open_pdf": "📂 Abrir PDF",
        "add_sign": "✒️ Añadir Firma",
        "add_text": "T Añadir Texto",
        "prev": "⬅️ Ant",
        "next": "Sig ➡️",
        "save_pdf": "💾 Guardar PDF",
        "help": "❓ Ayuda",
        "del_text": "🗑️ Borrar Texto",
        "del_sign": "🗑️ Borrar Firma",
        "change_font": "🔠 Cambiar Fuente",
        "change_color": "🎨 Cambiar Color",
        "edit_text_title": "Editar Texto",
        "edit_text_label": "Contenido:",
        "default_text": "Texto aquí...",
        "select_sign": "Seleccionar Firma",
        "save_dialog": "Guardar PDF Firmado",
        "success": "Éxito",
        "saved_msg": "PDF guardado correctamente.",
        "error": "Error",
        "help_title": "Acerca de Sign & Seal",
        "help_content": """
        <h3>Sign & Seal</h3>
        <p>Una herramienta simple para firmar documentos PDF en Linux.</p>
        <b>Instrucciones:</b>
        <ul>
            <li><b>Abrir PDF:</b> Carga tu documento.</li>
            <li><b>Añadir Firma/Texto:</b> Arrastra los elementos.</li>
            <li><b>Rotar:</b> Selecciona la firma y arrastra el círculo azul superior.</li>
            <li><b>Redimensionar:</b> Usa la rueda del ratón sobre la firma seleccionada.</li>
            <li><b>Guardar:</b> Exporta el resultado a PDF.</li>
        </ul>
        <hr>
        <b>Desarrollado por:</b><br>Daniel Serrano Armenta<br>
        <a href='mailto:anabasasoft@gmail.com'>anabasasoft@gmail.com</a><br>
        <a href='https://github.com/anabasasoft'>github.com/anabasasoft</a>
        """
    },
    "en": {
        "window_title": "Sign & Seal - Linux PDF Signer",
        "tools": "Tools",
        "open_pdf": "📂 Open PDF",
        "add_sign": "✒️ Add Signature",
        "add_text": "T Add Text",
        "prev": "⬅️ Prev",
        "next": "Next ➡️",
        "save_pdf": "💾 Save PDF",
        "help": "❓ Help",
        "del_text": "🗑️ Delete Text",
        "del_sign": "🗑️ Delete Signature",
        "change_font": "🔠 Change Font",
        "change_color": "🎨 Change Color",
        "edit_text_title": "Edit Text",
        "edit_text_label": "Content:",
        "default_text": "Text here...",
        "select_sign": "Select Signature",
        "save_dialog": "Save Signed PDF",
        "success": "Success",
        "saved_msg": "PDF saved successfully.",
        "error": "Error",
        "help_title": "About Sign & Seal",
        "help_content": """
        <h3>Sign & Seal</h3>
        <p>A simple tool to sign PDF documents on Linux.</p>
        <b>Instructions:</b>
        <ul>
            <li><b>Open PDF:</b> Load your document.</li>
            <li><b>Add Sign/Text:</b> Drag elements onto the page.</li>
            <li><b>Rotate:</b> Select signature and drag the top blue handle.</li>
            <li><b>Resize:</b> Use mouse wheel on selected signature.</li>
            <li><b>Save:</b> Export result to PDF.</li>
        </ul>
        <hr>
        <b>Developed by:</b><br>Daniel Serrano Armenta<br>
        <a href='mailto:anabasasoft@gmail.com'>anabasasoft@gmail.com</a><br>
        <a href='https://github.com/anabasasoft'>github.com/anabasasoft</a>
        """
    },
    "eu": {
        "window_title": "Sign & Seal - Linux PDF Sinatzailea",
        "tools": "Tresnak",
        "open_pdf": "📂 Ireki PDF",
        "add_sign": "✒️ Gehitu Sinadura",
        "add_text": "T Gehitu Testua",
        "prev": "⬅️ Aurr",
        "next": "Hur ➡️",
        "save_pdf": "💾 Gorde PDF",
        "help": "❓ Laguntza",
        "del_text": "🗑️ Ezabatu Testua",
        "del_sign": "🗑️ Ezabatu Sinadura",
        "change_font": "🔠 Aldatu Letra-tipoa",
        "change_color": "🎨 Aldatu Kolorea",
        "edit_text_title": "Editatu Testua",
        "edit_text_label": "Edukia:",
        "default_text": "Testua hemen...",
        "select_sign": "Hautatu Sinadura",
        "save_dialog": "Gorde Sinatutako PDFa",
        "success": "Arrakasta",
        "saved_msg": "PDFa ondo gorde da.",
        "error": "Errorea",
        "help_title": "Sign & Seal-ari buruz",
        "help_content": """
        <h3>Sign & Seal</h3>
        <p>Linux-en PDF dokumentuak sinatzeko tresna sinplea.</p>
        <b>Argibideak:</b>
        <ul>
            <li><b>Ireki PDF:</b> Kargatu dokumentua.</li>
            <li><b>Gehitu Sinadura/Testua:</b> Arrastatu elementuak.</li>
            <li><b>Biratu:</b> Hautatu sinadura eta arrastatu goiko zirkulu urdina.</li>
            <li><b>Tamaina:</b> Erabili saguaren gurpila sinaduraren gainean.</li>
            <li><b>Gorde:</b> Esportatu emaitza PDFra.</li>
        </ul>
        <hr>
        <b>Garatzailea:</b><br>Daniel Serrano Armenta<br>
        <a href='mailto:anabasasoft@gmail.com'>anabasasoft@gmail.com</a><br>
        <a href='https://github.com/anabasasoft'>github.com/anabasasoft</a>
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

# --- CLASES DE ELEMENTOS GRÁFICOS ---

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
    """Imagen (Firma) con rotación visual y redimensionado por rueda."""
    def __init__(self, pixmap, parent=None):
        super().__init__(pixmap, parent)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
                      QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        # Establecer punto de origen en el centro para rotación correcta
        rect = pixmap.rect()
        self.setTransformOriginPoint(rect.width() / 2, rect.height() / 2)

        # Configuración del manejador de rotación
        self.handle_size = 12
        self.handle_offset = 25  # Distancia del handle por encima de la imagen
        self.is_rotating = False

    def boundingRect(self):
        """Sobrescribimos para incluir el área del manejador de rotación."""
        rect = super().boundingRect()
        # Ampliamos el área hacia arriba para incluir el handle
        return rect.adjusted(0, -self.handle_offset - self.handle_size, 0, 0)

    def shape(self):
        """
        Define la forma exacta de colisión para incluir el manejador.
        Esto soluciona el problema de que al hacer clic en el círculo se deseleccione.
        """
        path = QPainterPath()
        rect = self.pixmap().rect()
        path.addRect(QRectF(rect))

        if self.isSelected():
            # Si está seleccionado, añadimos el círculo del manejador a la forma interactuable
            center_x = rect.width() / 2
            handle_center = QPointF(center_x, -self.handle_offset)
            hit_radius = self.handle_size / 1.5
            path.addEllipse(handle_center, hit_radius, hit_radius)

        return path

    def paint(self, painter, option, widget=None):
        """Dibujado personalizado para mostrar guías de selección."""
        super().paint(painter, option, widget)

        if self.isSelected():
            painter.save()
            rect = self.pixmap().rect()

            # Dibujar borde discontinuo
            pen = QPen(QColor("#2196F3"))
            pen.setStyle(Qt.PenStyle.DashLine)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(rect)

            # Dibujar handle de rotación
            center_x = rect.width() / 2
            handle_center = QPointF(center_x, -self.handle_offset)

            pen.setStyle(Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.drawLine(QPointF(center_x, 0), handle_center)

            painter.setBrush(QColor("white"))
            # Dibujamos el círculo visual
            painter.drawEllipse(handle_center, self.handle_size/2, self.handle_size/2)

            painter.restore()

    def wheelEvent(self, event):
        """Redimensionar con la rueda del ratón si está seleccionado."""
        if self.isSelected():
            delta = event.delta()
            step = 1.1

            if delta > 0:
                new_scale = self.scale() * step
            else:
                new_scale = self.scale() / step

            if 0.05 < new_scale < 5.0:
                self.setScale(new_scale)

            event.accept()
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):
        """Detectar si clicamos en el handle para rotar."""
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
        """Calcular rotación si estamos en modo rotación."""
        if self.is_rotating:
            item_pos = self.mapToScene(self.transformOriginPoint())
            cursor_pos = event.scenePos()

            angle_rad = math.atan2(cursor_pos.y() - item_pos.y(),
                                   cursor_pos.x() - item_pos.x())

            angle_deg = math.degrees(angle_rad) + 90
            self.setRotation(angle_deg)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.is_rotating = False
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu()
        # Eliminada opción redundante de redimensionar
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

# --- VENTANA PRINCIPAL ---

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

                    rect = fitz.Rect(pdf_center_x - final_w/2,
                                     pdf_center_y - final_h/2,
                                     pdf_center_x + final_w/2,
                                     pdf_center_y + final_h/2)

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
