import sys
import os
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
                             QGraphicsPixmapItem, QGraphicsTextItem, QFileDialog,
                             QToolBar, QVBoxLayout, QWidget, QMessageBox, QInputDialog,
                             QGraphicsItem, QLabel, QMenu, QSizePolicy, QComboBox,
                             QFontDialog, QColorDialog)
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPixmap, QImage, QColor, QFont, QAction, QIcon, QPainter

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
            <li><b>Editar:</b> Doble clic (texto) o Click derecho (formato/borrar).</li>
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
            <li><b>Edit:</b> Double click (text) or Right click (format/delete).</li>
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
            <li><b>Editatu:</b> Klik bikoitza (testua) edo Eskuineko botoia (formatua/ezabatu).</li>
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
    """Función helper para traducir cadenas según el idioma actual."""
    return TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["es"]).get(key, key)

def get_resource_path(relative_path):
    """
    Obtiene la ruta absoluta al recurso.
    Funciona para desarrollo (dev) y para cuando se compila con PyInstaller (_MEIPASS).
    """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

# --- CLASES DE ELEMENTOS GRÁFICOS ---

class DraggableTextItem(QGraphicsTextItem):
    """Caja de texto que se puede arrastrar, editar, borrar y formatear."""
    def __init__(self, text="Texto aquí", parent=None):
        super().__init__(text, parent)
        # Flags para permitir interacción
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
                      QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
                      QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setDefaultTextColor(QColor("black"))
        font = QFont("Arial", 12)
        self.setFont(font)

    def mouseDoubleClickEvent(self, event):
        """Doble clic para editar el contenido del texto."""
        text, ok = QInputDialog.getMultiLineText(
            None, tr("edit_text_title"), tr("edit_text_label"), self.toPlainText()
        )
        if ok:
            self.setPlainText(text)
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        """Menú contextual con opciones de formato y borrado."""
        menu = QMenu()

        # Acciones de estilo
        action_font = menu.addAction(tr("change_font"))
        action_color = menu.addAction(tr("change_color"))

        menu.addSeparator()

        # Acciones de edición
        action_delete = menu.addAction(tr("del_text"))

        # Ejecutar menú en la posición del ratón
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
    """Imagen (Firma) que se puede arrastrar y borrar."""
    def __init__(self, pixmap, parent=None):
        super().__init__(pixmap, parent)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
                      QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        # BoundingRectShape es más preciso para la selección
        self.setShapeMode(QGraphicsPixmapItem.ShapeMode.BoundingRectShape)

    def contextMenuEvent(self, event):
        """Clic derecho para borrar la firma."""
        menu = QMenu()
        action_delete = menu.addAction(tr("del_sign"))
        action = menu.exec(event.screenPos())
        if action == action_delete:
            self.scene().removeItem(self)

class PDFCanvas(QGraphicsView):
    """El visor principal que maneja la escena gráfica."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        # Renderizado de alta calidad
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.NoDrag) # Usamos select mode
        self.setBackgroundBrush(QColor("#e0e0e0"))

# --- VENTANA PRINCIPAL ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de icono usando la ruta segura
        icon_path = get_resource_path("sign_and_seal_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.resize(1000, 800)

        # Estado del PDF
        self.doc = None
        self.current_page_num = 0
        self.zoom_level = 1.5
        self.pdf_item = None

        self.init_ui()
        # Aplicar textos iniciales según el idioma por defecto
        self.update_texts()

    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        self.canvas = PDFCanvas()
        layout.addWidget(self.canvas)
        self.setCentralWidget(main_widget)

        # Barra de Herramientas
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        # --- Definición de Acciones ---
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

        # Espaciador para empujar elementos a la derecha
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(empty)

        # Selector de Idioma
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
        """Actualiza todas las etiquetas de la UI al cambiar el idioma."""
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
        # Abrir en el directorio Home por defecto
        home_dir = os.path.expanduser("~")
        path, _ = QFileDialog.getOpenFileName(self, tr("open_pdf"), home_dir, "PDF Files (*.pdf)")
        if path:
            self.doc = fitz.open(path)
            self.current_page_num = 0
            self.render_page()

    def render_page(self):
        if not self.doc: return
        self.canvas.scene.clear()

        # Cargar página actual
        page = self.doc.load_page(self.current_page_num)

        # Renderizar con zoom para calidad
        mat = fitz.Matrix(self.zoom_level, self.zoom_level)
        pix = page.get_pixmap(matrix=mat)

        # Convertir a formato compatible con Qt
        img_format = QImage.Format.Format_RGBA8888 if pix.alpha else QImage.Format.Format_RGB888
        qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, img_format)

        pixmap = QPixmap.fromImage(qimg)
        self.pdf_item = self.canvas.scene.addPixmap(pixmap)
        self.pdf_item.setZValue(-1) # Enviar al fondo
        # El fondo no debe moverse
        self.pdf_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.pdf_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

        self.canvas.setSceneRect(QRectF(pixmap.rect()))
        self.lbl_page.setText(f" {self.current_page_num + 1} / {len(self.doc)} ")

    def add_text(self):
        if not self.doc: return
        item = DraggableTextItem(tr("default_text"))
        # Centrar en la vista actual
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
            # Escalar si es muy grande
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

            # Recorrer todos los elementos de la escena
            for item in self.canvas.scene.items():
                if item == self.pdf_item: continue # Ignorar el fondo

                # Calcular coordenadas relativas al PDF original (revertir zoom)
                pos = item.scenePos()
                x = pos.x() / self.zoom_level
                y = pos.y() / self.zoom_level

                if isinstance(item, DraggableTextItem):
                    text = item.toPlainText()
                    # Recuperar color y tamaño elegidos
                    qcolor = item.defaultTextColor()
                    # PyMuPDF usa tuplas RGB de 0 a 1 (ej: 0.5, 0.5, 0.5)
                    pdf_color = (qcolor.redF(), qcolor.greenF(), qcolor.blueF())

                    # Recuperar tamaño de fuente
                    font_size = item.font().pointSize()

                    point = fitz.Point(x, y + font_size) # Ajuste visual de baseline

                    # Insertar texto con los atributos personalizados
                    page.insert_text(point, text, fontsize=font_size, fontname="helv", color=pdf_color)

                elif isinstance(item, DraggableImageItem):
                    from PyQt6.QtCore import QBuffer, QByteArray
                    ba = QByteArray()
                    buf = QBuffer(ba)
                    buf.open(QBuffer.OpenModeFlag.WriteOnly)
                    # Guardar el pixmap actual (tal cual se ve) en memoria
                    item.pixmap().save(buf, "PNG")

                    width = item.pixmap().width() / self.zoom_level
                    height = item.pixmap().height() / self.zoom_level
                    rect = fitz.Rect(x, y, x + width, y + height)

                    # Insertar imagen desde el buffer
                    page.insert_image(rect, stream=ba.data())

            self.doc.save(out_path)
            QMessageBox.information(self, tr("success"), tr("saved_msg"))

        except Exception as e:
            QMessageBox.critical(self, tr("error"), str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # --- RUTA DE ICONO GLOBAL SEGURA ---
    icon_path = get_resource_path("sign_and_seal_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    # -----------------------------------

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
