import renpy
from renpy.rollback import NoRollback
from renpy.display.im import Image
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -99 python:
"""
import os

_VALID_IMAGE_EXTS = frozenset(['.jpg', '.jpeg', '.png', '.webp'])
_JPEG_MAGIC = b'\xff\xd8\xff'
_PNG_MAGIC  = b'\x89PNG\r\n\x1a\n'

def _is_valid_image_file(bg_path: str) -> bool:
    '''Return True only when bg_path has a supported extension AND its file
    header matches a known image format.  Filters out non-image files such as
    .txt or .gitkeep and also catches truncated / corrupt JPEGs that Ren'Py
    would otherwise silently render as the gray-checkered "missing image"
    placeholder at runtime.'''
    if os.path.splitext(bg_path)[1].lower() not in _VALID_IMAGE_EXTS:
        return False
    try:
        f = renpy.file(bg_path)
        header = f.read(8)
        f.close()
        if not header:
            return False
        if header[:3] == _JPEG_MAGIC:
            return True
        if header == _PNG_MAGIC:
            return True
        # WebP: first 4 bytes "RIFF", bytes 8-12 would be "WEBP" – 8 bytes is
        # enough to confirm it's a RIFF container even without the WEBP tag.
        if header[:4] == b'RIFF':
            return True
        return False
    except Exception:
        return False

class BackGroundManager(NoRollback):
    bg_list: dict[str, Image] = {}

    def __init__(self):
        self.load("images/background_images")

    def load(self, path: str):
        '''
        Load all images from path as background images
        When calling method again, images with same filename will be changed
        '''
        for bg in (x for x in renpy.exports.list_files() if path in x):
            if not _is_valid_image_file(bg):
                print(f"INFO BackGroundManager: Skipping '{bg}' – not a valid image file.")
                continue
            # extract filename without extension
            name = os.path.splitext(os.path.basename(bg))[0]
            BackGroundManager.bg_list[name] = Image(bg)
        # Backward compat: older game installs shipped "Engeneering_Background.jpg"
        # (misspelled). If the corrected name is absent but the misspelled one
        # exists, create an alias so both old and new saves display the background.
        if ("images/background_images" in path
                and "Engineering_Background" not in BackGroundManager.bg_list
                and "Engeneering_Background" in BackGroundManager.bg_list):
            BackGroundManager.bg_list["Engineering_Background"] = BackGroundManager.bg_list["Engeneering_Background"]
        # If Engineering_Background is still missing (not yet added to the image
        # distribution package), fall back to the closest available office scene
        # so the Engineering Division room always has a visible background.
        if ("images/background_images" in path
                and "Engineering_Background" not in BackGroundManager.bg_list):
            for _fallback in ("RandD_Background", "Marketing_Background",
                              "Main_Office_Background", "CEO_Office_Background"):
                if _fallback in BackGroundManager.bg_list:
                    BackGroundManager.bg_list["Engineering_Background"] = BackGroundManager.bg_list[_fallback]
                    print(f"INFO BackGroundManager: Using '{_fallback}' as fallback for missing Engineering_Background.")
                    break

    def background(self, name: str) -> Image:
        '''
        Retrieve background image by name -> filename without extension.
        Returns None and logs a warning when the image is not found.
        '''
        result = BackGroundManager.bg_list.get(name)
        if result is None:
            print(f"WARNING background(): No background image found for '{name}'.")
        return result

bg_manager = BackGroundManager()
