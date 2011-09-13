def sanitize_filename(filename):
    filename = filename.replace('/', '')
    filename = filename.replace('\\', '')
    filename = filename.replace('?', '')
    filename = filename.replace('%', '')
    filename = filename.replace('*', '')
    filename = filename.replace(':', '')
    filename = filename.replace('|', '')
    filename = filename.replace('"', '')
    filename = filename.replace('<', '')
    filename = filename.replace('>', '')
    filename = filename.replace('.', '')
    return filename
