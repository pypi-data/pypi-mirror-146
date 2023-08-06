"""The core ACE Hunter classes and client.

This client is derived directly from the ACE Hunting System and can
be used to validate and execute hunts, as well as submit hunting results to ACE.

Ideally this library should be imported and used directly by the ACE Hunting System;
specifically the `saq.collectors.hunter.HunterCollector`. This will standardize the code
used for ACE Hunting so changes are easier to make.
"""

import os
import json
import logging
import configparser
import datetime
import importlib
import operator
import signal
import threading
import traceback
import sqlite3

from croniter import croniter
from zoneinfo import ZoneInfo

from ace_hunter.config import CONFIG, DATA_DIR, ACE_DEFAULT_QUEUE, DEFAULT_ANALYSIS_MODE
from ace_hunter.util import create_directory, abs_path, create_timedelta, local_time
from ace_hunter.hunt_type import validate_hunt_type_config_requirements

from typing import List, Dict

__version__ = "1.0.0"

LOGGER = logging.getLogger("ace_hunter")


class InvalidHuntTypeError(ValueError):
    pass


def get_hunt_db_path(hunt_type):
    return os.path.join(DATA_DIR, CONFIG["collection"]["persistence_dir"], "hunt", f"{hunt_type}.db")


def open_hunt_db(hunt_type):
    """Utility function to open sqlite3 database with correct parameters."""
    return sqlite3.connect(get_hunt_db_path(hunt_type), detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)


class Hunt(object):
    """Abstract class that represents a single hunt."""

    def __init__(
        self,
        enabled=None,
        name=None,
        description=None,
        manager=None,
        alert_type=None,
        analysis_mode=None,
        frequency=None,
        tags=[],
    ):

        self.enabled = enabled
        self.name = name
        self.description = description
        self.manager = manager
        self.alert_type = alert_type
        self.analysis_mode = analysis_mode
        self.frequency = frequency
        self.tags = tags
        self.cron_schedule = None
        self.queue = ACE_DEFAULT_QUEUE
        self.logger = logging.getLogger("ace_hunter.Hunt")

        # a datetime.timedelta that represents how long to suppress until this hunt starts to fire again
        self.suppression = None
        # datetime.datetime of when the suppression currently applied to this hunt ends
        # if this value is None then no suppression is currently being applied
        self.suppression_end = None

        # the last time the hunt was executed
        # see the last_executed_time property
        # self.last_executed_time = None # datetime.datetime

        # a threading.RLock that is held while executing
        self.execution_lock = threading.RLock()

        # a way for the controlling thread to wait for the hunt execution thread to start
        self.startup_barrier = threading.Barrier(2)

        # if this is True then we're executing the Hunt outside of normal operations
        # in that case we don't want to record any of the execution time stamps
        self.manual_hunt = False

        # this property maps to the "tool_instance" property of alerts
        # this shows where the alert came from
        # by default we use localhost
        # subclasses might use the address or url they are hitting for their queries
        self.tool_instance = "localhost"

        # when we load from an ini file we record the last modified time of the file
        self.ini_path = None
        self.last_mtime = None

        # The directory relative to detections.
        # Where we should look for files referenced in hunt configurations.
        # If configured, this value should be passed by the HuntManager.
        self.relative_dir = self.manager.relative_detection_dir

    @property
    def type(self):
        if self.manager is not None:
            return self.manager.hunt_type or None
        else:
            return None

    @property
    def last_executed_time(self):
        # if we don't already have this value then load it from the sqlite db
        if hasattr(self, "_last_executed_time"):
            return self._last_executed_time
        else:
            with open_hunt_db(self.type) as db:
                c = db.cursor()
                c.execute("SELECT last_executed_time FROM hunt WHERE hunt_name = ?", (self.name,))
                row = c.fetchone()
                if row is None:
                    self._last_executed_time = None
                    return self._last_executed_time
                else:
                    self._last_executed_time = row[0]
                    if self._last_executed_time is not None and self._last_executed_time.tzinfo is None:
                        self._last_executed_time = self._last_executed_time.replace(tzinfo=ZoneInfo("UTC"))
                    return self._last_executed_time

    @last_executed_time.setter
    def last_executed_time(self, value):
        if value.tzinfo is None:
            value = value.replace(tzinfo=ZoneInfo("UTC"))

        with open_hunt_db(self.type) as db:
            c = db.cursor()
            c.execute(
                "UPDATE hunt SET last_executed_time = ? WHERE hunt_name = ?", (value.replace(tzinfo=None), self.name)
            )
            # NOTE -- datetime with tzinfo not supported by default timestamp converter in 3.6
            db.commit()

        self._last_executed_time = value

    def __str__(self):
        return f"Hunt({self.name}[{self.type}])"

    def cancel(self):
        """Called when the hunt needs to be cancelled, such as when the system is shutting down.
        This must be safe to call even if the hunt is not currently executing."""
        self.logger.warning(f"called cancel on hunt {self} but {self.type} does not support cancel")

    def execute_with_lock(self, *args, **kwargs):
        # we use this lock to determine if a hunt is running, and, to wait for execution to complete.
        self.logger.debug(f"waiting for execution lock on {self}")
        self.execution_lock.acquire()

        # remember the last time we executed
        self.last_executed_time = local_time()

        # notify the manager that this is now executing
        # this releases the manager thread to continue processing hunts
        self.logger.debug(f"clearing barrier for {self}")
        self.startup_barrier.wait()

        submission_list = None

        try:
            self.logger.info(f"executing {self}")
            start_time = local_time()
            return self.execute(*args, **kwargs)
            self.record_execution_time(local_time() - start_time)
        except Exception as e:
            self.logger.error(f"{self} failed: {e}")
            traceback.print_exc()
            self.record_hunt_exception(e)
        finally:
            self.startup_barrier.reset()
            self.execution_lock.release()

    def execute(self, *args, **kwargs):
        """Called to execute the hunt."""
        raise NotImplementedError()

    def wait(self, *args, **kwargs):
        """Waits for the hunt to complete execution. If the hunt is not running then it returns right away.
        Returns False if a timeout is set and the lock is not released during that timeout.
        Additional parameters are passed to execution_lock.acquire()."""
        result = self.execution_lock.acquire(*args, **kwargs)
        if result:
            self.execution_lock.release()

        return result

    @property
    def running(self):
        """Returns True if the hunt is currently executing, False otherwise."""
        # when the hunt is executing it will have this lock enabled
        result = self.execution_lock.acquire(blocking=False)
        if result:
            self.execution_lock.release()
            return False

        return True

    def load_from_ini(self, path):
        """Loads the settings for the hunt from an ini formatted file.

        Args:
            path (str): the path to the ini file to load
        Returns:
            ConfigParser: the ConfigParser object used to load the settings
        """
        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str  # preserve case when reading option names
        config.read(path)

        section_rule = config["rule"]

        # is this a supported type?
        if section_rule["type"] != self.type:
            raise InvalidHuntTypeError(section_rule["type"])

        self.enabled = section_rule.getboolean("enabled")

        # if we don't pass the name then we create it from the name of the ini file
        self.name = section_rule.get(
            "name", fallback=(os.path.splitext(os.path.basename(path))[0]).replace("_", " ").title()
        )

        self.description = section_rule["description"]
        # if we don't pass an alert type then we default to the type field
        self.alert_type = section_rule.get("alert_type", fallback=f"hunter - {self.type}")
        self.analysis_mode = section_rule.get("analysis_mode", fallback=DEFAULT_ANALYSIS_MODE)

        # frequency can be either a timedelta or a crontab entry
        self.frequency = None
        if ":" in section_rule["frequency"]:
            self.frequency = create_timedelta(section_rule["frequency"])

        # suppression must be either empty for a time range
        self.suppression = None
        if "suppression" in section_rule and section_rule["suppression"]:
            self.suppression = create_timedelta(section_rule["suppression"])

        self.cron_schedule = None
        if self.frequency is None:
            self.cron_schedule = section_rule.get("cron_schedule", fallback=section_rule["frequency"])
            # make sure this crontab entry parses
            croniter(self.cron_schedule)

        self.tags = [_.strip() for _ in section_rule["tags"].split(",") if _]
        self.queue = section_rule["queue"] if "queue" in section_rule else ACE_DEFAULT_QUEUE

        self.ini_path = path
        self.last_mtime = os.path.getmtime(path)

        return config

    @property
    def is_modified(self):
        """ "Returns True if this hunt has been modified since it has been loaded."""
        return self.ini_is_modified

    @property
    def ini_is_modified(self):
        """Returns True if this hunt was loaded from an ini file and that file has been modified since we loaded it."""
        try:
            return self.last_mtime != os.path.getmtime(self.ini_path)
        except FileNotFoundError:
            return True
        except:
            self.logger.error(f"unable to check last modified time of {self.ini_path}: {e}")
            return False

    @property
    def ready(self):
        """Returns True if the hunt is ready to execute, False otherwise."""
        # if it's already running then it's not ready to run again
        if self.running:
            return False

        # is this hunt currently suppressed?
        if self.suppression_end:
            if datetime.datetime.now() < self.suppression_end:
                return False

            self.suppression_end = None
            self.logger.info(f"hunt {self} has exited suppression")

        # if we haven't executed it yet then it's ready to go
        if self.last_executed_time is None:
            return True

        # otherwise we're not ready until it's past the next execution time
        return local_time() >= self.next_execution_time

    @property
    def next_execution_time(self):
        """Returns the next time this hunt should execute."""
        # if using cron schedule instead of frequency
        if self.cron_schedule is not None:
            if self.last_executed_time is None:
                self.last_executed_time = local_time()
            cron_parser = croniter(self.cron_schedule, self.last_executed_time)
            return cron_parser.get_next(datetime.datetime)

        # if using frequency instead of cron shedule
        else:
            # if it hasn't executed at all yet, then execute it now
            if self.last_executed_time is None:
                return local_time()

            return self.last_executed_time + self.frequency

    def apply_suppression(self):
        """Apply suppression to this hunt if it is configured to do so.
        This is called by the manager when the hunt generates Submissions."""
        if self.suppression:
            self.suppression_end = datetime.datetime.now() + self.suppression
            self.logger.info(f"hunt {self} is suppressed until {self.suppression_end}")

    def record_execution_time(self, time_delta):
        """Record the amount of time it took to execute this hunt."""
        pass

    def record_hunt_exception(self, exception):
        """Record the details of a failed hunt."""
        pass


CONCURRENCY_TYPE_NETWORK_SEMAPHORE = "network_semaphore"
CONCURRENCY_TYPE_LOCAL_SEMAPHORE = "local_semaphore"


class HuntManager(object):
    """Manages the hunting for a single hunt type."""

    def __init__(
        self,
        hunt_type,
        rule_dirs,
        hunt_cls,
        concurrency_limit,
        persistence_dir,
        update_frequency,
        config,
        requirements={},
    ):

        assert isinstance(hunt_type, str)
        assert isinstance(rule_dirs, list)
        assert issubclass(hunt_cls, Hunt)
        assert concurrency_limit is None or isinstance(concurrency_limit, int) or isinstance(concurrency_limit, str)
        assert isinstance(persistence_dir, str)
        assert isinstance(update_frequency, int)

        self.logger = logging.getLogger("ace_hunter.HuntManager")

        # primary execution thread
        self.manager_thread = None

        # thread that handles tracking changes made to the hunts loaded from ini
        self.update_manager_thread = None

        # shutdown valve
        self.manager_control_event = threading.Event()
        self.wait_control_event = threading.Event()

        # control signal to reload the hunts (set by SIGHUP indirectly)
        self.reload_hunts_flag = False

        # the type of hunting this manager manages
        self.hunt_type = hunt_type

        # when loaded from config, store the entire config so it available to Hunts
        self.config = config

        # the list of directories that contain the hunt configuration ini files for this type of hunt
        self.rule_dirs = rule_dirs

        # if the hunt_type configures a detection_dir then we use that as the relative path
        # when loading rule directories, as well as when loading files referenced in hunt configs (search_query_path, etc).
        # this is a non-standard setting for the ecosystem, so we evaluate it from the config.
        self.relative_detection_dir = None
        _detection_dir = self.config.get("detection_dir")
        if _detection_dir:
            if os.path.exists(_detection_dir):
                self.relative_detection_dir = _detection_dir
            elif _detection_dir.startswith("~/"):
                _detection_dir = os.path.expanduser(_detection_dir)
                if os.path.exists(_detection_dir):
                    self.relative_detection_dir = _detection_dir
            else:
                self.logger.warning(f"detection_dir {_detection_dir} does not exist")
        if self.relative_detection_dir is not None:
            self.logger.debug(f"using relative directory {self.relative_detection_dir} when loading hunt files.")

        # the class used to instantiate the rules in the given rules directories
        self.hunt_cls = hunt_cls

        # sqlite3 database used to keep track of hunt persistence data
        create_directory(os.path.dirname(get_hunt_db_path(self.hunt_type)))
        if not os.path.exists(get_hunt_db_path(self.hunt_type)):
            with open_hunt_db(self.hunt_type) as db:
                c = db.cursor()
                # XXX have to support all future schemas here -- not a great design
                c.execute(
                    """
CREATE TABLE hunt ( 
    hunt_name TEXT NOT NULL,
    last_executed_time timestamp,
    last_end_time timestamp )"""
                )
                c.execute(
                    """
CREATE UNIQUE INDEX idx_name ON hunt(hunt_name)"""
                )
                db.commit()

        # the list of Hunt objects that are being managed
        self._hunts = []

        # acquire this lock before making any modifications to the hunts
        self.hunt_lock = threading.RLock()

        # the ini files that failed to load
        self.failed_ini_files = {}  # key = ini_path, value = os.path.getmtime()

        # the ini files that we skipped
        self.skipped_ini_files = set()  # key = ini_path

        # the type of concurrency contraint this type of hunt uses (can be None)
        # use the set_concurrency_limit() function to change it
        self.concurrency_type = None

        # the local threading.Semaphore if the type is CONCURRENCY_TYPE_LOCAL_SEMAPHORE
        # or the string name of the network semaphore if tye type is CONCURRENCY_TYPE_NETWORK_SEMAPHORE
        self.concurrency_semaphore = None

        if concurrency_limit is not None:
            self.set_concurrency_limit(concurrency_limit)

        # this is set to True if load_hunts_from_config() is called
        # and used when reload_hunts_flag is set
        self.hunts_loaded_from_config = False

        # how often do we check to see if the hunts have been modified?
        self.update_frequency = update_frequency

        # are all the configured requirements met for this hunt type?
        self.requirements = requirements
        self.requirements_met = validate_hunt_type_config_requirements(self.requirements)

    def __str__(self):
        return f"Hunt Manager({self.hunt_type})"

    @property
    def hunts(self):
        """Returns a sorted copy of the list of hunts in execution order."""
        return sorted(self._hunts, key=operator.attrgetter("next_execution_time"))

    def get_hunts(self, spec):
        """Returns the hunts that match the given specification, where spec is a function that takes a Hunt
        as it's single parameter and return True or False if it should be included in the results."""
        return [hunt for hunt in self._hunts if spec(hunt)]

    def get_hunt(self, spec):
        """Returns the first hunt that matches the given specification, where spec is a function that takes a Hunt
        as it's single parameter and return True or False if it should be included in the results.
        Returns None if no hunts are matched."""
        result = self.get_hunts(spec)
        if not result:
            return None

        return result[0]

    def get_hunt_by_name(self, name):
        """Returns the Hunt with the given name, or None if the hunt does not exist."""
        for hunt in self._hunts:
            if hunt.name == name:
                return hunt

        return None

    def signal_reload(self):
        """Signals to this manager that the hunts should be reloaded.
        The work takes place on the manager thread."""
        self.logger.debug("received signal to reload hunts")
        self.reload_hunts_flag = True
        self.wait_control_event.set()

    def reload_hunts(self):
        """Reloads the hunts. This is called when reload_hunts_flag is set to True.
        If the hunts were loaded from the configuration then the current Hunt objects
        are discarded and new ones are loaded from configuration.
        Otherwise this function does nothing."""

        self.reload_hunts_flag = False
        if not self.hunts_loaded_from_config:
            self.logger.debug(f"{self} received signal to reload but hunts were not loaded from configuration")
            return

        self.logger.info(f"{self} reloading hunts")

        # first cancel any currently executing hunts
        self.cancel_hunts()
        self.clear_hunts()
        self.load_hunts_from_config()

    def start(self):
        self.manager_control_event.clear()
        self.load_hunts_from_config()
        self.manager_thread = threading.Thread(target=self.loop, name=f"Hunt Manager {self.hunt_type}")
        self.manager_thread.start()
        self.update_manager_thread = threading.Thread(
            target=self.update_loop, name=f"Hunt Manager Updater {self.hunt_type}"
        )
        self.update_manager_thread.start()

    def debug(self):
        self.manager_control_event.clear()
        self.load_hunts_from_config()
        self.execute()

    def stop(self):
        self.logger.info(f"stopping {self}")
        self.manager_control_event.set()
        self.wait_control_event.set()

        for hunt in self.hunts:
            try:
                hunt.cancel()
            except Exception as e:
                self.logger.error("unable to cancel hunt {hunt}: {e}")
                traceback.print_exc()

    def wait(self, *args, **kwargs):
        self.manager_control_event.wait(*args, **kwargs)
        for hunt in self._hunts:
            hunt.wait(*args, **kwargs)

        if self.manager_thread:
            self.manager_thread.join()

        if self.update_manager_thread:
            self.update_manager_thread.join()

    def update_loop(self):
        self.logger.debug(f"started update manager for {self}")
        while not self.manager_control_event.is_set():
            try:
                self.manager_control_event.wait(timeout=self.update_frequency)
                if not self.manager_control_event.is_set():
                    self.check_hunts()
            except Exception as e:
                self.logger.error(f"uncaught exception {e}")
                traceback.print_exc()

        self.logger.debug(f"stopped update manager for {self}")

    def check_hunts(self):
        """Checks to see if any existing hunts have been modified, created or deleted."""
        self.logger.debug("checking for hunt modifications")
        trigger_reload = False
        with self.hunt_lock:
            # have any hunts been modified?
            for hunt in self._hunts:
                if hunt.is_modified:
                    self.logger.info(f"detected modification to {hunt}")
                    trigger_reload = True

            # if any hunts failed to load last time, check to see if they were modified
            for ini_path, mtime in self.failed_ini_files.items():
                try:
                    if os.path.getmtime(ini_path) != mtime:
                        self.logger.info(f"detected modification to failed ini file {ini_path}")
                        trigger_reload = True
                except Exception as e:
                    self.logger.error(f"unable to check failed ini file {ini_path}: {e}")

            # are there any new hunts?
            existing_ini_paths = set([hunt.ini_path for hunt in self._hunts])
            for ini_path in self._list_hunt_ini():
                if (
                    ini_path not in existing_ini_paths
                    and ini_path not in self.failed_ini_files
                    and ini_path not in self.skipped_ini_files
                ):
                    self.logger.info(f"detected new hunt ini {ini_path}")
                    trigger_reload = True

        if trigger_reload:
            self.signal_reload()

    def loop(self):
        self.logger.debug(f"started {self}")
        while not self.manager_control_event.is_set():
            try:
                self.execute()
            except Exception as e:
                self.logger.error(f"uncaught exception {e}")
                traceback.print_exc()
                self.manager_control_event.wait(timeout=1)

            if self.reload_hunts_flag:
                self.reload_hunts()

        self.logger.debug(f"stopped {self}")

    def execute(self):
        # the next one to run should be the first in our list
        for hunt in self.hunts:
            if not hunt.enabled:
                continue

            if hunt.ready:
                self.execute_hunt(hunt)
                continue
            else:
                # this one isn't ready so wait for this hunt to be ready
                wait_time = (hunt.next_execution_time - local_time()).total_seconds()
                self.logger.info(f"next hunt is {hunt} @ {hunt.next_execution_time} ({wait_time} seconds)")
                self.wait_control_event.wait(wait_time)
                self.wait_control_event.clear()

                # if a hunt ends while we're waiting, wait_control_event will break out before wait_time seconds
                # at this point, it's possible there's another hunt ready to execute before this one we're waiting on
                # so no matter what, we break out so that we re-enter with a re-ordered list of hunts
                return

    def execute_hunt(self, hunt):
        # are we ready to run another one of these types of hunts?
        # NOTE this will BLOCK until a semaphore is ready OR this manager is shutting down
        start_time = local_time()
        hunt.semaphore = self.acquire_concurrency_lock()

        if self.manager_control_event.is_set():
            if hunt.semaphore is not None:
                hunt.semaphore.release()
            return

        # keep track of how long it's taking to acquire the resource
        if hunt.semaphore is not None:
            self.record_semaphore_acquire_time(local_time() - start_time)

        # start the execution of the hunt on a new thread
        hunt_execution_thread = threading.Thread(
            target=self.execute_threaded_hunt, args=(hunt,), name=f"Hunt Execution {hunt}"
        )
        hunt_execution_thread.start()

        # wait for the signal that the hunt has started
        # this will block for a short time to ensure we don't wrap back around before the
        # execution lock is acquired
        hunt.startup_barrier.wait()

    def execute_threaded_hunt(self, hunt):
        try:
            submissions = hunt.execute_with_lock()
            if submissions:
                hunt.apply_suppression()
        except Exception as e:
            self.logger.error(f"uncaught exception: {e}")
            traceback.print_exc()
        finally:
            self.release_concurrency_lock(hunt.semaphore)
            # at this point this hunt has finished and is eligible to execute again
            self.wait_control_event.set()

        if submissions is not None:
            for submission in submissions:
                self.collector.queue_submission(submission)

    def cancel_hunts(self):
        """Cancels all the currently executing hunts."""
        for hunt in self._hunts:  # order doesn't matter here
            try:
                if hunt.running:
                    self.logger.info("cancelling {hunt}")
                    hunt.cancel()
                    hunt.wait()
            except Exception as e:
                self.logger.info("unable to cancel {hunt}: {e}")

    def set_concurrency_limit(self, limit):
        """Sets the concurrency limit for this type of hunt.
        If limit is a string then it's considered to be the name of a network semaphore.
        If limit is an integer then a local threading.Semaphore is used."""
        try:
            # if the limit value is an integer then it's a local semaphore
            self.concurrency_type = CONCURRENCY_TYPE_LOCAL_SEMAPHORE
            self.concurrency_semaphore = threading.Semaphore(int(limit))
            self.logger.debug(f"concurrency limit for {self.hunt_type} set to local limit {limit}")
        except ValueError:
            # otherwise it's the name of a network semaphore
            self.concurrency_type = CONCURRENCY_TYPE_NETWORK_SEMAPHORE
            self.concurrency_semaphore = limit
            self.logger.debug(
                f"concurrency limit for {self.hunt_type} set to " f"network semaphore {self.concurrency_semaphore}"
            )

    def acquire_concurrency_lock(self):
        """Acquires a concurrency lock for this type of hunt if specified in the configuration for the hunt.
        Returns a NetworkSemaphoreClient object if the concurrency_type is CONCURRENCY_TYPE_NETWORK_SEMAPHORE
        or a reference to the threading.Semaphore object if concurrency_type is CONCURRENCY_TYPE_LOCAL_SEMAPHORE.
        Immediately returns None if non concurrency limits are in place for this type of hunt."""

        if self.concurrency_type is None:
            return None

        result = None
        start_time = local_time()
        if self.concurrency_type == CONCURRENCY_TYPE_NETWORK_SEMAPHORE:
            self.logger.debug(
                f"acquiring network concurrency semaphore {self.concurrency_semaphore} "
                f"for hunt type {self.hunt_type}"
            )
            result = NetworkSemaphoreClient(cancel_request_callback=self.manager_control_event.is_set)
            # make sure we cancel outstanding request
            # when shutting down
            result.acquire(self.concurrency_semaphore)
        else:
            self.logger.debug(f"acquiring local concurrency semaphore for hunt type {self.hunt_type}")
            while not self.manager_control_event.is_set():
                if self.concurrency_semaphore.acquire(blocking=True, timeout=0.1):
                    result = self.concurrency_semaphore
                    break

        if result is not None:
            total_seconds = (local_time() - start_time).total_seconds()
            self.logger.debug(
                f"acquired concurrency semaphore for hunt type {self.hunt_type} in {total_seconds} seconds"
            )

        return result

    def release_concurrency_lock(self, semaphore):
        if semaphore is not None:
            # both types of semaphores support this function call
            self.logger.debug(f"releasing concurrency semaphore for hunt type {self.hunt_type}")
            semaphore.release()

    def load_hunts_from_config(self, hunt_filter=lambda hunt: True):
        """Loads the hunts from the configuration settings.
        Returns True if all of the hunts were loaded correctly, False if any errors occurred.
        The hunt_filter paramter defines an optional lambda function that takes the Hunt object
        after it is loaded and returns True if the Hunt should be added, False otherwise.
        This is useful for unit testing."""
        for hunt_config in self._list_hunt_ini():
            hunt = self.hunt_cls(manager=self)
            self.logger.debug(f"loading hunt from {hunt_config}")
            try:
                hunt.load_from_ini(hunt_config)

                if hunt_filter(hunt):
                    self.logger.debug(f"loaded {hunt} from {hunt_config}")
                    self.add_hunt(hunt)
                else:
                    self.logger.debug(f"not loading {hunt} (hunt_filter returned False)")

            except InvalidHuntTypeError as e:
                self.skipped_ini_files.add(hunt_config)
                self.logger.debug(f"skipping {hunt_config} for {self}: {e}")
                continue
            except Exception as e:
                self.logger.error(f"unable to load hunt {hunt}: {e}")
                traceback.print_exc()
                try:
                    self.failed_ini_files[hunt_config] = os.path.getmtime(hunt_config)
                except Exception as e:
                    self.logger.error(f"unable to get mtime for {hunt_config}: {e}")

        # remember that we loaded the hunts from the configuration file
        # this is used when we receive the signal to reload the hunts
        self.hunts_loaded_from_config = True

    def add_hunt(self, hunt):
        assert isinstance(hunt, Hunt)
        if hunt.type != self.hunt_type:
            raise ValueError(f"hunt {hunt} has wrong type for {self.hunt_type}")

        with self.hunt_lock:
            # make sure this hunt doesn't already exist
            for _hunt in self._hunts:
                if _hunt.name == hunt.name:
                    raise KeyError(f"duplicate hunt {hunt.name}")

            with open_hunt_db(self.hunt_type) as db:
                c = db.cursor()
                c.execute("INSERT OR IGNORE INTO hunt(hunt_name) VALUES ( ? )", (hunt.name,))
                db.commit()

            self._hunts.append(hunt)

        self.wait_control_event.set()
        return hunt

    def clear_hunts(self):
        """Removes all hunts."""
        with self.hunt_lock:
            with open_hunt_db(self.hunt_type) as db:
                c = db.cursor()
                c.execute("DELETE FROM hunt")
                db.commit()

            self._hunts = []
            self.failed_ini_files = {}
            self.skipped_ini_files = set()

        self.wait_control_event.set()

    def remove_hunt(self, hunt):
        assert isinstance(hunt, Hunt)

        with self.hunt_lock:
            with open_hunt_db(hunt.type) as db:
                c = db.cursor()
                c.execute("DELETE FROM hunt WHERE hunt_name = ?", (hunt.name,))
                db.commit()

            self._hunts.remove(hunt)

        self.wait_control_event.set()
        return hunt

    def _list_hunt_ini(self):
        """Returns the list of ini files for hunts in self.rule_dirs."""
        result = []
        for rule_dir in self.rule_dirs:
            rule_dir = abs_path(rule_dir, self.relative_detection_dir)
            if not os.path.isdir(rule_dir):
                self.logger.error(f"rules directory {rule_dir} specified for {self} is not a directory")
                continue

            # load each .ini file found in this rules directory
            self.logger.debug(f"searching {rule_dir} for hunt configurations")
            for root, dirnames, filenames in os.walk(rule_dir):
                for hunt_config in filenames:
                    if not hunt_config.endswith(".ini"):
                        continue

                    result.append(os.path.join(root, hunt_config))

        return result

    def record_semaphore_acquire_time(self, time_delta):
        pass


class Hunter:
    """ACE Hunter Client.

    Attributes:
        config: (optional) A loaded ConfigParser object for the ACE Hunter client.
    """

    def __init__(self, config: configparser.ConfigParser = None, update_frequency: int = 60, **kwargs):
        self.logger = logging.getLogger("ace_hunter.Hunter")
        self.config = config
        if self.config is None:
            self.config = CONFIG

        self.update_frequency = update_frequency

        # each type of hunt is grouped and managed as a single unit
        self.hunt_managers = {}  # key = hunt_type, value = HuntManager

        # the directory that can contain various forms of persistence for collections
        self.persistence_dir = os.path.join(DATA_DIR, self.config["collection"]["persistence_dir"])

    def load_hunt_managers(self):
        """Loads all configured hunt managers."""
        for section_name in self.config.sections():
            if not section_name.startswith("hunt_type_"):
                continue

            section = self.config[section_name]

            if "rule_dirs" not in section:
                self.logger.error(f"config section {section} does not define rule_dirs")
                continue

            hunt_type = section_name[len("hunt_type_") :]

            # make sure the class definition for this hunt is valid
            module_name = section["module"]
            try:
                _module = importlib.import_module(module_name)
            except Exception as e:
                self.logger.error(f"unable to import hunt module {module_name}: {e}")
                continue

            class_name = section["class"]
            try:
                class_definition = getattr(_module, class_name)
            except AttributeError as e:
                self.logger.error(
                    "class {} does not exist in module {} in hunt {} config".format(class_name, module_name, section)
                )
                continue

            requirements = {}
            if hasattr(_module, "hunt_type_config_requirements"):
                # requirements_met = validate_hunt_type_config_requirements(_module.hunt_type_config_requirements)
                requirements = _module.hunt_type_config_requirements

            self.logger.debug(f"loading hunt manager for {hunt_type} class {class_definition}")
            self.hunt_managers[hunt_type] = HuntManager(
                hunt_type=hunt_type,
                rule_dirs=[_.strip() for _ in section["rule_dirs"].split(",")],
                hunt_cls=class_definition,
                concurrency_limit=section.get("concurrency_limit", fallback=None),
                persistence_dir=self.persistence_dir,
                update_frequency=self.update_frequency,
                config=section,
                requirements=requirements,
            )

        if not self.hunt_managers:
            return False
        return True
