import os

import geopandas as gpd
from sqlalchemy import create_engine

from .auth import auth
from .exceptions import PermissionDeniedException
from .utils import get_asset_info
from .utils import Singleton

__all__ = ['Importer']


class Importer(metaclass=Singleton):
    def __init__(self):
        auth_info = auth.check_login()
        self.username = auth_info['nick_name']
        self.db_username = os.environ['db_user']
        self.db_passwd = os.environ['db_pass']
        self.db_url = 'postgis:5432'

    def import_table(self, asset_id, **kwargs):
        """
        Imports table datas from PostGIS.

        :param asset_id: like `asset_owner:asset_name`, if you are the owner of the asset, just `asset_name` is ok.
        :return:
        """
        asset_owner, asset_name = get_asset_info(asset_id)
        asset_owner = asset_owner or self.username
        if asset_owner not in ["public", "share", self.username]:
            raise PermissionDeniedException(f'{self.username} has no permission to import {asset_id} table.')
        sql = 'SELECT * FROM "{}"'.format(asset_name)
        return gpd.read_postgis(con=self._get_engine(asset_owner), geom_col='the_geom', sql=sql, **kwargs)

    def _get_engine(self, asset_owner):
        return create_engine(f'postgresql://{self.db_username}:{self.db_passwd}@{self.db_url}/{asset_owner}')

    def import_raster(self, raster_name):
        """
        Imports raster datas.
        :param raster_name:
        :return:
        """
        pass
