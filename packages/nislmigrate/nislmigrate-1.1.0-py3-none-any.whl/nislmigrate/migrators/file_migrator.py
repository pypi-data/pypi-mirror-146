import os
from typing import Any, Dict, Callable

from nislmigrate.extensibility.migrator_plugin import MigratorPlugin, ArgumentManager
from nislmigrate.facades.facade_factory import FacadeFactory
from nislmigrate.facades.file_system_facade import FileSystemFacade
from nislmigrate.facades.mongo_configuration import MongoConfiguration
from nislmigrate.facades.mongo_facade import MongoFacade
from nislmigrate.logs.migration_error import MigrationError
from nislmigrate.migration_action import MigrationAction
from nislmigrate.utility.paths import get_ni_application_data_directory_path

DEFAULT_DATA_DIRECTORY = os.path.join(
    get_ni_application_data_directory_path(),
    'Skyline',
    'Data',
    'FileIngestion')

PATH_CONFIGURATION_KEY = 'OutputPath'

S3_CONFIGURATION_KEY = 'UseS3BackEnd'

_METADATA_ONLY_ARGUMENT = 'metadata-only'

_METADATA_ONLY_HELP = 'When used with --files or --all, migrate only the file metadata, \
but not the files themselves. Otherwise ignored.'

_CHANGE_FILE_STORE_ARGUMENT = 'change-file-store-root'
_CHANGE_FILE_STORE_HELP = 'Change the file storage location path'

_CHANGE_FILE_STORE_SLASHES_ARGUMENT = 'switch-to-forward-slashes'
_CHANGE_FILE_STORE_SLASHES_HELP = 'Change the file storage location path from backward slashes to forward slashes'

_FILE_STORE_ROOT_ARGUMENT = 'file-store-root'
_FILE_STORE_ROOT_HELP = 'The file store root directory for file storage locations to be updated by \
"--files-change-file-store-root" when run with the "modify" operation. For "restore" operations this \
value is inferred from the database and this argument is ignored.'

_NO_FILES_ERROR = """

Files data was not found. If you intend to restore metadata only, pass
--files-metadata-only.

"""

_CANNOT_MIGRATE_S3_FILES_ERROR = """

S3 file storage is enabled on the backend. nislmigrate cannot capture/restore the files
stored in S3. If you intend to migrate metadata only, pass --files-metadata-only.

"""

_FILE_STORE_ROOT_NOT_SET_FOR_MODIFY_CHANGE_FILE_STORE_ERROR = """

--files-file-store-root must be set with operation 'modify --files-change-file-store-root'

"""

_SAVED_OLD_FILE_STORE_ROOT_FILE_NAME = 'file-store-root'


class _FileMigratorConfiguration:
    def __init__(
        self,
        action: MigrationAction,
        migration_directory: str,
        facade_factory: FacadeFactory,
        arguments: Dict[str, Any],
        config: Dict[str, Any]
    ):
        self.mongo_facade: MongoFacade = facade_factory.get_mongo_facade()
        self.file_facade: FileSystemFacade = facade_factory.get_file_system_facade()
        self.mongo_configuration: MongoConfiguration = MongoConfiguration(config)
        self.file_migration_directory: str = os.path.join(migration_directory, 'files')
        self.file_migration_directory_exists: bool = self.file_facade.does_directory_exist(
                self.file_migration_directory)

        self.data_directory: str = config.get(PATH_CONFIGURATION_KEY) or DEFAULT_DATA_DIRECTORY

        self.is_s3_backend: bool = config.get(S3_CONFIGURATION_KEY, '').lower() == 'true'
        self.has_metadata_only_argument: bool = arguments.get(_METADATA_ONLY_ARGUMENT, False)
        self.should_migrate_files: bool = not self.has_metadata_only_argument
        self.update_store_path: str = arguments.get(_CHANGE_FILE_STORE_ARGUMENT, '')
        if action is MigrationAction.MODIFY:
            self.old_store_path: str = arguments.get(_FILE_STORE_ROOT_ARGUMENT, '')
        else:
            self.old_store_path = ''
        self.should_update_store: bool = not self.update_store_path == ''
        self.use_forward_slashes: bool = arguments.get(_CHANGE_FILE_STORE_SLASHES_ARGUMENT, False)


class FileMigrator(MigratorPlugin):

    @property
    def name(self):
        return 'FileIngestion'

    @property
    def argument(self):
        return 'files'

    @property
    def help(self):
        return 'Migrate ingested files'

    def capture(self, migration_directory: str, facade_factory: FacadeFactory, arguments: Dict[str, Any]):
        configuration = _FileMigratorConfiguration(
            MigrationAction.CAPTURE,
            migration_directory,
            facade_factory,
            arguments,
            self.config(facade_factory)
        )
        configuration.mongo_facade.capture_database_to_directory(
            configuration.mongo_configuration,
            migration_directory,
            self.name)

        captured_file_store_root_path = os.path.join(migration_directory, _SAVED_OLD_FILE_STORE_ROOT_FILE_NAME)
        configuration.file_facade.write_file(captured_file_store_root_path, configuration.data_directory)

        if configuration.should_migrate_files:
            configuration.file_facade.copy_directory(
                configuration.data_directory,
                configuration.file_migration_directory,
                False)

    def restore(self, migration_directory: str, facade_factory: FacadeFactory, arguments: Dict[str, Any]):
        configuration = _FileMigratorConfiguration(
            MigrationAction.RESTORE,
            migration_directory,
            facade_factory,
            arguments,
            self.config(facade_factory)
        )

        configuration.mongo_facade.restore_database_from_directory(
            configuration.mongo_configuration,
            migration_directory,
            self.name)
        if configuration.should_update_store:
            configuration.old_store_path = configuration.file_facade.read_file(_SAVED_OLD_FILE_STORE_ROOT_FILE_NAME)
        self.update_database(configuration)
        if configuration.should_migrate_files:
            configuration.file_facade.copy_directory(
                configuration.file_migration_directory,
                configuration.data_directory,
                True)

    def modify(self, migration_directory: str, facade_factory: FacadeFactory, arguments: Dict[str, Any]):
        configuration = _FileMigratorConfiguration(
            MigrationAction.MODIFY,
            migration_directory,
            facade_factory,
            arguments,
            self.config(facade_factory)
        )
        if configuration.should_update_store:
            self.update_root_file_path_in_metadata(configuration)
        if configuration.use_forward_slashes:
            self.update_file_path_slashes_in_metadata(configuration)

    def pre_capture_check(
            self,
            migration_directory: str,
            facade_factory: FacadeFactory,
            arguments: Dict[str, Any]) -> None:

        configuration = _FileMigratorConfiguration(
            MigrationAction.CAPTURE,
            migration_directory,
            facade_factory,
            arguments,
            self.config(facade_factory)
        )
        if not configuration.has_metadata_only_argument and configuration.is_s3_backend:
            raise MigrationError(_CANNOT_MIGRATE_S3_FILES_ERROR)

    def pre_restore_check(
            self,
            migration_directory: str,
            facade_factory: FacadeFactory,
            arguments: Dict[str, Any]) -> None:

        configuration = _FileMigratorConfiguration(
            MigrationAction.RESTORE,
            migration_directory,
            facade_factory,
            arguments,
            self.config(facade_factory)
        )

        configuration.mongo_facade.validate_can_restore_database_from_directory(
            migration_directory,
            self.name)

        if configuration.is_s3_backend and not configuration.has_metadata_only_argument:
            raise MigrationError(_CANNOT_MIGRATE_S3_FILES_ERROR)
        elif not configuration.file_migration_directory_exists and configuration.should_migrate_files:
            raise MigrationError(_NO_FILES_ERROR)

    def pre_modify_check(
            self,
            migration_directory: str,
            facade_factory: FacadeFactory,
            arguments: Dict[str, Any]) -> None:

        configuration = _FileMigratorConfiguration(
            MigrationAction.MODIFY,
            migration_directory,
            facade_factory,
            arguments,
            self.config(facade_factory)
        )
        if configuration.update_store_path != '' and configuration.old_store_path == '':
            raise MigrationError(_FILE_STORE_ROOT_NOT_SET_FOR_MODIFY_CHANGE_FILE_STORE_ERROR)

    def add_additional_arguments(self, argument_manager: ArgumentManager):
        argument_manager.add_switch(_METADATA_ONLY_ARGUMENT, help=_METADATA_ONLY_HELP)
        argument_manager.add_argument(_CHANGE_FILE_STORE_ARGUMENT, help=_CHANGE_FILE_STORE_HELP, metavar='new-root-dir')
        argument_manager.add_argument(
            _FILE_STORE_ROOT_ARGUMENT,
            help=_FILE_STORE_ROOT_HELP,
            metavar='existing-root-dir')
        argument_manager.add_switch(_CHANGE_FILE_STORE_SLASHES_ARGUMENT, help=_CHANGE_FILE_STORE_SLASHES_HELP)

    def update_database(self, configuration: _FileMigratorConfiguration):
        if configuration.should_update_store:
            self.update_root_file_path_in_metadata(configuration)
        if configuration.use_forward_slashes:
            self.update_file_path_slashes_in_metadata(configuration)

    def update_root_file_path_in_metadata(self, configuration: _FileMigratorConfiguration):
        old_path = configuration.old_store_path
        new_path = configuration.update_store_path
        collection_name = self.name.lower()
        does_path_field_start_with_old_path = self.does_path_start_with_prefix_predicate(old_path)
        replace_old_path_with_new_path = self.replace_path_prefix_in_document_function(old_path, new_path)
        mongo_configuration = configuration.mongo_configuration
        configuration.mongo_facade.conditionally_update_documents_in_collection(
            mongo_configuration,
            collection_name,
            does_path_field_start_with_old_path,
            replace_old_path_with_new_path)

    def update_file_path_slashes_in_metadata(self, configuration: _FileMigratorConfiguration):
        collection_name = self.name.lower()
        replace_back_slashes_with_forward_slashes = self.replace_back_slashes_in_document_function()
        mongo_configuration = configuration.mongo_configuration
        configuration.mongo_facade.update_documents_in_collection(
            mongo_configuration,
            collection_name,
            replace_back_slashes_with_forward_slashes)

    @staticmethod
    def does_path_start_with_prefix_predicate(prefix: str) -> Callable[[Dict[str, Any]], bool]:
        return lambda document: document['path'].startswith(prefix)

    def replace_path_prefix_in_document_function(
            self,
            old_prefix: str,
            new_prefix: str
    ) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
        return lambda document: self.replace_prefix_of_field_in_document('path', old_prefix, new_prefix, document)

    @staticmethod
    def replace_prefix_of_field_in_document(
            field: str,
            old_prefix: str,
            new_prefix: str,
            document: Dict[str, Any]
    ) -> Dict[str, Any]:
        postfix = document[field][len(old_prefix):]
        document[field] = new_prefix + postfix
        return document

    def replace_back_slashes_in_document_function(self) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
        return lambda document: self.replace_back_slashes_with_forward_slashes('path', document)

    @staticmethod
    def replace_back_slashes_with_forward_slashes(
            field: str,
            document: Dict[str, Any]
    ) -> Dict[str, Any]:
        field_value = document[field]
        field_value = field_value.replace('\\', '/')
        document[field] = field_value
        return document
