def get_asset_info(asset_id: str):
    """
    Get asset information from asset ID.
    """
    if ":" in asset_id:
        asset_owner, asset_name = asset_id.split(':')
    else:
        asset_owner = None
        asset_name = asset_id
    return asset_owner, asset_name


# 单例类
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]