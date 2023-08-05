import pathlib
import requests

PAXURL = 'https://pax.ulaval.ca'

class Path(pathlib.Path):
    """This class behaves has a PAX replacement for the standard `pathlib.Path`.

    It adds a path prefix that is either:
    1. `../fichiers/` if this relative folder exists;
    2. `/pax/shared/{course}/{paths}` if this absolute path exists locally;
    3. or an absolute writeable `/tmp/pax/{course}/` prefix otherwise.

    Moreover, if the path does not exist, it tries to download it from the PAX server.

    Otherwise, it behaves as a standard pathlib path.
    """
    _flavour = type(pathlib.Path())._flavour

    def __new__(cls, *paths, course: str=None):
        if course:
            # check for local sibling 'fichiers' folder
            local_path = pathlib.Path('../fichiers')
            if local_path.exists() and local_path.is_dir():
                # use local relative file path prefix
                return super(Path, cls).__new__(cls, '../fichiers', *paths)

            local_path = pathlib.Path('/pax/shared', course.upper(), *paths)
            if local_path.exists():
                # use local absolute shared prefix
                return super(Path, cls).__new__(cls, '/pax/shared', course.upper(), *paths)

            # use local writeable temp prefix
            return super(Path, cls).__new__(cls, '/tmp/pax', course.lower(), *paths)

        else:
            # assume normal pathlib behavior
            return super(Path, cls).__new__(cls, *paths)

    def __init__(self, *paths, course: str=None):
        # initialize base path
        super().__init__()

        # save course id
        self._course = course

        # try to fetch path from the PAX server
        self.fetch_from_pax()

    def __truediv__(self, path):
        # apply inherited operator
        return Path(super().__truediv__(path))

    def fetch_from_pax(self) -> bool:
        if self._course and not self.exists():
            # fetch file content from PAX server
            r = requests.get(f'{PAXURL}/static/{self._course.upper()}/fichiers/{str(self)}')

            if r.status_code == 200:
                # make sure parent exists
                self.parent.mkdir(parents=True, exist_ok=True)

                # write downloaded content to local file
                self.write_bytes(r.content)

                return True

        return False
