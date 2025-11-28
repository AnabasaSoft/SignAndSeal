# ✒️ Sign & Seal

<p align="center">
  <strong>Tu herramienta definitiva para firmar PDFs en Linux: Rápida, Ligera y Visual.</strong>
</p>

---

## 📖 Descripción

En el ecosistema de Linux, a menudo nos encontramos en una encrucijada al tratar con PDFs: o usamos visores simples que no permiten editar (Evince, Okular) o recurrimos a suites pesadas y complejas (LibreOffice Draw, Inkscape).

**Sign & Seal** nace para llenar ese vacío. Es el punto medio perfecto: *"Solo quiero firmar esto y enviarlo"*.

Esta aplicación no modifica el texto original del PDF (evitando corrupción de formato), sino que renderiza el documento como un lienzo de alta calidad y te permite superponer firmas y texto de manera intuitiva, tal como lo harías en una app de tablet.

---

## ✨ Características Principales

- **👆 Interfaz "Arrastrar y Soltar"**: Mueve tus firmas y textos libremente por el documento.
- **🖼️ Soporte de Imagen**: Añade tu firma escaneada (PNG/JPG) con transparencia automática (próximamente).
- **📝 Texto Enriquecido**: Rellena formularios no interactivos añadiendo cajas de texto.
- **🎨 Edición Visual**: Cambia la fuente, el tamaño y el color del texto con un clic derecho.
- **🌍 Multi-idioma**: Disponible en Español, Inglés y Euskera.
- **🚀 Rendimiento Nativo**: Construido sobre `PyMuPDF` para una renderización instantánea y `PyQt6` para una interfaz fluida.

---

## 🛠️ Instalación

### 📦 Instalación Rápida (Paquetes Precompilados)

La forma más sencilla de instalar Sign & Seal es descargando el paquete correspondiente a tu sistema operativo desde la [página de releases](https://github.com/danitxu79/SignAndSeal/releases):

#### 🐧 Linux (Debian/Ubuntu/Mint)
```bash
# Descarga el archivo .deb y ejecuta:
sudo dpkg -i sign-and-seal_*.deb
sudo apt-get install -f  # Para resolver dependencias si es necesario
```

#### 🐧 Linux (Fedora/RHEL/openSUSE)
```bash
# Descarga el archivo .rpm y ejecuta:
sudo rpm -i sign-and-seal_*.rpm
# o con dnf:
sudo dnf install sign-and-seal_*.rpm
```

#### 🐧 Linux (Arch/Manjaro/EndeavourOS)
```bash
# Disponible en AUR (Arch User Repository)
yay -S sign-and-seal
# o con otro helper de AUR:
paru -S sign-and-seal
```

#### 🪟 Windows
1. Descarga el instalador `sign-and-seal.exe`
2. Haz doble clic y sigue el asistente de instalación
3. La aplicación estará disponible en el menú de inicio

#### 🍎 macOS
1. Descarga el archivo `sign-and-seal_*.dmg` o `sign-and-seal_*.app`
2. Arrastra la aplicación a tu carpeta de Aplicaciones
3. En el primer arranque, puede que necesites permitir la ejecución en Preferencias del Sistema → Seguridad

---

### 🔧 Instalación desde el Código Fuente

Si prefieres ejecutar la aplicación desde el código fuente o contribuir al desarrollo:

#### Prerrequisitos

Necesitas tener Python 3 instalado.

```bash
# En Debian/Ubuntu/Mint
sudo apt install python3 python3-pip python3-venv

# En Arch/Manjaro
sudo pacman -S python python-pip
```

#### Pasos

1. **Clona el repositorio:**

```bash
git clone https://github.com/danitxu79/SignAndSeal.git
cd SignAndSeal
```

2. **Crea un entorno virtual (Recomendado):**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

> **Nota:** Si no tienes el archivo `requirements.txt`, las dependencias principales son: `PyQt6` y `pymupdf`.

4. **Ejecuta la aplicación:**

```bash
python sign_and_seal.py
```

---

## 🎮 Uso

1. Pulsa **Abrir PDF** para cargar tu documento.
2. Usa **Añadir Firma** para buscar una imagen de tu firma y colocarla en el documento.
3. Usa **Añadir Texto** para escribir fechas, nombres o rellenar campos.
4. **Click Derecho** sobre cualquier elemento para borrarlo o editar sus propiedades (fuente/color).
5. Pulsa **Guardar PDF** para exportar el documento final firmado.

---

## 📄 Licencia

Este proyecto se ofrece bajo un modelo de **Doble Licencia (Dual License)**:

### 1. LGPLv3 (GNU Lesser General Public License v3)

Ideal para proyectos de código abierto. Si usas esta biblioteca (especialmente si la modificas), debes cumplir con las obligaciones de la LGPLv3. Esto asegura que las mejoras al núcleo open-source se compartan con la comunidad.

### 2. Comercial (Privativa)

Si los términos de la LGPLv3 no se ajustan a tus necesidades (por ejemplo, para incluir este software en productos propietarios de código cerrado sin revelar el código fuente), por favor contacta al autor para adquirir una licencia comercial.

Para más detalles, consulta el archivo `LICENSE` incluido en este repositorio.

---

## 📬 Contacto y Autor

Este proyecto ha sido desarrollado con ❤️ y mucho café por:

**Daniel Serrano Armenta (AnabasaSoft)**

- 📧 **Email:** [anabasasoft@gmail.com](mailto:anabasasoft@gmail.com)
- 🐙 **GitHub:** [github.com/danitxu79](https://github.com/anabasasoft)
- 🌐 **Portafolio:** [danitxu79.github.io](https://danitxu79.github.io)

---

<p align="center">
  Si encuentras útil este proyecto, ¡no olvides darle una ⭐ en GitHub!
</p>
