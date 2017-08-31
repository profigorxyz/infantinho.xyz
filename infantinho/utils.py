from storages.backends.gs import GSBotoStorage

StaticRootGSBotoStorage = lambda: GSBotoStorage(location='static/')
MediaRootGSBotoStorage = lambda: GSBotoStorage(location='media/')
