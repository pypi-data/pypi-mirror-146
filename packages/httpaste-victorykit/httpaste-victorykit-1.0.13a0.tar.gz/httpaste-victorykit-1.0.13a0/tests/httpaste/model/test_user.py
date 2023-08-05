#!/usr/bin/env python3
import pytest
from collections import namedtuple

import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def _kdf(passwd):

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'#',
        iterations=390000,
    )

    return base64.urlsafe_b64encode(kdf.derive(passwd))


def _encrypt(data:bytes, passwd:str):

    return Fernet(_kdf(passwd)).encrypt(data)


def _decrypt(data:bytes, passwd:str):

    return Fernet(_kdf(passwd)).decrypt(data)


@pytest.fixture
def module():

    from httpaste.model import user

    return user



@pytest.fixture
def encrypt():

    return _encrypt


def decrypt():

    return _decrypt


class Test_load():

    @pytest.fixture(autouse=True)
    def setup(self, module):

        self.func = module.load

    def test_default(self, module, encrypt):

        master_key = b'test'
        key_hash = b'foobar-hash'
        data = {'foo': 'bar'}
        sdata =  b'{"foo": "bar"}'
        sub = b'foobar-sub'
        _model = module.Model(sub, key_hash, encrypt(sdata, master_key))
        backend_mock = namedtuple('Backend', ['load',])(load=lambda m: _model)

        result = self.func(module.Model(sub), master_key, backend_mock)

        assert result.sub == sub
        assert result.key_hash == key_hash
        assert result.index == data


    def test_index_not_map(self, module, encrypt):

        master_key = b'test'
        key_hash = b'foobar-hash'
        sdata =  b'"foo"'
        sub = b'foobar-sub'
        _model = module.Model(sub, key_hash, encrypt(sdata, master_key))
        backend_mock = namedtuple('Backend', ['load',])(load=lambda m: _model)

        with pytest.raises(TypeError):
            self.func(module.Model(sub), master_key, backend_mock)


    def test_decryption_error(self, module):

        master_key = b'test'
        key_hash = b'foobar-hash'
        sub = b'foobar-sub'
        _model = module.Model(sub, key_hash, b'34powkgopk')
        backend_mock = namedtuple('Backend', ['load',])(load=lambda m: _model)

        with pytest.raises(InvalidToken):
            self.func(module.Model(sub), master_key, backend_mock)