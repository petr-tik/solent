#
# ipval_cog (testing)
#
# // license
# Copyright 2016, Free Software Foundation.
#
# This file is part of Solent.
#
# Solent is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Solent is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# Solent. If not, see <http://www.gnu.org/licenses/>.

from solent.eng import activity_new
from solent.eng import gruel_schema_new
from solent.eng import gruel_press_new
from solent.eng import gruel_puff_new
from solent.eng import nearcast_orb_new
from solent.eng import nearcast_schema_new
from solent.eng.cs import *
from solent.eng.gruel.gruel_schema import GruelMessageType
from solent.eng.gruel.server.gs_nearcast_schema import gs_nearcast_schema_new
from solent.eng.gruel.server.ipval_cog import ipval_cog_new
from solent.log import log
from solent.util import uniq

from testing import run_tests
from testing import test
from testing.eng import engine_fake
from testing.eng import nearcast_snoop_fake
from testing.eng.gruel.receiver_cog import receiver_cog_fake

import sys

@test
def should_reject_unauthorised_ip():
    engine = engine_fake()
    nearcast_schema = gs_nearcast_schema_new()
    nearcast_snoop = nearcast_snoop_fake(
        nearcast_schema=nearcast_schema)
    nearcast_snoop.disable()
    orb = nearcast_orb_new(
        engine=engine,
        nearcast_schema=nearcast_schema,
        nearcast_snoop=nearcast_snoop)
    r = orb.init_cog(
        fn=receiver_cog_fake)
    ipval_cog = orb.init_cog(
        fn=ipval_cog_new)
    #
    # scenario: unauth ip connects
    ip = '127.0.0.1'
    port = 5000
    r.nc_announce_tcp_connect(
        ip=ip,
        port=port)
    #
    # check effects: we should send a messaage to boot
    assert 1 == r.count_please_tcp_boot()
    #
    return True

@test
def should_allow_authorised_ip():
    engine = engine_fake()
    nearcast_schema = gs_nearcast_schema_new()
    nearcast_snoop = nearcast_snoop_fake(
        nearcast_schema=nearcast_schema)
    nearcast_snoop.disable()
    orb = nearcast_orb_new(
        engine=engine,
        nearcast_schema=nearcast_schema,
        nearcast_snoop=nearcast_snoop)
    r = orb.init_cog(
        fn=receiver_cog_fake)
    ipval_cog = orb.init_cog(
        fn=ipval_cog_new)
    #
    ip = '127.0.0.1'
    port = 5000
    #
    # scenario: we see permission for a differnt ip and then a connect
    r.nc_ipval_add_ip(
        ip='203.15.93.2')
    r.nc_announce_tcp_connect(
        ip=ip,
        port=port)
    #
    # check effects: we should still see a boot messaage
    assert 1 == r.count_please_tcp_boot()
    # but we do get a note to say it's ok
    assert 0 == r.count_nearnote()
    #
    # scenario: now we permit the relevant ip, and then see a connect
    r.nc_ipval_add_ip(
        ip=ip)
    r.nc_announce_tcp_connect(
        ip=ip,
        port=port)
    #
    # check effects: we should see no more boot messages
    assert 1 == r.count_please_tcp_boot()
    # but we do get a note to say it's ok
    assert 1 == r.count_nearnote()
    #
    return True

@test
def should_allow_any_ip():
    engine = engine_fake()
    nearcast_schema = gs_nearcast_schema_new()
    nearcast_snoop = nearcast_snoop_fake(
        nearcast_schema=nearcast_schema)
    nearcast_snoop.disable()
    orb = nearcast_orb_new(
        engine=engine,
        nearcast_schema=nearcast_schema,
        nearcast_snoop=nearcast_snoop)
    r = orb.init_cog(
        fn=receiver_cog_fake)
    ipval_cog = orb.init_cog(
        fn=ipval_cog_new)
    #
    ip = '127.0.0.1'
    port = 5000
    r.nc_ipval_disable()
    r.nc_announce_tcp_connect(
        ip=ip,
        port=port)
    #
    assert 0 == r.count_please_tcp_boot()
    assert 1 == r.count_nearnote()
    #
    return True

if __name__ == '__main__':
    run_tests(
        unders_file=sys.modules['__main__'].__file__)

