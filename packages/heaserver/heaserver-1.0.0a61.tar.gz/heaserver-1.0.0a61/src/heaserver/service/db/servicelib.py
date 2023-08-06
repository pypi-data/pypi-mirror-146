from typing import Optional, Mapping, Tuple, Union, Type, List, Callable, Awaitable
from aiohttp.web import Request, Response
from aiohttp import hdrs
from heaobject.volume import Volume, FileSystem
from yarl import URL

from .. import client
from ..heaobjectsupport import type_to_resource_url
from ..oidcclaimhdrs import SUB
from .. import response
from heaobject.keychain import Credentials
from heaobject.volume import FileSystemTypeVar


async def get_file_system_and_credentials_from_volume(request: Request, volume_id: Optional[str], file_system_type: Type[FileSystemTypeVar]) -> Tuple[FileSystemTypeVar, Optional[Credentials]]:
    """
    Get the file system and credentials for the given volume.

    :param request: the aiohttp request (required).
    :param volume_id: a volume id string (required).
    :param file_system_type: the type of file system (required).
    :return: a tuple containing a FileSystem object and, if one exists, a Credentials object (or None if one does not).
    :raise ValueError: if no volume with that id exists, no file system exists for the given volume, or the volumes's
    credentials were not found.
    """
    headers = {SUB: request.headers[SUB]} if SUB in request.headers else None
    volume, volume_url = await _get_volume(request, volume_id, headers)
    if volume is None:
        raise ValueError(f'No volume with id {volume_id}')
    if volume_url is None:
        raise ValueError(f'Volume {volume_id} has no URL')
    fs_url = await type_to_resource_url(request, FileSystem)
    if fs_url is None:
        raise ValueError('No file system service registered')
    file_system = await client.get(request.app,
                                   URL(fs_url) / 'bytype' / file_system_type.get_type_name() / 'byname' / volume.file_system_name, file_system_type,
                                   headers=headers)
    if file_system is None:
        raise ValueError(f"Volume {volume.id}'s file system {volume.file_system_name} does not exist")
    return file_system, await _get_credentials(request, volume, headers)


async def has_volume(request: Request, volume_id: Optional[str] = None, headers: Optional[Mapping[str, str]] = None) -> Response:
    if volume_id is None:
        if 'volume_id' in request.match_info:
            volume_id_ = request.match_info['volume_id']
        elif 'id' in request.match_info:
            volume_id_ = request.match_info['id']
        else:
            volume_id_ = None
    else:
        volume_id_ = volume_id
    if volume_id_ is not None:
        volume_url = await type_to_resource_url(request, Volume)
        if volume_url is None:
            raise ValueError('No Volume service registered')
        volume = await client.get(request.app, URL(volume_url) / volume_id_, Volume, headers=headers)
        if volume is None:
            return response.status_not_found()
        return response.status_ok()
    else:
        return response.status_not_found()


async def get_options(request: Request, methods: List[str], fn: Callable[[Request], Awaitable[Response]]):
    """
    Responds to an OPTIONS request. It calls the provided function, checks for the 200 status code, and if 200 is
    returned, returns a response with a 200 status code and an Allow header. The function should check if a REST API
    endpoint would return a 200 status code if called.

    :param request: the HTTP request (required).
    :param methods: a list of methods to include in the Allow header (required).
    :param fn: the function to call.
    :return: the HTTP response.
    """
    resp = await fn(request)
    if resp.status == 200:
        return await response.get_options(request, methods)
    else:
        headers = {hdrs.CONTENT_TYPE: 'text/plain; charset=utf-8'}
        return response.status_generic(status=resp.status, body=resp.text, headers=headers)


async def _get_volume(request: Request, volume_id: Optional[str], headers: Optional[Mapping[str, str]] = None) -> Tuple[Optional[Volume], Optional[Union[str, URL]]]:
    """
    Gets the volume with the provided id.

    :param request: the HTTP request (required).
    :param volume_id: the id string of a volume.
    :param headers: any headers.
    :return: a two-tuple with either the Volume and its URL, or (None, None).
    :raise ValueError: if there is no volume with the provided volume id or no volume service is registered.
    """
    if volume_id is not None:
        volume_url = await type_to_resource_url(request, Volume)
        if volume_url is None:
            raise ValueError('No Volume service registered')
        volume = await client.get(request.app, URL(volume_url) / volume_id, Volume, headers=headers)
        if volume is None:
            raise ValueError(f'No volume with volume_id={volume_id}')
        return volume, volume_url
    else:
        return None, None


async def _get_credentials(request: Request, volume: Volume, headers: Optional[Mapping] = None) -> Optional[Credentials]:
    """
    Gets a credential specified in the provided volume, or if there is none, a credential with the where attribute set
    to the volume's URL.

    :param request: the HTTP request (required).
    :param volume: the Volume (required).
    :param volume_url: the volume's URL (required).
    :param headers: any headers.
    :return: the Credentials, or None if the volume has no credentials.
    :raise ValueError: if no credentials service is registered or if the volume's credentials were not found.
    """
    if volume.credential_id is not None:
        cred_url = await type_to_resource_url(request, Credentials)
        if cred_url is None:
            raise ValueError('No credentials service registered')
        credential = await client.get(request.app, URL(cred_url) / volume.credential_id, Credentials, headers=headers)
        if credential is not None:
            return credential
        else:
            raise ValueError(f'Credentials {volume.credential_id} not found')
    else:
        return None
