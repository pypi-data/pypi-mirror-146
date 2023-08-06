""" Utilities for the Python SDK of the YooniK BiometricInThings API.
"""
import yk_utils.apis


class Key:
    """Manage YooniK BiometricInThings API Subscription Key."""
    @classmethod
    def set(cls, key: str):
        """Set the Subscription Key.
        :param key:
        :return:
        """
        yk_utils.apis.Key.set(key)


class BaseUrl:
    """Manage YooniK BiometricInThings API Base URL."""
    @classmethod
    def set(cls, base_url: str):
        yk_utils.apis.BaseUrl.set(base_url)
