# Copyright 2020 Michael Thies <mail@mhthies.de>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
import asyncio
import unittest
import unittest.mock
import time
from typing import NamedTuple

import aiohttp

import shc.web
import shc.interfaces.shc_client
from test._helper import ExampleReadable, InterfaceThreadRunner, ExampleWritable, ExampleSubscribable, async_test


class ExampleType(NamedTuple):
    the_value: float
    is_it_real: bool


class SHCWebsocketClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.server = shc.web.WebServer("localhost", 42080)
        self.client = shc.interfaces.shc_client.SHCWebClient('http://localhost:42080')

        self.client_runner = InterfaceThreadRunner(self.client)
        self.server_runner = InterfaceThreadRunner(self.server)

    def tearDown(self) -> None:
        self.client_runner.stop()
        self.server_runner.stop()

    def test_subscribe(self) -> None:
        self.server.api(int, "foo")
        bar_object = self.server.api(ExampleType, "bar")\
            .connect(ExampleReadable(ExampleType, ExampleType(42, True)))
        bar_source = ExampleSubscribable(ExampleType).connect(bar_object)

        client_foo = self.client.object(int, 'foo')
        client_bar = self.client.object(ExampleType, 'bar')
        foo_target = ExampleWritable(int).connect(client_foo)
        bar_target = ExampleWritable(ExampleType).connect(client_bar)

        self.server_runner.start()
        self.client_runner.start()

        time.sleep(0.05)
        foo_target._write.assert_not_called()
        bar_target._write.assert_called_once_with(ExampleType(42, True), [client_bar])
        self.assertIsInstance(bar_target._write.call_args[0][0], ExampleType)
        bar_target._write.reset_mock()

        asyncio.run_coroutine_threadsafe(bar_source.publish(ExampleType(56, False), [self]),
                                         loop=self.server_runner.loop).result()
        time.sleep(0.05)
        bar_target._write.assert_called_once_with(ExampleType(56, False), [client_bar])

    @async_test
    async def test_subscribe_error(self) -> None:
        self.server.api(int, "foo")
        self.server.api(ExampleType, "bar")

        bar_client = self.client.object(int, 'bar')

        # Creating an option with equal name should return the same object again or raise a type error
        self.assertIs(self.client.object(int, 'bar'), bar_client)
        with self.assertRaises(TypeError):
            self.client.object(str, 'bar')

        # Test raising of connection errors on startup (server is not started yet)
        with self.assertRaises(aiohttp.ClientConnectionError):
            await self.client.start()

        self.server_runner.start()

        # Test raising of subscription errors on startup (inexistent api object name)
        another_client = shc.interfaces.shc_client.SHCWebClient('http://localhost:42080')
        another_client.object(int, 'foobar')
        with self.assertRaises(shc.interfaces.shc_client.WebSocketAPIError):
            await another_client.start()

    def test_read(self) -> None:
        self.server.api(int, "foo")
        self.server.api(ExampleType, "bar")\
            .connect(ExampleReadable(ExampleType, ExampleType(42, True)))

        client_foo = self.client.object(int, 'foo')
        client_bar = self.client.object(ExampleType, 'bar')

        self.server_runner.start()
        self.client_runner.start()

        with self.assertRaises(shc.base.UninitializedError):
            asyncio.run_coroutine_threadsafe(client_foo.read(), loop=self.client_runner.loop).result()

        result = asyncio.run_coroutine_threadsafe(client_bar.read(), loop=self.client_runner.loop).result()
        self.assertIsInstance(result, ExampleType)
        self.assertEqual(ExampleType(42, True), result)

    def test_write(self) -> None:
        server_bar = self.server.api(ExampleType, "bar")
        target = ExampleWritable(ExampleType).connect(server_bar)

        client_bar = self.client.object(ExampleType, 'bar')

        self.server_runner.start()
        self.client_runner.start()

        asyncio.run_coroutine_threadsafe(client_bar.write(ExampleType(42, True), [self]),
                                         loop=self.client_runner.loop).result()
        time.sleep(0.05)
        target._write.assert_called_once_with(ExampleType(42, True), unittest.mock.ANY)
        self.assertIsInstance(target._write.call_args[0][0], ExampleType)
