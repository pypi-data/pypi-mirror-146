import pathlib
import requests

PAXURL = 'https://pax.ulaval.ca'

class Path(pathlib.Path):
    """This class behaves has a PAX replacement for the standard `pathlib.Path`.

    It adds a path prefix that is either:
    1. `../fichiers/` if this relative folder exists;
    2. or an absolute `/tmp/pax/{course}/` prefix otherwise.

    Moreover, if the path does not exist, it tries to download it from the pAX server,
    via its static URL.
    """
    _flavour = type(pathlib.Path())._flavour

    def __new__(cls, *paths, course: str=None):
        if course:
            # check for local sibling 'fichiers' folder
            local_path = pathlib.Path('../fichiers')
            if local_path.exists() and local_path.is_dir():
                # add local relative path prefix
                return super(Path, cls).__new__(cls, '../fichiers', *paths)

            else:
                # add /tmp PAX prefix
                return super(Path, cls).__new__(cls, '/tmp/pax', course.lower(), *paths)

        else:
            # assume normal behavior
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
