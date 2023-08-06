import logging
import os

from nislmigrate.argument_handler import ArgumentHandler, MIGRATION_OPERATION_NOT_PROVIDED_ERROR_TEXT
from nislmigrate.facades.facade_factory import FacadeFactory
from nislmigrate.facades.ni_web_server_manager_facade import NiWebServerManagerFacade
from nislmigrate.logs.migration_error import MigrationError
from nislmigrate.migration_action import MigrationAction
from nislmigrate.extensibility.migrator_plugin import MigratorPlugin
from nislmigrate.facades.system_link_service_manager_facade import SystemLinkServiceManagerFacade
from nislmigrate.utility.permission_checker import PermissionChecker


class MigrationFacilitator:
    """
    Facilitates an entire migration operation from start to finish.
    """
    def __init__(self, facade_factory: FacadeFactory, argument_handler: ArgumentHandler):
        self.facade_factory: FacadeFactory = facade_factory
        self.web_server_manager: NiWebServerManagerFacade = facade_factory.get_ni_web_server_manager_facade()
        self.service_manager: SystemLinkServiceManagerFacade = facade_factory.get_system_link_service_manager_facade()

        self._action = argument_handler.get_migration_action()
        action_not_restore = not self._action == MigrationAction.RESTORE
        action_not_capture = not self._action == MigrationAction.CAPTURE
        action_not_modify = not self._action == MigrationAction.MODIFY
        if action_not_restore and action_not_capture and action_not_modify:
            raise MigrationError(MIGRATION_OPERATION_NOT_PROVIDED_ERROR_TEXT)
        self._migrators = argument_handler.get_list_of_services_to_capture_or_restore()
        self._migration_directory = argument_handler.get_migration_directory()
        self._argument_handler = argument_handler

    def migrate(self):
        """Facilitates an entire migration operation from start to finish.
        """

        self.__pre_migration_error_check()
        self.__stop_services_and_perform_migration()

    def __stop_services_and_perform_migration(self) -> None:
        self.service_manager.stop_all_system_link_services()
        try:
            for migrator in self._migrators:
                migrator_directory = os.path.join(self._migration_directory, migrator.name)
                self.__report_migration_starting(migrator.name)
                self.__migrate_service(migrator, migrator_directory)
                self.__report_migration_finished(migrator.name)
        finally:
            if self._action == MigrationAction.RESTORE or self._action == MigrationAction.MODIFY:
                self.web_server_manager.restart_web_server()
            self.service_manager.start_all_system_link_services()

    def __migrate_service(self, migrator: MigratorPlugin, migrator_directory) -> None:
        migrator_arguments = self._argument_handler.get_migrator_additional_arguments(migrator)
        if self._action == MigrationAction.CAPTURE:
            migrator.capture(migrator_directory, self.facade_factory, migrator_arguments)
        elif self._action == MigrationAction.RESTORE:
            migrator.restore(migrator_directory, self.facade_factory, migrator_arguments)
        elif self._action == MigrationAction.MODIFY:
            migrator.modify(migrator_directory, self.facade_factory, migrator_arguments)
        else:
            raise ValueError('Migration action is not the correct type.')

    def __report_migration_starting(self, migrator_name: str):
        action_pretty_name = 'capture'
        if self._action == MigrationAction.RESTORE:
            action_pretty_name = 'restore'
        if self._action == MigrationAction.MODIFY:
            action_pretty_name = 'modify'

        migrator_names = (action_pretty_name, migrator_name)
        info = f'Starting to {action_pretty_name} data using {migrator_names} migrator strategy ...'
        log = logging.getLogger(MigrationFacilitator.__name__)
        log.log(logging.INFO, info)

    def __report_migration_finished(self, migrator_name: str):
        action_pretty_name = 'capturing'
        if self._action == MigrationAction.RESTORE:
            action_pretty_name = 'restoring'
        if self._action == MigrationAction.MODIFY:
            action_pretty_name = 'modifying'

        info = f'Done {action_pretty_name} data using {migrator_name} migrator strategy.'
        log = logging.getLogger(MigrationFacilitator.__name__)
        log.log(logging.INFO, info)

    def __pre_migration_error_check(self) -> None:
        is_force_migration_flag_present = self._argument_handler.is_force_migration_flag_present()
        PermissionChecker.verify_force_if_restoring(is_force_migration_flag_present, self._action)

        migrator: MigratorPlugin
        for migrator in self._migrators:
            self.__pre_migration_error_check_for_single_migrator(migrator)

    def __pre_migration_error_check_for_single_migrator(self, migrator) -> None:
        self.__report_pre_migration_check_starting(migrator.name)
        migrator_directory = os.path.join(self._migration_directory, migrator.name)
        arguments = self._argument_handler.get_migrator_additional_arguments(migrator)
        if self._action == MigrationAction.CAPTURE:
            migrator.pre_capture_check(migrator_directory, self.facade_factory, arguments)
        elif self._action == MigrationAction.RESTORE:
            migrator.pre_restore_check(migrator_directory, self.facade_factory, arguments)
        elif self._action == MigrationAction.MODIFY:
            migrator.pre_modify_check(migrator_directory, self.facade_factory, arguments)
        else:
            raise ValueError('Migration action is not the correct type.')
        self.__report_pre_migration_check_finished(migrator.name)

    @staticmethod
    def __report_pre_migration_check_starting(migrator_name: str) -> None:
        info = f'Performing pre-migration check for {migrator_name}'
        log = logging.getLogger(MigrationFacilitator.__name__)
        log.log(logging.INFO, info)

    @staticmethod
    def __report_pre_migration_check_finished(migrator_name: str) -> None:
        info = f'Pre-migration check passed for {migrator_name}.'
        log = logging.getLogger(MigrationFacilitator.__name__)
        log.log(logging.INFO, info)
