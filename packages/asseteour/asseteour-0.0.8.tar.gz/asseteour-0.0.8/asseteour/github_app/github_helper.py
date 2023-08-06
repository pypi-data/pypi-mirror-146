import hashlib
import json
import logging
import os
import re
from collections import OrderedDict
from contextlib import contextmanager

from compipe.exception.validate_error import GErrorValue
from compipe.utils.access import GITHUB_TOKEN_KEY, AccessHub
from compipe.utils.logging import logger
from compipe.utils.parameters import (ARG_DATA, ARG_DIR, ARG_FILE, ARG_OUTPUT,
                                      ARG_PARENT)
from github import Github, UnknownObjectException


@contextmanager
def logger_blocker(logger_level=logging.DEBUG):
    try:
        logger = logging.getLogger()  # pylint: disable=no-member
        ori_level = logger.level
        logger.setLevel(logger_level)
        yield
    finally:
        logger.setLevel(ori_level)


class JSONPropertyFile():
    def __init__(self, config):
        self.file_path = config[ARG_FILE]
        self.output = config[ARG_OUTPUT]
        self.parent = config[ARG_PARENT]

        # remove temporary (internal) keys from the config data before committing
        _data = OrderedDict(sorted(config[ARG_DATA].items()))
        # tmp attribute name has '_' prefix
        _tmp_keys = [key for key in _data.keys() if key[0] == '_']
        # remove keys
        for _key in _tmp_keys:
            del _data[_key]

        self.data = json.dumps(_data, indent=4)

    def commit(self, repo, sha=None, branch='master'):
        # represent the git status
        # true: add/change
        # message: logging message
        results = (True, 'None')

        with logger_blocker(logger_level=logging.WARNING):
            message_header = '[AUTO] Generate configs'
            # message = f'{message_header} - source:{self.file_path} target:{self.output}'
            # if 'sha' is valid, it would perform update behaviors
            # update_file and create_file methods are the build-in functions
            # from pygithub Repository https://github.com/PyGithub/PyGithub
            if sha:
                # compare the str hash between local data and remote file. It would skip commit if the
                # hash values are the same.
                remote_file_data = json.dumps(json.loads(repo.get_contents(self.output).decoded_content),
                                              indent=4)
                # remote config file hash
                remote_data_hash = hashlib.md5(remote_file_data.encode('utf-8')).hexdigest()
                # local config file hash
                local_data_hash = hashlib.md5(self.data.encode('utf-8')).hexdigest()
                # compare config hash and perform the commit if they were different
                if remote_data_hash != local_data_hash:
                    repo.update_file(self.output,
                                     f'{message_header} [UPDATED]',
                                     self.data,
                                     sha,
                                     branch=branch)
                    results = (True, f'Updated config: {self.output}')
                else:
                    results = (False, f'[Skip Commit] No change happend on file: [{self.output}]')

            else:
                repo.create_file(self.output,
                                 f'{message_header} [ADDED]',
                                 self.data,
                                 branch=branch)

                results = (True, f'Added config: {self.output}')

        return results


class GithubHelper():
    def __init__(self, repo_name, re_filter_source=None, re_filter_export=None, output=None):
        token = AccessHub().get_credential(GITHUB_TOKEN_KEY)
        self.g = Github(token)
        # parse repo client
        self.repo_name = repo_name

        with logger_blocker(logger_level=logging.ERROR):  # hide massive http logs
            self.repo = self.g.get_repo(self.repo_name)
        # initialize filters
        self.re_filter_source = re_filter_source
        # keep exsiting file sha information
        self.re_filter_export = re_filter_export or r'^(Export\/Data\/.*)\.json'
        # it could help keep the 'sha' info for the existing file
        self.export_files = {}
        # keep the export config path
        self.output = output

    def get_config(self, name):
        with logger_blocker(logger_level=logging.ERROR):
            return self.repo.get_contents(name)

    def get_properties(self):
        with logger_blocker(logger_level=logging.ERROR):
            file_lists = []
            if not self.repo_name or not self.repo:
                raise GErrorValue('Repo\'s not been initialized.')
            contents = self.repo.get_contents("")
            while contents:
                file_content = contents.pop(0)
                if file_content.type == ARG_DIR:
                    contents.extend(self.repo.get_contents(file_content.path))
                elif not self.re_filter_source or re.fullmatch(self.re_filter_source, file_content.path):
                    file_lists.append(file_content)
                elif not self.re_filter_export or re.fullmatch(self.re_filter_export, file_content.path):
                    # keep the the 'sha' info to the existing files, it would help to perform 'update'
                    # changes on github
                    self.export_files.update({
                        file_content.path: file_content.sha
                    })

        logger.debug(f'Loaded properties from repo: [{self.repo_name}]')
        return file_lists


class JsonPropertiesHelper(GithubHelper):
    def get_properties(self):
        configs = super().get_properties()
        properties = {}
        with logger_blocker(logger_level=logging.ERROR):
            for config in configs:
                path, _ = os.path.splitext(config.path)
                json_content = json.loads(config.decoded_content)

                properties.update({
                    path: {
                        ARG_FILE: config.path,
                        ARG_OUTPUT: f'{self.output}/{os.path.basename(config.path)}',
                        ARG_PARENT: json_content.get(ARG_PARENT),
                        ARG_DATA: json_content}
                })
        return properties

    def commit(self, msg: str, path: str, branch: str, data: dict):
        results = (True, 'None')
        with logger_blocker(logger_level=logging.ERROR):

            # it would throw a not-found error when the specific file path doesn't
            # exist on git repo
            try:
                content_file = self.repo.get_contents(path)
            except UnknownObjectException:
                content_file = None

            if content_file:
                remote_file_data = json.dumps(json.loads(content_file.decoded_content), indent=4)

                # remote config file hash
                remote_data_hash = hashlib.md5(remote_file_data.encode('utf-8')).hexdigest()
                # local config file hash
                local_data_hash = hashlib.md5(data.encode('utf-8')).hexdigest()
                if remote_data_hash != local_data_hash:
                    self.repo.update_file(path,
                                          msg,
                                          data,
                                          content_file.sha,
                                          branch=branch)
                    results = (True, f'Updated config: {path}')
                else:
                    results = (False, f'[Skip Commit] No change happend on file: [{path}]')
            else:
                self.repo.create_file(path,
                                      msg,
                                      data,
                                      branch=branch)

                results = (True, f'Added config: {path}')

        return results
