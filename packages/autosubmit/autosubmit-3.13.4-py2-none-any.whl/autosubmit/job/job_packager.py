#!/usr/bin/env python

# Copyright 2017-2020 Earth Sciences Department, BSC-CNS

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

from log.log import Log
from autosubmit.job.job_common import Status, Type
from bscearth.utils.date import sum_str_hours
from autosubmit.job.job_packages import JobPackageSimple, JobPackageVertical, JobPackageHorizontal, \
    JobPackageSimpleWrapped, JobPackageHorizontalVertical, JobPackageVerticalHorizontal
from operator import attrgetter
from math import ceil
import operator
from time import sleep
from collections import defaultdict
from log.log import AutosubmitError, AutosubmitCritical, Log


class JobPackager(object):
    """
    Main class that manages Job wrapping.

    :param as_config: Autosubmit basic configuration.\n
    :type as_config: AutosubmitConfig object.\n
    :param platform: A particular platform we are dealing with, e.g. Lsf Platform.\n
    :type platform: Specific Platform Object, e.g. LsfPlatform(), EcPlatform(), ...\n
    :param jobs_list: Contains the list of the jobs, along other properties.\n
    :type jobs_list: JobList object.
    """

    def __init__(self, as_config, platform, jobs_list, hold=False):
        self._as_config = as_config
        self._platform = platform
        self._jobs_list = jobs_list
        self.hold = hold

        # Submitted + Queuing Jobs for specific Platform
        queuing_jobs = jobs_list.get_queuing(platform)
        # We now consider the running jobs count
        running_jobs_count = len(jobs_list.get_running(platform))
        queued_by_id = dict()
        for queued_job in queuing_jobs:
            queued_by_id[queued_job.id] = queued_job
        queuing_jobs_len = len(queued_by_id.keys())

        submitted_jobs = jobs_list.get_submitted(platform)
        submitted_by_id = dict()
        for submitted_job in submitted_jobs:
            submitted_by_id[submitted_job.id] = submitted_job
        submitted_jobs_len = len(submitted_by_id.keys())

        waiting_jobs = submitted_jobs_len + queuing_jobs_len
        # Calculate available space in Platform Queue
        self._max_wait_jobs_to_submit = platform.max_waiting_jobs - waiting_jobs
        # .total_jobs is defined in each section of platforms_.conf, if not from there, it comes form autosubmit_.conf
        # .total_jobs Maximum number of jobs at the same time
        self._max_jobs_to_submit = platform.total_jobs - queuing_jobs_len
        # Substracting running jobs
        self._max_jobs_to_submit = self._max_jobs_to_submit - running_jobs_count
        self._max_jobs_to_submit = self._max_jobs_to_submit if self._max_jobs_to_submit > 0 else 0
        self.max_jobs = min(self._max_wait_jobs_to_submit,
                            self._max_jobs_to_submit)
        # These are defined in the [wrapper] section of autosubmit_,conf
        self.wrapper_type = self._as_config.get_wrapper_type()
        self.wrapper_policy = self._as_config.get_wrapper_policy()
        self.wrapper_method = self._as_config.get_wrapper_method().lower()
        # True or False
        self.jobs_in_wrapper = self._as_config.get_wrapper_jobs()
        Log.debug(
            "Number of jobs available: {0}", self._max_wait_jobs_to_submit)
        if self.hold:
            Log.debug("Number of jobs prepared: {0}", len(
                jobs_list.get_prepared(platform)))
            if len(jobs_list.get_prepared(platform)) > 0:
                Log.debug("Jobs ready for {0}: {1}", self._platform.name, len(
                    jobs_list.get_prepared(platform)))
        else:
            Log.debug("Number of jobs ready: {0}", len(
                jobs_list.get_ready(platform, hold=False)))
            if len(jobs_list.get_ready(platform)) > 0:
                Log.debug("Jobs ready for {0}: {1}", self._platform.name, len(
                    jobs_list.get_ready(platform)))
        self._maxTotalProcessors = 0

    def compute_weight(self, job_list):
        job = self
        jobs_by_section = dict()
        held_jobs = self._jobs_list.get_held_jobs()
        jobs_held_by_section = dict()
        for job in held_jobs:
            if job.section not in jobs_held_by_section:
                jobs_held_by_section[job.section] = []
            jobs_held_by_section[job.section].append(job)
        for job in job_list:
            if job.section not in jobs_by_section:
                jobs_by_section[job.section] = []
            jobs_by_section[job.section].append(job)

        for section in jobs_by_section:
            if section in jobs_held_by_section.keys():
                weight = len(jobs_held_by_section[section]) + 1
            else:
                weight = 1
            highest_completed = []

            for job in sorted(jobs_by_section[section], key=operator.attrgetter('chunk')):
                weight = weight + 1
                job.distance_weight = weight
                completed_jobs = 9999
                if job.has_parents() > 1:
                    tmp = [
                        parent for parent in job.parents if parent.status == Status.COMPLETED]
                    if len(tmp) > completed_jobs:
                        completed_jobs = len(tmp)
                        highest_completed = [job]
                    else:
                        highest_completed.append(job)
            for job in highest_completed:
                job.distance_weight = job.distance_weight - 1

    def build_packages(self):
        """
        Returns the list of the built packages to be submitted

        :return: List of packages depending on type of package, JobPackageVertical Object for 'vertical-mixed' or 'vertical'. \n
        :rtype: List() of JobPackageVertical
        """
        packages_to_submit = list()
        dependencies_keys = list()
        max_wrapper_job_by_section = dict()
        # only_wrappers = False when coming from Autosubmit.submit_ready_jobs, jobs_filtered empty
        jobs_ready = list()
        if len(self._jobs_list.jobs_to_run_first) > 0:
            jobs_ready = [job for job in self._jobs_list.jobs_to_run_first if
                     ( self._platform is None or job.platform.name.lower() == self._platform.name.lower() ) and
                     job.status == Status.READY]
        if len(jobs_ready) == 0:
            if self.hold:
                jobs_ready = self._jobs_list.get_prepared(self._platform)
            else:
                jobs_ready = self._jobs_list.get_ready(self._platform)

        if self.hold and len(jobs_ready) > 0:
            self.compute_weight(jobs_ready)
            sorted_jobs = sorted(
                jobs_ready, key=operator.attrgetter('distance_weight'))
            jobs_in_held_status = self._jobs_list.get_held_jobs(
            ) + self._jobs_list.get_submitted(self._platform, hold=self.hold)
            held_by_id = dict()
            for held_job in jobs_in_held_status:
                if held_job.id not in held_by_id:
                    held_by_id[held_job.id] = []
                held_by_id[held_job.id].append(held_job)
            current_held_jobs = len(held_by_id.keys())
            remaining_held_slots = 5 - current_held_jobs
            try:
                while len(sorted_jobs) > remaining_held_slots:
                    if sorted_jobs[-1].packed:
                        sorted_jobs[-1].packed = False
                    del sorted_jobs[-1]
                for job in sorted_jobs:
                    if job.distance_weight > 3:
                        sorted_jobs.remove(job)
                jobs_ready = sorted_jobs
                pass
            except IndexError:
                pass
        if len(jobs_ready) == 0:
            # If there are no jobs ready, result is tuple of empty
            return packages_to_submit
        if not (self._max_wait_jobs_to_submit > 0 and self._max_jobs_to_submit > 0):
            # If there is no more space in platform, result is tuple of empty
            return packages_to_submit

        # Sort by 6 first digits of date
        available_sorted = sorted(
            jobs_ready, key=lambda k: k.long_name.split('_')[1][:6])
        # Sort by Priority, highest first
        list_of_available = sorted(
            available_sorted, key=lambda k: k.priority, reverse=True)
        num_jobs_to_submit = min(self._max_wait_jobs_to_submit, len(
            jobs_ready), self._max_jobs_to_submit)
        # Take the first num_jobs_to_submit from the list of available
        jobs_to_submit_tmp = list_of_available[0:num_jobs_to_submit]
        jobs_to_submit = [
            fresh_job for fresh_job in jobs_to_submit_tmp if fresh_job.fail_count == 0]

        jobs_to_submit_seq = [
            failed_job for failed_job in jobs_to_submit_tmp if failed_job.fail_count > 0]
        jobs_to_submit_by_section = self._divide_list_by_section(
            jobs_to_submit)
        packages_to_submit = []
        for job in jobs_to_submit_seq:  # Failed jobs at least one time, this shouldn't be there for strict wrappers :/
            job.packed = False
            if job.type == Type.PYTHON and not self._platform.allow_python_jobs:
                package = JobPackageSimpleWrapped([job])
            else:
                package = JobPackageSimple([job])
            packages_to_submit.append(package)

        for section in jobs_to_submit_by_section:
            wrapped = False
            # Only if platform allows wrappers, wrapper type has been correctly defined, and job names for wrappers have been correctly defined
            # ('None' is a default value) or the correct section is included in the corresponding sections in [wrappers]
            if self._platform.allow_wrappers and self.wrapper_type in ['horizontal', 'vertical', 'vertical-mixed','vertical-horizontal', 'horizontal-vertical'] and section in self.jobs_in_wrapper:
                # Trying to find the value in jobs_parser, if not, default to an autosubmit_.conf value (Looks first in [wrapper] section)
                max_wrapped_jobs = int(self._as_config.jobs_parser.get_option(section, "MAX_WRAPPED", self._as_config.get_max_wrapped_jobs()))
                if '&' not in section:
                    if self._as_config.jobs_parser.has_option(section, 'DEPENDENCIES'):
                        dependencies_keys = self._as_config.jobs_parser.get(
                            section, "DEPENDENCIES").split()
                    else:
                        dependencies_keys = []
                    max_wrapper_job_by_section[section] = max_wrapped_jobs
                else:
                    multiple_sections = section.split('&')
                    dependencies_keys = []
                    for sectionN in multiple_sections:
                        if self._as_config.jobs_parser.has_option(sectionN, 'DEPENDENCIES'):
                            dependencies_keys += self._as_config.jobs_parser.get(
                                sectionN, "DEPENDENCIES").split()
                        if self._as_config.jobs_parser.has_option(sectionN, 'MAX_WRAPPED'):
                            max_wrapper_job_by_section[sectionN] = int(self._as_config.jobs_parser.get(
                                sectionN, "MAX_WRAPPED"))
                        else:
                            max_wrapper_job_by_section[sectionN] = max_wrapped_jobs
                hard_limit_wrapper = max_wrapped_jobs
                for k in dependencies_keys:
                    if "-" in k:
                        k_divided = k.split("-")
                        if k_divided[0] not in self.jobs_in_wrapper:
                            number = int(k_divided[1].strip(" "))
                            if number < max_wrapped_jobs:
                                hard_limit_wrapper = number
                min_wrapped_jobs = min(self._as_config.jobs_parser.get_option(section, "MIN_WRAPPED", self._as_config.get_min_wrapped_jobs()), hard_limit_wrapper)
                if self.wrapper_type in ['vertical', 'vertical-mixed']:
                    built_packages_tmp = self._build_vertical_packages(jobs_to_submit_by_section[section],
                                                                       max_wrapped_jobs, max_wrapper_job_by_section)
                elif self.wrapper_type == 'horizontal':
                    built_packages_tmp = self._build_horizontal_packages(jobs_to_submit_by_section[section],
                                                                         max_wrapped_jobs, section, max_wrapper_job_by_section)
                elif self.wrapper_type in ['vertical-horizontal', 'horizontal-vertical']:
                    built_packages_tmp = list()
                    built_packages_tmp.append(self._build_hybrid_package(
                        jobs_to_submit_by_section[section], max_wrapped_jobs, section, max_wrapper_job_by_section))
                else:
                    built_packages_tmp = self._build_vertical_packages(jobs_to_submit_by_section[section],
                                                                       max_wrapped_jobs, max_wrapper_job_by_section)
                for p in built_packages_tmp:
                    infinite_deadlock = False  # This will raise an autosubmit critical if true
                    failed_innerjobs = False
                    job_has_to_run_first = False
                    aux_jobs = []
                    # Check failed jobs first
                    for job in p.jobs:
                        if len(self._jobs_list.jobs_to_run_first) > 0:
                            if job not in self._jobs_list.jobs_to_run_first:
                                job.packed = False
                                aux_jobs.append(job)
                        if job.fail_count > 0:
                            failed_innerjobs = True
                    if len(self._jobs_list.jobs_to_run_first) > 0:
                        job_has_to_run_first = True
                        for job in aux_jobs:
                            job.packed = False
                            p.jobs.remove(job)
                            if self.wrapper_type != "horizontal" and self.wrapper_type != "vertical" and self.wrapper_type != "vertical-mixed":
                                for seq in range(0,len(p.jobs_lists)):
                                    try:
                                        p.jobs_lists[seq].remove(job)
                                    except:
                                        pass
                        if self.wrapper_type != "horizontal" and self.wrapper_type != "vertical" and self.wrapper_type != "vertical-mixed":
                            aux = p.jobs_lists
                            p.jobs_lists = []
                            for seq in range(0,len(aux)):
                                if len(aux[seq]) > 0:
                                    p.jobs_lists.append(aux[seq])
                    if len(p.jobs) > 0:
                        if failed_innerjobs and self.wrapper_policy == "mixed":
                            for job in p.jobs:
                                if job.fail_count == 0:
                                    continue
                                Log.debug("Wrapper policy is set to mixed and there are failed jobs")
                                job.packed = False
                                if job.status == Status.READY:
                                    if job.type == Type.PYTHON and not self._platform.allow_python_jobs:
                                        package = JobPackageSimpleWrapped([job])
                                    else:
                                        package = JobPackageSimple([job])
                                    packages_to_submit.append(package)
                        else:
                            balanced = True
                            if self.wrapper_type == 'vertical-horizontal':
                                min_h = len(p.jobs_lists)
                                min_v = len(p.jobs_lists[0])
                                for list_of_jobs in p.jobs_lists[1:-1]:
                                    min_v = min(min_v, len(list_of_jobs))
                                min_t = min_h
                            elif self.wrapper_type == 'horizontal-vertical':
                                min_v = len(p.jobs_lists)
                                min_h = len(p.jobs_lists[0])
                                for list_of_jobs in p.jobs_lists[1:-1]:
                                    min_h = min(min_h, len(list_of_jobs))
                                for list_of_jobs in p.jobs_lists[:-1]:
                                    if min_h != len(list_of_jobs):
                                        balanced = False
                                min_t = min_h
                            elif self.wrapper_type == 'horizontal':
                                min_h = len(p.jobs)
                                min_v = 0
                                min_t = len(p.jobs)
                            elif self.wrapper_type == 'vertical':
                                min_v = len(p.jobs)
                                min_h = 0
                                min_t = len(p.jobs)
                            else:
                                min_v = 0
                                min_h = 0
                                min_t = 0
                            # if the quantity is enough, make the wrapper
                            if min_t >= min_wrapped_jobs or job_has_to_run_first:
                                for job in p.jobs:
                                    job.packed = True
                                packages_to_submit.append(p)
                            else:
                                deadlock = True
                                if deadlock: # Remaining jobs if chunk is the last one
                                    for job in p.jobs:
                                        if job.running =="chunk" and job.chunk == int(job.parameters["NUMCHUNKS"]):
                                            deadlock = False
                                            break
                                if not deadlock: # Submit package if deadlock has been liberated
                                    for job in p.jobs:
                                        job.packed = True
                                    packages_to_submit.append(p)
                                else:
                                    wallclock_sum = p.jobs[0].wallclock
                                    for seq in xrange(1, min_v):
                                        wallclock_sum = sum_str_hours(wallclock_sum, p.jobs[0].wallclock)
                                    next_wrappable_jobs = self._jobs_list.get_jobs_by_section(self.jobs_in_wrapper)
                                    next_wrappable_jobs = [job for job in next_wrappable_jobs if job.status == Status.WAITING and job not in p.jobs ] # Get only waiting jobs
                                    active_jobs = list()
                                    aux_active_jobs = list()
                                    for job in next_wrappable_jobs: # Prone tree by looking for only the closest children
                                        direct_children = False
                                        for related in job.parents:
                                            if related in p.jobs:
                                                direct_children = True
                                                break
                                        if direct_children: # Get parent of direct children that aren't in in wrapper
                                            aux_active_jobs += [aux_parent for aux_parent in job.parents if (  aux_parent.status != Status.COMPLETED and aux_parent.status != Status.FAILED) and ( aux_parent.section not in self.jobs_in_wrapper or ( aux_parent.section in self.jobs_in_wrapper and aux_parent.status != Status.COMPLETED and aux_parent.status != Status.FAILED and aux_parent.status != Status.WAITING and aux_parent.status != Status.READY ) ) ]
                                    aux_active_jobs = list(set(aux_active_jobs))
                                    track = [] # Tracker to prone tree for avoid the checking of the same parent from diferent nodes.
                                    active_jobs_names = [ job.name for job in p.jobs ] # We want to search if the actual wrapped jobs needs to run for add more jobs to this wrapper
                                    hard_deadlock = False
                                    for job in aux_active_jobs:
                                        parents_to_check = []
                                        if job.status == Status.WAITING: # We only want to check uncompleted parents
                                            aux_job = job
                                            for parent in aux_job.parents: # First case
                                                if parent.name in active_jobs_names:
                                                    hard_deadlock = True
                                                    infinite_deadlock = True
                                                    break
                                                if (parent.status == Status.WAITING ) and parent.name != aux_job.name:
                                                    parents_to_check.append(parent)
                                            track.extend(parents_to_check)
                                            while len(parents_to_check) > 0 and not infinite_deadlock: # We want to look deeper on the tree until all jobs are completed or we find an unresolveable deadlock.
                                                aux_job = parents_to_check.pop(0)
                                                for parent in aux_job.parents:
                                                    if parent.name in active_jobs_names:
                                                        hard_deadlock = True
                                                        infinite_deadlock = True
                                                        break
                                                    if (parent.status == Status.WAITING ) and parent.name != aux_job.name and parent not in track:
                                                        parents_to_check.append(parent)
                                                track.extend(parents_to_check)
                                        if not infinite_deadlock:
                                            active_jobs.append(job)  # List of jobs that can continue to run without run this wrapper
                                    # Act in base of active_jobs and Policies
                                    if self.wrapper_policy == "strict":
                                        error = True
                                        for job in p.jobs:
                                            job.packed = False
                                            if job in self._jobs_list.jobs_to_run_first:
                                                error = False
                                                if job.status == Status.READY:
                                                    if job.type == Type.PYTHON and not self._platform.allow_python_jobs:
                                                        package = JobPackageSimpleWrapped(
                                                            [job])
                                                    else:
                                                        package = JobPackageSimple([job])
                                                    packages_to_submit.append(package)
                                        if len(active_jobs) > 0 or not error:
                                            Log.printlog("Wrapper policy is set to STRICT and there are not enough jobs to form a wrapper. [wrappeable:{0} < defined_min:{1}] waiting until the wrapper can be formed.".format(min_t, min_wrapped_jobs), 6013)
                                        else:
                                            message = "Wrapper couldn't be formed under {0} POLICY due minimum limit not being reached: [wrappeable:{1} < defined_min:{2}] ".format(
                                                self.wrapper_policy, min_t, min_wrapped_jobs)
                                            if hard_deadlock:
                                                message += "\nCheck your configuration: The next wrappeable job can't be wrapped until some of inner jobs of current packages finishes which is imposible"
                                            if min_t > 1:
                                                message += "\nCheck your configuration: Check if current {0} vertical wallclock has reached the max defined on platforms.conf.".format(wallclock_sum)
                                            else:
                                                message += "\nCheck your configuration: Only jobs_in_wrappers are active, check your jobs_in_wrapper dependencies."
                                            if not balanced:
                                                message += "\nPackages are not well balanced: Check your dependencies(This is not the main cause of the Critical error)"
                                            if len(self._jobs_list.get_in_queue()) == 0:
                                                raise AutosubmitCritical(message, 7014)
                                    elif self.wrapper_policy == "mixed":
                                        error = True
                                        show_log = True
                                        for job in p.jobs:
                                            job.packed = False
                                            if job in self._jobs_list.jobs_to_run_first:
                                                error = False
                                                if job.status == Status.READY:
                                                    if job.type == Type.PYTHON and not self._platform.allow_python_jobs:
                                                        package = JobPackageSimpleWrapped(
                                                            [job])
                                                    else:
                                                        package = JobPackageSimple([job])
                                                    packages_to_submit.append(package)
                                            else:
                                                if job.fail_count > 0 and job.status == Status.READY:
                                                    Log.printlog(
                                                        "Wrapper policy is set to mixed, there is a failed job that will be sent sequential")
                                                    error = False
                                                    show_log = False
                                                    if job.type == Type.PYTHON and not self._platform.allow_python_jobs:
                                                        package = JobPackageSimpleWrapped(
                                                            [job])
                                                    else:
                                                        package = JobPackageSimple([job])
                                                    packages_to_submit.append(package)
                                            if len(active_jobs) > 0:
                                                if show_log:
                                                    Log.printlog("Wrapper policy is set to MIXED and there are not enough jobs to form a wrapper. [wrappeable:{0} < defined_min:{1}] waiting until the wrapper can be formed.".format(min_t, min_wrapped_jobs), 6013)
                                            else:
                                                message = "Wrapper couldn't be formed under {0} POLICY due minimum limit not being reached: [wrappeable:{1} < defined_min:{2}] ".format(
                                                    self.wrapper_policy,min_t,min_wrapped_jobs)
                                                if hard_deadlock:
                                                    message += "\nCheck your configuration: The next wrappeable job can't be wrapped until some of inner jobs of current packages finishes which is imposible"
                                                if min_t > 1:
                                                    message += "\nCheck your configuration: Check if current {0} vertical wallclock has reached the max defined on platforms.conf.".format(
                                                        wallclock_sum)
                                                else:
                                                    message += "\nCheck your configuration: Only jobs_in_wrappers are active, check your jobs_in_wrapper dependencies."
                                                if not balanced:
                                                    message += "\nPackages are not well balanced! (This is not the main cause of the Critical error)"
                                                if len(self._jobs_list.get_in_queue()) == 0: # When there are not more posible jobs, autosubmit will stop the execution
                                                    raise AutosubmitCritical(message, 7014)
                                    else:
                                        for job in p.jobs:
                                            job.packed = False
                                            if job.status == Status.READY:
                                                if job.type == Type.PYTHON and not self._platform.allow_python_jobs:
                                                    package = JobPackageSimpleWrapped(
                                                        [job])
                                                else:
                                                    package = JobPackageSimple([job])
                                                packages_to_submit.append(package)
                                        Log.info("Wrapper policy is set to flexible and there is a deadlock, As will submit the jobs sequentally")
            else:
                for job in jobs_to_submit_by_section[section]:
                    if job.type == Type.PYTHON and not self._platform.allow_python_jobs:
                        package = JobPackageSimpleWrapped([job])
                    else:
                        package = JobPackageSimple([job])
                    packages_to_submit.append(package)

        for package in packages_to_submit:
            self.max_jobs = self.max_jobs - 1
            package.hold = self.hold

        return packages_to_submit

    def _divide_list_by_section(self, jobs_list):
        """
        Returns a dict() with as many keys as 'jobs_list' different sections
        The value for each key is a list() with all the jobs with the key section.

        :param jobs_list: list of jobs to be divided
        :rtype: Dictionary Key: Section Name, Value: List(Job Object)
        """
        # .jobs_in_wrapper defined in .conf, see constructor.
        sections_split = self.jobs_in_wrapper.split()

        jobs_section = dict()
        for job in jobs_list:
            # This iterator will always return None if there is no '&' defined in the section name
            section = next(
                (s for s in sections_split if job.section in s and '&' in s), None)
            if section is None:
                section = job.section
            if section not in jobs_section:
                jobs_section[section] = list()
            jobs_section[section].append(job)
        return jobs_section

    def _build_horizontal_packages(self, section_list, max_wrapped_jobs, section, max_wrapper_job_by_section):
        packages = []
        horizontal_packager = JobPackagerHorizontal(section_list, self._platform.max_processors, max_wrapped_jobs,
                                                    self.max_jobs, self._platform.processors_per_node, self.wrapper_method, max_wrapper_job_by_section=max_wrapper_job_by_section)

        package_jobs = horizontal_packager.build_horizontal_package()

        jobs_resources = dict()

        current_package = None
        if package_jobs:
            machinefile_function = self._as_config.get_wrapper_machinefiles()
            if machinefile_function == 'COMPONENTS':
                jobs_resources = horizontal_packager.components_dict
            jobs_resources['MACHINEFILES'] = machinefile_function
            current_package = JobPackageHorizontal(
                package_jobs, jobs_resources=jobs_resources, method=self.wrapper_method, configuration=self._as_config)
            packages.append(current_package)

        return packages

    def _build_vertical_packages(self, section_list, max_wrapped_jobs, max_wrapper_job_by_section):
        """
        Builds Vertical-Mixed or Vertical

        :param section_list: Jobs defined as wrappable belonging to a common section.\n
        :type section_list: List() of Job Objects. \n
        :param max_wrapped_jobs: Number of maximum jobs that can be wrapped (Can be user defined), per section. \n
        :type max_wrapped_jobs: Integer. \n
        :param min_wrapped_jobs: Number of maximum jobs that can be wrapped (Can be user defined), per section. \n
        :type min_wrapped_jobs: Integer. \n
        :return: List of Wrapper Packages, Dictionary that details dependencies. \n
        :rtype: List() of JobPackageVertical(), Dictionary Key: String, Value: (Dictionary Key: Variable Name, Value: String/Int)
        """
        packages = []
        for job in section_list:
            if self.max_jobs > 0:
                if job.packed is False:
                    job.packed = True
                    if self.wrapper_type == 'vertical-mixed':
                        dict_jobs = self._jobs_list.get_ordered_jobs_by_date_member()
                        job_vertical_packager = JobPackagerVerticalMixed(dict_jobs, job, [job], job.wallclock, self.max_jobs,
                                                                         max_wrapped_jobs, self._platform.max_wallclock, max_wrapper_job_by_section)
                    else:
                        job_vertical_packager = JobPackagerVerticalSimple([job], job.wallclock, self.max_jobs,
                                                                          max_wrapped_jobs, self._platform.max_wallclock, max_wrapper_job_by_section)

                    jobs_list = job_vertical_packager.build_vertical_package(
                        job)

                    if job.status is Status.READY:
                        packages.append(JobPackageVertical(
                            jobs_list, configuration=self._as_config))
                    else:
                        package = JobPackageVertical(jobs_list, None)
                        packages.append(package)

            else:
                break
        return packages

    def _build_hybrid_package(self, jobs_list, max_wrapped_jobs, section, max_wrapper_job_by_section=dict()):
        jobs_resources = dict()
        jobs_resources['MACHINEFILES'] = self._as_config.get_wrapper_machinefiles()

        ## READY JOBS ##
        ## Create the horizontal ##
        horizontal_packager = JobPackagerHorizontal(jobs_list, self._platform.max_processors, max_wrapped_jobs,
                                                    self.max_jobs, self._platform.processors_per_node, max_wrapper_job_by_section=max_wrapper_job_by_section)
        if self.wrapper_type == 'vertical-horizontal':
            return self._build_vertical_horizontal_package(horizontal_packager, jobs_resources)
        else:
            return self._build_horizontal_vertical_package(horizontal_packager, section, jobs_resources)

    def _build_horizontal_vertical_package(self, horizontal_packager, section, jobs_resources):
        total_wallclock = '00:00'
        horizontal_package = horizontal_packager.build_horizontal_package()
        horizontal_packager.create_sections_order(section)
        horizontal_packager.add_sectioncombo_processors(
            horizontal_packager.total_processors)
        horizontal_package.sort(
            key=lambda job: horizontal_packager.sort_by_expression(job.name))
        job = max(horizontal_package, key=attrgetter('total_wallclock'))
        wallclock = job.wallclock
        current_package = [horizontal_package]
        #current_package = []
        ## Get the next horizontal packages ##
        max_procs = horizontal_packager.total_processors
        new_package = horizontal_packager.get_next_packages(
            section, max_wallclock=self._platform.max_wallclock, horizontal_vertical=True, max_procs=max_procs)

        if new_package is not None:
            current_package += new_package

        for i in xrange(len(current_package)):
            total_wallclock = sum_str_hours(total_wallclock, wallclock)
        if len(current_package) > 1:
            for level in xrange(1, len(current_package)):
                for job in current_package[level]:
                    job.level = level
        return JobPackageHorizontalVertical(current_package, max_procs, total_wallclock,
                                            jobs_resources=jobs_resources, configuration=self._as_config)

    def _build_vertical_horizontal_package(self, horizontal_packager, jobs_resources):
        total_wallclock = '00:00'
        horizontal_package = horizontal_packager.build_horizontal_package()
        total_processors = horizontal_packager.total_processors
        current_package = []

        ## Create the vertical ##
        for job in horizontal_package:
            job_list = JobPackagerVerticalSimple([job], job.wallclock, self.max_jobs,
                                                 horizontal_packager.max_wrapped_jobs,
                                                 self._platform.max_wallclock, horizontal_packager.max_wrapper_job_by_section).build_vertical_package(job)

            current_package.append(job_list)

        for job in current_package[-1]:
            total_wallclock = sum_str_hours(total_wallclock, job.wallclock)
        if len(current_package) > 1:
            for level in xrange(1, len(current_package)):
                for job in current_package[level]:
                    job.level = level
        return JobPackageVerticalHorizontal(current_package, total_processors, total_wallclock,
                                            jobs_resources=jobs_resources, method=self.wrapper_method, configuration=self._as_config)


class JobPackagerVertical(object):
    """
    Vertical Packager Parent Class

    :param jobs_list: Usually there is only 1 job in this list. \n
    :type jobs_list: List() of Job Objects \n
    :param total_wallclock: Wallclock per object. \n
    :type total_wallclock: String  \n
    :param max_jobs: Maximum number of jobs per platform. \n
    :type max_jobs: Integer \n
    :param max_wrapped_jobs: Value from jobs_parser, if not found default to an autosubmit_.conf value (Looks first in [wrapper] section). \n
    :type max_wrapped_jobs: Integer \n
    :param max_wallclock: Value from Platform. \n
    :type max_wallclock: Integer

    """

    def __init__(self, jobs_list, total_wallclock, max_jobs, max_wrapped_jobs, max_wallclock, max_wrapper_job_by_section):
        self.jobs_list = jobs_list
        self.total_wallclock = total_wallclock
        self.max_jobs = max_jobs
        self.max_wrapped_jobs = max_wrapped_jobs
        self.max_wrapper_job_by_section = max_wrapper_job_by_section
        self.max_wallclock = max_wallclock

    def build_vertical_package(self, job, level=0):
        """
        Goes trough the job and all the related jobs (children, or part of the same date member ordered group), finds those suitable
        and groups them together into a wrapper. 

        :param job: Job to be wrapped. \n
        :type job: Job Object \n
        :return: List of jobs that are wrapped together. \n
        :rtype: List() of Job Object \n
        """
        # self.jobs_list starts as only 1 member, but wrapped jobs are added in the recursion
        if len(self.jobs_list) >= self.max_jobs or len(self.jobs_list) >= self.max_wrapped_jobs or len(self.jobs_list) >= self.max_wrapper_job_by_section[job.section]:
            return self.jobs_list

        child = self.get_wrappable_child(job)
        # If not None, it is wrappable
        if child is not None:
            # Calculate total wallclock per possible wrapper
            self.total_wallclock = sum_str_hours(
                self.total_wallclock, child.wallclock)
            # Testing against max from platform
            if self.total_wallclock <= self.max_wallclock:
                # Marking, this is later tested in the main loop
                child.packed = True
                child.level = level
                self.jobs_list.append(child)
                # Recursive call
                return self.build_vertical_package(child, level=level + 1)
        # Wrapped jobs are accumulated and returned in this list
        return self.jobs_list

    def get_wrappable_child(self, job):
        pass

    def _is_wrappable(self, job):
        pass


class JobPackagerVerticalSimple(JobPackagerVertical):
    """
    Vertical Packager Class. First statement of the constructor builds JobPackagerVertical.

    :param jobs_list: List of jobs, usually only receives one job. \n
    :type jobs_list: List() of Job Objects \n
    :param total_wallclock: Wallclock from Job. \n
    :type total_wallclock: String \n
    :param max_jobs: Maximum number of jobs per platform. \n
    :type max_jobs: Integer \n
    :param max_wrapped_jobs: Value from jobs_parser, if not found default to an autosubmit_.conf value (Looks first in [wrapper] section). \n
    :type max_wrapped_jobs: Integer \n
    :param max_wallclock: Value from Platform. \n
    :type max_wallclock: Integer
    """

    def __init__(self, jobs_list, total_wallclock, max_jobs, max_wrapped_jobs, max_wallclock, max_wrapper_job_by_section):
        super(JobPackagerVerticalSimple, self).__init__(
            jobs_list, total_wallclock, max_jobs, max_wrapped_jobs, max_wallclock, max_wrapper_job_by_section)

    def get_wrappable_child(self, job):
        """
        Goes through the children jobs of job, tests if wrappable using self._is_wrappable.

        :param job: job to be evaluated. \n
        :type job: Job Object \n
        :return: job (children) that is wrappable. \n
        :rtype: Job Object
        """
        for child in job.children:
            if child.status in [Status.WAITING, Status.READY] and self._is_wrappable(child, job):
                return child
            continue
        return None

    def _is_wrappable(self, job, parent=None):
        """
        Determines if a job (children) is wrappable. Basic condition is that the parent should have the same section as the child.
        Also, test that the parents of the job (children) are COMPLETED.

        :param job: Children Job to be tested. \n
        :type job: Job Object \n
        :param parent: Original Job whose children are tested. \n
        :type parent: Job Object \n
        :return: True if wrappable, False otherwise. \n
        :rtype: Boolean
        """
        if job.section != parent.section:
            return False
        for other_parent in job.parents:
            # First part, parents should be COMPLETED.
            # Second part, no cycles.
            if other_parent.status != Status.COMPLETED and other_parent not in self.jobs_list:
                return False
        return True


class JobPackagerVerticalMixed(JobPackagerVertical):
    """
    Vertical Mixed Class. First statement of the constructor builds JobPackagerVertical.

    :param dict_jobs: Jobs sorted by date, member, RUNNING, and chunk number. Only those relevant to the wrapper. \n
    :type dict_jobs: Dictionary Key: date, Value: (Dictionary Key: Member, Value: List of jobs sorted) \n
    :param ready_job: Job to be wrapped. \n
    :type ready_job: Job Object \n
    :param jobs_list: ready_job as a list. \n
    :type jobs_list: List() of Job Object \n
    :param total_wallclock: wallclock time per job. \n
    :type total_wallclock: String \n
    :param max_jobs: Maximum number of jobs per platform. \n
    :type max_jobs: Integer \n
    :param max_wrapped_jobs: Value from jobs_parser, if not found default to an autosubmit_.conf value (Looks first in [wrapper] section). \n
    :type max_wrapped_jobs: Integer \n
    :param max_wallclock: Value from Platform. \n
    :type max_wallclock: String \n
    """

    def __init__(self, dict_jobs, ready_job, jobs_list, total_wallclock, max_jobs, max_wrapped_jobs, max_wallclock, max_wrapper_job_by_section):
        super(JobPackagerVerticalMixed, self).__init__(
            jobs_list, total_wallclock, max_jobs, max_wrapped_jobs, max_wallclock, max_wrapper_job_by_section)
        self.ready_job = ready_job
        self.dict_jobs = dict_jobs
        # Last date from the ordering
        date = dict_jobs.keys()[-1]
        # Last member from the last date from the ordering
        member = dict_jobs[date].keys()[-1]
        # If job to be wrapped has date and member, use those
        if ready_job.date is not None:
            date = ready_job.date
        if ready_job.member is not None:
            member = ready_job.member
        # Extract list of sorted jobs per date and member
        self.sorted_jobs = dict_jobs[date][member]
        self.index = 0

    def get_wrappable_child(self, job):
        """
        Goes through the jobs with the same date and member than the input job, and return the first that satisfies self._is_wrappable()

        :param job: job to be evaluated. \n
        :type job: Job Object \n
        :return: job that is wrappable. \n
        :rtype: Job Object
        """
        # Unnecessary assignment
        sorted_jobs = self.sorted_jobs

        for index in xrange(self.index, len(sorted_jobs)):
            child = sorted_jobs[index]
            if self._is_wrappable(child):
                self.index = index + 1
                return child
            continue
        return None

    def _is_wrappable(self, job):
        """
        Determines if a job is wrappable. Basically, the job shouldn't have been packed already and the status must be READY or WAITING,
        Its parents should be COMPLETED.

        :param job: job to be evaluated. \n
        :type job: Job Object \n
        :return: True if wrappable, False otherwise. \n
        :rtype: Boolean
        """
        if job.packed is False and (job.status == Status.READY or job.status == Status.WAITING):
            for parent in job.parents:
                # First part of this conditional is always going to be true because otherwise there would be a cycle
                # Second part is actually relevant, parents of a wrapper should be COMPLETED
                if parent not in self.jobs_list and parent.status != Status.COMPLETED:
                    return False
            return True
        return False


class JobPackagerHorizontal(object):
    def __init__(self, job_list, max_processors, max_wrapped_jobs, max_jobs, processors_node, method="ASThread", max_wrapper_job_by_section=dict()):
        self.processors_node = processors_node
        self.max_processors = max_processors
        self.max_wrapped_jobs = max_wrapped_jobs
        self.max_wrapper_job_by_section = max_wrapper_job_by_section
        self.job_list = job_list
        self.max_jobs = max_jobs
        self._current_processors = 0
        self._sort_order_dict = dict()
        self._components_dict = dict()
        self._section_processors = dict()
        self.method = method

        self._maxTotalProcessors = 0
        self._sectionList = list()
        self._package_sections = dict()

    def build_horizontal_package(self, horizontal_vertical=False):
        current_package = []
        current_package_by_section = {}
        if horizontal_vertical:
            self._current_processors = 0
        jobs_by_section = dict()
        for job in self.job_list:
            if job.section not in jobs_by_section:
                jobs_by_section[job.section] = list()
            jobs_by_section[job.section].append(job)
        for section in jobs_by_section:
            current_package_by_section[section] = 0
            for job in jobs_by_section[section]:
                if self.max_jobs > 0 and len(current_package) < self.max_wrapped_jobs and current_package_by_section[section] < self.max_wrapper_job_by_section[section]:
                    if int(job.tasks) != 0 and int(job.tasks) != int(self.processors_node) and \
                            int(job.tasks) < job.total_processors:
                        nodes = int(
                            ceil(job.total_processors / float(job.tasks)))
                        total_processors = int(self.processors_node) * nodes
                    else:
                        total_processors = job.total_processors
                    if (self._current_processors + total_processors) <= int(self.max_processors):
                        current_package.append(job)
                        self._current_processors += total_processors
                    else:
                        current_package = [job]
                        self._current_processors = total_processors
                    current_package_by_section[section] += 1
                else:
                    break

        self.create_components_dict()

        return current_package

    def create_sections_order(self, jobs_sections):
        for i, section in enumerate(jobs_sections.split('&')):
            self._sort_order_dict[section] = i

    # EXIT FALSE IF A SECTION EXIST AND HAVE LESS PROCESSORS
    def add_sectioncombo_processors(self, total_processors_section):
        keySection = ""

        self._sectionList.sort()
        for section in self._sectionList:
            keySection += str(section)
        if keySection in self._package_sections:
            if self._package_sections[keySection] < total_processors_section:
                return False
        else:
            self._package_sections[keySection] = total_processors_section
        self._maxTotalProcessors = max(
            max(self._package_sections.values()), self._maxTotalProcessors)
        return True

    def sort_by_expression(self, jobname):
        jobname = jobname.split('_')[-1]
        return self._sort_order_dict[jobname]

    def get_next_packages(self, jobs_sections, max_wallclock=None, potential_dependency=None, packages_remote_dependencies=list(), horizontal_vertical=False, max_procs=0):
        packages = []
        job = max(self.job_list, key=attrgetter('total_wallclock'))
        wallclock = job.wallclock
        total_wallclock = wallclock

        while self.max_jobs > 0:
            next_section_list = []
            for job in self.job_list:
                for child in job.children:
                    if job.section == child.section or (job.section in jobs_sections and child.section in jobs_sections) \
                            and child.status in [Status.READY, Status.WAITING]:
                        wrappable = True
                        for other_parent in child.parents:
                            if other_parent.status != Status.COMPLETED and other_parent not in self.job_list:
                                wrappable = False
                        if wrappable and child not in next_section_list:
                            next_section_list.append(child)

            next_section_list.sort(
                key=lambda job: self.sort_by_expression(job.name))
            self.job_list = next_section_list
            package_jobs = self.build_horizontal_package(horizontal_vertical)

            if package_jobs:
                sections_aux = set()
                wallclock = package_jobs[0].wallclock
                for job in package_jobs:
                    if job.section not in sections_aux:
                        sections_aux.add(job.section)
                        if job.wallclock > wallclock:
                            wallclock = job.wallclock
                if self._current_processors > max_procs:
                    return packages
                if max_wallclock:
                    total_wallclock = sum_str_hours(total_wallclock, wallclock)
                    if total_wallclock > max_wallclock:
                        return packages
                packages.append(package_jobs)

            else:
                break

        return packages

    @property
    def total_processors(self):
        return self._current_processors

    @property
    def components_dict(self):
        return self._components_dict

    def create_components_dict(self):
        self._sectionList = []
        for job in self.job_list:
            if job.section not in self._sectionList:
                self._sectionList.append(job.section)
            if job.section not in self._components_dict:
                self._components_dict[job.section] = dict()
                self._components_dict[job.section]['COMPONENTS'] = {parameter: job.parameters[parameter]
                                                                    for parameter in job.parameters.keys()
                                                                    if '_NUMPROC' in parameter}
