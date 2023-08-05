import hashlib
from json import loads

import os
import shutil
from imagination.decorator import service, EnvironmentVariable
from imagination.decorator.config import Service
from pydantic import BaseModel
from threading import Lock
from time import time
from typing import Optional, Dict

from dnastack.constants import CLI_DIRECTORY
from dnastack.helpers.logger import get_logger


class Session(BaseModel):
    version: int = 3
    config_hash: Optional[str]
    access_token: Optional[str]
    refresh_token: Optional[str]
    scope: Optional[str]
    token_type: str

    # Pre-computed Properties
    issued_at: int  # Epoch timestamp (UTC)
    valid_until: int  # Epoch timestamp (UTC)

    def is_valid(self) -> bool:
        return time() <= self.valid_until


class UnknownSessionError(RuntimeError):
    """ Raised when an unknown session is requested """


class BaseSessionStorage:
    def __contains__(self, id: str) -> bool:
        raise NotImplementedError()

    def __getitem__(self, id: str) -> Optional[Session]:
        raise NotImplementedError()

    def __setitem__(self, id: str, session: Session):
        raise NotImplementedError()

    def __delitem__(self, id: str):
        raise NotImplementedError()


class InMemorySessionStorage(BaseSessionStorage):
    def __init__(self):
        self.__cache_map: Dict[str, Session] = dict()

    def __contains__(self, id: str) -> bool:
        return id in self.__cache_map

    def __getitem__(self, id: str) -> Optional[Session]:
        return self.__cache_map.get(id)

    def __setitem__(self, id: str, session: Session):
        self.__cache_map[id] = session

    def __delitem__(self, id: str):
        del self.__cache_map[id]


@service.registered(
    params=[
        EnvironmentVariable('DNASTACK_SESSION_DIR',
                            default=os.path.join(CLI_DIRECTORY, 'sessions'),
                            allow_default=True)
    ]
)
class FileSessionStorage(BaseSessionStorage):
    def __init__(self, dir_path : str):
        self.__dir_path = dir_path

        if not os.path.exists(self.__dir_path):
            os.makedirs(self.__dir_path, exist_ok=True)

    def __contains__(self, id: str) -> bool:
        return os.path.exists(self.__get_file_path(id))

    def __getitem__(self, id: str) -> Optional[Session]:
        final_file_path = self.__get_file_path(id)

        with open(final_file_path, 'r') as f:
            content = f.read()

        return Session(**loads(content))

    def __setitem__(self, id: str, session: Session):
        os.makedirs(self.__dir_path, exist_ok=True)

        final_file_path = self.__get_file_path(id)
        temp_file_path = f'{final_file_path}.{time()}.swap'

        content: str = session.json(indent=2)

        with open(temp_file_path, 'w') as f:
            f.write(content)
        shutil.copy(temp_file_path, final_file_path)
        os.unlink(temp_file_path)

    def __delitem__(self, id: str):
        final_file_path = os.path.join(self.__dir_path, f'{id}.session')
        os.unlink(final_file_path)

    def __get_file_path(self, id: str) -> str:
        return os.path.join(self.__dir_path, f'{id}.session')


@service.registered(
    params=[
        Service(FileSessionStorage)
    ],
    auto_wired=False
)
class SessionManager:
    def __init__(self, storage: BaseSessionStorage):
        self.__logger = get_logger(type(self).__name__)
        self.__storage = storage
        self.__change_locks: Dict[str, Lock] = dict()

        self.__logger.debug('Session Storage: %s', type(self.__storage).__name__)

    def restore(self, id: str) -> Optional[Session]:
        with self.__lock(id):
            if id not in self.__storage:
                return None

            session = self.__storage[id]

        return session

    def save(self, id: str, session: Session):
        # Note (1): This is designed to have file operation done as quickly as possible to reduce race conditions.
        # Note (2): Instead of interfering with the main file directly, the new content is written to a temp file before
        #           swapping with the real file to minimize the I/O block.
        with self.__lock(id):
            self.__storage[id] = session

    def delete(self, id: str):
        with self.__lock(id):
            try:
                if id not in self.__storage:
                    return
                del self.__storage[id]
            finally:
                del self.__change_locks[id]

    def __lock(self, id) -> Lock:
        if id not in self.__change_locks:
            self.__change_locks[id] = Lock()
        return self.__change_locks[id]
