"""Command dispatcher and commands to run.

Look up the command from the command center, attempt to map it to a local method.

"""

from eventlet import patcher
patcher.monkey_patch(all=True)

import boto
import time
import datetime
import sys
import cmd
import settings

from microarmy.firepower import (init_cannons,
                                 terminate_cannons,
                                 reboot_cannons,
                                 setup_cannons,
                                 slam_host,
                                 find_deployed_cannons,
                                 destroy_deployed_cannons)


class CommandCenter(cmd.Cmd):
    """Commands and helpers for command center."""

    def __init__(self):
        cmd.Cmd.__init__(self)
        self._cannons_deployed = False
        self._cannon_hosts = None
        self._cannon_infos = None
        self.prompt = 'microarmy> '

    def default(self, line):
        print
        print 'Cannot find command: "%s"' % line
        self.do_help(None)

    def emptyline(self):
        pass

    def do_EOF(self, line):
        print 'bye'
        return True

    def do_long_help(self, line):
        """Long help output"""
        print """
        long_help:    This.
        status:       Get info about current cannons
        deploy:       Deploys N cannons
        setup:        Runs the setup functions on each host
        config:       Allows a user to specify existing cannons
        find_cannons  Find deployed cannons, add them to your hosts
        fire:         Asks for a url and then fires the cannons
        mfire:        Runs `fire` multiple times and aggregates totals
        term:         Terminate cannons
        quit:         Exit command center
        """

    def do_deploy(self, line):
        """Deploy N cannons"""
        start_time = time.time()
        self._cannon_infos = init_cannons()

        print 'Time: %s' % (time.time() - start_time)

    def do_term(self, line):
        """Terminate cannons"""
        if not self._cannon_infos:
            print 'ERROR: No cannons defined, try "config" or "deploy"'
            return

        terminate_cannons([h[0] for h in self._cannon_infos])
        self._cannon_infos = None
        self._cannon_hosts = None
        self._cannons_deployed = False
        print 'Deployed cannons destroyed'

    def do_quit(self, line):
        """Exit command center"""
        print 'bye'
        sys.exit(0)

    def do_setup(self, line):
        """Setup system, deploy configs and urls"""
        if not self._cannon_infos:
            print 'ERROR: No cannons defined, try "config" or "deploy"'
            return

        start_time = time.time()
        print 'Setting up cannons'
        self._cannon_hosts = [h[1] for h in self._cannon_infos]
        status = setup_cannons(self._cannon_hosts)


        print status

        print 'Finished setup - time: %s' % (time.time() - start_time)

        print 'Sending reboot message to cannons'
        reboot_cannons([h[0] for h in self._cannon_infos])
        self._cannons_deployed = True

    def do_status(self, line):
        """Get information about current cannons, siege configs and urls"""
        if not self._cannon_infos:
            print '  No cannons defined, try "config" or "deploy"'
            return
        for host in self._cannon_infos:
            iid, ihost = [h for h in host]
            print '  Cannon: %s:%s' % (iid, ihost)

    def do_config(self, line, cannon_data=None):
        """Allows a user to specify existing cannons"""
        if not cannon_data:
            cannon_data = raw_input('  Enter host data: ')
        if cannon_data != '':
            if isinstance(cannon_data, str):
                self._cannon_infos = eval(cannon_data)
            else:
                self._cannon_infos = cannon_data
            self._cannon_hosts = [h[1] for h in self._cannon_infos]
            self._cannons_deployed = True
        else:
            print 'ERROR: No host data specified'
        return

    def do_find_cannons(self, line):
        """Find all cannons deployed for microarmy"""
        hosts = find_deployed_cannons()
        if hosts:
            print 'Deployed cannons:', hosts
            answer = raw_input('Would you like to import these cannons now? (y/n) ')
            if answer.lower() == 'n':
                return
            self.do_config(None, hosts)
        else:
            print 'No cannons found'

    def do_cleanup(self, line):
        """Find all cannons we have deployed, destroy them all"""
        destroy_deployed_cannons()
        print 'Deployed cannons destroyed'

    def do_fire(self, line):
        """Fires the cannons"""
        if self._cannons_deployed:
            report = slam_host(self._cannon_hosts)

            print 'Results ]------------------'
            print report
        else:
            print 'ERROR: Cannons not deployed yet'

    def do_mfire(self, line):
        """Runs `fire` multiple times and aggregates totals"""
        if self._cannons_deployed:
            ### Get test arguments from user
            try:
                n_times = raw_input('  n times: ')
                n_times = int(n_times)
            except:
                print '<n_times> must be a number.'
                return

            print 'Results ]------------------'
            for run_instance in xrange(n_times):
                report = slam_host(self._cannon_hosts)
                print '%s:' % (run_instance)
                print report
        else:
            print 'ERROR: Cannons not deployed yet'
