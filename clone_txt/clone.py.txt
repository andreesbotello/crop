import os
import shutil
from docx import Document
from fpdf import FPDF

def setup_folders(folders):
    """Limpia y crea las carpetas de destino."""
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

def create_word(dest_path, title, content):
    """Genera un archivo .docx con el contenido del script."""
    doc = Document()
    doc.add_heading(title, 0)
    # Usamos fuente monoespaciada para que el código sea legible
    p = doc.add_paragraph()
    run = p.add_run(content)
    run.font.name = 'Courier New'
    doc.save(dest_path)

def create_pdf(dest_path, title, content):
    """Genera un archivo .pdf básico."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=10)
    # Reemplazamos caracteres que FPDF no maneja bien en modo simple
    clean_content = content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 5, txt=f"--- {title} ---\n\n" + clean_content)
    pdf.output(dest_path)

def clone_project():
    # Configuración
    source_dir = os.getcwd()
    folders = {
        'txt': os.path.join(source_dir, 'clone_txt'),
        'word': os.path.join(source_dir, 'clone_word'),
        'pdf': os.path.join(source_dir, 'clone_pdf')
    }
    
    allowed_exts = {'.py', '.sh', '.json', '.txt'}
    ignored = {'__pycache__', '.git', 'venv', 'env', 'migrations'}
    ignored.update(folders.keys())

    setup_folders(folders.values())

    print("🚀 Iniciando clonación multisectorial...")

    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if d not in ignored]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in allowed_exts:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, source_dir)
                base_name = rel_path.replace(os.sep, '_')

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 1. Guardar TXT
                    with open(os.path.join(folders['txt'], base_name + ".txt"), 'w', encoding='utf-8') as f_txt:
                        f_txt.write(content)

                    # 2. Guardar Word
                    create_word(os.path.join(folders['word'], base_name + ".docx"), rel_path, content)

                    # 3. Guardar PDF
                    create_pdf(os.path.join(folders['pdf'], base_name + ".pdf"), rel_path, content)

                    print(f"✅ Procesado: {rel_path}")

                except Exception as e:
                    print(f"❌ Error en {rel_path}: {e}")

    print(f"\n✨ ¡Listo! Revisa las carpetas: {', '.join(folders.keys())}")

if __name__ == "__main__":
    clone_project()