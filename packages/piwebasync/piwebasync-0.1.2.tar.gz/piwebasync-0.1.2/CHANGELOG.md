# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 0.1.1 (March 29, 2022)

### Added
* Rollback feature to `.update()` in `WebsocketClient`. If `rollback=True`, the client will attempt to rollback to previous endpoint should the update fail. If the rollback is successful, a `ChannelRollback` exception is raised. If rollback fails, `ChannelUpdateError` is raised like before
* Added `raise_for_status()` method to `HTTPResponse` objects. If called, non 200 status codes will raise an `HTTPStatusError`. Additionally, if a successful response could not be processed due to a `JSONDecodeError`, this will also raise an `HTTPStatusError`

### Removed
* Support for python 3.8. piwebasync supports python >= 3.9

## 0.1.2 (April 12, 2022)
* Fix for httpx_extensions issue [#1](https://github.com/newvicx/httpx_extensions/issues/1)